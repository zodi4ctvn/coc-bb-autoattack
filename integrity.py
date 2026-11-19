# -*- coding: utf-8 -*-
# Copyright (c) 2026 zodi4c (https://github.com/zodi4ctvn)
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)
import os
import sys

# Toplu bul-degistir ile atlatilmasini engellemek icin byte dizisi olarak tutulur
_AUTHOR = bytes((122, 111, 100, 105, 52, 99)).decode("ascii")
_HANDLE = bytes((122, 111, 100, 105, 52, 99, 116, 118, 110)).decode("ascii")
_BRAND = bytes((99, 108, 97, 115, 104, 32, 116, 105, 116, 97, 110)).decode("ascii")
_REPO_URL = f"https://github.com/{_HANDLE}"

_SOURCE_RULES = {
    "main.py": [
        _BRAND,
        f"created by {_AUTHOR}",
        f"github.com/{_HANDLE}",
    ],
    "gui.py": [
        f"@author: {_AUTHOR}",
        f'text="created by {_AUTHOR}"',
        f"• created by {_AUTHOR}",
        _REPO_URL,
    ],
    "bot.py": [
        f"@author: {_AUTHOR}",
        _BRAND,
        f"created by {_AUTHOR}",
    ],
    "setup_wizard.py": [
        f"@author: {_AUTHOR}",
        _BRAND,
        f"created by {_AUTHOR}",
    ],
    "locales.py": [
        f"@author: {_AUTHOR}",
    ],
    "config.py": [
        f"@author: {_AUTHOR}",
    ],
    "human_mouse.py": [
        f"@author: {_AUTHOR}",
    ],
    "icons.py": [
        f"@author: {_AUTHOR}",
    ],
    "vision.py": [
        f"@author: {_AUTHOR}",
    ],
}


def _check_runtime_locales() -> tuple[bool, str]:
    try:
        import locales
        strings = getattr(locales, "STRINGS", None)
    except Exception:
        return False, "locales.py"

    if not isinstance(strings, dict):
        return False, "locales.py"

    for lang in ("TR", "EN"):
        pack = strings.get(lang)
        if not isinstance(pack, dict):
            return False, f"locales.py ({lang})"

        app_title = str(pack.get("app_title", "")).lower()
        brand_name = str(pack.get("brand_name", "")).lower()
        brand_sub = str(pack.get("brand_sub", "")).lower()
        credit_footer = str(pack.get("credit_footer", "")).lower()

        if _BRAND not in app_title or _AUTHOR not in app_title:
            return False, f"locales.py ({lang}.app_title)"
        if _BRAND not in brand_name:
            return False, f"locales.py ({lang}.brand_name)"
        if _AUTHOR not in brand_sub:
            return False, f"locales.py ({lang}.brand_sub)"
        if _AUTHOR not in credit_footer:
            return False, f"locales.py ({lang}.credit_footer)"

    return True, ""


def _check_source_files(base_dir: str) -> tuple[bool, str]:
    for filename, required in _SOURCE_RULES.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.isfile(filepath):
            return False, filename
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().lower()
        except OSError:
            return False, filename

        for needle in required:
            if needle not in content:
                return False, filename

    return True, ""


def _abort(violated_target: str):
    title = f"CLASH TITAN 2.0 — Attribution Integrity Check Failed"
    detail = (
        f"[TR] '{violated_target}' icindeki orijinal '{_AUTHOR}' yazar veya proje bilgisi\n"
        f"silinmis ya da degistirilmis. Bu yazilim Custom Non-Commercial\n"
        f"Attribution License kapsaminda korunmaktadir.\n"
        f"Devam etmek icin orijinal '{_AUTHOR}' atfini geri yukleyin.\n\n"
        f"[EN] Original '{_AUTHOR}' author or project attribution was modified in:\n"
        f"    {violated_target}\n"
        f"This software is protected under a Custom Non-Commercial Attribution\n"
        f"License. Please restore the original '{_AUTHOR}' attribution to continue.\n\n"
        f"Original Author / Yazar : {_AUTHOR}\n"
        f"GitHub                  : {_REPO_URL}"
    )

    shown = False
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

    if not shown:
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, detail, title, 0x10 | 0x1000)
        except Exception:
            pass

    border = "=" * 65
    print(f"\n{border}", file=sys.stderr)
    print("  ATTRIBUTION INTEGRITY CHECK FAILED / ATIF DOGRULAMA HATASI", file=sys.stderr)
    print(f"{border}", file=sys.stderr)
    print(f"  Target / Hedef  : {violated_target}", file=sys.stderr)
    print(f"  Author / Yazar  : {_AUTHOR}", file=sys.stderr)
    print(f"  GitHub          : {_REPO_URL}", file=sys.stderr)
    print(f"{border}\n", file=sys.stderr)

    sys.exit(1)


def verify_integrity():
    passed, target = _check_runtime_locales()
    if not passed:
        _abort(target)

    if not getattr(sys, "frozen", False):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        passed, target = _check_source_files(base_dir)
        if not passed:
            _abort(target)
