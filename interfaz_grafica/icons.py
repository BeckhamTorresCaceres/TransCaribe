# -*- coding: utf-8 -*-
"""
icons.py - Biblioteca de íconos vectoriales modernos (estilo Feather/Lucide).
Genera íconos transparentes de alta resolución con supersampling y suavizado anti-aliasing.
"""

from PIL import Image, ImageDraw, ImageTk

# Caché global para evitar que el recolector de basura de Tkinter elimine las imágenes
_icon_cache = {}


def crear_icono(name, size=18, color="#0f172a"):
    """
    Renderiza un ícono con supersampling 4x y filtrado Lanczos para máxima nitidez.
    """
    key = (name, size, color)
    if key in _icon_cache:
        return _icon_cache[key]

    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = max(1, int(1.8 * scale))

    # Definiciones geométricas estilo Lucide / Feather
    if name == "bus":
        # Carrocería del bus
        d.rounded_rectangle([s * 0.15, s * 0.15, s * 0.85, s * 0.75], radius=int(s * 0.08), outline=color, width=w)
        # Parabrisas / Ventana
        d.line([s * 0.22, s * 0.42, s * 0.78, s * 0.42], fill=color, width=w)
        d.line([s * 0.50, s * 0.18, s * 0.50, s * 0.42], fill=color, width=w)
        # Luces delanteras
        d.ellipse([s * 0.22, s * 0.58, s * 0.32, s * 0.68], fill=color)
        d.ellipse([s * 0.68, s * 0.58, s * 0.78, s * 0.68], fill=color)
        # Ruedas
        d.rectangle([s * 0.22, s * 0.75, s * 0.35, s * 0.88], fill=color)
        d.rectangle([s * 0.65, s * 0.75, s * 0.78, s * 0.88], fill=color)

    elif name == "user":
        # Cabeza
        r = int(s * 0.16)
        cx, cy = int(s * 0.5), int(s * 0.32)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        # Torso / Hombros
        d.arc([s * 0.18, s * 0.52, s * 0.82, s * 0.95], start=0, end=180, fill=color, width=w)

    elif name == "user-plus":
        # Usuario
        r = int(s * 0.13)
        cx, cy = int(s * 0.42), int(s * 0.32)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.arc([s * 0.15, s * 0.54, s * 0.70, s * 0.94], start=0, end=180, fill=color, width=w)
        # Signo Más
        d.line([s * 0.78, s * 0.30, s * 0.78, s * 0.54], fill=color, width=w)
        d.line([s * 0.66, s * 0.42, s * 0.90, s * 0.42], fill=color, width=w)

    elif name == "briefcase":
        # Maletín / Cargo
        d.rounded_rectangle([s * 0.12, s * 0.32, s * 0.88, s * 0.82], radius=int(s * 0.06), outline=color, width=w)
        # Asa superior
        d.rectangle([s * 0.36, s * 0.18, s * 0.64, s * 0.32], outline=color, width=w)
        # Línea central
        d.line([s * 0.12, s * 0.54, s * 0.88, s * 0.54], fill=color, width=w)

    elif name == "clock":
        # Reloj de horas
        cx, cy, r = int(s * 0.5), int(s * 0.5), int(s * 0.36)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.line([cx, cy, cx, cy - int(r * 0.55)], fill=color, width=w)
        d.line([cx, cy, cx + int(r * 0.45), cy], fill=color, width=w)

    elif name == "clock-plus":
        # Horas extras
        cx, cy, r = int(s * 0.42), int(s * 0.5), int(s * 0.32)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.line([cx, cy, cx, cy - int(r * 0.55)], fill=color, width=w)
        d.line([cx, cy, cx + int(r * 0.45), cy], fill=color, width=w)
        # Más
        d.line([s * 0.82, s * 0.22, s * 0.82, s * 0.44], fill=color, width=w)
        d.line([s * 0.71, s * 0.33, s * 0.93, s * 0.33], fill=color, width=w)

    elif name == "receipt":
        # Volante / Ticket de pago
        d.rectangle([s * 0.20, s * 0.14, s * 0.80, s * 0.86], outline=color, width=w)
        # Líneas simuladas de texto
        d.line([s * 0.32, s * 0.32, s * 0.68, s * 0.32], fill=color, width=w)
        d.line([s * 0.32, s * 0.48, s * 0.68, s * 0.48], fill=color, width=w)
        d.line([s * 0.32, s * 0.64, s * 0.54, s * 0.64], fill=color, width=w)

    elif name == "table":
        # Tabla de nómina
        d.rounded_rectangle([s * 0.12, s * 0.16, s * 0.88, s * 0.84], radius=int(s * 0.05), outline=color, width=w)
        d.line([s * 0.12, s * 0.40, s * 0.88, s * 0.40], fill=color, width=w)
        d.line([s * 0.12, s * 0.62, s * 0.88, s * 0.62], fill=color, width=w)
        d.line([s * 0.42, s * 0.16, s * 0.42, s * 0.84], fill=color, width=w)
        d.line([s * 0.68, s * 0.16, s * 0.68, s * 0.84], fill=color, width=w)

    elif name == "search":
        # Lupa de búsqueda
        cx, cy, r = int(s * 0.42), int(s * 0.42), int(s * 0.28)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.line([cx + int(r * 0.70), cy + int(r * 0.70), int(s * 0.85), int(s * 0.85)], fill=color, width=int(w * 1.2))

    elif name == "filter":
        # Embudo de filtro
        pts = [
            (s * 0.18, s * 0.20),
            (s * 0.82, s * 0.20),
            (s * 0.58, s * 0.54),
            (s * 0.58, s * 0.82),
            (s * 0.42, s * 0.74),
            (s * 0.42, s * 0.54),
        ]
        d.polygon(pts, outline=color, width=w)

    elif name == "folder-open":
        # Cargar archivo / Abrir carpeta
        d.line([s * 0.14, s * 0.32, s * 0.42, s * 0.32], fill=color, width=w)
        d.line([s * 0.42, s * 0.32, s * 0.50, s * 0.42], fill=color, width=w)
        d.line([s * 0.50, s * 0.42, s * 0.86, s * 0.42], fill=color, width=w)
        pts = [
            (s * 0.12, s * 0.82),
            (s * 0.24, s * 0.44),
            (s * 0.90, s * 0.44),
            (s * 0.78, s * 0.82),
        ]
        d.polygon(pts, outline=color, width=w)

    elif name == "save":
        # Guardar en disco
        d.rounded_rectangle([s * 0.16, s * 0.16, s * 0.84, s * 0.84], radius=int(s * 0.06), outline=color, width=w)
        # Pestaña / Ventana de disquete
        d.rectangle([s * 0.30, s * 0.16, s * 0.70, s * 0.42], fill=color)
        d.rectangle([s * 0.30, s * 0.56, s * 0.70, s * 0.84], outline=color, width=w)

    elif name == "trash":
        # Tapa
        d.line([s * 0.18, s * 0.28, s * 0.82, s * 0.28], fill=color, width=w)
        d.rectangle([s * 0.38, s * 0.18, s * 0.62, s * 0.28], outline=color, width=w)
        # Bote
        d.line([s * 0.26, s * 0.28, s * 0.30, s * 0.84], fill=color, width=w)
        d.line([s * 0.74, s * 0.28, s * 0.70, s * 0.84], fill=color, width=w)
        d.line([s * 0.30, s * 0.84, s * 0.70, s * 0.84], fill=color, width=w)
        # Líneas internas
        d.line([s * 0.44, s * 0.38, s * 0.44, s * 0.74], fill=color, width=w)
        d.line([s * 0.56, s * 0.38, s * 0.56, s * 0.74], fill=color, width=w)

    elif name == "printer":
        # Impresora
        d.rounded_rectangle([s * 0.16, s * 0.36, s * 0.84, s * 0.74], radius=int(s * 0.05), outline=color, width=w)
        # Hoja superior
        d.rectangle([s * 0.28, s * 0.18, s * 0.72, s * 0.36], outline=color, width=w)
        # Hoja inferior
        d.rectangle([s * 0.28, s * 0.62, s * 0.72, s * 0.84], fill="#ffffff", outline=color, width=w)

    elif name == "copy":
        # Portapapeles / Copiar
        d.rectangle([s * 0.32, s * 0.14, s * 0.84, s * 0.68], outline=color, width=w)
        d.rectangle([s * 0.16, s * 0.32, s * 0.68, s * 0.86], fill="#ffffff", outline=color, width=w)

    elif name == "file-text":
        # Documento TXT
        d.rectangle([s * 0.22, s * 0.14, s * 0.78, s * 0.86], outline=color, width=w)
        d.line([s * 0.34, s * 0.32, s * 0.66, s * 0.32], fill=color, width=w)
        d.line([s * 0.34, s * 0.48, s * 0.66, s * 0.48], fill=color, width=w)
        d.line([s * 0.34, s * 0.64, s * 0.52, s * 0.64], fill=color, width=w)

    elif name == "calculator":
        # Calculadora
        d.rounded_rectangle([s * 0.20, s * 0.14, s * 0.80, s * 0.86], radius=int(s * 0.06), outline=color, width=w)
        # Pantalla
        d.rectangle([s * 0.30, s * 0.22, s * 0.70, s * 0.38], fill=color)
        # Botones
        d.ellipse([s * 0.32, s * 0.48, s * 0.44, s * 0.60], fill=color)
        d.ellipse([s * 0.56, s * 0.48, s * 0.68, s * 0.60], fill=color)
        d.ellipse([s * 0.32, s * 0.68, s * 0.44, s * 0.80], fill=color)
        d.ellipse([s * 0.56, s * 0.68, s * 0.68, s * 0.80], fill=color)

    elif name == "refresh":
        # Flecha de refrescar / limpiar
        cx, cy, r = int(s * 0.5), int(s * 0.5), int(s * 0.28)
        d.arc([cx - r, cy - r, cx + r, cy + r], start=45, end=315, fill=color, width=w)
        # Flecha
        d.polygon([(cx + r - int(s * 0.04), cy - int(s * 0.10)), (cx + r + int(s * 0.14), cy - int(s * 0.10)), (cx + r + int(s * 0.05), cy + int(s * 0.05))], fill=color)

    elif name == "info":
        # Círculo informativo
        cx, cy, r = int(s * 0.5), int(s * 0.5), int(s * 0.34)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.ellipse([cx - int(w * 0.6), cy - int(r * 0.6), cx + int(w * 0.6), cy - int(r * 0.3)], fill=color)
        d.line([cx, cy - int(r * 0.1), cx, cy + int(r * 0.55)], fill=color, width=w)

    elif name == "check":
        # Marca de verificación
        d.line([s * 0.22, s * 0.52, s * 0.44, s * 0.74], fill=color, width=int(w * 1.3))
        d.line([s * 0.44, s * 0.74, s * 0.82, s * 0.28], fill=color, width=int(w * 1.3))

    elif name == "settings":
        # Engranaje / Configuración
        cx, cy, r_out, r_in = int(s * 0.5), int(s * 0.5), int(s * 0.34), int(s * 0.16)
        d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], outline=color, width=w)
        d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=color, width=w)
        # Dientes del engranaje
        d.line([cx, s * 0.10, cx, s * 0.22], fill=color, width=int(w * 1.2))
        d.line([cx, s * 0.78, cx, s * 0.90], fill=color, width=int(w * 1.2))
        d.line([s * 0.10, cy, s * 0.22, cy], fill=color, width=int(w * 1.2))
        d.line([s * 0.78, cy, s * 0.90, cy], fill=color, width=int(w * 1.2))

    elif name == "plus-circle":
        # Círculo con más
        cx, cy, r = int(s * 0.5), int(s * 0.5), int(s * 0.36)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.line([cx, cy - int(r * 0.55), cx, cy + int(r * 0.55)], fill=color, width=w)
        d.line([cx - int(r * 0.55), cy, cx + int(r * 0.55), cy], fill=color, width=w)

    else:
        # Ícono genérico (círculo con punto)
        cx, cy, r = int(s * 0.5), int(s * 0.5), int(s * 0.34)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
        d.ellipse([cx - int(w), cy - int(w), cx + int(w), cy + int(w)], fill=color)

    # Redimensionar suavemente con Lanczos
    res = img.resize((size, size), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(res)
    _icon_cache[key] = tk_img
    return tk_img
