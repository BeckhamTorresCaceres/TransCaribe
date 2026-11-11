# -*- coding: utf-8 -*-
"""
regimenes_manager.py - Gestor de Regímenes Laborales y Cargos de TransCaribeCol.
Permite agregar, editar, eliminar y persistir cargos y regímenes laborales personalizados.
"""

import os
import json
from interfaz_grafica.config import BASE_DIR
import calculos

ARCHIVO_CONFIG = os.path.join(BASE_DIR, "config_regimenes.json")

# Clases oficiales de ARL según normativa colombiana (Decreto 1295 de 1994)
CLASES_ARL = [
    {"clase": "Clase I (Riesgo Mínimo - 0,522%)", "tasa": 0.00522, "texto": "0,522%"},
    {"clase": "Clase II (Riesgo Bajo - 1,044%)", "tasa": 0.01044, "texto": "1,044%"},
    {"clase": "Clase III (Riesgo Medio - 2,436%)", "tasa": 0.02436, "texto": "2,436%"},
    {"clase": "Clase IV (Riesgo Alto - 4,350%)", "tasa": 0.04350, "texto": "4,350%"},
    {"clase": "Clase V (Riesgo Máximo - 6,960%)", "tasa": 0.06960, "texto": "6,960%"},
]

CONFIG_POR_DEFECTO = {
    "regimenes": {
        "ADMINISTRATIVO": {
            "codigo": "ADMINISTRATIVO",
            "nombre": "Administrativo",
            "tarifa_hora": 20000,
            "permite_extras": True,
            "tarifa_extra": 25000,
            "horas_fijas": False,
            "porcentaje_ibc": 1.0,
            "porcentaje_salud": 0.04,
            "porcentaje_pension": 0.04,
            "porcentaje_arl_defecto": 0.00522,
            "texto_arl_defecto": "0,522%",
            "descripcion": "Tarifa $20.000/h + extras. Deducciones 4% salud, 4% pensión, 0.522% ARL sobre devengado.",
            "cargos": [
                {"cargo": "Auxiliar Administrativo", "horas": None, "arl": 0.00522, "texto_arl": "0,522%"},
            ],
        },
        "OPERATIVO": {
            "codigo": "OPERATIVO",
            "nombre": "Operativo",
            "tarifa_hora": 40000,
            "permite_extras": False,
            "tarifa_extra": 0,
            "horas_fijas": True,
            "porcentaje_ibc": 0.40,
            "porcentaje_salud": 0.125,
            "porcentaje_pension": 0.16,
            "porcentaje_arl_defecto": 0.01044,
            "texto_arl_defecto": "1,044%",
            "descripcion": "Tarifa $40.000/h fijas según cargo. IBC al 40%. Deducciones 12.5% salud, 16% pensión y ARL según riesgo.",
            "cargos": [
                {"cargo": "Conductor", "horas": 160, "arl": 0.01044, "texto_arl": "1,044%"},
                {"cargo": "Oficios Generales", "horas": 100, "arl": 0.00522, "texto_arl": "0,522%"},
                {"cargo": "Vigilancia", "horas": 336, "arl": 0.04350, "texto_arl": "4,350%"},
            ],
        },
    }
}


def cargar_configuracion():
    """Carga los regímenes y cargos desde el archivo JSON o crea el inicial."""
    if not os.path.exists(ARCHIVO_CONFIG):
        guardar_configuracion(CONFIG_POR_DEFECTO)
        return CONFIG_POR_DEFECTO

    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar claves esenciales
            if "regimenes" not in data or not data["regimenes"]:
                data = CONFIG_POR_DEFECTO
                guardar_configuracion(data)
            sincronizar_con_calculos(data)
            return data
    except Exception as e:
        print(f"Error cargando {ARCHIVO_CONFIG}: {e}. Usando valores por defecto.")
        return CONFIG_POR_DEFECTO


def guardar_configuracion(data):
    """Guarda la configuración en disco y actualiza calculos.py en memoria."""
    try:
        with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        sincronizar_con_calculos(data)
        return True
    except Exception as e:
        print(f"Error guardando {ARCHIVO_CONFIG}: {e}")
        return False


