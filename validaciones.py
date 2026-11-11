# validaciones.py - Funciones para pedir datos al usuario


def pedir_nombre(mensaje):
    nombre = ""
    es_invalido = True

    while es_invalido == True:
        nombre = input(mensaje).strip()
        sin_espacios = nombre.replace(" ", "")
        if sin_espacios != "" and sin_espacios.isalpha():
            es_invalido = False
        else:
            print("El nombre solo puede tener letras y espacios.")

    return nombre


def pedir_numero(mensaje, minimo):
    numero = 0
    es_invalido = True

    while es_invalido == True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                es_invalido = False
            else:
                print("El número debe ser mayor o igual a", minimo)
        except ValueError:
            print("Debe ingresar un número entero.")

    return numero


def pedir_opcion(mensaje, opciones):
    opcion = ""
    es_invalido = True

    while es_invalido == True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            es_invalido = False
        else:
            print("Opción inválida, intente de nuevo.")

    return opcion
