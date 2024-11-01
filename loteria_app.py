import psycopg2
import tkinter as tk
from tkinter import ttk

# Conexión a la base de datos
def conectar():
    conexion = psycopg2.connect(
        dbname="database_jps",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )
    return conexion

# Calcular frecuencia de rangos
def calcular_frecuencia():
    conexion = conectar()
    cursor = conexion.cursor()
    rangos = {"00-24": 0, "25-49": 0, "50-74": 0, "75-99": 0}
    cursor.execute("SELECT primer_numero, segundo_numero, tercer_numero FROM sorteosLN")
    numeros = cursor.fetchall()
    for fila in numeros:
        for numero in fila:
            if 0 <= numero <= 24:
                rangos["00-24"] += 1
            elif 25 <= numero <= 49:
                rangos["25-49"] += 1
            elif 50 <= numero <= 74:
                rangos["50-74"] += 1
            elif 75 <= numero <= 99:
                rangos["75-99"] += 1
    conexion.close()
    return rangos

# Obtener números nunca sorteados
def numeros_nunca_sorteados():
    conexion = conectar()
    cursor = conexion.cursor()
    numeros_existentes = set(range(100))
    cursor.execute("SELECT DISTINCT primer_numero FROM sorteosLN UNION SELECT DISTINCT segundo_numero FROM sorteosLN UNION SELECT DISTINCT tercer_numero FROM sorteosLN")
    numeros_sorteados = set(numero[0] for numero in cursor.fetchall())
    numeros_nunca = numeros_existentes - numeros_sorteados
    conexion.close()
    return sorted(numeros_nunca)

# Obtener los números que más se han repetido
def numeros_mas_frecuentes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT primer_numero, segundo_numero, tercer_numero FROM sorteosLN")
    numeros = [num for fila in cursor.fetchall() for num in fila]
    conexion.close()
    from collections import Counter
    contador = Counter(numeros)
    return contador.most_common(5)  # Los 5 números más frecuentes

# Obtener lista de sorteos para la lista desplegable
def obtener_sorteos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT numero_sorteo FROM sorteosLN ORDER BY numero_sorteo")
    sorteos = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return sorteos

# Obtener detalles de un sorteo específico
def obtener_detalles_sorteo(sorteo_numero):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM sorteosLN WHERE numero_sorteo = %s", (sorteo_numero,))
    sorteo = cursor.fetchone()
    conexion.close()
    return sorteo

