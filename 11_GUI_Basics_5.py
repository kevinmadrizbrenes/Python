import tkinter as tk
from tkinter import StringVar


# Clase para almacenar y manejar datos
class UserData:
    def __init__(self):
        # Variables de datos
        self.nombre = StringVar(value="Yenitza Josefina Baldo Febres")
        self.nacimiento = StringVar(value="15 de noviembre de 1986")
        self.nacionalidad = StringVar(value="Venezolana")
        self.trabajo_actual = StringVar(value="Supervisora de planta en Comercializadora Oso Blanco")

    # Método para actualizar los datos
    #def actualizar_datos(self, nombre, nacimiento, nacionalidad, trabajo_actual):
        #self.nombre.set(nombre)
        #self.nacimiento.set(nacimiento)
        #self.nacionalidad.set(nacionalidad)
        #self.trabajo_actual.set(trabajo_actual)


# Función para inicializar la ventana y mostrar los datos
def mostrar_datos():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Información del Usuario")

    # Crear una instancia de la clase UserData
    datos_usuario = UserData()

    # Crear etiquetas para mostrar la información
    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky="e")
    tk.Label(ventana, textvariable=datos_usuario.nombre).grid(row=0, column=1, sticky="w")

    tk.Label(ventana, text="Fecha de nacimiento:").grid(row=1, column=0, sticky="e")
    tk.Label(ventana, textvariable=datos_usuario.nacimiento).grid(row=1, column=1, sticky="w")

    tk.Label(ventana, text="Nacionalidad:").grid(row=2, column=0, sticky="e")
    tk.Label(ventana, textvariable=datos_usuario.nacionalidad).grid(row=2, column=1, sticky="w")

    tk.Label(ventana, text="Trabajo actual:").grid(row=3, column=0, sticky="e")
    tk.Label(ventana, textvariable=datos_usuario.trabajo_actual).grid(row=3, column=1, sticky="w")

    # Botón para cerrar la ventana
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).grid(row=4, column=1, pady=10)

    ventana.mainloop()


# Llamar a la función para mostrar la ventana
mostrar_datos()
