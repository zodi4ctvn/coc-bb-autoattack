# -*- coding: utf-8 -*-
# Kalibrasyon sihirbazi - ilk kurulum icin (23-slot modern format)
# @author: zodi4c  |  github.com/zodi4ctvn
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

BASE_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
CONFIG_COORDS_FILE = os.path.join(BASE_DIR, "coordinates.json")

DEFAULT_COORDINATES = {
    "attack_button": None,         # Yan Köy sol alttaki 'Saldır'
    "find_now_button": None,       # Saldırı ekranındaki 'Şimdi Bul'
    "hero_slot": None,             # Ekranın altındaki Savaş Makinesi (Hero)
    "troop_slot_1": None,          # 1. Birlik Yuvası
    "troop_slot_2": None,          # 2. Birlik Yuvası
    "troop_slot_3": None,          # 3. Birlik Yuvası
    "troop_slot_4": None,          # 4. Birlik Yuvası
    "troop_slot_5": None,          # 5. Birlik Yuvası
    "troop_slot_6": None,          # 6. Birlik Yuvası
    "troop_slot_7": None,          # 7. Birlik Yuvası (2. Aşama Takviye 1)
    "troop_slot_8": None,          # 8. Birlik Yuvası (2. Aşama Takviye 2)
    "deploy_zone_1": None,         # 1. Saldırı Konumu
    "deploy_zone_2": None,         # 2. Saldırı Konumu
    "deploy_zone_3": None,         # 3. Saldırı Konumu
    "deploy_zone_4": None,         # 4. Saldırı Konumu
    "deploy_zone_5": None,         # 5. Saldırı Konumu
    "deploy_zone_6": None,         # 6. Saldırı Konumu
    "deploy_zone_7": None,         # 7. Saldırı Konumu
    "return_home_button": None,    # Savaş bittiğinde çıkan 'TAMAM' / 'EVE DÖN'
    "zoom_out_point": None,        # (Opsiyonel) Köyü küçültürken odak noktası
    "collect_elixir_1": None,      # (Opsiyonel) 1. İksir / Ganimet toplama noktası
    "collect_elixir_2": None,      # (Opsiyonel) 2. İksir / Ganimet toplama noktası
    "collect_elixir_3": None,      # (Opsiyonel) 3. İksir / Ganimet toplama noktası
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

                # Eski first_troop_slot varsa troop_slot_1'e aktar
                if not coords.get("troop_slot_1") and data.get("first_troop_slot"):
                    coords["troop_slot_1"] = data.get("first_troop_slot")

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
    from integrity import verify_integrity
    verify_integrity()
    print("""
==================================================================
   CLASH TITAN 2.0 — KURULUM SİHİRBAZI • Created by zodi4c
==================================================================
Bu sihirbaz 19 zorunlu noktayı sırayla kaydeder (modern 23-slot şeması).
Opsiyonel 4 nokta (zoom_out_point ve collect_elixir_1..3) istenirse
GUI üzerindeki Slot & Kalibrasyon sekmesinden eklenebilir.
Her adımda fareyi ilgili yere götürüp sayacın bitmesini bekleyin.
==================================================================
""", flush=True)

    print("5 saniye içinde Oyun/Emülatör penceresini (Google Play Games, BlueStacks, LDPlayer, GameLoop vb.) öne getirin...", flush=True)
    for i in range(5, 0, -1):
        print(f"Hazırlık: {i}...", flush=True)
        time.sleep(1)

    coords = load_coordinates()
    steps = [
        ("attack_button", "Sol alttaki 'SALDIR' butonunun üzerine gelin.", 4),
        ("find_now_button", "'ŞİMDİ BUL' butonunun üzerine gelin.", 4),
        ("hero_slot", "Alt çubuktaki HERO (Savaş Makinesi) kutusunun üzerine gelin.", 4),
    ]
    for i in range(1, 9):
        suffix = " (2. Aşama Takviye)" if i >= 7 else ""
        steps.append((f"troop_slot_{i}", f"Alt çubuktaki {i}. BİRLİK YUVASI'nın üzerine gelin.{suffix}", 4))
    for i in range(1, 8):
        steps.append((f"deploy_zone_{i}", f"Haritadaki {i}. SALDIRI KONUMU'na gelin.", 4))
    steps.append(("return_home_button", "Savaş sonu 'TAMAM' / 'EVE DÖN' butonunun olacağı yere gelin.", 5))

    total_steps = len(steps)
    for idx, (key, desc, cd) in enumerate(steps, start=1):
        coords[key] = wait_for_pointer(idx, total_steps, desc, countdown=cd)

    save_coordinates(coords)
    print("\n" + "=" * 65, flush=True)
    print("TEBRİKLER! 19 ZORUNLU NOKTA BAŞARIYLA KAYDEDİLDİ.", flush=True)
    print("Artık ClashTitan.bat veya 'python main.py' ile savaşı başlatabilirsiniz!", flush=True)
    print("=" * 65 + "\n", flush=True)

if __name__ == "__main__":
    run_calibration_wizard()
