# -*- coding: utf-8 -*-
# Clash Titan 2.0 - ana calistirici
# Copyright (c) 2026 Zodi4c (https://github.com/Zodi4ctvn)
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)
import sys
import os

# Calisma dizinini projenin kok dizinine sabitle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ---------------------------------------------------------------
# Attribution Integrity Check — Yazilim koruma katmani
# Orijinal yazar bilgisi (Zodi4c) silinmis/degistirilmisse dur.
# ---------------------------------------------------------------
from integrity import verify_integrity
verify_integrity()
# ---------------------------------------------------------------


def print_banner():
    print("""
==================================================================
          CLASH TITAN 2.0 -- BUILDER BASE AUTOMATION
                    Created by Zodi4c
              DirectInput Heuristic Anti-Detection
       (c) 2026 Zodi4c | github.com/Zodi4ctvn
==================================================================
    """)


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_banner()
        print("""Kullanim / Usage:
    ClashTitan.bat           -> Gorsel Kontrol Panelini (GUI) Baslatir
    ClashTitan.bat --cli     -> Konsol Tabanli Botu Baslatir
    ClashTitan.bat --wizard  -> Kalibrasyon Sihirbazini Baslatir
        """)
        return

    if "--cli" in args:
        print_banner()
        from bot import BuilderBase2Bot
        bot = BuilderBase2Bot()
        bot.start()

    elif "--wizard" in args:
        print_banner()
        from setup_wizard import run_calibration_wizard
        run_calibration_wizard()

    else:
        # Varsayilan: Modern Gorsel Arayuz (GUI)
        from gui import LuxuryBotDashboard
        app = LuxuryBotDashboard()
        app.mainloop()


if __name__ == "__main__":
    main()
