# -*- coding: utf-8 -*-
"""
tk_bootstrap.py - Asegura la carga de las bibliotecas de Tkinter en entornos Linux locales.
"""

import os
import sys
import ctypes

def asegurar_tkinter():
    """Garantiza la vinculación de libtk y libBLT sin necesidad de permisos root."""
    user_lib = os.path.expanduser("~/.local/lib")
    tk_so = os.path.join(user_lib, "libtk8.6.so.0")
    blt_so = os.path.join(user_lib, "libBLT.2.5.so.8.6")
    tk_share = os.path.expanduser("~/.local/share/tcltk/tk8.6")

    if os.path.exists(tk_so):
        try:
            ctypes.CDLL(tk_so, mode=ctypes.RTLD_GLOBAL)
        except Exception:
            pass

    if os.path.exists(blt_so):
        try:
            ctypes.CDLL(blt_so, mode=ctypes.RTLD_GLOBAL)
        except Exception:
            pass

    if os.path.exists(tk_share) and "TK_LIBRARY" not in os.environ:
        os.environ["TK_LIBRARY"] = tk_share

    user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
    if os.path.exists(user_site) and user_site not in sys.path:
        sys.path.insert(0, user_site)

# Ejecutar automáticamente al importar
asegurar_tkinter()
