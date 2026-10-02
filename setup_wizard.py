# -*- coding: utf-8 -*-
# Kalibrasyon sihirbazi - ilk kurulum icin
# @author: Zodi4c  |  github.com/Zodi4ctvn
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

import os
import sys
import time
import json
import pyautogui

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_COORDS_FILE = os.path.join(BASE_DIR, "coordinates.json")

DEFAULT_COORDINATES = {
    "attack_button": None,         # Yan Köy sol alttaki 'Saldır'
    "find_now_button": None,       # Saldırı ekranındaki 'Şimdi Bul'
    "hero_slot": None,             # Ekranın altındaki Savaş Makinesi (Hero)
    "first_troop_slot": None,      # En soldaki 1. normal birlik yuvası
    "troop_slot_spacing": 75,      # Asker yuvaları arası piksel aralığı
    "deploy_zone_1": None,         # 1. Saldırı Konumu
    "deploy_zone_2": None,         # 2. Saldırı Konumu
    "deploy_zone_3": None,         # 3. Saldırı Konumu
    "deploy_zone_4": None,         # 4. Saldırı Konumu
    "deploy_zone_5": None,         # 5. Saldırı Konumu
    "deploy_zone_6": None,         # 6. Saldırı Konumu
    "deploy_zone_7": None,         # 7. Saldırı Konumu
    "return_home_button": None,    # Savaş bittiğinde çıkan 'TAMAM' / 'EVE DÖN'
    "zoom_out_point": None,        # Köyü küçültürken farenin üzerinde duracağı odak noktası
    "collect_elixir_1": None,      # Savaş sonrası 1. İksir / Ganimet toplama noktası
    "collect_elixir_2": None,      # Savaş sonrası 2. İksir / Ganimet toplama noktası
    "collect_elixir_3": None,      # Savaş sonrası 3. İksir / Ganimet toplama noktası
}

def load_coordinates():
    if os.path.exists(CONFIG_COORDS_FILE):
        try:
            with open(CONFIG_COORDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                coords = DEFAULT_COORDINATES.copy()
                coords.update(data)

                # Eski 4 kenar koordinatını yeni 1..4 saldırı noktalarına otomatik aktar
                if not coords.get("deploy_zone_1") and data.get("deploy_zone_top"):
                    coords["deploy_zone_1"] = data.get("deploy_zone_top")
                if not coords.get("deploy_zone_2") and data.get("deploy_zone_right"):
                    coords["deploy_zone_2"] = data.get("deploy_zone_right")
                if not coords.get("deploy_zone_3") and data.get("deploy_zone_bottom"):
                    coords["deploy_zone_3"] = data.get("deploy_zone_bottom")
                if not coords.get("deploy_zone_4") and data.get("deploy_zone_left"):
                    coords["deploy_zone_4"] = data.get("deploy_zone_left")

                # Eski gereksiz anahtarları temizle
                for old_k in ["deploy_zone_top", "deploy_zone_bottom", "deploy_zone_left", "deploy_zone_right"]:
                    coords.pop(old_k, None)

                return coords
        except Exception:
            pass
    return DEFAULT_COORDINATES.copy()

def save_coordinates(coords):
    with open(CONFIG_COORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(coords, f, indent=4, ensure_ascii=False)
    print(f"\n[+] Koordinatlar başarıyla '{CONFIG_COORDS_FILE}' dosyasına kaydedildi!", flush=True)

def play_beep():
    if HAS_SOUND:
        try:
            winsound.Beep(1200, 180)
        except Exception:
            pass

def wait_for_pointer(step_num, total_steps, target_desc, countdown=4):
    print(f"\n[{step_num}/{total_steps}] >> {target_desc}", flush=True)
    print(">> Fareyi bu noktanın üzerine götürün...", flush=True)
    
    for i in range(countdown, 0, -1):
        print(f"   Kalan süre: {i}...", flush=True)
        time.sleep(1)
        
    pos = pyautogui.position()
    play_beep()
    print(f"   [KAYDEDİLDİ!] X={pos.x}, Y={pos.y}", flush=True)
    return {"x": pos.x, "y": pos.y}

def run_calibration_wizard():
    print("""
==================================================================
   CLASH TITAN 2.0 — KURULUM SİHİRBAZI • Created by Zodi4c
==================================================================
Bu sihirbaz noktaları sırayla kaydeder.
Her adımda fareyi ilgili yere götürüp sayacın bitmesini bekleyin.
Nokta kaydedildiğinde 'bip' sesi duyacaksınız.
==================================================================
""", flush=True)

    print("5 saniye içinde Oyun/Emülatör penceresini (Google Play Games, BlueStacks, LDPlayer, GameLoop vb.) öne getirin...", flush=True)
    for i in range(5, 0, -1):
        print(f"Hazırlık: {i}...", flush=True)
        time.sleep(1)

    coords = load_coordinates()
    total_steps = 12

    # 1. Saldır
    coords["attack_button"] = wait_for_pointer(1, total_steps, "Sol alttaki 'SALDIR' butonunun üzerine gelin.")

    # 2. Şimdi Bul
    coords["find_now_button"] = wait_for_pointer(2, total_steps, "'ŞİMDİ BUL' butonunun üzerine gelin.")

    # 3. Hero
    coords["hero_slot"] = wait_for_pointer(3, total_steps, "Alt çubuktaki HERO (Savaş Makinesi) kutusunun üzerine gelin.")

    # 4. 1. Birlik Yuvası
    coords["first_troop_slot"] = wait_for_pointer(4, total_steps, "Alt çubuktaki 1. NORMAL ASKER YUVASI'nın üzerine gelin.")

    # 5 - 11. Saldırı Konumları (1..7)
    for i in range(1, 8):
        step_idx = 4 + i
        coords[f"deploy_zone_{i}"] = wait_for_pointer(step_idx, total_steps, f"Haritadaki {i}. SALDIRI KONUMU'na gelin.")

    # 12. Eve Dön (Tamam)
    print("\n* Son Adım: Savaş bitiminde çıkan 'TAMAM / EVE DÖN' butonu (veya sol alttaki Teslim Ol butonu yeri)", flush=True)
    coords["return_home_button"] = wait_for_pointer(total_steps, total_steps, "Savaş sonu 'TAMAM' / 'EVE DÖN' butonunun olacağı yere gelin.", countdown=5)

    save_coordinates(coords)
    print("\n" + "="*65, flush=True)
    print("TEBRİKLER! TÜM NOKTALAR BAŞARIYLA KAYDEDİLDİ.", flush=True)
    print("Artık '2. Botu Başlat' butonuna basarak savaşı başlatabilirsiniz!", flush=True)
    print("="*65 + "\n", flush=True)

if __name__ == "__main__":
    run_calibration_wizard()
