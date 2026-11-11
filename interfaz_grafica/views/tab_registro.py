# -*- coding: utf-8 -*-
"""
views/tab_registro.py - Pestaña moderna de Registro y Liquidación con soporte para cargos y regímenes dinámicos.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_PRIMARY_LIGHT,
    COLOR_ACCENT,
    COLOR_ACCENT_BG,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_SUCCESS,
    COLOR_SUCCESS_BG,
    FONT_FAMILY,
    FONT_SUBTITLE,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_CAPTION,
)
from interfaz_grafica.styles import crear_tarjeta
from interfaz_grafica.storage import generar_volante_texto
from interfaz_grafica.icons import crear_icono
from interfaz_grafica.regimenes_manager import (
    obtener_regimenes,
    obtener_regimen,
    calcular_empleado_dinamico,
)
from volante import formato_pesos, imprimir_volante


class TabRegistro(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=COLOR_BG, **kwargs)
        self.controller = controller
        self.empleado_actual = None

        # Cargar íconos necesarios para la vista
        self.icon_user_plus = crear_icono("user-plus", size=18, color="#ffffff")
        self.icon_refresh = crear_icono("refresh", size=16, color=COLOR_TEXT)
        self.icon_printer = crear_icono("printer", size=16, color=COLOR_TEXT)
        self.icon_copy = crear_icono("copy", size=16, color=COLOR_TEXT)
        self.icon_save_txt = crear_icono("file-text", size=16, color=COLOR_TEXT)
        self.icon_calc = crear_icono("calculator", size=16, color=COLOR_ACCENT)
        self.icon_receipt = crear_icono("receipt", size=20, color=COLOR_PRIMARY)
        self.icon_user_title = crear_icono("user", size=20, color=COLOR_PRIMARY)

        self.construir_vista()

    def construir_vista(self):
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        container.columnconfigure(0, weight=4, minsize=420)
        container.columnconfigure(1, weight=5, minsize=460)
        container.rowconfigure(0, weight=1)

        # =====================================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE REGISTRO DINÁMICO
        # =====================================================================
        card_form = crear_tarjeta(container, padx=18, pady=16)
        card_form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        lbl_sec1 = tk.Label(
            card_form,
            text=" Liquidación y Registro de Personal",
            image=self.icon_user_title,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        )
        lbl_sec1.pack(anchor="w", pady=(0, 8))

        # Selector Dinámico de Régimen
        lbl_tipo = tk.Label(
            card_form,
            text="Régimen Laboral Aplicable:",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        )
        lbl_tipo.pack(anchor="w", pady=(2, 2))

        self.var_tipo = tk.StringVar(value="ADMINISTRATIVO")
        self.cb_regimen = ttk.Combobox(
            card_form,
            textvariable=self.var_tipo,
            state="readonly",
            font=(FONT_FAMILY, 10, "bold"),
        )
        self.cb_regimen.pack(fill=tk.X, pady=(0, 4))
        self.cb_regimen.bind("<<ComboboxSelected>>", self.al_cambiar_tipo)

        self.lbl_regimen_desc = tk.Label(
            card_form,
            text="",
            font=FONT_CAPTION,
            fg=COLOR_ACCENT,
            bg=COLOR_SURFACE,
            wraplength=380,
            justify="left",
        )
        self.lbl_regimen_desc.pack(anchor="w", pady=(0, 6))

        ttk.Separator(card_form, orient="horizontal").pack(fill=tk.X, pady=4)

        # Nombre Completo
        lbl_nom = tk.Label(
            card_form,
            text="Nombre Completo del Trabajador:",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        )
        lbl_nom.pack(anchor="w", pady=(2, 2))

        self.ent_nombre = ttk.Entry(card_form, font=(FONT_FAMILY, 10))
        self.ent_nombre.pack(fill=tk.X, pady=(0, 2))
        self.ent_nombre.bind("<KeyRelease>", lambda e: self.actualizar_previsualizacion())

        self.lbl_nom_hint = tk.Label(
            card_form,
            text="Solo letras y espacios (ej: Carlos Andrés Pérez Rojas)",
            font=FONT_CAPTION,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        )
        self.lbl_nom_hint.pack(anchor="w", pady=(0, 6))

        # Cargo (Se actualiza dinámicamente con los cargos del régimen)
        lbl_carg = tk.Label(
            card_form,
            text="Cargo Asignado:",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        )
        lbl_carg.pack(anchor="w", pady=(2, 2))

        self.cb_cargo = ttk.Combobox(card_form, state="readonly", font=FONT_BODY)
        self.cb_cargo.pack(fill=tk.X, pady=(0, 4))
        self.cb_cargo.bind("<<ComboboxSelected>>", self.al_seleccionar_cargo)

        self.lbl_cargo_hint = tk.Label(
            card_form,
            text="",
            font=FONT_CAPTION,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        )
        self.lbl_cargo_hint.pack(anchor="w", pady=(0, 6))

        # Horas Trabajadas
        lbl_ht = tk.Label(
            card_form,
            text="Horas Trabajadas en el Mes (HT):",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        )
        lbl_ht.pack(anchor="w", pady=(2, 2))

        self.var_horas = tk.StringVar(value="40")
        self.ent_horas = ttk.Entry(card_form, textvariable=self.var_horas, font=(FONT_FAMILY, 10))
        self.ent_horas.pack(fill=tk.X, pady=(0, 2))
        self.ent_horas.bind("<KeyRelease>", lambda e: self.actualizar_previsualizacion())

        self.lbl_ht_hint = tk.Label(
            card_form,
            text="",
            font=FONT_CAPTION,
            fg=COLOR_ACCENT,
            bg=COLOR_SURFACE,
        )
        self.lbl_ht_hint.pack(anchor="w", pady=(0, 6))

        # Horas Extras
        self.lbl_he = tk.Label(
            card_form,
            text="Horas Extras (HE):",
            font=FONT_BODY_BOLD,
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
        )
        self.lbl_he.pack(anchor="w", pady=(2, 2))

        self.var_he = tk.StringVar(value="0")
        self.ent_he = ttk.Entry(card_form, textvariable=self.var_he, font=(FONT_FAMILY, 10))
        self.ent_he.pack(fill=tk.X, pady=(0, 2))
        self.ent_he.bind("<KeyRelease>", lambda e: self.actualizar_previsualizacion())

        self.lbl_he_hint = tk.Label(
            card_form,
            text="",
            font=FONT_CAPTION,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        )
        self.lbl_he_hint.pack(anchor="w", pady=(0, 8))

        # Tarjeta de Pre-liquidación en vivo
        self.frame_preview = tk.Frame(
            card_form,
            bg=COLOR_ACCENT_BG,
            highlightbackground="#bae6fd",
            highlightthickness=1,
            padx=12,
            pady=8,
        )
        self.frame_preview.pack(fill=tk.X, pady=(0, 10))

        lbl_prev_title = tk.Label(
            self.frame_preview,
            text=" Cálculo Estimado en Vivo:",
            image=self.icon_calc,
            compound="left",
            font=(FONT_FAMILY, 8, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_ACCENT_BG,
        )
        lbl_prev_title.pack(anchor="w")

        self.lbl_prev_valores = tk.Label(
            self.frame_preview,
            text="Bruto: $0  |  Deducciones: $0  |  Neto: $0",
            font=(FONT_FAMILY, 9, "bold"),
            fg=COLOR_PRIMARY,
            bg=COLOR_ACCENT_BG,
        )
        self.lbl_prev_valores.pack(anchor="w", pady=(2, 0))

        # Botones de Acción
        btn_box = tk.Frame(card_form, bg=COLOR_SURFACE)
        btn_box.pack(fill=tk.X, pady=(4, 0))

        self.btn_guardar = ttk.Button(
            btn_box,
            text=" Registrar y Liquidar",
            image=self.icon_user_plus,
            compound="left",
            style="Primary.TButton",
            command=self.procesar_registro,
        )
        self.btn_guardar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_limpiar = ttk.Button(
            btn_box,
            text=" Limpiar",
            image=self.icon_refresh,
            compound="left",
            style="Secondary.TButton",
            command=self.limpiar_formulario,
        )
        btn_limpiar.pack(side=tk.RIGHT)

        # Inicializar opciones de regímenes y cargos
        self.recargar_regimenes_y_cargos()

        # =====================================================================
        # COLUMNA DERECHA: VOLANTE DE PAGO OFICIAL
        # =====================================================================
        card_volante = crear_tarjeta(container, padx=18, pady=16)
        card_volante.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        # Cabecera del volante
        header_v = tk.Frame(card_volante, bg=COLOR_SURFACE)
        header_v.pack(fill=tk.X, pady=(0, 8))

        lbl_vol_title = tk.Label(
            header_v,
            text=" Comprobante Oficial de Pago",
            image=self.icon_receipt,
            compound="left",
            font=FONT_SUBTITLE,
            fg=COLOR_PRIMARY,
            bg=COLOR_SURFACE,
        )
        lbl_vol_title.pack(side=tk.LEFT)

        self.badge_trabajador = tk.Label(
            header_v,
            text="Sin liquidación activa",
            font=FONT_CAPTION,
            fg=COLOR_TEXT_MUTED,
            bg="#f1f5f9",
            padx=8,
            pady=3,
        )
        self.badge_trabajador.pack(side=tk.RIGHT)

        # Área de texto estilizada con scrollbar
        text_container = tk.Frame(card_volante, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(4, 10))

        scroll_y = ttk.Scrollbar(text_container, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_volante = tk.Text(
            text_container,
            font=("Courier New", 10),
            bg="#ffffff",
            fg=COLOR_TEXT,
            padx=14,
            pady=12,
            wrap="word",
            yscrollcommand=scroll_y.set,
            relief="flat",
        )
        self.txt_volante.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.txt_volante.yview)

        # Mensaje de bienvenida inicial
        self.mostrar_mensaje_inicial()

        # Barra de herramientas del volante
        tools_box = tk.Frame(card_volante, bg=COLOR_SURFACE)
        tools_box.pack(fill=tk.X)

        btn_consola = ttk.Button(
            tools_box,
            text=" En Consola",
            image=self.icon_printer,
            compound="left",
            style="Secondary.TButton",
            command=self.imprimir_consola,
        )
        btn_consola.pack(side=tk.LEFT, padx=(0, 6))

        btn_copiar = ttk.Button(
            tools_box,
            text=" Copiar Volante",
            image=self.icon_copy,
            compound="left",
            style="Secondary.TButton",
            command=self.copiar_texto,
        )
        btn_copiar.pack(side=tk.LEFT, padx=(0, 6))

        btn_exportar = ttk.Button(
            tools_box,
            text=" Guardar TXT",
            image=self.icon_save_txt,
            compound="left",
            style="Secondary.TButton",
            command=self.guardar_individual,
        )
        btn_exportar.pack(side=tk.RIGHT)

    def recargar_regimenes_y_cargos(self):
        """Carga dinámicamente los regímenes disponibles desde regimenes_manager."""
        regimenes = obtener_regimenes()
        codigos = list(regimenes.keys())
        self.cb_regimen["values"] = codigos

        if codigos:
            actual = self.var_tipo.get()
            if actual not in codigos:
                self.var_tipo.set(codigos[0])
            self.al_cambiar_tipo()

    def al_cambiar_tipo(self, event=None):
        cod_reg = self.var_tipo.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            return

        # Descripción
        desc = regimen.get("descripcion") or f"Tarifa: {formato_pesos(regimen.get('tarifa_hora', 0))}/h."
        self.lbl_regimen_desc.config(text=desc)

        # Cargar cargos del régimen
        cargos = regimen.get("cargos", [])
        nombres_cargos = [c["cargo"] for c in cargos]
        self.cb_cargo["values"] = nombres_cargos

        if nombres_cargos:
            self.cb_cargo.current(0)
            self.al_seleccionar_cargo()
        else:
            self.cb_cargo.set("")
            self.lbl_cargo_hint.config(text="No hay cargos registrados. Agregue uno en la pestaña 'Cargos y Regímenes'.", fg="#b91c1c")

        # Configurar Horas y Horas Extras según el régimen
        horas_fijas = regimen.get("horas_fijas", False)
        permite_he = regimen.get("permite_extras", False)

        if not horas_fijas:
            self.ent_horas.config(state="normal")
            if not self.var_horas.get() or self.var_horas.get() == "0":
                self.var_horas.set("40")
            self.lbl_ht_hint.config(
                text=f"Horas mensuales libres (Tarifa: {formato_pesos(regimen.get('tarifa_hora', 0))}/h, mín. 1)",
                fg=COLOR_ACCENT,
            )
        else:
            self.ent_horas.config(state="disabled")

        if permite_he:
            self.ent_he.config(state="normal")
            tarifa_extra = regimen.get("tarifa_extra", 0)
            self.lbl_he_hint.config(
                text=f"Horas extras permitidas (Tarifa: {formato_pesos(tarifa_extra)} c/u)",
                fg=COLOR_TEXT_MUTED,
            )
        else:
            self.var_he.set("0")
            self.ent_he.config(state="disabled")
            self.lbl_he_hint.config(text="Este régimen no reconoce horas extras.", fg=COLOR_TEXT_MUTED)

        self.actualizar_previsualizacion()

    def al_seleccionar_cargo(self, event=None):
        cod_reg = self.var_tipo.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            return

        idx = self.cb_cargo.current()
        cargos = regimen.get("cargos", [])

        if 0 <= idx < len(cargos):
            cargo_obj = cargos[idx]
            arl_txt = cargo_obj.get("texto_arl", regimen.get("texto_arl_defecto", "0,522%"))

            if regimen.get("horas_fijas", False):
                h = cargo_obj.get("horas", 160)
                self.var_horas.set(str(h))
                self.lbl_ht_hint.config(
                    text=f"Horas fijas para {cargo_obj['cargo']}: {h}h · ARL: {arl_txt}",
                    fg=COLOR_PRIMARY_LIGHT,
                )
            else:
                self.lbl_cargo_hint.config(text=f"Riesgo ARL: {arl_txt}", fg=COLOR_TEXT_MUTED)

        self.actualizar_previsualizacion()

    def actualizar_previsualizacion(self):
        """Calcula los valores en tiempo real a medida que el usuario interactúa."""
        cod_reg = self.var_tipo.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            return

        nom_cargo = self.cb_cargo.get().strip()
        if not nom_cargo:
            self.lbl_prev_valores.config(text="Seleccione un cargo...")
            return

        try:
            h_str = self.var_horas.get().strip() or "0"
            he_str = self.var_he.get().strip() or "0"
            horas = int(h_str)
            extras = int(he_str)

            emp = calcular_empleado_dinamico(
                nombre="Vista Previa",
                codigo_regimen=cod_reg,
                nombre_cargo=nom_cargo,
                horas=horas,
                horas_extras=extras,
            )

            dev = emp["salario"] + emp["pago_extras"]
            self.lbl_prev_valores.config(
                text=f"Bruto: {formato_pesos(dev)}  |  Deducciones: {formato_pesos(emp['total_descuentos'])}  |  Neto: {formato_pesos(emp['total_pagar'])}"
            )
        except Exception:
            self.lbl_prev_valores.config(text="Ingrese valores válidos...")

    def validar_formulario(self):
        nombre = self.ent_nombre.get().strip()
        sin_espacios = nombre.replace(" ", "")

        if not sin_espacios or not sin_espacios.isalpha():
            messagebox.showerror(
                "Nombre Inválido",
                "El nombre completo es obligatorio y solo puede contener letras y espacios.",
                parent=self,
            )
            self.ent_nombre.focus()
            return None

        cod_reg = self.var_tipo.get()
        regimen = obtener_regimen(cod_reg)
        if not regimen:
            messagebox.showerror("Régimen Inválido", "Seleccione un régimen laboral válido.", parent=self)
            return None

        cargo_nom = self.cb_cargo.get().strip()
        if not cargo_nom:
            messagebox.showerror("Cargo Requerido", "Debe seleccionar un cargo de la lista.", parent=self)
            self.cb_cargo.focus()
            return None

        horas_fijas = regimen.get("horas_fijas", False)
        if not horas_fijas:
            try:
                horas = int(self.var_horas.get().strip())
                if horas < 1:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(
                    "Horas Inválidas",
                    "Las horas trabajadas en el mes deben ser un número entero mayor o igual a 1.",
                    parent=self,
                )
                self.ent_horas.focus()
                return None
        else:
            horas = int(self.var_horas.get().strip() or 160)

        permite_he = regimen.get("permite_extras", False)
        horas_extras = 0
        if permite_he:
            try:
                horas_extras = int(self.var_he.get().strip())
                if horas_extras < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(
                    "Horas Extras Inválidas",
                    "Las horas extras deben ser un número entero mayor o igual a 0.",
                    parent=self,
                )
                self.ent_he.focus()
                return None

        return {
            "nombre": nombre,
            "regimen": cod_reg,
            "cargo": cargo_nom,
            "horas": horas,
            "horas_extras": horas_extras,
        }

    def procesar_registro(self):
        datos = self.validar_formulario()
        if not datos:
            return

        try:
            empleado = calcular_empleado_dinamico(
                nombre=datos["nombre"],
                codigo_regimen=datos["regimen"],
                nombre_cargo=datos["cargo"],
                horas=datos["horas"],
                horas_extras=datos["horas_extras"],
            )

            self.controller.agregar_empleado(empleado)
            self.mostrar_volante(empleado)

            messagebox.showinfo(
                "Liquidación Exitosa",
                f"Se ha liquidado y registrado a:\n\n"
                f"• {empleado['nombre']}\n"
                f"• Régimen: {empleado['tipo']}\n"
                f"• Cargo: {empleado['cargo']}\n"
                f"• Total a Pagar: {formato_pesos(empleado['total_pagar'])}",
                parent=self,
            )
        except Exception as e:
            messagebox.showerror("Error al Liquidar", f"No se pudo liquidar al empleado:\n{e}", parent=self)

    def mostrar_volante(self, empleado):
        self.empleado_actual = empleado
        texto = generar_volante_texto(empleado)

        self.txt_volante.config(state="normal")
        self.txt_volante.delete("1.0", tk.END)
        self.txt_volante.insert(tk.END, texto)
        self.txt_volante.config(state="disabled")

        self.badge_trabajador.config(
            text=f"🟢 {empleado['nombre']} · {formato_pesos(empleado['total_pagar'])}",
            fg=COLOR_SUCCESS,
            bg=COLOR_SUCCESS_BG,
        )

    def mostrar_mensaje_inicial(self):
        self.txt_volante.config(state="normal")
        self.txt_volante.delete("1.0", tk.END)
        self.txt_volante.insert(
            tk.END,
            "==========================================================\n"
            "                 TRANSCARIBECOL S.C.A.                    \n"
            "                VOLANTE DE PAGO OFICIAL                   \n"
            "==========================================================\n\n"
            "  Seleccione o liquide un empleado para visualizar aquí  \n"
            "  el desglose de su salario, horas y deducciones.        \n\n"
            "  También puede hacer doble clic sobre cualquier fila    \n"
            "  en la pestaña 'Nómina General'.                         \n"
            "==========================================================\n",
        )
        self.txt_volante.config(state="disabled")

    def limpiar_formulario(self):
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.focus()
        self.al_cambiar_tipo()

    def imprimir_consola(self):
        if not self.empleado_actual:
            messagebox.showwarning("Aviso", "No hay ningún volante cargado para imprimir.", parent=self)
            return
        imprimir_volante(self.empleado_actual)
        self.controller.notificar(f"Volante de '{self.empleado_actual['nombre']}' impreso en la terminal.")
        messagebox.showinfo("Impresión", "El volante se imprimió en la terminal del sistema.", parent=self)

    def copiar_texto(self):
        texto = self.txt_volante.get("1.0", tk.END).strip()
        if not texto:
            return
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Comprobante copiado al portapapeles.", parent=self)

    def guardar_individual(self):
        if not self.empleado_actual:
            messagebox.showwarning("Aviso", "Primero liquide o seleccione un empleado.", parent=self)
            return

        limpio = "".join(c for c in self.empleado_actual["nombre"] if c.isalnum() or c in (" ", "_")).replace(" ", "_")
        sugerido = f"Volante_{limpio}.txt"

        ruta = filedialog.asksaveasfilename(
            initialfile=sugerido,
            defaultextension=".txt",
            filetypes=[("Archivos TXT", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar Volante de Pago Individual",
            parent=self,
        )
        if ruta:
            try:
                texto = generar_volante_texto(self.empleado_actual)
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(texto)
                messagebox.showinfo("Guardado", f"Volante guardado exitosamente en:\n{ruta}", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}", parent=self)
