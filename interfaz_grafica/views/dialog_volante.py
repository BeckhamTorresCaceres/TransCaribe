# -*- coding: utf-8 -*-
"""
views/dialog_volante.py - Ventana modal estilizada para inspección de volante de pago individual.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_TEXT,
    FONT_FAMILY,
    FONT_SUBTITLE,
)
from interfaz_grafica.storage import generar_volante_texto
from volante import imprimir_volante


class DialogVolante(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.empleado = empleado

        self.title(f"Volante de Pago - {empleado['nombre']}")
        self.geometry("640x560")
        self.minsize(560, 480)
        self.configure(bg=COLOR_BG)
        self.transient(parent)
        self.grab_set()

        self.construir_vista()

    def construir_vista(self):
        container = tk.Frame(self, bg=COLOR_BG, padx=16, pady=16)
        container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(container, bg=COLOR_BG)
        header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header,
            text=f"🧾 Volante de Pago: {self.empleado['nombre']}",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_BG,
        ).pack(side=tk.LEFT)

        # Recuadro de texto del volante
        box = tk.Frame(container, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1)
        box.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        scroll = ttk.Scrollbar(box, orient="vertical")
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        txt = tk.Text(
            box,
            font=("Courier New", 10),
            bg="#ffffff",
            fg=COLOR_TEXT,
            padx=16,
            pady=14,
            wrap="word",
            yscrollcommand=scroll.set,
            relief="flat",
        )
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=txt.yview)

        texto_vol = generar_volante_texto(self.empleado)
        txt.insert(tk.END, texto_vol)
        txt.config(state="disabled")

        # Botones de Acción
        btn_bar = tk.Frame(container, bg=COLOR_BG)
        btn_bar.pack(fill=tk.X)

        btn_consola = ttk.Button(
            btn_bar,
            text="🖨️ En Consola",
            style="Secondary.TButton",
            command=lambda: (imprimir_volante(self.empleado), messagebox.showinfo("Impresión", "Impreso en consola.", parent=self)),
        )
        btn_consola.pack(side=tk.LEFT, padx=(0, 6))

        btn_copiar = ttk.Button(
            btn_bar,
            text="📋 Copiar",
            style="Secondary.TButton",
            command=lambda: (self.clipboard_clear(), self.clipboard_append(texto_vol), messagebox.showinfo("Copiado", "Copiado al portapapeles.", parent=self)),
        )
        btn_copiar.pack(side=tk.LEFT, padx=(0, 6))

        btn_cerrar = ttk.Button(
            btn_bar,
            text="Cerrar",
            style="Primary.TButton",
            command=self.destroy,
        )
        btn_cerrar.pack(side=tk.RIGHT)
