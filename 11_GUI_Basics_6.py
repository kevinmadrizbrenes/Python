import tkinter as tk
from tkinter import ttk

# Datos de los sorteos en una lista de diccionarios
data = [
    {"Numero": 4757, "Fecha": "23/07/2023", "Primer_Numero": "60", "Primer_Serie": "063",
     "Premio_Mayor": 150_000_000.00,
     "Segundo_Numero": "97", "Segunda_Serie": "234", "Segundo_Premio": 22_000_000.00, "Tercer_Numero": "93",
     "Tercer_Serie": "618", "Tercer_Premio": 10_000_000.00},
    {"Numero": 4758, "Fecha": "30/07/2023", "Primer_Numero": "40", "Primer_Serie": "395",
     "Premio_Mayor": 150_000_000.00,
     "Segundo_Numero": "75", "Segunda_Serie": "101", "Segundo_Premio": 22_000_000.00, "Tercer_Numero": "67",
     "Tercer_Serie": "087", "Tercer_Premio": 10_000_000.00},
    {"Numero": 4759, "Fecha": "06/08/2023", "Primer_Numero": "22", "Primer_Serie": "832",
     "Premio_Mayor": 150_000_000.00,
     "Segundo_Numero": "05", "Segunda_Serie": "306", "Segundo_Premio": 22_000_000.00, "Tercer_Numero": "33",
     "Tercer_Serie": "471", "Tercer_Premio": 10_000_000.00},
    # Agrega el resto de las filas aquí...
]

# Variables para los totales de premios
total_premio_mayor = sum(item["Premio_Mayor"] for item in data)
total_segundo_premio = sum(item["Segundo_Premio"] for item in data)
total_tercer_premio = sum(item["Tercer_Premio"] for item in data)


# Función para inicializar la ventana y mostrar los datos en el Treeview
def mostrar_datos():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Datos de Sorteos")

    # Crear el widget Treeview para mostrar los datos
    columnas = ("Numero", "Fecha", "Primer_Numero", "Primer_Serie", "Premio_Mayor",
                "Segundo_Numero", "Segunda_Serie", "Segundo_Premio", "Tercer_Numero", "Tercer_Serie", "Tercer_Premio")

    tree = ttk.Treeview(ventana, columns=columnas, show='headings')

    # Definir los encabezados de las columnas
    for col in columnas:
        tree.heading(col, text=col)

    # Insertar datos en el Treeview
    for item in data:
        tree.insert("", "end", values=(item["Numero"], item["Fecha"], item["Primer_Numero"], item["Primer_Serie"],
                                       item["Premio_Mayor"], item["Segundo_Numero"], item["Segunda_Serie"],
                                       item["Segundo_Premio"], item["Tercer_Numero"], item["Tercer_Serie"],
                                       item["Tercer_Premio"]))

    # Colocar el Treeview en la ventana
    tree.pack(expand=True, fill="both")

    # Mostrar los totales
    tk.Label(ventana, text=f"Total Premio Mayor: ₡{total_premio_mayor:,.2f}", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana, text=f"Total Segundo Premio: ₡{total_segundo_premio:,.2f}", font=("Arial", 12, "bold")).pack(
        pady=5)
    tk.Label(ventana, text=f"Total Tercer Premio: ₡{total_tercer_premio:,.2f}", font=("Arial", 12, "bold")).pack(pady=5)

    # Botón para cerrar la ventana
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    ventana.mainloop()


# Llamar a la función para mostrar la ventana
mostrar_datos()
