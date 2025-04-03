import tkinter as tk
from tkinter import messagebox
import json

class RiskManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Riesgos")
        self.root.geometry("600x400")
        
        # Lista donde se guardarán los riesgos
        self.risks = []

        # Crear las listas desplegables y demás componentes gráficos
        self.create_widgets()

    def create_widgets(self):
        # Etiquetas y campos de entrada para analista, impacto y probabilidad
        tk.Label(self.root, text="Analista").grid(row=0, column=0)
        self.analyst_entry = tk.Entry(self.root)
        self.analyst_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Categoría").grid(row=1, column=0)
        self.category_options = ['Seleccione...', 'Riesgo 1', 'Riesgo 2', 'Riesgo 3']
        self.category_var = tk.StringVar(self.root)
        self.category_var.set(self.category_options[0])
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.category_options)
        self.category_menu.grid(row=1, column=1)

        tk.Label(self.root, text="Impacto").grid(row=2, column=0)
        self.impact_options = ['Seleccione...', 'Bajo', 'Medio', 'Alto']
        self.impact_var = tk.StringVar(self.root)
        self.impact_var.set(self.impact_options[0])
        self.impact_menu = tk.OptionMenu(self.root, self.impact_var, *self.impact_options)
        self.impact_menu.grid(row=2, column=1)

        tk.Label(self.root, text="Probabilidad").grid(row=3, column=0)
        self.probability_entry = tk.Entry(self.root)
        self.probability_entry.grid(row=3, column=1)

        # Botón para agregar un riesgo
        self.add_button = tk.Button(self.root, text="Agregar Riesgo", command=self.add_risk)
        self.add_button.grid(row=4, column=0, columnspan=2)

        # Tabla para mostrar los riesgos agregados
        self.risk_table = tk.Listbox(self.root, height=10, width=50)
        self.risk_table.grid(row=5, column=0, columnspan=2)

        # Botón para generar un reporte (enlace a la siguiente parte)
        self.report_button = tk.Button(self.root, text="Generar Reporte", command=self.generate_report)
        self.report_button.grid(row=6, column=0, columnspan=2)

    def add_risk(self):
        # Obtener datos de los campos de entrada
        analyst = self.analyst_entry.get()
        category = self.category_var.get()
        impact = self.impact_var.get()
        probability = self.probability_entry.get()

        # Validar campos
        if not (analyst and category != 'Seleccione...' and impact != 'Seleccione...' and probability):
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente.")
            return

        # Agregar el riesgo a la lista de riesgos
        risk = {
            'analyst': analyst,
            'category': category,
            'impact': impact,
            'probability': probability
        }

        self.risks.append(risk)
        self.update_risk_table()

        # Limpiar los campos después de agregar
        self.clear_fields()

    def update_risk_table(self):
        # Limpiar la tabla y volver a agregar los riesgos
        self.risk_table.delete(0, tk.END)
        for risk in self.risks:
            self.risk_table.insert(tk.END, f"{risk['analyst']} - {risk['category']} - {risk['impact']} - {risk['probability']}")

    def clear_fields(self):
        # Limpiar los campos de entrada después de agregar un riesgo
        self.analyst_entry.delete(0, tk.END)
        self.probability_entry.delete(0, tk.END)
        self.category_var.set(self.category_options[0])
        self.impact_var.set(self.impact_options[0])

    def generate_report(self):
        # Aquí vamos a generar un reporte en formato JSON (para ilustrar, puede ser PDF o cualquier otro formato)
        if not self.risks:
            messagebox.showwarning("Advertencia", "No hay riesgos agregados para generar un reporte.")
            return

        # Guardar los riesgos en un archivo JSON (puedes usar otros formatos)
        with open('risks_report.json', 'w') as f:
            json.dump(self.risks, f, indent=4)
        
        messagebox.showinfo("Reporte Generado", "El reporte ha sido generado exitosamente.")

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = RiskManagementApp(root)
    root.mainloop()
