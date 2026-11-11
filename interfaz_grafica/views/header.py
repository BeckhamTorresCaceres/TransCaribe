# -*- coding: utf-8 -*-
"""
views/header.py - Encabezado corporativo moderno con íconos vectoriales y estadísticas.
"""

import tkinter as tk
from interfaz_grafica.config import (
    COLOR_PRIMARY,
    COLOR_PRIMARY_LIGHT,
    COLOR_TEXT_INVERSE,
    EMPRESA,
    SIGLA,
    SISTEMA,
    FONT_FAMILY,
)
from interfaz_grafica.icons import crear_icono


class ModernHeader(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_PRIMARY, height=76, **kwargs)
        self.pack(fill=tk.X, side=tk.TOP)
        self.pack_propagate(False)

        inner = tk.Frame(self, bg=COLOR_PRIMARY)
        inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=10)

        # Lado izquierdo: Ícono de bus y títulos
        left_box = tk.Frame(inner, bg=COLOR_PRIMARY)
        left_box.pack(side=tk.LEFT, fill=tk.Y)

        self.icon_bus = crear_icono("bus", size=32, color="#38bdf8")
        lbl_logo = tk.Label(
            left_box,
            image=self.icon_bus,
            bg=COLOR_PRIMARY,
        )
        lbl_logo.pack(side=tk.LEFT, padx=(0, 14))

        titles_box = tk.Frame(left_box, bg=COLOR_PRIMARY)
        titles_box.pack(side=tk.LEFT, fill=tk.Y)

        lbl_sigla = tk.Label(
            titles_box,
            text=f"{SIGLA} · {SISTEMA.upper()}",
            font=(FONT_FAMILY, 14, "bold"),
            fg=COLOR_TEXT_INVERSE,
            bg=COLOR_PRIMARY,
            anchor="w",
        )
        lbl_sigla.pack(anchor="w")

        lbl_empresa = tk.Label(
            titles_box,
            text=f"{EMPRESA} | Liquidación y Descuentos Legales de Ley",
            font=(FONT_FAMILY, 9),
            fg="#94a3b8",
            bg=COLOR_PRIMARY,
            anchor="w",
        )
        lbl_empresa.pack(anchor="w")

        # Lado derecho: Píldora de estado con registros
        right_box = tk.Frame(inner, bg=COLOR_PRIMARY)
        right_box.pack(side=tk.RIGHT, fill=tk.Y)

        self.badge_box = tk.Frame(
            right_box,
            bg=COLOR_PRIMARY_LIGHT,
            padx=14,
            pady=6,
            highlightbackground="#334155",
            highlightthickness=1,
        )
        self.badge_box.pack(side=tk.RIGHT, pady=4)

        self.icon_user_badge = crear_icono("user", size=16, color="#38bdf8")
        self.lbl_badge_text = tk.Label(
            self.badge_box,
            text=" Nómina: 0 empleados",
            image=self.icon_user_badge,
            compound="left",
            font=(FONT_FAMILY, 9, "bold"),
            fg="#38bdf8",
            bg=COLOR_PRIMARY_LIGHT,
        )
        self.lbl_badge_text.pack()

    def actualizar_conteo(self, total):
        """Actualiza el contador de empleados en el encabezado."""
        self.lbl_badge_text.config(text=f" Nómina: {total} empleados")
