# -*- coding: utf-8 -*-
"""
main.py - Punto de entrada ejecutable dentro de la carpeta interfaz_grafica.
Uso: python interfaz_grafica/main.py
"""

import os
import sys

# Asegurar que el directorio padre esté en sys.path
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from interfaz_grafica.app import iniciar_interfaz

if __name__ == "__main__":
    iniciar_interfaz()
