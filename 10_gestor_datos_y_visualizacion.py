import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime
import os
import argparse


class DataManager:
    def __init__(self):
        self.data = None

    def cargar_datos_csv(self, archivo):
        try:
            self.data = pd.read_csv(archivo)
            print(f"Datos cargados exitosamente desde {archivo}")
        except FileNotFoundError:
            print("Error: El archivo no fue encontrado.")
        except pd.errors.EmptyDataError:
            print("Error: El archivo está vacío.")
        except Exception as e:
            print(f"Error: {e}")

    def mostrar_informacion(self):
        if self.data is not None:
            print("Primeras 5 filas del dataset:")
            print(self.data.head())
            print("\nResumen estadístico:")
            print(self.data.describe())
        else:
            print("No hay datos cargados.")

    def generar_grafico(self, columna):
        if self.data is not None and columna in self.data.columns:
            plt.figure(figsize=(8, 6))
            plt.hist(self.data[columna].dropna(), bins=20, alpha=0.7)
            plt.title(f"Histograma de {columna}")
            plt.xlabel(columna)
            plt.ylabel("Frecuencia")
            plt.grid(True)
            plt.show()
        else:
            print(f"No se encontró la columna '{columna}' en los datos.")

    def realizar_calculos(self):
        if self.data is not None:
            try:
                suma = self.data.sum(numeric_only=True)
                media = self.data.mean(numeric_only=True)
                print("Suma de valores numéricos por columna:")
                print(suma)
                print("\nMedia de valores numéricos por columna:")
                print(media)
            except Exception as e:
                print(f"Error al realizar cálculos: {e}")
        else:
            print("No hay datos cargados para realizar cálculos.")

    def llamar_api(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Datos obtenidos de la API:")
                print(json.dumps(data, indent=4))
            else:
                print(f"Error: No se pudo conectar a la API. Código de estado: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    def guardar_datos_csv(self, archivo_salida):
        if self.data is not None:
            self.data.to_csv(archivo_salida, index=False)
            print(f"Datos guardados exitosamente en {archivo_salida}")
        else:
            print("No hay datos para guardar.")


def mostrar_fecha_actual():
    fecha = datetime.now()
    print(f"Fecha y hora actual: {fecha.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    parser = argparse.ArgumentParser(description="Herramienta de Gestión de Datos y Visualización")
    parser.add_argument("--csv", help="Ruta del archivo CSV a cargar", type=str)
    parser.add_argument("--grafico", help="Nombre de la columna para generar un gráfico", type=str)
    parser.add_argument("--api", help="URL de la API para obtener datos", type=str)
    parser.add_argument("--guardar", help="Ruta del archivo CSV para guardar los datos procesados", type=str)
    parser.add_argument("--calcular", help="Realizar cálculos básicos (suma y media)", action='store_true')
    parser.add_argument("--fecha", help="Mostrar la fecha y hora actual", action='store_true')

    args = parser.parse_args()

    gestor = DataManager()

    if args.csv:
        gestor.cargar_datos_csv(args.csv)
        gestor.mostrar_informacion()

    if args.grafico:
        gestor.generar_grafico(args.grafico)

    if args.api:
        gestor.llamar_api(args.api)

    if args.calcular:
        gestor.realizar_calculos()

    if args.fecha:
        mostrar_fecha_actual()

    if args.guardar:
        gestor.guardar_datos_csv(args.guardar)


if __name__ == "__main__":
    main()
