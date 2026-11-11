# -*- coding: utf-8 -*-
"""
views/tab_reglas.py - Pestaña informativa moderna con íconos vectoriales y tarifas de ley.
"""

import tkinter as tk
from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_PRIMARY_LIGHT,
    COLOR_ACCENT,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    FONT_FAMILY,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_BODY,
    EMPRESA,
    EQUIPO,
    INTEGRANTES,
    INSTRUCTORA,
)
from interfaz_grafica.styles import crear_tarjeta
from interfaz_grafica.icons import crear_icono


class TabReglas(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)

        self.icon_admin = crear_icono("user", size=20, color=COLOR_PRIMARY)
        self.icon_bus = crear_icono("bus", size=20, color=COLOR_PRIMARY)
        self.icon_matrix = crear_icono("briefcase", size=20, color=COLOR_PRIMARY)
        self.icon_info = crear_icono("info", size=20, color=COLOR_ACCENT)

        self.construir_vista()

    def construir_vista(self):
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

        # Fila superior de 3 tarjetas
        grid_top = tk.Frame(container, bg=COLOR_BG)
        grid_top.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        grid_top.columnconfigure(0, weight=1)
        grid_top.columnconfigure(1, weight=1)
        grid_top.columnconfigure(2, weight=1)

        # ---------------- TARJETA 1: ADMINISTRATIVO ----------------
        c1 = crear_tarjeta(grid_top, padx=16, pady=16)
        c1.grid(row=0, column=0, sticky="nsew", padx=6)

        tk.Label(
            c1,
            text=" RÉGIMEN ADMINISTRATIVO",
            image=self.icon_admin,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor="w", pady=(0, 8))

        txt_admin = (
            "• Salario Base: $20.000 COP por hora.\n"
            "• Horas Laborales: Libres mensuales (mínimo 1).\n"
            "• Horas Extras: Permitidas a $25.000 COP c/u.\n"
            "• Devengado: (HT × $20.000) + (HE × $25.000).\n\n"
            "DEDUCCIONES DE LEY (Sobre Devengado):\n"
            "  - Salud: 4,0%\n"
            "  - Pensión: 4,0%\n"
            "  - ARL (Riesgo I): 0,522%\n\n"
            "• Neto = Total Devengado - Deducciones."
        )
        tk.Label(c1, text=txt_admin, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_SURFACE, justify="left").pack(anchor="w")

        # ---------------- TARJETA 2: OPERATIVO ----------------
        c2 = crear_tarjeta(grid_top, padx=16, pady=16)
        c2.grid(row=0, column=1, sticky="nsew", padx=6)

        tk.Label(
            c2,
            text=" RÉGIMEN OPERATIVO",
            image=self.icon_bus,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor="w", pady=(0, 8))

        txt_oper = (
            "• Salario Base: $40.000 COP por hora.\n"
            "• Horas fijas según cargo contractual.\n"
            "• Horas Extras: NO perciben horas extras.\n"
            "• Base de Cotización (IBC): 40% del salario.\n\n"
            "DEDUCCIONES DE LEY (Sobre el IBC):\n"
            "  - Salud: 12,5% del IBC\n"
            "  - Pensión: 16,0% del IBC\n"
            "  - ARL: Según nivel de riesgo del cargo.\n\n"
            "• Neto = Salario Bruto - Deducciones."
        )
        tk.Label(c2, text=txt_oper, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_SURFACE, justify="left").pack(anchor="w")

        # ---------------- TARJETA 3: CARGOS OPERATIVOS ----------------
        c3 = crear_tarjeta(grid_top, padx=16, pady=16)
        c3.grid(row=0, column=2, sticky="nsew", padx=6)

        tk.Label(
            c3,
            text=" MATRIZ DE CARGOS",
            image=self.icon_matrix,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor="w", pady=(0, 8))

        txt_matriz = (
            "1. Conductor:\n"
            "   • Horas: 160 h / mes\n"
            "   • Tarifa ARL: 1,044% (Riesgo II)\n\n"
            "2. Oficios Generales:\n"
            "   • Horas: 100 h / mes\n"
            "   • Tarifa ARL: 0,522% (Riesgo I)\n\n"
            "3. Vigilancia:\n"
            "   • Horas: 336 h / mes\n"
            "   • Tarifa ARL: 4,350% (Riesgo IV)\n\n"
            "Las tarifas y horas son fijas según contrato."
        )
        tk.Label(c3, text=txt_matriz, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_SURFACE, justify="left").pack(anchor="w")

        # ---------------- TARJETA INFERIOR: FICHA TÉCNICA ----------------
        c_bottom = crear_tarjeta(container, padx=18, pady=14)
        c_bottom.pack(fill=tk.X)

        tk.Label(
            c_bottom,
            text=f" {EMPRESA}",
            image=self.icon_info,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor="w")

        info_txt = f"{EQUIPO}  |  Instructora: {INSTRUCTORA}  |  Integrantes: {INTEGRANTES}"
        tk.Label(c_bottom, text=info_txt, font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor="w", pady=(2, 0))
