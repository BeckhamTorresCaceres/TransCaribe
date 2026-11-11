# -*- coding: utf-8 -*-
"""
styles.py - Definición y configuración de temas modernos para Tkinter y TTK.
"""

import tkinter as tk
from tkinter import ttk
from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_BORDER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_LIGHT,
    COLOR_ACCENT,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_SUCCESS,
    COLOR_DANGER,
    FONT_FAMILY,
    FONT_BODY,
    FONT_BODY_BOLD,
)


def aplicar_estilos_modernos(root):
    """Configura el tema ttk y define los estilos modernos para los widgets."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Fondo general de la ventana
    root.configure(bg=COLOR_BG)

    # 1. Notebook (Pestañas modernas superiores)
    style.configure(
        "TNotebook",
        background=COLOR_BG,
        borderwidth=0,
        tabmargins=[4, 4, 4, 0],
    )
    style.configure(
        "TNotebook.Tab",
        font=(FONT_FAMILY, 10, "bold"),
        padding=[18, 9],
        background="#e2e8f0",
        foreground=COLOR_PRIMARY,
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_PRIMARY), ("active", "#cbd5e1")],
        foreground=[("selected", "#ffffff"), ("active", COLOR_PRIMARY)],
        expand=[("selected", [1, 2, 1, 0])],
    )

    # 2. Botones Modernos
    # Botón Primario (Azul Marino)
    style.configure(
        "Primary.TButton",
        font=(FONT_FAMILY, 10, "bold"),
        background=COLOR_PRIMARY,
        foreground="#ffffff",
        padding=[14, 7],
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARY_LIGHT), ("pressed", "#091e33")],
        foreground=[("active", "#ffffff")],
    )

    # Botón Éxito (Verde Esmeralda)
    style.configure(
        "Success.TButton",
        font=(FONT_FAMILY, 10, "bold"),
        background=COLOR_SUCCESS,
        foreground="#ffffff",
        padding=[12, 6],
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Success.TButton",
        background=[("active", "#15803d"), ("pressed", "#166534")],
        foreground=[("active", "#ffffff")],
    )

    # Botón Secundario (Gris suave neutro)
    style.configure(
        "Secondary.TButton",
        font=(FONT_FAMILY, 9),
        background="#e2e8f0",
        foreground=COLOR_TEXT,
        padding=[10, 5],
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Secondary.TButton",
        background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")],
        foreground=[("active", COLOR_TEXT)],
    )

    # Botón Peligro / Eliminar (Rojo)
    style.configure(
        "Danger.TButton",
        font=(FONT_FAMILY, 9, "bold"),
        background=COLOR_DANGER,
        foreground="#ffffff",
        padding=[10, 5],
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#b91c1c"), ("pressed", "#991b1b")],
        foreground=[("active", "#ffffff")],
    )

    # 3. Treeview (Tabla moderna y estilizada)
    style.configure(
        "Treeview.Heading",
        font=(FONT_FAMILY, 9, "bold"),
        background="#f1f5f9",
        foreground=COLOR_PRIMARY,
        padding=[6, 7],
        relief="flat",
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#e2e8f0")],
    )
    style.configure(
        "Treeview",
        font=FONT_BODY,
        rowheight=28,
        background="#ffffff",
        fieldbackground="#ffffff",
        foreground=COLOR_TEXT,
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", "#dbeafe")],
        foreground=[("selected", "#1e40af")],
    )

    # 4. Combobox y Entry
    style.configure(
        "TCombobox",
        font=FONT_BODY,
        padding=[6, 4],
    )
    style.configure(
        "TEntry",
        font=FONT_BODY,
        padding=[6, 4],
    )

    # 5. Separadores
    style.configure("TSeparator", background=COLOR_BORDER)

    return style


def crear_tarjeta(parent, padx=16, pady=16, **kwargs):
    """
    Crea un marco contenedor con estilo de tarjeta moderna:
    fondo blanco, borde sutil y margen interno.
    """
    frame = tk.Frame(
        parent,
        bg=COLOR_SURFACE,
        highlightbackground=COLOR_BORDER,
        highlightcolor=COLOR_ACCENT,
        highlightthickness=1,
        padx=padx,
        pady=pady,
        **kwargs,
    )
    return frame
