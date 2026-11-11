# reportes.py - Muestra la tabla de empleados y la guarda en el archivo TXT
import csv

# Títulos de la tabla (como en el enunciado) y la clave del diccionario de cada uno
titulos = ["Nombre", "Tipo", "Cargo", "HT", "Salario", "HE",
           "TPHE", "Salud", "Pension", "ARL", "Total a pagar"]

claves = ["nombre", "tipo", "cargo", "horas", "salario", "horas_extras",
          "pago_extras", "salud", "pension", "arl", "total_pagar"]


def crear_fila(empleado):
    fila = []
    for clave in claves:
        fila.append(empleado[clave])
    return fila


def calcular_anchos(empleados):
    anchos = []
    for i in range(len(titulos)):
        ancho = len(titulos[i])
        for empleado in empleados:
            largo = len(str(empleado[claves[i]]))
            if largo > ancho:
                ancho = largo
        anchos.append(ancho)
    return anchos


def mostrar_empleados(empleados):
    if len(empleados) == 0:
        print("No hay empleados registrados.")
    else:
        anchos = calcular_anchos(empleados)

        encabezado = ""
        for i in range(len(titulos)):
            encabezado = encabezado + titulos[i].ljust(anchos[i]) + "  "

        linea = "-" * len(encabezado)
        print(linea)
        print(encabezado)
        print(linea)

        for empleado in empleados:
            fila = crear_fila(empleado)
            texto = ""
            for i in range(len(fila)):
                texto = texto + str(fila[i]).ljust(anchos[i]) + "  "
            print(texto)

        print(linea)


def guardar_txt(empleados):
    if len(empleados) == 0:
        print("No hay empleados para guardar.")
    else:
        archivo = open("03_Registros_Nomina.txt", "w", newline="", encoding="utf-8")
        escritor = csv.writer(archivo)

        escritor.writerow(titulos)
        for empleado in empleados:
            escritor.writerow(crear_fila(empleado))

        archivo.close()
        print("Nómina guardada en 03_Registros_Nomina.txt")
