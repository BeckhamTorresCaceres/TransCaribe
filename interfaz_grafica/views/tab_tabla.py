# -*- coding: utf-8 -*-
"""
views/tab_tabla.py - Pestaña moderna de consulta de nómina con íconos vectoriales.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_PRIMARY_LIGHT,
    COLOR_ACCENT,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_SUCCESS,
    FONT_FAMILY,
    FONT_SUBTITLE,
    FONT_BODY,
    FONT_BODY_BOLD,
)
from interfaz_grafica.styles import crear_tarjeta
from interfaz_grafica.icons import crear_icono
from reportes import titulos, claves
from volante import formato_pesos


class TabTabla(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self.controller = controller

        # Cargar íconos para la barra de herramientas y filtros
        self.icon_search = crear_icono("search", size=16, color=COLOR_PRIMARY)
        self.icon_filter = crear_icono("filter", size=16, color=COLOR_TEXT_MUTED)
        self.icon_cargar = crear_icono("folder-open", size=16, color="#ffffff")
        self.icon_guardar = crear_icono("save", size=16, color="#ffffff")
        self.icon_eliminar = crear_icono("trash", size=16, color="#ffffff")
        self.icon_limpiar = crear_icono("refresh", size=16, color=COLOR_TEXT)
        self.icon_receipt = crear_icono("receipt", size=16, color=COLOR_TEXT)

        self.construir_vista()

    def construir_vista(self):
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        # ---------------------------------------------------------------------
        # BARRA SUPERIOR: BÚSQUEDA Y FILTROS MODERNOS CON ÍCONOS
        # ---------------------------------------------------------------------
        bar_filtro = crear_tarjeta(container, padx=14, pady=10)
        bar_filtro.pack(fill=tk.X, pady=(0, 10))

        # Buscador por texto con ícono de lupa
        lbl_buscar = tk.Label(
            bar_filtro,
            text=" Buscar:",
            image=self.icon_search,
            compound="left",
            font=FONT_BODY_BOLD,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        )
        lbl_buscar.pack(side=tk.LEFT, padx=(0, 6))

        self.var_buscar = tk.StringVar()
        self.ent_buscar = ttk.Entry(bar_filtro, textvariable=self.var_buscar, font=FONT_BODY, width=28)
        self.ent_buscar.pack(side=tk.LEFT, padx=(0, 14))
        self.ent_buscar.bind("<KeyRelease>", lambda e: self.aplicar_filtros())

        # Filtro por Tipo de Régimen con ícono de filtro
        lbl_filtro_tipo = tk.Label(
            bar_filtro,
            text=" Régimen:",
            image=self.icon_filter,
            compound="left",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        )
        lbl_filtro_tipo.pack(side=tk.LEFT, padx=(0, 6))

        self.var_filtro_tipo = tk.StringVar(value="TODOS")
        self.cb_filtro_tipo = ttk.Combobox(
            bar_filtro,
            textvariable=self.var_filtro_tipo,
            values=["TODOS", "ADMINISTRATIVO", "OPERATIVO"],
            state="readonly",
            width=16,
            font=FONT_BODY,
        )
        self.cb_filtro_tipo.pack(side=tk.LEFT, padx=(0, 16))
        self.cb_filtro_tipo.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        self.recargar_filtros_regimen()

        # Botones de Acción con íconos
        btn_cargar = ttk.Button(
            bar_filtro,
            text=" Cargar TXT",
            image=self.icon_cargar,
            compound="left",
            style="Primary.TButton",
            command=self.controller.cargar_txt,
        )
        btn_cargar.pack(side=tk.LEFT, padx=(0, 6))

        btn_guardar = ttk.Button(
            bar_filtro,
            text=" Guardar TXT",
            image=self.icon_guardar,
            compound="left",
            style="Success.TButton",
            command=self.controller.guardar_txt,
        )
        btn_guardar.pack(side=tk.LEFT, padx=(0, 6))

        btn_ver_vol = ttk.Button(
            bar_filtro,
            text=" Ver Volante",
            image=self.icon_receipt,
            compound="left",
            style="Secondary.TButton",
            command=self.ver_volante_seleccionado,
        )
        btn_ver_vol.pack(side=tk.LEFT, padx=(0, 6))

        btn_eliminar = ttk.Button(
            bar_filtro,
            text=" Eliminar",
            image=self.icon_eliminar,
            compound="left",
            style="Danger.TButton",
            command=self.eliminar_seleccionado,
        )
        btn_eliminar.pack(side=tk.RIGHT)

        btn_limpiar = ttk.Button(
            bar_filtro,
            text=" Vaciar",
            image=self.icon_limpiar,
            compound="left",
            style="Secondary.TButton",
            command=self.vaciar_tabla,
        )
        btn_limpiar.pack(side=tk.RIGHT, padx=(0, 6))

        # ---------------------------------------------------------------------
        # TABLA TREEVIEW CON SCROLLBARS
        # ---------------------------------------------------------------------
        table_card = crear_tarjeta(container, padx=0, pady=0)
        table_card.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(table_card, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = ttk.Scrollbar(table_card, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        cols = ("idx",) + tuple(claves)
        self.tree = ttk.Treeview(
            table_card,
            columns=cols,
            show="headings",
            selectmode="browse",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar Columnas
        self.tree.heading("idx", text="#")
        self.tree.column("idx", width=38, anchor="center")

        anchos = {
            "nombre": 180,
            "tipo": 115,
            "cargo": 145,
            "horas": 55,
            "salario": 95,
            "horas_extras": 50,
            "pago_extras": 85,
            "salud": 80,
            "pension": 80,
            "arl": 80,
            "total_pagar": 115,
        }

        for i, clave in enumerate(claves):
            nom_col = titulos[i]
            self.tree.heading(clave, text=nom_col)
            ancho = anchos.get(clave, 90)
            alinear = "w" if clave in ("nombre", "cargo") else ("center" if clave in ("tipo", "horas", "horas_extras") else "e")
            self.tree.column(clave, width=ancho, anchor=alinear)

        # Evento doble clic para ver el volante del empleado seleccionado
        self.tree.bind("<Double-1>", lambda e: self.ver_volante_seleccionado())

        # Colores alternados de filas
        self.tree.tag_configure("par", background="#f8fafc")
        self.tree.tag_configure("impar", background="#ffffff")

        # ---------------------------------------------------------------------
        # TARJETAS DE MÉTRICAS KPI INFERIORES
        # ---------------------------------------------------------------------
        kpi_row = tk.Frame(container, bg=COLOR_BG)
        kpi_row.pack(fill=tk.X, pady=(10, 0))

        self.kpi_count = self.crear_tarjeta_kpi(kpi_row, "Total Trabajadores", "0", 0)
        self.kpi_bruto = self.crear_tarjeta_kpi(kpi_row, "Total Devengado Bruto", "$0", 1)
        self.kpi_desc = self.crear_tarjeta_kpi(kpi_row, "Deducciones de Ley", "$0", 2)
        self.kpi_neto = self.crear_tarjeta_kpi(kpi_row, "Total Nómina a Pagar", "$0", 3, destacado=True)

    def crear_tarjeta_kpi(self, parent, titulo, valor_ini, col, destacado=False):
        bg_card = "#0f766e" if destacado else COLOR_SURFACE
        fg_tit = "#ccfbf1" if destacado else COLOR_TEXT_MUTED
        fg_val = "#ffffff" if destacado else COLOR_PRIMARY

        card = tk.Frame(
            parent,
            bg=bg_card,
            highlightbackground="#0d9488" if destacado else "#cbd5e1",
            highlightthickness=1,
            padx=14,
            pady=8,
        )
        card.grid(row=0, column=col, sticky="nsew", padx=4)
        parent.columnconfigure(col, weight=1)

        lbl_t = tk.Label(card, text=titulo.upper(), font=(FONT_FAMILY, 8, "bold"), fg=fg_tit, bg=bg_card)
        lbl_t.pack(anchor="w")

        lbl_v = tk.Label(card, text=valor_ini, font=(FONT_FAMILY, 12, "bold"), fg=fg_val, bg=bg_card)
        lbl_v.pack(anchor="w", pady=(2, 0))

        return lbl_v

    def recargar_filtros_regimen(self):
        from interfaz_grafica.regimenes_manager import obtener_regimenes
        regs = list(obtener_regimenes().keys())
        self.cb_filtro_tipo["values"] = ["TODOS"] + regs
        if self.var_filtro_tipo.get() not in self.cb_filtro_tipo["values"]:
            self.var_filtro_tipo.set("TODOS")

    def renderizar_tabla(self, empleados):
        """Llena la tabla y actualiza los indicadores KPI."""
        self.empleados_cache = empleados
        self.aplicar_filtros()

    def aplicar_filtros(self):
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        texto_busqueda = self.var_buscar.get().strip().lower()
        filtro_tipo = self.var_filtro_tipo.get()

        empleados = getattr(self, "empleados_cache", [])

        total_dev = 0
        total_desc = 0
        total_neto = 0
        conteo_mostrados = 0

        for i, emp in enumerate(empleados):
            # Filtro por tipo
            if filtro_tipo != "TODOS" and emp["tipo"] != filtro_tipo:
                continue

            # Filtro por texto
            if texto_busqueda:
                nombre = emp["nombre"].lower()
                cargo = emp["cargo"].lower()
                if texto_busqueda not in nombre and texto_busqueda not in cargo:
                    continue

            conteo_mostrados += 1
            tag = "par" if conteo_mostrados % 2 == 0 else "impar"

            dev_emp = emp["salario"] + emp.get("pago_extras", 0)
            total_dev += dev_emp
            total_desc += emp["total_descuentos"]
            total_neto += emp["total_pagar"]

            valores = (
                i + 1,
                emp["nombre"],
                emp["tipo"],
                emp["cargo"],
                emp["horas"],
                formato_pesos(emp["salario"]),
                emp["horas_extras"],
                formato_pesos(emp["pago_extras"]),
                formato_pesos(emp["salud"]),
                formato_pesos(emp["pension"]),
                formato_pesos(emp["arl"]),
                formato_pesos(emp["total_pagar"]),
            )
            # Guardamos el índice real del empleado en el iid
            self.tree.insert("", tk.END, iid=str(i), values=valores, tags=(tag,))

        # Actualizar KPIs
        self.kpi_count.config(text=f"{conteo_mostrados} de {len(empleados)}")
        self.kpi_bruto.config(text=formato_pesos(total_dev))
        self.kpi_desc.config(text=formato_pesos(total_desc))
        self.kpi_neto.config(text=formato_pesos(total_neto))

    def ver_volante_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Haga clic en un empleado de la tabla.", parent=self)
            return

        indice = int(sel[0])
        self.controller.seleccionar_para_volante(indice)

    def eliminar_seleccionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Seleccione una fila para eliminar.", parent=self)
            return

        indice = int(sel[0])
        emp = self.controller.obtener_empleado(indice)
        if not emp:
            return

        conf = messagebox.askyesno(
            "Confirmación",
            f"¿Desea eliminar a '{emp['nombre']}' de la nómina?",
            parent=self,
        )
        if conf:
            self.controller.eliminar_empleado(indice)

    def vaciar_tabla(self):
        if not self.controller.empleados:
            return
        conf = messagebox.askyesno(
            "Vaciar Nómina",
            "¿Está seguro de vaciar todos los registros cargados en memoria?",
            parent=self,
        )
        if conf:
            self.controller.vaciar_empleados()
