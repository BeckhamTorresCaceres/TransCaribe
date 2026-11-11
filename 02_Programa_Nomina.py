# main.py - Menú principal del módulo de nómina de TransCaribeCol
from validaciones import pedir_nombre, pedir_numero, pedir_opcion
from calculos import cargos_administrativos, cargos_operativos
from calculos import calcular_administrativo, calcular_operativo
from volante import imprimir_volante
from reportes import mostrar_empleados, guardar_txt

# Sincronizar con cargos y regímenes configurados si existen
try:
    from interfaz_grafica.regimenes_manager import cargar_configuracion
    cargar_configuracion()
except Exception:
    pass


def elegir_de_lista(nombres):
    opciones = []
    for i in range(len(nombres)):
        print(i + 1, "-", nombres[i])
        opciones.append(str(i + 1))

    opcion = pedir_opcion("Seleccione el cargo: ", opciones)
    return int(opcion) - 1


def registrar_administrativo(empleados):
    print("\n--- Registro de Empleado Administrativo ---")
    nombre = pedir_nombre("Nombre completo: ")

    posicion = elegir_de_lista(cargos_administrativos)
    cargo = cargos_administrativos[posicion]

    horas = pedir_numero("Horas trabajadas en el mes: ", 1)
    horas_extras = pedir_numero("Horas extras trabajadas: ", 0)

    empleado = calcular_administrativo(nombre, cargo, horas, horas_extras)
    empleados.append(empleado)
    imprimir_volante(empleado)


def registrar_operativo(empleados):
    print("\n--- Registro de Empleado Operativo ---")
    nombre = pedir_nombre("Nombre completo: ")

    nombres_cargos = []
    for cargo in cargos_operativos:
        nombres_cargos.append(cargo["cargo"] + " (" + str(cargo["horas"]) + " horas)")

    posicion = elegir_de_lista(nombres_cargos)
    cargo_elegido = cargos_operativos[posicion]

    empleado = calcular_operativo(nombre, cargo_elegido)
    empleados.append(empleado)
    imprimir_volante(empleado)


def mostrar_menu():
    print("\n=============================================")
    print("    TRANSCARIBECOL - MÓDULO DE NÓMINA")
    print("=============================================")
    print("1. Registrar empleado Administrativo")
    print("2. Registrar empleado Operativo")
    print("3. Mostrar empleados registrados")
    print("4. Guardar nómina en archivo TXT")
    print("5. Abrir Interfaz Gráfica (Tkinter)")
    print("6. Salir")


def abrir_gui(empleados):
    try:
        from interfaz_grafica import TransCaribeApp
        print("\nIniciando interfaz gráfica modular (Tkinter)...")
        app = TransCaribeApp()
        # Si ya se registraron empleados en consola, sincronizarlos
        if empleados:
            for emp in empleados:
                if emp not in app.empleados:
                    app.empleados.append(emp)
            app.sincronizar_vistas()
            if app.empleados:
                app.seleccionar_para_volante(len(app.empleados) - 1)
        app.mainloop()
    except Exception as e:
        print("No se pudo iniciar la interfaz gráfica:", e)


def main():
    empleados = []
    continuar = True

    while continuar == True:
        mostrar_menu()
        opcion = pedir_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6"])

        if opcion == "1":
            registrar_administrativo(empleados)
        elif opcion == "2":
            registrar_operativo(empleados)
        elif opcion == "3":
            mostrar_empleados(empleados)
        elif opcion == "4":
            guardar_txt(empleados)
        elif opcion == "5":
            abrir_gui(empleados)
        else:
            print("Saliendo del sistema... ¡Hasta pronto!")
            continuar = False


main()
