import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import requests
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL = "http://127.0.0.1:5000/riesgos"

# Escala de impacto en valores numéricos
escala_impacto = {
    "Baja Crítica": 1,
    "Significativa": 2,
    "Moderada": 3,
    "Alta": 4,
    "Extrema": 5
}

riesgos_disponibles = ["Seleccione...", "Robo", "Asalto", "Secuestro", "Iluminación", "Vegetación", "Cerco perimetral"]

datos_riesgo = []

def calcular_mosler(impacto, profundidad):
    impacto_num = escala_impacto.get(impacto, 1)
    profundidad = float(profundidad) if profundidad else 1
    probabilidad = np.random.uniform(1, 5)
    
    # Método Mosler
    I = impacto_num * profundidad
    D = probabilidad * profundidad
    C = I + D
    Pb = impacto_num * probabilidad
    ER = C * Pb
    
    return probabilidad, impacto_num, ER

def obtener_riesgos():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            lista_riesgos.delete(*lista_riesgos.get_children())
            riesgos = response.json().get("riesgos", [])
            global datos_riesgo
            datos_riesgo = []
            for riesgo in riesgos:
                id_, categoria, impacto, profundidad, riesgo_txt, mitigacion, analista = (
                    riesgo["id"], riesgo["categoria"], riesgo["impacto"], riesgo["profundidad"],
                    riesgo["riesgo"], riesgo["mitigacion"], riesgo["analista"]
                )
                lista_riesgos.insert("", "end", values=(id_, categoria, impacto, profundidad, riesgo_txt, mitigacion, analista))
                
                probabilidad, impacto_num, ER = calcular_mosler(impacto, profundidad)
                datos_riesgo.append((categoria, probabilidad, impacto_num, ER))
            
            actualizar_grafico()
        else:
            messagebox.showerror("Error", "No se pudo obtener los riesgos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {str(e)}")

def actualizar_grafico():
    ax.clear()
    ax.set_title("Evaluación de Riesgo (Mosler)")
    ax.set_xlabel("Probabilidad")
    ax.set_ylabel("Impacto")
    
    for categoria, probabilidad, impacto, ER in datos_riesgo:
        ax.scatter(probabilidad, impacto, label=f"{categoria} (ER: {ER:.2f})", alpha=0.7, edgecolors='k')
    
    ax.legend()
    canvas.draw()

def editar_riesgo():
    seleccionado = lista_riesgos.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Seleccione un riesgo para editar.")
        return
    
    item = lista_riesgos.item(seleccionado)
    valores = item['values']
    if not valores:
        return
    
    riesgo_id = valores[0]
    nuevos_datos = {}
    
    for i, campo in enumerate(["Categoría", "Impacto", "Profundidad", "Riesgo", "Mitigación", "Analista"]):
        nuevo_valor = simpledialog.askstring("Editar Riesgo", f"Nuevo valor para {campo} (actual: {valores[i+1]})")
        if nuevo_valor:
            nuevos_datos[campo.lower()] = nuevo_valor
    
    try:
        response = requests.put(f"{API_URL}/{riesgo_id}", json=nuevos_datos)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Riesgo editado correctamente")
            obtener_riesgos()
        else:
            messagebox.showerror("Error", "No se pudo editar el riesgo.")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {str(e)}")

def descargar_informe():
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")])
    if not archivo:
        return
    
    try:
        with open(archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Categoría", "Impacto", "Profundidad", "Riesgo", "Mitigación", "Analista"])
            for item in lista_riesgos.get_children():
                writer.writerow(lista_riesgos.item(item, "values"))
        messagebox.showinfo("Éxito", "Informe guardado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el informe: {str(e)}")

root = tk.Tk()
root.title("Gestión de Riesgos - Método Mosler")
root.geometry("1000x600")

frame_lista = tk.Frame(root)
frame_lista.pack(side="left", fill="both", expand=True)

columnas = ("ID", "Categoría", "Impacto", "Profundidad", "Riesgo", "Mitigación", "Analista")
lista_riesgos = ttk.Treeview(frame_lista, columns=columnas, show="headings")

for col in columnas:
    lista_riesgos.heading(col, text=col)
    lista_riesgos.column(col, width=100, anchor="center")

lista_riesgos.pack(fill="both", expand=True)
btn_actualizar = tk.Button(frame_lista, text="Actualizar", command=obtener_riesgos)
btn_actualizar.pack()
btn_editar = tk.Button(frame_lista, text="Editar", command=editar_riesgo)
btn_editar.pack()
btn_descargar = tk.Button(frame_lista, text="Descargar Informe", command=descargar_informe)
btn_descargar.pack()

frame_grafico = tk.Frame(root)
frame_grafico.pack(side="right", fill="both", expand=True)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack()

btn_actualizar.invoke()
root.mainloop()
