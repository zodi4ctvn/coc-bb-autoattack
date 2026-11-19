# -*- coding: utf-8 -*-
# Attribution integrity check - yazilim korumasi
# Copyright (c) 2026 Zodi4c (https://github.com/zodi4ctvn)
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)
import os
import sys


_AUTHOR_NAME = "Zodi4c"
_REPO_URL = "https://github.com/zodi4ctvn"

# Dogrulama icin izlenen dosyalar ve iclerindeki zorunlu dizeler
_REQUIRED_STRINGS = {
    "config.py":       ["@author: Zodi4c"],
    "human_mouse.py":  ["@author: Zodi4c"],
    "icons.py":        ["@author: Zodi4c"],
    "vision.py":       ["@author: Zodi4c"],
    "locales.py":      ["Zodi4c"],
    "bot.py":          ["Zodi4c"],
    "gui.py":          ["Zodi4ctvn"],
}


def _check_attribution(base_dir: str) -> tuple[bool, str]:
    """
    Her korunan dosyada zorunlu Zodi4c imzasinin var oldugunu dogrular.
    (bool: gecti/kaldi, str: ihlal eden dosya adi)
    """
    for filename, required in _REQUIRED_STRINGS.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except (IOError, OSError):
            continue
        for needle in required:
            if needle not in content:
                return False, filename
    return True, ""


def _abort(violated_file: str):
    """Imza ihlali tespit edildiginde tek bir popup gosterip programi durdurur."""

    title = "CLASH TITAN 2.0 — Atif / Attribution Integrity Check Failed"
    detail = (
        f"[TR] '{violated_file}' dosyasindaki orijinal 'Zodi4c' yazar bilgisi\n"
        f"silinmis veya degistirilmis. Bu yazilim Custom Non-Commercial\n"
        f"Attribution License kapsaminda korunmaktadir.\n"
        f"Kullanmak icin lutfen orijinal Zodi4c atfini geri yukleyin.\n\n"
        f"[EN] The original 'Zodi4c' author credit was removed or modified in:\n"
        f"    {violated_file}\n"
        f"This software is protected under a Custom Non-Commercial Attribution\n"
        f"License. Please restore the original Zodi4c attribution to continue.\n\n"
        f"Original Author / Yazar : {_AUTHOR_NAME}\n"
        f"GitHub                  : {_REPO_URL}"
    )

    shown = False

    # 1. Oncelik: tkinter messagebox (GUI popup)
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror(title, detail)
        root.destroy()
        shown = True
    except Exception:
        shown = False

    # 2. Yedek: Yalnizca tkinter basarisiz olursa Windows native MessageBox
    if not shown:
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                detail,
                title,
                0x10 | 0x1000  # MB_ICONERROR | MB_SYSTEMMODAL
            )
            shown = True
        except Exception:
            pass

    # 3. Konsol stderr cikisi
    border = "=" * 65
    print(f"\n{border}", file=sys.stderr)
    print("  ATTRIBUTION INTEGRITY CHECK FAILED / ATIF DOGRULAMA HATASI", file=sys.stderr)
    print(f"{border}", file=sys.stderr)
    print(f"  Violated file / Dosya : {violated_file}", file=sys.stderr)
    print(f"  Author / Yazar        : {_AUTHOR_NAME}", file=sys.stderr)
    print(f"  GitHub                : {_REPO_URL}", file=sys.stderr)
    print("  Restore the original Zodi4c attribution to use this software.", file=sys.stderr)
    print(f"{border}\n", file=sys.stderr)

    sys.exit(1)


def verify_integrity():
    """
    Ana dogrulama fonksiyonu.
    main.py'den import edilerek program baslamadan once cagrilir.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    passed, violated_file = _check_attribution(base_dir)
    if not passed:
        _abort(violated_file)
