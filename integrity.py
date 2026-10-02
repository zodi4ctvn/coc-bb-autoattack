# -*- coding: utf-8 -*-
# Attribution integrity check - yazilim korumasi
# Copyright (c) 2026 Zodi4c (https://github.com/Zodi4ctvn)
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)
import os
import sys


_AUTHOR_NAME = "Zodi4c"
_REPO_URL    = "https://github.com/Zodi4ctvn"

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
    """Imza ihlali tespit edildiginde popup gosterip programi durdurur."""

    title  = "CLASH TITAN 2.0 — Attribution Integrity Check Failed"
    detail = (
        f"The author credit 'Zodi4c' was removed or modified in:\n\n"
        f"    {violated_file}\n\n"
        f"This software is protected under a Custom Non-Commercial\n"
        f"Attribution License. Removing the original author credit\n"
        f"is strictly prohibited.\n\n"
        f"Original Author  : {_AUTHOR_NAME}\n"
        f"Repository       : {_REPO_URL}\n\n"
        f"Restore the original attribution to use this software."
    )

    # 1. Oncelik: tkinter messagebox (GUI popup - her zaman gorunur)
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror(title, detail)
        root.destroy()
    except Exception:
        pass

    # 2. Yedek: Windows native MessageBox (ctypes ile)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            detail,
            title,
            0x10 | 0x1000  # MB_ICONERROR | MB_SYSTEMMODAL (her zaman on planda)
        )
    except Exception:
        pass

    # 3. Son yedek: stderr + konsol pause
    border = "=" * 65
    print(f"\n{border}", file=sys.stderr)
    print(f"  ATTRIBUTION INTEGRITY CHECK FAILED", file=sys.stderr)
    print(f"{border}", file=sys.stderr)
    print(f"  Violated file : {violated_file}", file=sys.stderr)
    print(f"  Author        : {_AUTHOR_NAME}", file=sys.stderr)
    print(f"  Repo          : {_REPO_URL}", file=sys.stderr)
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
