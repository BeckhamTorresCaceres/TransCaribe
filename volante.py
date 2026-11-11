# volante.py - Imprime el volante de pago en pantalla


def formato_pesos(valor):
    return "$" + f"{valor:,}"


def imprimir_volante(empleado):
    linea = "*" * 56

    print()
    print(linea)
    print("******************* VOLANTE DE PAGO ********************")
    print(linea)
    print("Nombre:", empleado["nombre"])
    print("Tipo:", empleado["tipo"])
    print("Cargo:", empleado["cargo"])
    print("Horas Trabajadas(mes):", empleado["horas"])
    print("Salario Bruto:", formato_pesos(empleado["salario"]))

    if empleado["tipo"] == "ADMINISTRATIVO":
        print("Horas Extras:", empleado["horas_extras"])
        print("Total pago Horas Extras:", formato_pesos(empleado["pago_extras"]))
        porcentaje_salud = "4%"
        porcentaje_pension = "4%"
    else:
        print("IBC (40%):", formato_pesos(empleado["ibc"]))
        porcentaje_salud = "12,5%"
        porcentaje_pension = "16%"

    print()
    print(linea)
    print("****************** DESCUENTOS DE LEY *******************")
    print(linea)
    print("Salud(" + porcentaje_salud + "):", formato_pesos(empleado["salud"]))
    print("Pensión(" + porcentaje_pension + "):", formato_pesos(empleado["pension"]))
    print("ARL(" + empleado["porcentaje_arl"] + "):", formato_pesos(empleado["arl"]))
    print("Total Descuentos:", formato_pesos(empleado["total_descuentos"]))
    print()
    print("Total a pagar:", formato_pesos(empleado["total_pagar"]))
    print()
    print(linea)
    print("*************** FIN DEL VOLANTE DE PAGO ****************")
    print(linea)
