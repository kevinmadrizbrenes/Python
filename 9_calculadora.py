from fractions import Fraction

class Calculadora:
    def __init__(self):
        self.resultado = 0

    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("Error: No se puede dividir por cero.")
            return None

    def potencia_triple(self, a, b, c):
        try:
            return a ** b ** c
        except Exception as e:
            print(f"Error: {e}")
            return None

    def raiz_cuadrada(self, a, b):
        if a >= 2:
            try:
                return b ** (1/a)
            except Exception as e:
                print(f"Error: {e}")
                return None
        else:
            print("Número tiene que ser mayor o igual a 2")

    def es_racional(self, x):
        try:
            Fraction(x)
            return True
        except ValueError:
            return False

def mostrar_menu():
    print("\n--- MENÚ DE CALCULADORA ---")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Potencia Triple")
    print("6. Radical")
    print("7. Salir")

def obtener_numero(numero):
    while True:
        try:
            return float(input("Ingrese el número " + numero + ": "))
        except ValueError:
            print("Error: Por favor, ingresa un número válido.")

def evaluar_racionales(resultado):
    es_fraccion = Fraction(resultado)
    if es_fraccion == True:
        print("El resultado es racional.")
    else:
        print("El resultado no es racional.")

def ejecutar_opcion(opcion, calculadora):
    if opcion == 1:
        a = obtener_numero("a")
        b = obtener_numero("b")
        resultado = calculadora.sumar(a, b)
        print("Resultado:", resultado)
        evaluar_racionales(resultado)

    elif opcion == 2:
        a = obtener_numero("a")
        b = obtener_numero("b")
        resultado = calculadora.restar(a, b)
        print("Resultado:", resultado)
        evaluar_racionales(resultado)

    elif opcion == 3:
        a = obtener_numero("a")
        b = obtener_numero("b")
        resultado = calculadora.multiplicar(a, b)
        print("Resultado:", resultado)
        evaluar_racionales(resultado)

    elif opcion == 4:
        a = obtener_numero("a")
        b = obtener_numero("b")
        resultado = calculadora.dividir(a, b)
        if resultado is not None:
            print("Resultado:", resultado)
            evaluar_racionales(resultado)

    elif opcion == 5:
        a = obtener_numero("a")
        b = obtener_numero("b")
        c = obtener_numero("c")
        resultado = calculadora.potencia_triple(a, b, c)
        print("Resultado:", resultado)

    elif opcion == 6:
        a = obtener_numero("índice de la raíz")
        b = obtener_numero("radicando")
        resultado = calculadora.raiz_cuadrada(a, b)
        print("Resultado:", resultado)
        evaluar_racionales(resultado)

    elif opcion == 7:
        print("Saliendo del programa...")
    else:
        print("Opción no válida. Por favor, elige una opción del menú.")

def main():
    calculadora = Calculadora()
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-7): "))
            if opcion == 7:
                break
            ejecutar_opcion(opcion, calculadora)
        except ValueError:
            print("Error: Por favor, ingresa un número válido.")

if __name__ == "__main__":
    main()