# Interfaz gráfica
class LoteriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Junta de Protección Social API")

        # Entrada de número de consulta
        tk.Label(root, text="Ingrese un número (00-99):").pack()
        self.entry_numero = tk.Entry(root)
        self.entry_numero.pack()
        self.entry_numero.bind("<Return>", self.consultar_numero)

        # Menú desplegable para seleccionar sorteo
        tk.Label(root, text="Seleccione un sorteo:").pack()
        self.sorteos = obtener_sorteos()
        self.sorteo_seleccionado = tk.StringVar()
        self.menu_sorteos = ttk.Combobox(root, textvariable=self.sorteo_seleccionado, values=self.sorteos)
        self.menu_sorteos.pack()
        self.menu_sorteos.bind("<<ComboboxSelected>>", self.mostrar_detalles_sorteo)

        # Frame para mostrar detalles del sorteo
        self.detalles_frame = tk.Frame(root)
        self.detalles_frame.pack(pady=10)

        # Sección de frecuencia de rangos
        tk.Label(root, text="Frecuencia de Rangos:").pack()
        self.rangos_texto = tk.Text(root, height=5, width=55, state="disabled")
        self.rangos_texto.pack(pady=10)

        # Sección de números nunca sorteados
        tk.Label(root, text="Números Nunca Sorteados:").pack()
        self.nunca_sorteados_texto = tk.Text(root, height=5, width=55, state="disabled")
        self.nunca_sorteados_texto.pack(pady=10)

        # Sección de números más frecuentes
        tk.Label(root, text="Números Más Frecuentes:").pack()
        self.mas_frecuentes_texto = tk.Text(root, height=5, width=55, state="disabled")
        self.mas_frecuentes_texto.pack(pady=10)

        # Sección para mostrar el resultado de la consulta
        tk.Label(root, text="Resultado de la Consulta:").pack()
        self.resultado_texto = tk.Text(root, height=2, width=55, state="disabled")
        self.resultado_texto.pack(pady=10)

        self.mostrar_estadisticas()

    # Mostrar estadísticas generales
    def mostrar_estadisticas(self):
        rangos = calcular_frecuencia()
        nunca_sorteados = numeros_nunca_sorteados()
        mas_frecuentes = numeros_mas_frecuentes()

        # Mostrar frecuencia de rangos
        rangos_texto = (
            f"00-24: {rangos['00-24']} veces\n"
            f"25-49: {rangos['25-49']} veces\n"
            f"50-74: {rangos['50-74']} veces\n"
            f"75-99: {rangos['75-99']} veces\n"
        )
        self.rangos_texto.config(state="normal")
        self.rangos_texto.delete(1.0, tk.END)
        self.rangos_texto.insert(tk.END, rangos_texto)
        self.rangos_texto.config(state="disabled")

        # Mostrar números nunca sorteados
        nunca_sorteados_texto = ", ".join(map(str, nunca_sorteados))
        self.nunca_sorteados_texto.config(state="normal")
        self.nunca_sorteados_texto.delete(1.0, tk.END)
        self.nunca_sorteados_texto.insert(tk.END, nunca_sorteados_texto)
        self.nunca_sorteados_texto.config(state="disabled")

        # Mostrar números más frecuentes
        mas_frecuentes_texto = "\n".join([f"Número {num}: {count} veces" for num, count in mas_frecuentes])
        self.mas_frecuentes_texto.config(state="normal")
        self.mas_frecuentes_texto.delete(1.0, tk.END)
        self.mas_frecuentes_texto.insert(tk.END, mas_frecuentes_texto)
        self.mas_frecuentes_texto.config(state="disabled")

    # Consultar frecuencia de un número ingresado
    def consultar_numero(self, event):
        numero = self.entry_numero.get()
        if not numero.isdigit() or not (0 <= int(numero) <= 99):
            resultado_texto = "Ingrese un número válido entre 00 y 99."
            self.mostrar_resultado_consulta(resultado_texto)
            return

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM sorteosLN WHERE primer_numero = %s OR segundo_numero = %s OR tercer_numero = %s", (numero, numero, numero))
        frecuencia = cursor.fetchone()[0]
        conexion.close()

        resultado_texto = f"Número {numero} ha salido {frecuencia} veces."
        self.mostrar_resultado_consulta(resultado_texto)

    # Mostrar el resultado de la consulta en el cuadro de texto
    def mostrar_resultado_consulta(self, resultado_texto):
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, resultado_texto)
        self.resultado_texto.config(state="disabled")

    # Mostrar detalles de un sorteo específico
    def mostrar_detalles_sorteo(self, event):
        sorteo_numero = int(self.sorteo_seleccionado.get())
        detalles = obtener_detalles_sorteo(sorteo_numero)

        if detalles:
            info = (
                f"Sorteo {detalles[1]}\n"
                f"Fecha: {detalles[2]}\n"
                f"Primer Premio: {detalles[3]} Serie: {detalles[4]}\n"
                f"Segundo Premio: {detalles[5]} Serie: {detalles[6]}\n"
                f"Tercer Premio: {detalles[7]} Serie: {detalles[8]}"
            )
            for widget in self.detalles_frame.winfo_children():
                widget.destroy()
            tk.Label(self.detalles_frame, text=info, justify="left").pack()
        else:
            tk.Label(self.detalles_frame, text="Detalles no disponibles.", justify="left").pack()

root = tk.Tk()
app = LoteriaApp(root)
root.mainloop()