def sincronizar_con_calculos(data):
    """Sincroniza las listas globales de calculos.py con la configuración activa."""
    try:
        regimenes = data.get("regimenes", {})
        if "ADMINISTRATIVO" in regimenes:
            cargos_admin = [c["cargo"] for c in regimenes["ADMINISTRATIVO"].get("cargos", [])]
            calculos.cargos_administrativos.clear()
            calculos.cargos_administrativos.extend(cargos_admin)

        if "OPERATIVO" in regimenes:
            cargos_oper = regimenes["OPERATIVO"].get("cargos", [])
            calculos.cargos_operativos.clear()
            for cop in cargos_oper:
                calculos.cargos_operativos.append({
                    "cargo": cop["cargo"],
                    "horas": cop.get("horas", 160),
                    "arl": cop.get("arl", 0.01044),
                    "texto_arl": cop.get("texto_arl", "1,044%"),
                })
    except Exception as e:
        print(f"Error sincronizando con calculos.py: {e}")


def obtener_regimenes():
    cfg = cargar_configuracion()
    return cfg.get("regimenes", {})


def obtener_regimen(codigo):
    regimenes = obtener_regimenes()
    return regimenes.get(codigo.upper())


def agregar_o_actualizar_regimen(codigo, nombre, tarifa_hora, permite_extras, tarifa_extra,
                                  horas_fijas, porcentaje_ibc, pct_salud, pct_pension,
                                  pct_arl_def, texto_arl_def, descripcion=""):
    """Crea o actualiza un régimen laboral."""
    cfg = cargar_configuracion()
    cod = codigo.strip().upper()

    cargos_existentes = []
    if cod in cfg["regimenes"]:
        cargos_existentes = cfg["regimenes"][cod].get("cargos", [])

    cfg["regimenes"][cod] = {
        "codigo": cod,
        "nombre": nombre.strip(),
        "tarifa_hora": int(tarifa_hora),
        "permite_extras": bool(permite_extras),
        "tarifa_extra": int(tarifa_extra) if permite_extras else 0,
        "horas_fijas": bool(horas_fijas),
        "porcentaje_ibc": float(porcentaje_ibc),
        "porcentaje_salud": float(pct_salud),
        "porcentaje_pension": float(pct_pension),
        "porcentaje_arl_defecto": float(pct_arl_def),
        "texto_arl_defecto": str(texto_arl_def),
        "descripcion": descripcion.strip(),
        "cargos": cargos_existentes,
    }
    return guardar_configuracion(cfg)


def eliminar_regimen(codigo):
    """Elimina un régimen laboral personalizado."""
    cod = codigo.strip().upper()
    if cod in ("ADMINISTRATIVO", "OPERATIVO"):
        return False, "No se pueden eliminar los regímenes base del sistema (Administrativo y Operativo)."

    cfg = cargar_configuracion()
    if cod in cfg["regimenes"]:
        del cfg["regimenes"][cod]
        guardar_configuracion(cfg)
        return True, f"Régimen '{cod}' eliminado exitosamente."
    return False, "El régimen no existe."


def agregar_cargo(codigo_regimen, nombre_cargo, horas=None, arl=0.00522, texto_arl="0,522%"):
    """Agrega un nuevo cargo a un régimen específico."""
    cfg = cargar_configuracion()
    cod = codigo_regimen.strip().upper()

    if cod not in cfg["regimenes"]:
        return False, f"El régimen '{cod}' no existe."

    cargos = cfg["regimenes"][cod].setdefault("cargos", [])
    nom_limpio = nombre_cargo.strip()

    # Verificar si ya existe
    for c in cargos:
        if c["cargo"].lower() == nom_limpio.lower():
            return False, f"El cargo '{nom_limpio}' ya existe en el régimen {cod}."

    nuevo_cargo = {
        "cargo": nom_limpio,
        "horas": int(horas) if horas is not None and str(horas).strip() != "" else None,
        "arl": float(arl),
        "texto_arl": str(texto_arl),
    }
    cargos.append(nuevo_cargo)
    guardar_configuracion(cfg)
    return True, f"Cargo '{nom_limpio}' agregado exitosamente al régimen {cod}."


