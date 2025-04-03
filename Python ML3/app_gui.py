import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class RiskManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Riesgos")
        self.master.geometry("600x500")
        self.master.config(bg="white")

        # Crear el diccionario de etiquetas (simulación de cambio de idioma)
        self.labels = {
            "analyst": "Analista:",
            "add_risk": "Agregar Riesgo",
            "risk_name": "Nombre del Riesgo:",
            "probability": "Probabilidad:",
            "impact": "Impacto:"
        }

        # Inicializar variables
        self.risks = []

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Crear un marco principal para organizar los widgets
        self.frame_main = tk.Frame(self.master)
        self.frame_main.grid(padx=20, pady=20, sticky="nsew")

        # Crear un marco para los botones (usar grid en lugar de pack)
        self.frame_buttons = tk.Frame(self.frame_main)
        self.frame_buttons.grid(row=0, column=0, pady=10)

        # Etiqueta y entrada para el nombre del analista
        self.label_analyst = tk.Label(self.frame_main, text=self.labels["analyst"], font=("Arial", 12), fg="blue")
        self.label_analyst.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.entry_analyst = tk.Entry(self.frame_main, bg="lightgray", font=("Arial", 12))
        self.entry_analyst.grid(row=1, column=1, padx=10, pady=5)

        # Etiqueta y entrada para el nombre del riesgo
        self.label_risk_name = tk.Label(self.frame_main, text=self.labels["risk_name"], font=("Arial", 12), fg="blue")
        self.label_risk_name.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.entry_risk_name = tk.Entry(self.frame_main, bg="lightgray", font=("Arial", 12))
        self.entry_risk_name.grid(row=2, column=1, padx=10, pady=5)

        # Etiqueta y entrada para la probabilidad
        self.label_probability = tk.Label(self.frame_main, text=self.labels["probability"], font=("Arial", 12), fg="blue")
        self.label_probability.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.entry_probability = tk.Entry(self.frame_main, bg="lightgray", font=("Arial", 12))
        self.entry_probability.grid(row=3, column=1, padx=10, pady=5)

        # Etiqueta y entrada para el impacto
        self.label_impact = tk.Label(self.frame_main, text=self.labels["impact"], font=("Arial", 12), fg="blue")
        self.label_impact.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.entry_impact = tk.Entry(self.frame_main, bg="lightgray", font=("Arial", 12))
        self.entry_impact.grid(row=4, column=1, padx=10, pady=5)

        # Botón para agregar riesgo
        self.button_add = tk.Button(self.frame_buttons, text=self.labels["add_risk"], command=self.add_risk, bg="green", fg="white", font=("Arial", 10))
        self.button_add.grid(row=0, column=0, padx=10, pady=10)

        # Cuadro de texto para mostrar los riesgos
        self.text_risks = tk.Text(self.frame_main, width=40, height=10, wrap="word")
        self.text_risks.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.text_risks.config(state=tk.DISABLED)  # Deshabilitar la edición directamente

        # Scrollbar para el cuadro de texto
        self.scrollbar = tk.Scrollbar(self.frame_main, orient="vertical", command=self.text_risks.yview)
        self.scrollbar.grid(row=5, column=2, sticky="ns")
        self.text_risks.config(yscrollcommand=self.scrollbar.set)

    def add_risk(self):
        analyst = self.entry_analyst.get()
        risk_name = self.entry_risk_name.get()
        probability = self.entry_probability.get()
        impact = self.entry_impact.get()

        # Validar los datos
        if not analyst or not risk_name or not probability or not impact:
            messagebox.showerror("Error", "Todos los campos deben ser completados")
            return

        # Agregar el riesgo a la lista y actualizar el cuadro de texto
        risk = f"Analista: {analyst}, Riesgo: {risk_name}, Probabilidad: {probability}, Impacto: {impact}\n"
        self.risks.append(risk)
        self.update_risks_display()

    def update_risks_display(self):
        self.text_risks.config(state=tk.NORMAL)
        self.text_risks.delete(1.0, tk.END)
        for risk in self.risks:
            self.text_risks.insert(tk.END, risk)
        self.text_risks.config(state=tk.DISABLED)

    def show_report(self):
        # Mostrar reporte en una nueva ventana
        report_window = tk.Toplevel(self.master)
        report_window.title("Reporte de Riesgos")
        report_text = tk.Text(report_window, width=50, height=15)
        report_text.pack(padx=10, pady=10)
        report_text.insert(tk.END, "Aquí va el contenido del reporte...")
        report_text.config(state=tk.DISABLED)

# Crear la ventana principal
root = tk.Tk()

# Crear la aplicación
app = RiskManagementApp(root)

# Ejecutar la aplicación
root.mainloop()
