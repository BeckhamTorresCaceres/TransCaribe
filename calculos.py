# calculos.py - Cargos disponibles y cálculo de la nómina

# La guía solo menciona este cargo administrativo.
# Si la instructora autoriza otros, se agregan a esta lista.
cargos_administrativos = [
    "Auxiliar Administrativo",
]

cargos_operativos = [
    {"cargo": "Conductor", "horas": 160, "arl": 0.01044, "texto_arl": "1,044%"},
    {"cargo": "Oficios Generales", "horas": 100, "arl": 0.00522, "texto_arl": "0,522%"},
    {"cargo": "Vigilancia", "horas": 336, "arl": 0.04350, "texto_arl": "4,350%"},
]


def calcular_administrativo(nombre, cargo, horas, horas_extras):
    salario = horas * 20000
    pago_extras = horas_extras * 25000
    total_devengado = salario + pago_extras

    salud = round(total_devengado * 0.04)
    pension = round(total_devengado * 0.04)
    arl = round(total_devengado * 0.00522)
    total_descuentos = salud + pension + arl
    total_pagar = total_devengado - total_descuentos

    empleado = {
        "nombre": nombre,
        "tipo": "ADMINISTRATIVO",
        "cargo": cargo,
        "horas": horas,
        "salario": salario,
        "horas_extras": horas_extras,
        "pago_extras": pago_extras,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "porcentaje_arl": "0,522%",
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar,
    }
    return empleado


def calcular_operativo(nombre, cargo_elegido):
    horas = cargo_elegido["horas"]
    salario = horas * 40000
    ibc = salario * 0.40

    salud = round(ibc * 0.125)
    pension = round(ibc * 0.16)
    arl = round(ibc * cargo_elegido["arl"])
    total_descuentos = salud + pension + arl
    total_pagar = salario - total_descuentos

    empleado = {
        "nombre": nombre,
        "tipo": "OPERATIVO",
        "cargo": cargo_elegido["cargo"],
        "horas": horas,
        "salario": salario,
        "horas_extras": 0,
        "pago_extras": 0,
        "ibc": round(ibc),
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "porcentaje_arl": cargo_elegido["texto_arl"],
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar,
    }
    return empleado