def eliminar_cargo(codigo_regimen, nombre_cargo):
    """Elimina un cargo de un régimen."""
    cfg = cargar_configuracion()
    cod = codigo_regimen.strip().upper()

    if cod not in cfg["regimenes"]:
        return False, f"El régimen '{cod}' no existe."

    cargos = cfg["regimenes"][cod].get("cargos", [])
    idx_a_borrar = None
    for i, c in enumerate(cargos):
        if c["cargo"].lower() == nombre_cargo.strip().lower():
            idx_a_borrar = i
            break

    if idx_a_borrar is None:
        return False, f"No se encontró el cargo '{nombre_cargo}'."

    cargos.pop(idx_a_borrar)
    guardar_configuracion(cfg)
    return True, f"Cargo '{nombre_cargo}' eliminado del régimen {cod}."


def calcular_empleado_dinamico(nombre, codigo_regimen, nombre_cargo, horas, horas_extras=0):
    """
    Calcula la nómina de cualquier empleado aplicando dinámicamente las reglas
    del régimen y del cargo seleccionados.
    """
    regimen = obtener_regimen(codigo_regimen)
    if not regimen:
        raise ValueError(f"Régimen '{codigo_regimen}' no encontrado.")

    # Buscar cargo dentro del régimen
    cargo_obj = None
    for c in regimen.get("cargos", []):
        if c["cargo"].lower() == nombre_cargo.strip().lower():
            cargo_obj = c
            break

    if not cargo_obj:
        cargo_obj = {
            "cargo": nombre_cargo,
            "horas": horas,
            "arl": regimen.get("porcentaje_arl_defecto", 0.00522),
            "texto_arl": regimen.get("texto_arl_defecto", "0,522%"),
        }

    tarifa_hora = regimen.get("tarifa_hora", 20000)
    permite_extras = regimen.get("permite_extras", False)
    tarifa_extra = regimen.get("tarifa_extra", 0) if permite_extras else 0
    horas_fijas = regimen.get("horas_fijas", False)

    if horas_fijas:
        horas_reales = cargo_obj.get("horas", 160) or 160
        horas_extras_reales = 0
        pago_extras = 0
    else:
        horas_reales = max(1, int(horas))
        horas_extras_reales = max(0, int(horas_extras)) if permite_extras else 0
        pago_extras = horas_extras_reales * tarifa_extra

    salario = horas_reales * tarifa_hora
    total_devengado = salario + pago_extras

    pct_ibc = regimen.get("porcentaje_ibc", 1.0)
    es_operativo_o_independiente = pct_ibc < 1.0

    if es_operativo_o_independiente:
        ibc = round(salario * pct_ibc)
        base_calculo = ibc
    else:
        ibc = None
        base_calculo = total_devengado

    pct_salud = regimen.get("porcentaje_salud", 0.04)
    pct_pension = regimen.get("porcentaje_pension", 0.04)
    pct_arl = cargo_obj.get("arl", regimen.get("porcentaje_arl_defecto", 0.00522))
    texto_arl = cargo_obj.get("texto_arl", regimen.get("texto_arl_defecto", "0,522%"))

    salud = round(base_calculo * pct_salud)
    pension = round(base_calculo * pct_pension)
    arl = round(base_calculo * pct_arl)
    total_descuentos = salud + pension + arl
    total_pagar = total_devengado - total_descuentos

    empleado = {
        "nombre": nombre,
        "tipo": codigo_regimen.upper(),
        "cargo": cargo_obj["cargo"],
        "horas": horas_reales,
        "salario": salario,
        "horas_extras": horas_extras_reales,
        "pago_extras": pago_extras,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "porcentaje_arl": texto_arl,
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar,
    }
    if ibc is not None:
        empleado["ibc"] = ibc

    return empleado
