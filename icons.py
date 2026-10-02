# -*- coding: utf-8 -*-
# Vektor ikon motoru - supersampled, emoji yok
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

from PIL import Image, ImageDraw
import customtkinter as ctk

def _create_canvas(size=(64, 64)):
    """Supersampling için 4 katı büyük tuval oluşturur (anti-aliasing)."""
    return Image.new("RGBA", size, (0, 0, 0, 0))

def _scale_to_ctk(img, display_size=(18, 18)):
    """Büyük tuvali pürüzsüzce küçülterek CTkImage yapar."""
    smooth = img.resize(display_size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=smooth, dark_image=smooth, size=display_size)

def get_dashboard_icon(color="#94a3b8", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # 4 kareli modern ızgara ikonu
    d.rounded_rectangle([8, 8, 28, 28], radius=4, fill=color)
    d.rounded_rectangle([36, 8, 56, 28], radius=4, fill=color)
    d.rounded_rectangle([8, 36, 28, 56], radius=4, fill=color)
    d.rounded_rectangle([36, 36, 56, 56], radius=4, fill=color)
    return _scale_to_ctk(img, size)

def get_target_icon(color="#94a3b8", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Hassas nişangah / hedef dairesi
    d.ellipse([10, 10, 54, 54], outline=color, width=5)
    d.ellipse([24, 24, 40, 40], fill=color)
    d.line([32, 4, 32, 14], fill=color, width=4)
    d.line([32, 50, 32, 60], fill=color, width=4)
    d.line([4, 32, 14, 32], fill=color, width=4)
    d.line([50, 32, 60, 32], fill=color, width=4)
    return _scale_to_ctk(img, size)

def get_shield_icon(color="#94a3b8", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Geometrik modern kalkan
    points = [(32, 6), (54, 14), (50, 40), (32, 58), (14, 40), (10, 14)]
    d.polygon(points, fill=color)
    return _scale_to_ctk(img, size)

def get_terminal_icon(color="#94a3b8", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # >_ Komut satırı ikonu
    d.line([12, 16, 28, 32], fill=color, width=5)
    d.line([28, 32, 12, 48], fill=color, width=5)
    d.line([34, 48, 52, 48], fill=color, width=5)
    return _scale_to_ctk(img, size)

def get_play_icon(color="#022c22", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Sağa bakan üçgen
    d.polygon([(18, 10), (52, 32), (18, 54)], fill=color)
    return _scale_to_ctk(img, size)

def get_stop_icon(color="#ffffff", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Kare durdurma ikonu
    d.rounded_rectangle([14, 14, 50, 50], radius=5, fill=color)
    return _scale_to_ctk(img, size)

def get_fast_forward_icon(color="#ffffff", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Çift sağa ok >>
    d.polygon([(10, 14), (30, 32), (10, 50)], fill=color)
    d.polygon([(30, 14), (50, 32), (30, 50)], fill=color)
    return _scale_to_ctk(img, size)

def get_flag_icon(color="#ffffff", size=(18, 18)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Bayrak / Bitiş ikonu
    d.line([14, 8, 14, 56], fill=color, width=5)
    d.polygon([(14, 10), (52, 24), (14, 38)], fill=color)
    return _scale_to_ctk(img, size)

def get_pin_icon(color="#f8fafc", size=(14, 14)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # İğne / Konum ikonu
    d.ellipse([18, 8, 46, 36], fill=color)
    d.polygon([(20, 26), (44, 26), (32, 56)], fill=color)
    d.ellipse([27, 17, 37, 27], fill="#0b0e14")
    return _scale_to_ctk(img, size)

def get_check_icon(color="#10b981", size=(14, 14)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Minimalist tik işareti
    d.line([12, 34, 26, 48], fill=color, width=6)
    d.line([26, 48, 52, 16], fill=color, width=6)
    return _scale_to_ctk(img, size)

def get_brand_icon(color="#ef4444", size=(24, 24)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Taktiksel geometrik amblem (Elmas ve kalkan çizgileri)
    d.polygon([(32, 4), (58, 22), (48, 58), (16, 58), (6, 22)], outline=color, width=4)
    d.polygon([(32, 16), (46, 28), (38, 50), (26, 50), (18, 28)], fill=color)
    d.ellipse([26, 26, 38, 38], fill="#0a0b10")
    return _scale_to_ctk(img, size)

def get_status_dot(color="#10b981", size=(10, 10)):
    img = _create_canvas((32, 32))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 4, 28, 28], fill=color)
    return _scale_to_ctk(img, size)

def get_trash_icon(color="#94a3b8", size=(14, 14)):
    img = _create_canvas()
    d = ImageDraw.Draw(img)
    # Çöp kutusu ikonu
    d.line([16, 18, 48, 18], fill=color, width=4)
    d.line([24, 12, 40, 12], fill=color, width=4)
    d.line([20, 18, 22, 54], fill=color, width=4)
    d.line([44, 18, 42, 54], fill=color, width=4)
    d.line([22, 54, 42, 54], fill=color, width=4)
    d.line([28, 24, 28, 48], fill=color, width=3)
    d.line([36, 24, 36, 48], fill=color, width=3)
    return _scale_to_ctk(img, size)

