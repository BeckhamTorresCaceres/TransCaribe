# Módulo de Nómina – TransCaribeCol

Actividad 3.4 · Equipo 01 · Python

**Integrantes:** Joseph Herreño, Mateo Mercado y Beckham Torres  
**Instructora:** Norma Caro

## Objetivo

Aplicación de consola que registra la nómina del personal de Transportes del Gran Caribe Colombiano S.C.A. (TransCaribeCol). Calcula lo que corresponde a cada trabajador, muestra un volante de pago en pantalla y guarda los registros en un archivo `.TXT` para el módulo de confirmación y pago de salarios de la gerencia.

## Requisitos

- Python 3 (no usa librerías externas, solo el módulo `csv` que viene con Python).
- Visual Studio Code o cualquier terminal.

## Cómo ejecutarlo

1. Abrir la carpeta `TransCaribe` en Visual Studio Code o terminal.
2. Abrir una terminal en esa carpeta.
3. Ejecutar la **interfaz gráfica moderna con Tkinter**:

```bash
# Opción A (paquete modular)
python -m interfaz_grafica

# Opción B (lanzador rápido)
python interfaz_grafica.py

# Opción C (script directo)
./ejecutar_interfaz.sh
```

O también se puede ejecutar el programa de consola:

```bash
python 02_Programa_Nomina.py
```

## Estructura Modular de la Interfaz (`interfaz_grafica/`)

```text
interfaz_grafica/
├── __init__.py           # Exporta TransCaribeApp e iniciar_interfaz
├── __main__.py           # Permite ejecución como módulo (python -m interfaz_grafica)
├── main.py               # Punto de entrada directo
├── config.py             # Colores, fuentes y constantes de empresa
├── styles.py             # Configuración del tema moderno ttk y widgets de tarjeta
├── storage.py            # Persistencia con 03_Registros_Nomina.txt y generación de volantes
├── regimenes_manager.py  # Gestor y persistencia de cargos y regímenes laborales
├── icons.py              # Biblioteca de íconos vectoriales modernos (supersampling 4x)
├── tk_bootstrap.py       # Carga automática de bibliotecas Tkinter
├── app.py                # Controlador central y ventana principal
└── views/
    ├── __init__.py
    ├── header.py         # Encabezado corporativo moderno con contador de nómina
    ├── tab_registro.py   # Formulario dinámico con cálculo en vivo y volante oficial
    ├── tab_tabla.py      # Tabla con buscador en tiempo real, filtro por tipo y KPIs
    ├── tab_gestion.py    # Gestión visual para agregar/eliminar cargos y regímenes laborales
    ├── tab_reglas.py     # Tarjetas visuales con las reglas de negocio y tarifas
    └── dialog_volante.py # Ventana emergente para inspección rápida de comprobantes
```

Todos los archivos `.py` deben estar en la misma carpeta.

## Uso del menú de consola

| Opción | Qué hace |
|---|---|
| 1 | Registra un empleado **administrativo**: pide nombre, cargo, horas del mes y horas extras. Muestra el volante. |
| 2 | Registra un empleado **operativo**: pide nombre y cargo (Conductor, Oficios Generales o Vigilancia). Las horas las fija el cargo. Muestra el volante. |
| 3 | Muestra en una tabla todos los empleados registrados. |
| 4 | Guarda los empleados en `03_Registros_Nomina.txt`. |
| 5 | Abre la **Interfaz Gráfica (Tkinter)**. |
| 6 | Sale del programa. |

Si se ingresa un dato inválido (letras donde va un número, un nombre con números, una opción que no existe), el programa muestra un mensaje y lo vuelve a pedir.

## Características de la Interfaz Gráfica (Tkinter)

- **Pestaña de Registro y Liquidación:**
  - Formulario interactivo con selección de tipo (Administrativo u Operativo).
  - Carga automática de cargos y horas predefinidas para operativos.
  - Validación de nombre y horas en tiempo real según las reglas del proyecto.
  - Visualización inmediata del volante de pago oficial formateado.
  - Opciones para imprimir el volante en consola, copiarlo al portapapeles o guardarlo en archivo `.txt` individual.
- **Pestaña de Nómina General:**
  - Tabla interactiva con todas las columnas de ley y empleados registrados.
  - Carga automática y manual desde `03_Registros_Nomina.txt`.
  - Guardado en `03_Registros_Nomina.txt`.
  - Doble clic o botón para ver el volante del empleado seleccionado.
  - Eliminación de registros y tarjetas de métricas totales (empleados, devengados, descuentos y neto).
- **Pestaña de Reglas y Tarifas:**
  - Resumen detallado de fórmulas, porcentajes de salud, pensión, ARL e IBC.

## Reglas de cálculo

**Administrativo:** $20.000 por hora y $25.000 por hora extra. Sobre el total devengado se descuenta salud 4 %, pensión 4 % y ARL riesgo I 0,522 %.

**Operativo:** $40.000 por hora; horas según el cargo (Conductor 160, Oficios Generales 100, Vigilancia 336). IBC = 40 % del salario. Sobre el IBC se calcula salud 12,5 %, pensión 16 % y ARL según el riesgo (I 0,522 %, II 1,044 %, IV 4,350 %). No tiene horas extras.

## Archivos

| Archivo | Contenido |
|---|---|
| `01_Analisis_y_Diseno.pdf` | Problema, entradas/procesos/salidas, reglas, dudas, pseudocódigo, variables y diseño de datos. |
| `02_Programa_Nomina.py` | Punto de entrada: menú principal y registro de empleados en consola. |
| `interfaz_grafica.py` | Interfaz gráfica completa con Tkinter (registro, cálculo, volante y tabla). |
| `validaciones.py` | Funciones para pedir y validar datos. |
| `calculos.py` | Listas de cargos y cálculos de nómina. |
| `volante.py` | Impresión del volante de pago. |
| `reportes.py` | Tabla de empleados y escritura del archivo TXT. |
| `03_Registros_Nomina.txt` | Registros generados por el programa (una línea por trabajador, separados por comas). |
| `04_Pruebas_y_Evidencias.pdf` | Casos de prueba, resultados, capturas y correcciones. |
| `README.md` | Este archivo. |
