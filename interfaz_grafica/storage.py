# -*- coding: utf-8 -*-
"""
storage.py - Capa de persistencia y exportación de nómina.
Reutiliza la lógica de reportes.py y calculos.py.
"""

import os
import csv
from interfaz_grafica.config import ARCHIVO_NOMINA
from calculos import cargos_operativos
from reportes import titulos, claves, crear_fila, guardar_txt
from volante import formato_pesos


def cargar_nomina(ruta=ARCHIVO_NOMINA):
    """
    Lee el archivo CSV/TXT de nómina y reconstruye la lista
    de diccionarios de empleados con todos sus atributos.
    """
    if not os.path.exists(ruta):
        return []

    empleados = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            lector = csv.reader(f)
            encabezado = next(lector, None)
            if not encabezado:
                return []

            for fila in lector:
                if not fila or len(fila) < len(claves):
                    continue

                nombre = fila[0].strip()
                tipo = fila[1].strip()
                cargo = fila[2].strip()
                horas = int(fila[3])
                salario = int(fila[4])
                horas_extras = int(fila[5])
                pago_extras = int(fila[6])
                salud = int(fila[7])
                pension = int(fila[8])
                arl = int(fila[9])
                total_pagar = int(fila[10])
                total_descuentos = salud + pension + arl

                # Reconstruir datos adicionales para el volante
                if tipo == "ADMINISTRATIVO":
                    porcentaje_arl = "0,522%"
                    ibc = None
                else:
                    porcentaje_arl = "0,522%"
                    for cop in cargos_operativos:
                        if cop["cargo"].lower() == cargo.lower():
                            porcentaje_arl = cop["texto_arl"]
                            break
                    ibc = round(salario * 0.40)

                emp = {
                    "nombre": nombre,
                    "tipo": tipo,
                    "cargo": cargo,
                    "horas": horas,
                    "salario": salario,
                    "horas_extras": horas_extras,
                    "pago_extras": pago_extras,
                    "salud": salud,
                    "pension": pension,
                    "arl": arl,
                    "porcentaje_arl": porcentaje_arl,
                    "total_descuentos": total_descuentos,
                    "total_pagar": total_pagar,
                }
                if ibc is not None:
                    emp["ibc"] = ibc

                empleados.append(emp)
    except Exception as e:
        print(f"Error al leer archivo {ruta}: {e}")

    return empleados


def guardar_nomina(empleados, ruta=ARCHIVO_NOMINA):
    """
    Guarda los empleados en el archivo plano TXT.
    Si la ruta es la estándar, usa directamente guardar_txt(empleados).
    """
    if ruta == ARCHIVO_NOMINA:
        guardar_txt(empleados)
    else:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(titulos)
            for emp in empleados:
                escritor.writerow(crear_fila(emp))


def generar_volante_texto(empleado):
    """Genera la representación textual detallada del volante oficial."""
    linea = "=" * 58
    lineas = [
        linea,
        "             TRANSCARIBECOL S.C.A. - NIT 900.123.456-7",
        "                COMPROBANTE OFICIAL DE PAGO",
        linea,
        f"  Empleado        : {empleado['nombre']}",
        f"  Tipo Laboral    : {empleado['tipo']}",
        f"  Cargo Oficial   : {empleado['cargo']}",
        f"  Horas Mes (HT)  : {empleado['horas']} horas",
        f"  Salario Base    : {formato_pesos(empleado['salario'])}",
    ]

    if empleado["tipo"] == "ADMINISTRATIVO":
        lineas.append(f"  Horas Extras    : {empleado['horas_extras']} ($25.000 c/u)")
        lineas.append(f"  Pago H. Extras  : {formato_pesos(empleado['pago_extras'])}")
        tot_dev = empleado["salario"] + empleado["pago_extras"]
        lineas.append(f"  TOTAL DEVENGADO : {formato_pesos(tot_dev)}")
        p_salud = "4,0%"
        p_pension = "4,0%"
    else:
        ibc = empleado.get("ibc", round(empleado["salario"] * 0.40))
        lineas.append(f"  Base IBC (40%)  : {formato_pesos(ibc)}")
        p_salud = "12,5%"
        p_pension = "16,0%"

    lineas.append("-" * 58)
    lineas.append("                 DEDUCCIONES LEGALES DE LEY")
    lineas.append("-" * 58)
    lineas.append(f"  • Salud ({p_salud:<5})   : {formato_pesos(empleado['salud'])}")
    lineas.append(f"  • Pensión ({p_pension:<5}) : {formato_pesos(empleado['pension'])}")
    lineas.append(f"  • ARL ({empleado['porcentaje_arl']:<6})   : {formato_pesos(empleado['arl'])}")
    lineas.append(f"  TOTAL DEDUCCIONES : {formato_pesos(empleado['total_descuentos'])}")
    lineas.append(linea)
    lineas.append(f"  >>> TOTAL NETO A PAGAR : {formato_pesos(empleado['total_pagar'])} <<<")
    lineas.append(linea)
    lineas.append("         Transportes del Gran Caribe Colombiano S.C.A.")
    lineas.append(linea)
    return "\n".join(lineas)
