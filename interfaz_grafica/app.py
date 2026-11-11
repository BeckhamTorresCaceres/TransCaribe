# -*- coding: utf-8 -*-
"""
app.py - Ventana principal y controlador central con íconos vectoriales modernos.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import interfaz_grafica.tk_bootstrap  # Asegurar carga de bibliotecas Tk

from interfaz_grafica.config import (
    COLOR_BG,
    COLOR_PRIMARY,
    COLOR_TEXT_MUTED,
    ARCHIVO_NOMINA,
    SIGLA,
    EMPRESA,
    FONT_FAMILY,
)
from interfaz_grafica.styles import aplicar_estilos_modernos
from interfaz_grafica.storage import cargar_nomina, guardar_nomina
from interfaz_grafica.icons import crear_icono
from interfaz_grafica.views.header import ModernHeader
from interfaz_grafica.views.tab_registro import TabRegistro
from interfaz_grafica.views.tab_tabla import TabTabla
from interfaz_grafica.views.tab_gestion import TabGestion
from interfaz_grafica.views.tab_reglas import TabReglas


class TransCaribeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"{SIGLA} - Sistema de Nómina · {EMPRESA}")
        self.geometry("1160x780")
        self.minsize(1020, 680)

        # Estado central de la aplicación
        self.empleados = []

        # Configurar estilos modernos
        aplicar_estilos_modernos(self)

        # Íconos para la ventana y las pestañas
        try:
            self.icon_window = crear_icono("bus", size=32, color="#0284c7")
            self.iconphoto(False, self.icon_window)
        except Exception:
            pass

        self.tab_icon_reg = crear_icono("user-plus", size=16, color=COLOR_PRIMARY)
        self.tab_icon_tab = crear_icono("table", size=16, color=COLOR_PRIMARY)
        self.tab_icon_ges = crear_icono("settings", size=16, color=COLOR_PRIMARY)
        self.tab_icon_inf = crear_icono("info", size=16, color=COLOR_PRIMARY)

        # Construir Interfaz
        self.header = ModernHeader(self)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Pestañas
        self.tab_registro = TabRegistro(self.notebook, controller=self)
        self.tab_tabla = TabTabla(self.notebook, controller=self)
        self.tab_gestion = TabGestion(self.notebook, controller=self)
        self.tab_reglas = TabReglas(self.notebook)

        self.notebook.add(
            self.tab_registro,
            text=" Liquidación y Registro",
            image=self.tab_icon_reg,
            compound="left",
        )
        self.notebook.add(
            self.tab_tabla,
            text=" Nómina General y Archivo TXT",
            image=self.tab_icon_tab,
            compound="left",
        )
        self.notebook.add(
            self.tab_gestion,
            text=" Cargos y Regímenes",
            image=self.tab_icon_ges,
            compound="left",
        )
        self.notebook.add(
            self.tab_reglas,
            text=" Reglas y Tarifas",
            image=self.tab_icon_inf,
            compound="left",
        )

        # Barra de estado inferior
        self.crear_barra_estado()

        # Atajos de teclado
        self.bind("<Control-s>", lambda e: self.guardar_txt())
        self.bind("<Control-o>", lambda e: self.cargar_txt())

        # Carga automática inicial de registros existentes
        self.cargar_inicial()

    def crear_barra_estado(self):
        self.status_bar = tk.Label(
            self,
            text=f"Listo | Sistema {SIGLA} iniciado correctamente con biblioteca de íconos vectoriales.",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=(FONT_FAMILY, 8),
            bg="#e2e8f0",
            fg=COLOR_TEXT_MUTED,
            padx=12,
            pady=4,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def notificar(self, texto):
        """Actualiza el texto en la barra de estado."""
        self.status_bar.config(text=texto)

    def sincronizar_vistas(self):
        """Notifica a todas las vistas que los datos de empleados cambiaron."""
        self.header.actualizar_conteo(len(self.empleados))
        self.tab_tabla.renderizar_tabla(self.empleados)

    def al_actualizar_regimenes(self):
        """Se ejecuta cuando se agrega, edita o elimina un cargo o régimen laboral."""
        self.tab_registro.recargar_regimenes_y_cargos()
        self.tab_tabla.recargar_filtros_regimen()
        self.tab_tabla.renderizar_tabla(self.empleados)

    # =========================================================================
    # GESTIÓN DE EMPLEADOS (CONTROLADOR)
    # =========================================================================
    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)
        self.sincronizar_vistas()
        self.notificar(f"Empleado '{empleado['nombre']}' agregado exitosamente.")

    def obtener_empleado(self, indice):
        if 0 <= indice < len(self.empleados):
            return self.empleados[indice]
        return None

    def eliminar_empleado(self, indice):
        if 0 <= indice < len(self.empleados):
            eliminado = self.empleados.pop(indice)
            self.sincronizar_vistas()
            self.notificar(f"Se eliminó a '{eliminado['nombre']}' de la nómina.")

    def vaciar_empleados(self):
        self.empleados.clear()
        self.sincronizar_vistas()
        self.tab_registro.mostrar_mensaje_inicial()
        self.notificar("Se han vaciado todos los registros en memoria.")

    def seleccionar_para_volante(self, indice):
        emp = self.obtener_empleado(indice)
        if emp:
            self.tab_registro.mostrar_volante(emp)
            self.notebook.select(self.tab_registro)
            self.notificar(f"Visualizando volante de: {emp['nombre']}.")

    # =========================================================================
    # PERSISTENCIA EN ARCHIVO TXT
    # =========================================================================
    def cargar_inicial(self):
        if os.path.exists(ARCHIVO_NOMINA):
            cargados = cargar_nomina(ARCHIVO_NOMINA)
            if cargados:
                self.empleados = cargados
                self.sincronizar_vistas()
                self.tab_registro.mostrar_volante(self.empleados[0])
                self.notificar(f"Se precargaron {len(cargados)} registros desde {ARCHIVO_NOMINA}.")

    def cargar_txt(self):
        if not os.path.exists(ARCHIVO_NOMINA):
            messagebox.showwarning("Archivo no encontrado", f"No se encontró el archivo {ARCHIVO_NOMINA}.", parent=self)
            return

        cargados = cargar_nomina(ARCHIVO_NOMINA)
        if not cargados:
            messagebox.showinfo("Aviso", f"El archivo {ARCHIVO_NOMINA} está vacío o no tiene datos válidos.", parent=self)
            return

        self.empleados = cargados
        self.sincronizar_vistas()
        if self.empleados:
            self.tab_registro.mostrar_volante(self.empleados[0])

        self.notificar(f"Se cargaron {len(self.empleados)} registros desde {ARCHIVO_NOMINA}.")
        messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(self.empleados)} registros desde:\n{ARCHIVO_NOMINA}", parent=self)

    def guardar_txt(self):
        if not self.empleados:
            messagebox.showwarning("Sin datos", "No hay empleados registrados para guardar.", parent=self)
            return

        try:
            guardar_nomina(self.empleados, ARCHIVO_NOMINA)
            self.notificar(f"Nómina guardada en {ARCHIVO_NOMINA} ({len(self.empleados)} registros).")
            messagebox.showinfo("Guardado Exitoso", f"Se guardaron {len(self.empleados)} registros en:\n{ARCHIVO_NOMINA}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo TXT:\n{e}", parent=self)


def iniciar_interfaz():
    app = TransCaribeApp()
    app.mainloop()
    return app
