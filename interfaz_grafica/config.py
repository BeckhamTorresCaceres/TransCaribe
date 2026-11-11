# -*- coding: utf-8 -*-
"""
config.py - Constantes, temas y configuraciones del módulo de interfaz gráfica.
"""

import os
import sys

# Ruta raíz del proyecto (donde residen los archivos .py originales)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

ARCHIVO_NOMINA = os.path.join(BASE_DIR, "03_Registros_Nomina.txt")

# Metadatos del Sistema
EMPRESA = "Transportes del Gran Caribe Colombiano S.C.A."
SIGLA = "TransCaribeCol"
SISTEMA = "Módulo de Nómina y Liquidación Laboral"
EQUIPO = "Actividad 3.4 · Equipo 01 · Python"
INTEGRANTES = "Joseph Herreño, Mateo Mercado y Beckham Torres"
INSTRUCTORA = "Norma Caro"

# Paleta de Colores Moderna (Inspirada en Tailwind Slate / Navy / Cyan)
COLOR_BG = "#f8fafc"             # Fondo de la aplicación (slate-50)
COLOR_SURFACE = "#ffffff"        # Fondo de tarjetas y paneles
COLOR_BORDER = "#e2e8f0"         # Bordes sutiles (slate-200)
COLOR_BORDER_FOCUS = "#38bdf8"   # Borde activo

COLOR_PRIMARY = "#0f2d4a"        # Azul marino corporativo profundo
COLOR_PRIMARY_LIGHT = "#1e3a5f"  # Azul medio para hovers y selecciones
COLOR_ACCENT = "#0284c7"         # Azul cian destacado
COLOR_ACCENT_BG = "#f0f9ff"      # Fondo celeste suave

COLOR_TEXT = "#0f172a"           # Texto principal oscuro
COLOR_TEXT_MUTED = "#64748b"     # Texto secundario/atenuado
COLOR_TEXT_INVERSE = "#ffffff"   # Texto blanco sobre fondos oscuros

COLOR_SUCCESS = "#16a34a"        # Verde éxito / Total neto
COLOR_SUCCESS_BG = "#ecfdf5"     # Fondo verde claro
COLOR_DANGER = "#dc2626"         # Rojo acciones destructivas
COLOR_WARNING = "#d97706"        # Ámbar advertencias

# Tipografías recomendadas para Linux/Windows
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 15, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 9)
FONT_BODY_BOLD = (FONT_FAMILY, 9, "bold")
FONT_CAPTION = (FONT_FAMILY, 8)
FONT_MONO = ("Courier New", 9)
