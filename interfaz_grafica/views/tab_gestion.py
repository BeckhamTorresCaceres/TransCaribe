# -*- coding: utf-8 -*-
"""
views/tab_gestion.py - Pestaña moderna para agregar y gestionar Cargos y Regímenes Laborales.
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
    FONT_FAMILY,
    FONT_SUBTITLE,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_CAPTION,
)
from interfaz_grafica.styles import crear_tarjeta
from interfaz_grafica.icons import crear_icono
from interfaz_grafica.regimenes_manager import (
    obtener_regimenes,
    obtener_regimen,
    agregar_cargo,
    eliminar_cargo,
    agregar_o_actualizar_regimen,
    eliminar_regimen,
    CLASES_ARL,
)
from volante import formato_pesos


class TabGestion(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self.controller = controller

        # Íconos para la vista
        self.icon_cargos = crear_icono("briefcase", size=20, color=COLOR_PRIMARY)
        self.icon_regimen = crear_icono("settings", size=20, color=COLOR_PRIMARY)
        self.icon_plus = crear_icono("plus-circle", size=16, color="#ffffff")
        self.icon_trash = crear_icono("trash", size=16, color="#ffffff")

        self.construir_vista()

    def construir_vista(self):
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        container.columnconfigure(0, weight=5, minsize=460)
        container.columnconfigure(1, weight=5, minsize=460)
        container.rowconfigure(0, weight=1)

        # =====================================================================
        # COLUMNA IZQUIERDA: GESTIÓN DE CARGOS
        # =====================================================================
        card_cargos = crear_tarjeta(container, padx=16, pady=14)
        card_cargos.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

        lbl_tit_cargos = tk.Label(
            card_cargos,
            text=" Gestión de Cargos por Régimen",
            image=self.icon_cargos,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        )
        lbl_tit_cargos.pack(anchor="w", pady=(0, 6))

        # Selector del Régimen para filtrar cargos
        frame_sel_reg = tk.Frame(card_cargos, bg=COLOR_SURFACE)
        frame_sel_reg.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            frame_sel_reg,
            text="Seleccionar Régimen:",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.cb_filtro_regimen = ttk.Combobox(frame_sel_reg, state="readonly", font=FONT_BODY, width=22)
        self.cb_filtro_regimen.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cb_filtro_regimen.bind("<<ComboboxSelected>>", lambda e: self.cargar_cargos_de_regimen())

        # Tabla de Cargos Existentes
        frame_tree_cargos = tk.Frame(card_cargos, bg=COLOR_SURFACE)
        frame_tree_cargos.pack(fill=tk.BOTH, expand=True, pady=(4, 6))

        scroll_c = ttk.Scrollbar(frame_tree_cargos, orient="vertical")
        scroll_c.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_cargos = ttk.Treeview(
            frame_tree_cargos,
            columns=("cargo", "horas", "arl"),
            show="headings",
            selectmode="browse",
            height=6,
            yscrollcommand=scroll_c.set,
        )
        self.tree_cargos.pack(fill=tk.BOTH, expand=True)
        scroll_c.config(command=self.tree_cargos.yview)

        self.tree_cargos.heading("cargo", text="Cargo")
        self.tree_cargos.heading("horas", text="Horas Mes")
        self.tree_cargos.heading("arl", text="Tasa ARL")

        self.tree_cargos.column("cargo", width=180, anchor="w")
        self.tree_cargos.column("horas", width=80, anchor="center")
        self.tree_cargos.column("arl", width=90, anchor="center")

        btn_borrar_cargo = ttk.Button(
            card_cargos,
            text=" Eliminar Cargo Seleccionado",
            image=self.icon_trash,
            compound="left",
            style="Danger.TButton",
            command=self.accion_eliminar_cargo,
        )
        btn_borrar_cargo.pack(anchor="e", pady=(0, 10))

        # Sub-panel para agregar nuevo cargo
        frame_nuevo_cargo = tk.Frame(
            card_cargos,
            bg="#f8fafc",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            padx=12,
            pady=10,
        )
        frame_nuevo_cargo.pack(fill=tk.X)

        tk.Label(
            frame_nuevo_cargo,
            text="➕ Agregar Nuevo Cargo:",
            font=FONT_BODY_BOLD,
            fg=COLOR_PRIMARY,
            bg="#f8fafc",
        ).pack(anchor="w", pady=(0, 6))

        # Nombre del nuevo cargo
        tk.Label(frame_nuevo_cargo, text="Nombre del Cargo:", font=FONT_CAPTION, bg="#f8fafc", fg=COLOR_TEXT).pack(anchor="w")
        self.ent_nuevo_cargo = ttk.Entry(frame_nuevo_cargo, font=FONT_BODY)
        self.ent_nuevo_cargo.pack(fill=tk.X, pady=(1, 4))

        # Horas fijas (si el régimen lo requiere)
        self.lbl_horas_cargo = tk.Label(frame_nuevo_cargo, text="Horas Contractuales Fijas (ej: 160):", font=FONT_CAPTION, bg="#f8fafc", fg=COLOR_TEXT)
        self.lbl_horas_cargo.pack(anchor="w")
        self.ent_horas_cargo = ttk.Entry(frame_nuevo_cargo, font=FONT_BODY)
        self.ent_horas_cargo.pack(fill=tk.X, pady=(1, 4))

        # Nivel de riesgo ARL
        tk.Label(frame_nuevo_cargo, text="Clase de Riesgo ARL:", font=FONT_CAPTION, bg="#f8fafc", fg=COLOR_TEXT).pack(anchor="w")
        self.cb_arl_cargo = ttk.Combobox(
            frame_nuevo_cargo,
            state="readonly",
            font=FONT_BODY,
            values=[c["clase"] for c in CLASES_ARL],
        )
        self.cb_arl_cargo.pack(fill=tk.X, pady=(1, 8))
        self.cb_arl_cargo.current(0)

        btn_guardar_cargo = ttk.Button(
            frame_nuevo_cargo,
            text=" Guardar Cargo",
            image=self.icon_plus,
            compound="left",
            style="Primary.TButton",
            command=self.accion_guardar_cargo,
        )
        btn_guardar_cargo.pack(fill=tk.X)

        # =====================================================================
        # COLUMNA DERECHA: GESTIÓN DE REGÍMENES LABORALES
        # =====================================================================
        card_regimenes = crear_tarjeta(container, padx=16, pady=14)
        card_regimenes.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        lbl_tit_reg = tk.Label(
            card_regimenes,
            text=" Regímenes Laborales Activos",
            image=self.icon_regimen,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        )
        lbl_tit_reg.pack(anchor="w", pady=(0, 6))

        # Tabla de Regímenes Existentes
        frame_tree_reg = tk.Frame(card_regimenes, bg=COLOR_SURFACE)
        frame_tree_reg.pack(fill=tk.BOTH, expand=True, pady=(4, 6))

        scroll_r = ttk.Scrollbar(frame_tree_reg, orient="vertical")
        scroll_r.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_regimenes = ttk.Treeview(
            frame_tree_reg,
            columns=("codigo", "tarifa", "extras", "ibc"),
            show="headings",
            selectmode="browse",
            height=5,
            yscrollcommand=scroll_r.set,
        )
        self.tree_regimenes.pack(fill=tk.BOTH, expand=True)
        scroll_r.config(command=self.tree_regimenes.yview)

        self.tree_regimenes.heading("codigo", text="Régimen")
        self.tree_regimenes.heading("tarifa", text="Tarifa/Hora")
        self.tree_regimenes.heading("extras", text="H. Extras")
        self.tree_regimenes.heading("ibc", text="Base IBC")

        self.tree_regimenes.column("codigo", width=120, anchor="w")
        self.tree_regimenes.column("tarifa", width=95, anchor="e")
        self.tree_regimenes.column("extras", width=85, anchor="center")
        self.tree_regimenes.column("ibc", width=85, anchor="center")

        btn_borrar_reg = ttk.Button(
            card_regimenes,
            text=" Eliminar Régimen Seleccionado",
            image=self.icon_trash,
            compound="left",
            style="Danger.TButton",
            command=self.accion_eliminar_regimen,
        )
        btn_borrar_reg.pack(anchor="e", pady=(0, 8))

        # Sub-panel para agregar nuevo régimen
        frame_nuevo_reg = tk.Frame(
            card_regimenes,
            bg="#f8fafc",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            padx=12,
            pady=10,
        )
        frame_nuevo_reg.pack(fill=tk.X)

        tk.Label(
            frame_nuevo_reg,
            text="➕ Crear Nuevo Régimen Laboral:",
            font=FONT_BODY_BOLD,
            fg=COLOR_PRIMARY,
            bg="#f8fafc",
        ).pack(anchor="w", pady=(0, 6))

        # Fila 1: Código y Nombre
        r_f1 = tk.Frame(frame_nuevo_reg, bg="#f8fafc")
        r_f1.pack(fill=tk.X, pady=1)

        tk.Label(r_f1, text="Código Único (ej: DIRECTIVO):", font=FONT_CAPTION, bg="#f8fafc").pack(side=tk.LEFT)
        self.ent_reg_cod = ttk.Entry(r_f1, font=FONT_BODY, width=16)
        self.ent_reg_cod.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))

        # Fila 2: Tarifa por hora
        r_f2 = tk.Frame(frame_nuevo_reg, bg="#f8fafc")
        r_f2.pack(fill=tk.X, pady=2)

        tk.Label(r_f2, text="Tarifa Hora Ordinaria ($):", font=FONT_CAPTION, bg="#f8fafc").pack(side=tk.LEFT)
        self.ent_reg_tarifa = ttk.Entry(r_f2, font=FONT_BODY, width=16)
        self.ent_reg_tarifa.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))

        # Fila 3: Horas Extras
        r_f3 = tk.Frame(frame_nuevo_reg, bg="#f8fafc")
        r_f3.pack(fill=tk.X, pady=2)

        self.var_permite_he = tk.BooleanVar(value=True)
        chk_he = ttk.Checkbutton(
            r_f3,
            text="Permite Horas Extras  |  Tarifa Extra ($):",
            variable=self.var_permite_he,
            command=self.al_cambiar_check_he,
        )
        chk_he.pack(side=tk.LEFT)

        self.ent_reg_extra = ttk.Entry(r_f3, font=FONT_BODY, width=10)
        self.ent_reg_extra.pack(side=tk.RIGHT, padx=(6, 0))
        self.ent_reg_extra.insert(0, "25000")

        # Fila 4: Tipo de Horas
        r_f4 = tk.Frame(frame_nuevo_reg, bg="#f8fafc")
        r_f4.pack(fill=tk.X, pady=2)

        self.var_reg_tipo_horas = tk.StringVar(value="LIBRES")
        tk.Radiobutton(
            r_f4,
            text="Horas Libres Mes",
            variable=self.var_reg_tipo_horas,
            value="LIBRES",
            font=FONT_CAPTION,
            bg="#f8fafc",
        ).pack(side=tk.LEFT)

        tk.Radiobutton(
            r_f4,
            text="Horas Fijas según Cargo",
            variable=self.var_reg_tipo_horas,
            value="FIJAS",
            font=FONT_CAPTION,
            bg="#f8fafc",
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Fila 5: Base IBC y Deducciones
        r_f5 = tk.Frame(frame_nuevo_reg, bg="#f8fafc")
        r_f5.pack(fill=tk.X, pady=2)

        tk.Label(r_f5, text="Base IBC:", font=FONT_CAPTION, bg="#f8fafc").pack(side=tk.LEFT)
        self.cb_reg_ibc = ttk.Combobox(
            r_f5,
            state="readonly",
            font=FONT_CAPTION,
            width=14,
            values=["100% (Dependiente)", "40% (Independiente/Operativo)"],
        )
        self.cb_reg_ibc.pack(side=tk.LEFT, padx=(4, 10))
        self.cb_reg_ibc.current(0)

        tk.Label(r_f5, text="Salud %:", font=FONT_CAPTION, bg="#f8fafc").pack(side=tk.LEFT)
        self.ent_reg_salud = ttk.Entry(r_f5, font=FONT_CAPTION, width=6)
        self.ent_reg_salud.pack(side=tk.LEFT, padx=(2, 6))
        self.ent_reg_salud.insert(0, "4.0")

        tk.Label(r_f5, text="Pensión %:", font=FONT_CAPTION, bg="#f8fafc").pack(side=tk.LEFT)
        self.ent_reg_pension = ttk.Entry(r_f5, font=FONT_CAPTION, width=6)
        self.ent_reg_pension.pack(side=tk.LEFT, padx=(2, 0))
        self.ent_reg_pension.insert(0, "4.0")

        btn_guardar_reg = ttk.Button(
            frame_nuevo_reg,
            text=" Crear Nuevo Régimen",
            image=self.icon_plus,
            compound="left",
            style="Primary.TButton",
            command=self.accion_guardar_regimen,
        )
        btn_guardar_reg.pack(fill=tk.X, pady=(6, 0))

        # Cargar datos iniciales
        self.recargar_todo()

    def al_cambiar_check_he(self):
        if self.var_permite_he.get():
            self.ent_reg_extra.config(state="normal")
        else:
            self.ent_reg_extra.config(state="disabled")

    def recargar_todo(self):
        """Refresca todos los combos y tablas con la configuración activa."""
        regimenes = obtener_regimenes()

        # Actualizar combo de filtro
        codigos = list(regimenes.keys())
        self.cb_filtro_regimen["values"] = codigos
        if codigos:
            if self.cb_filtro_regimen.get() not in codigos:
                self.cb_filtro_regimen.current(0)
            self.cargar_cargos_de_regimen()

        # Actualizar tabla de regímenes
        for it in self.tree_regimenes.get_children():
            self.tree_regimenes.delete(it)

        for cod, r in regimenes.items():
            he_txt = f"Sí ({formato_pesos(r.get('tarifa_extra', 0))})" if r.get("permite_extras") else "No"
            ibc_txt = f"{int(r.get('porcentaje_ibc', 1.0) * 100)}%"
            self.tree_regimenes.insert("", tk.END, iid=cod, values=(
                cod,
                formato_pesos(r.get("tarifa_hora", 0)),
                he_txt,
                ibc_txt,
            ))

    def cargar_cargos_de_regimen(self):
        cod_reg = self.cb_filtro_regimen.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            return

        for it in self.tree_cargos.get_children():
            self.tree_cargos.delete(it)

        horas_fijas = regimen.get("horas_fijas", False)
        if horas_fijas:
            self.lbl_horas_cargo.config(text="Horas Contractuales Fijas (Obligatorio, ej: 160):", fg=COLOR_PRIMARY)
            self.ent_horas_cargo.config(state="normal")
        else:
            self.lbl_horas_cargo.config(text="Horas: No aplica (Régimen con horas variables mensuales)", fg=COLOR_TEXT_MUTED)
            self.ent_horas_cargo.delete(0, tk.END)

        for c in regimen.get("cargos", []):
            h_txt = f"{c['horas']} h" if c.get("horas") is not None else "Variable"
            self.tree_cargos.insert("", tk.END, iid=c["cargo"], values=(
                c["cargo"],
                h_txt,
                c.get("texto_arl", "0,522%"),
            ))

    def accion_guardar_cargo(self):
        cod_reg = self.cb_filtro_regimen.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            messagebox.showwarning("Aviso", "Seleccione un régimen válido.", parent=self)
            return

        nom_cargo = self.ent_nuevo_cargo.get().strip()
        if not nom_cargo:
            messagebox.showerror("Error", "Debe ingresar el nombre del nuevo cargo.", parent=self)
            self.ent_nuevo_cargo.focus()
            return

        horas_fijas = regimen.get("horas_fijas", False)
        horas = None
        if horas_fijas:
            try:
                horas = int(self.ent_horas_cargo.get().strip())
                if horas < 1:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Para este régimen debe ingresar horas fijas mensuales válidas (>= 1).", parent=self)
                self.ent_horas_cargo.focus()
                return

        idx_arl = self.cb_arl_cargo.current()
        arl_obj = CLASES_ARL[idx_arl]

        ok, msg = agregar_cargo(
            codigo_regimen=cod_reg,
            nombre_cargo=nom_cargo,
            horas=horas,
            arl=arl_obj["tasa"],
            texto_arl=arl_obj["texto"],
        )

        if ok:
            messagebox.showinfo("Éxito", msg, parent=self)
            self.ent_nuevo_cargo.delete(0, tk.END)
            self.ent_horas_cargo.delete(0, tk.END)
            self.cargar_cargos_de_regimen()
            self.controller.notificar(msg)
            self.controller.al_actualizar_regimenes()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def accion_eliminar_cargo(self):
        sel = self.tree_cargos.selection()
        if not sel:
            messagebox.showwarning("Selección requerida", "Seleccione un cargo de la lista.", parent=self)
            return

        nom_cargo = sel[0]
        cod_reg = self.cb_filtro_regimen.get()

        conf = messagebox.askyesno(
            "Confirmar",
            f"¿Desea eliminar el cargo '{nom_cargo}' del régimen {cod_reg}?",
            parent=self,
        )
        if conf:
            ok, msg = eliminar_cargo(cod_reg, nom_cargo)
            if ok:
                messagebox.showinfo("Éxito", msg, parent=self)
                self.cargar_cargos_de_regimen()
                self.controller.notificar(msg)
                self.controller.al_actualizar_regimenes()
            else:
                messagebox.showerror("Error", msg, parent=self)

    def accion_guardar_regimen(self):
        codigo = self.ent_reg_cod.get().strip().upper()
        if not codigo:
            messagebox.showerror("Error", "Debe ingresar el código único del régimen (ej: DIRECTIVO).", parent=self)
            self.ent_reg_cod.focus()
            return

        try:
            tarifa = int(self.ent_reg_tarifa.get().strip())
            if tarifa < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "La tarifa por hora debe ser un número entero mayor a 0.", parent=self)
            self.ent_reg_tarifa.focus()
            return

        permite_he = self.var_permite_he.get()
        tarifa_extra = 0
        if permite_he:
            try:
                tarifa_extra = int(self.ent_reg_extra.get().strip())
                if tarifa_extra < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "La tarifa de horas extras debe ser un número entero >= 0.", parent=self)
                self.ent_reg_extra.focus()
                return

        horas_fijas = (self.var_reg_tipo_horas.get() == "FIJAS")
        pct_ibc = 0.40 if "40%" in self.cb_reg_ibc.get() else 1.0

        try:
            pct_salud = float(self.ent_reg_salud.get().strip().replace("%", "")) / 100.0
            pct_pension = float(self.ent_reg_pension.get().strip().replace("%", "")) / 100.0
        except ValueError:
            messagebox.showerror("Error", "Los porcentajes de salud y pensión deben ser numéricos (ej: 4.0 o 12.5).", parent=self)
            return

        ok = agregar_o_actualizar_regimen(
            codigo=codigo,
            nombre=codigo.capitalize(),
            tarifa_hora=tarifa,
            permite_extras=permite_he,
            tarifa_extra=tarifa_extra,
            horas_fijas=horas_fijas,
            porcentaje_ibc=pct_ibc,
            pct_salud=pct_salud,
            pct_pension=pct_pension,
            pct_arl_def=0.00522,
            texto_arl_def="0,522%",
            descripcion=f"Régimen {codigo}: Tarifa ${tarifa:,}/h.",
        )

        if ok:
            messagebox.showinfo("Éxito", f"Régimen '{codigo}' creado exitosamente.", parent=self)
            self.ent_reg_cod.delete(0, tk.END)
            self.ent_reg_tarifa.delete(0, tk.END)
            self.recargar_todo()
            self.controller.notificar(f"Régimen '{codigo}' registrado.")
            self.controller.al_actualizar_regimenes()
        else:
            messagebox.showerror("Error", "No se pudo guardar el régimen.", parent=self)

    def accion_eliminar_regimen(self):
        sel = self.tree_regimenes.selection()
        if not sel:
            messagebox.showwarning("Selección requerida", "Seleccione un régimen de la lista.", parent=self)
            return

        cod = sel[0]
        conf = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el régimen '{cod}' y todos sus cargos?",
            parent=self,
        )
        if conf:
            ok, msg = eliminar_regimen(cod)
            if ok:
                messagebox.showinfo("Éxito", msg, parent=self)
                self.recargar_todo()
                self.controller.notificar(msg)
                self.controller.al_actualizar_regimenes()
            else:
                messagebox.showerror("Aviso", msg, parent=self)
