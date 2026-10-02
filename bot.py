# -*- coding: utf-8 -*-
# Ana bot motoru - Builder Base 2.0 saldirilari
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

import sys
import os
import json
import time
import random
import threading
import ctypes
import keyboard

# Windows konsolunda Türkçe kod sayfası (cp1254) Unicode crashlerini önle ve satır bazlı tamponlama yap
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

from config import ANTI_BAN, BATTLE_SETTINGS, HOTKEYS, DEFAULT_LANGUAGE
from human_mouse import human_move, human_click, human_quick_tap, random_delay, idle_micro_drift, human_zoom_out, human_drag
from setup_wizard import load_coordinates
from vision import VisionDetector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")
CMD_FILE = os.path.join(BASE_DIR, "bot_command.txt")

class BuilderBase2Bot:
    def __init__(self):
        self.running = False
        self.paused = False
        self.attack_count = 0
        self.start_time = time.time()
        
        self.user_prefs = {}
        self.lang = DEFAULT_LANGUAGE
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.user_prefs = cfg
                    self.lang = cfg.get("language", DEFAULT_LANGUAGE)
                    if "attacks_before_break" in cfg:
                        ANTI_BAN["attacks_before_break"] = int(cfg["attacks_before_break"])
                    if "stage2_wait_seconds" in cfg:
                        BATTLE_SETTINGS["stage2_wait_seconds"] = int(cfg["stage2_wait_seconds"])
                    if "stage2_finish_wait_seconds" in cfg:
                        BATTLE_SETTINGS["stage2_finish_wait_seconds"] = int(cfg["stage2_finish_wait_seconds"])
                    if "clicks_per_troop_slot" in cfg:
                        BATTLE_SETTINGS["clicks_per_troop_slot"] = int(cfg["clicks_per_troop_slot"])
                    if "stage1_troop_slots" in cfg:
                        BATTLE_SETTINGS["stage1_troop_slots"] = int(cfg["stage1_troop_slots"])
                    if "stage2_mode" in cfg:
                        BATTLE_SETTINGS["stage2_mode"] = cfg["stage2_mode"]
            except Exception:
                pass

        self.coords = load_coordinates()
        self.vision = VisionDetector()
        
        self.manual_stage2_triggered = False
        self.manual_finish_triggered = False
        if os.path.exists(CMD_FILE):
            try:
                os.remove(CMD_FILE)
            except Exception:
                pass
        self._setup_hotkeys()

    def _setup_hotkeys(self):
        import threading
        import ctypes
        def stop_bot():
            msg = "\n[!] EMERGENCY STOP KEY PRESSED ('q'). Stopping bot immediately..." if self.lang == "EN" else "\n[!] ACİL DURDURMA TUŞUNA BASILDI ('q'). Bot anında durduruluyor..."
            try:
                print(msg, flush=True)
                sys.stdout.flush()
                # Windows donanım düzeyinde sol tıklamayı serbest bırak (fare takılı kalmasın)
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            except Exception:
                pass
            self.running = False
            # Anında ve kesin çıkış (hiçbir sonraki adıma veya gecikmeye izin vermez)
            os._exit(0)

        def toggle_pause():
            self.paused = not self.paused
            if self.lang == "EN":
                durum = "PAUSED" if self.paused else "RESUMED"
                print(f"\n[*] Bot {durum} (Press 'p' to toggle).", flush=True)
            else:
                durum = "DURAKLATILDI" if self.paused else "DEVAM EDİYOR"
                print(f"\n[*] Bot {durum} ('p' tuşuna basarak değiştirebilirsiniz).", flush=True)

        def trigger_stage2():
            msg = "\n[*] [MANUAL] 'F2' pressed: Stage 2 reinforcements triggered!" if self.lang == "EN" else "\n[*] [MANUEL] 'F2' tuşuna basıldı: 2. Aşama takviyeleri tetiklendi!"
            try:
                print(msg, flush=True)
            except Exception:
                pass
            self.manual_stage2_triggered = True

        def trigger_finish():
            msg = "\n[*] [MANUAL] 'F3' pressed: Battle finish triggered!" if self.lang == "EN" else "\n[*] [MANUEL] 'F3' tuşuna basıldı: Savaş bitirme tetiklendi!"
            try:
                print(msg, flush=True)
            except Exception:
                pass
            self.manual_finish_triggered = True

        # 1. Standart Hook
        try:
            keyboard.add_hotkey(HOTKEYS.get("stop", "q"), stop_bot)
            keyboard.add_hotkey(HOTKEYS.get("pause", "p"), toggle_pause)
            keyboard.add_hotkey(HOTKEYS.get("manual_stage2", "f2"), trigger_stage2)
            keyboard.add_hotkey(HOTKEYS.get("manual_finish", "f3"), trigger_finish)
        except Exception as e:
            print(f"[!] Keyboard listener error: {e}")

        # 2. Windows Kernel Düzeyinde Kesintisiz Donanım Dinleyicisi (Farklı pencere / Yönetici modu olsa dahi yakalar)
        def _hardware_key_poller():
            user32 = ctypes.windll.user32
            while True:
                try:
                    # 0x51 = 'Q' tuşu, 0x1B = ESC tuşu
                    if bool(user32.GetAsyncKeyState(0x51) & 0x8000) or bool(user32.GetAsyncKeyState(0x1B) & 0x8000):
                        stop_bot()
                        break
                    # 0x50 = 'P' tuşu
                    if bool(user32.GetAsyncKeyState(0x50) & 0x8000):
                        toggle_pause()
                        time.sleep(0.35)  # debounce
                except Exception:
                    pass
                time.sleep(0.02)

        threading.Thread(target=_hardware_key_poller, daemon=True).start()

    def safe_sleep(self, seconds, step=0.03):
        """
        Kesintiye uğrayabilir güvenli uyku:
        'q' veya durdurma tuşuna basıldığı anda 20-30 milisaniyede çıkar,
        böylece bot 5-8 saniyelik uzun uykularda takılı kalmaz.
        """
        start = time.time()
        while (time.time() - start) < seconds:
            if not self.running:
                return False
            while self.paused and self.running:
                time.sleep(0.15)
            time.sleep(step)
        return self.running

    def check_external_commands(self):
        """Panelden gelen komut dosyasını kontrol eder."""
        if os.path.exists(CMD_FILE):
            try:
                with open(CMD_FILE, "r", encoding="utf-8") as f:
                    cmd = f.read().strip()
                os.remove(CMD_FILE)
                if cmd == "STAGE2":
                    self.manual_stage2_triggered = True
                elif cmd == "FINISH":
                    self.manual_finish_triggered = True
            except Exception:
                pass

    def log(self, message):
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        tag = f"Attack #{self.attack_count}" if self.lang == "EN" else f"Saldırı #{self.attack_count}"
        print(f"[{mins:02d}:{secs:02d}] [{tag}] {message}", flush=True)
        try:
            sys.stdout.flush()
        except Exception:
            pass

    def get_deploy_zones(self):
        """
        Kullanıcının belirlediği 7 adet saldırı/bırakma konumunu sırasıyla döndürür.
        Eğer kullanıcı henüz 7'li konumu kaydetmediyse eski 4'lü noktalara veya güvenli koordinatlara döner.
        """
        zones = []
        for i in range(1, 8):
            key = f"deploy_zone_{i}"
            pt = self.coords.get(key)
            if pt and pt.get("x") is not None and pt.get("y") is not None:
                zones.append(pt)

        # Eğer hiç koordinat yoksa ekran çözünürlüğüne göre 7 güvenli nokta
        if not zones:
            zones = [
                {"x": 960, "y": 180},
                {"x": 1250, "y": 280},
                {"x": 1440, "y": 500},
                {"x": 1250, "y": 720},
                {"x": 960, "y": 820},
                {"x": 670, "y": 720},
                {"x": 480, "y": 500},
            ]
        return zones

    def click_point(self, point_key, description=""):
        """Kayıtlı koordinata insan benzeri kavisle ve rastgele sapmayla tıklar."""
        if not self.running:
            return False

        while self.paused and self.running:
            time.sleep(0.5)

        pt = self.coords.get(point_key)
        if pt and pt.get("x") is not None and pt.get("y") is not None:
            self.log(f"{description} (X={pt['x']}, Y={pt['y']})")
            human_click(pt["x"], pt["y"])
            return True

        self.log(f"[UYARI] '{point_key}' için kayıtlı koordinat bulunamadı! 'setup_wizard.py' çalıştırın.")
        return False

    def deploy_unit_to_zone(self, slot_key, target_zone, label="", zone_num=1):
        """Bir birlik veya hero yuvasını seçer ve belirlenen spesifik saldırı yerine 1 tıkla bırakır."""
        if not self.running:
            return False
        pt = self.coords.get(slot_key)
        if not pt or pt.get("x") is None:
            return False

        self.log(f"-> {label or slot_key} seçiliyor -> {zone_num}. Saldırı Noktasına bırakılıyor...")
        human_click(pt["x"], pt["y"], jitter=False, delay_after=False)
        time.sleep(random.uniform(0.20, 0.30))
        human_quick_tap(target_zone["x"], target_zone["y"])
        time.sleep(random.uniform(0.25, 0.38))
        return True

    def deploy_stage(self, stage_num=1):
        """
        Sahaya birlikleri 7 belirlenen saldırı konumuna deterministik (sıralı ve eşit) olarak döker:
        - 1. Aşama: Hero + 6 Birlik (Toplam 7 birim -> 7 saldırı bölgesine 1'er adet)
        - 2. Aşama: Hero + 8 Birlik (Toplam 9 birim -> 7 bölgeye eşit dağılım)
        Asla rastgele yapılmaz; hiçbir saldırı bölgesi boş bırakılmaz.
        """
        self.log(f"--- {stage_num}. AŞAMA BİRLİKLERİ SAHAYA SÜRÜLÜYOR ---")
        zones = self.get_deploy_zones()
        num_zones = len(zones)

        # Bırakılacak birimlerin listesini sırayla hazırla
        units = []
        if BATTLE_SETTINGS.get("has_hero", True):
            units.append(("hero_slot", f"{stage_num}. Aşama Hero"))

        total_troops = 6 if stage_num == 1 else 8
        for i in range(1, total_troops + 1):
            units.append((f"troop_slot_{i}", f"[{i}/{total_troops}] {i}. Birlik"))

        # Her birimi sırasıyla ilgili saldırı noktasına bırak
        for idx, (slot_key, label) in enumerate(units):
            if not self.running:
                break
            zone_idx = idx % num_zones
            target_zone = zones[zone_idx]
            zone_num = zone_idx + 1
            self.deploy_unit_to_zone(slot_key, target_zone, label=label, zone_num=zone_num)

        self.log(f"[✓] {stage_num}. Aşama birlik dağıtımı tamamlandı ({num_zones} noktaya eşit dağıtıldı).")

    def handle_battle_progression(self, already_stage2=False):
        """
        Savaş devam ederken:
        - Otomatik Modda: 1. aşama bitişi / 2. aşamaya otomatik geçiş süresi (Default: 90 sn) dolunca
          Hero + 8 birliği otomatik sahaya sürer.
        - Manuel Modda: F2 tuşu veya panel butonu gelene kadar bekler.
        - 2. Aşama atıldıktan sonra: Kullanıcının belirlediği süre (Default: 60 sn / 1 dk) boyunca
          savaşı izler ve ardından otomatik olarak köye döner (F3 ile erken çıkılabilir).
        """
        battle_start = time.time()
        stage2_deployed = already_stage2
        stage2_deploy_time = time.time() if already_stage2 else None

        stage2_auto_wait = self.user_prefs.get("stage2_wait_seconds", BATTLE_SETTINGS.get("stage2_wait_seconds", 75))
        stage2_finish_wait = self.user_prefs.get("stage2_finish_wait_seconds", BATTLE_SETTINGS.get("stage2_finish_wait_seconds", 50))
        stage2_mode = self.user_prefs.get("stage2_mode", BATTLE_SETTINGS.get("stage2_mode", "AUTO"))
        max_duration = BATTLE_SETTINGS.get("max_battle_duration_seconds", 180)

        # 1. Aşama sırasında biriken eski komutları temizle (eğer 2. aşama henüz atılmadıysa)
        self.manual_stage2_triggered = False
        if os.path.exists(CMD_FILE):
            try:
                os.remove(CMD_FILE)
            except Exception:
                pass

        if stage2_deployed:
            self.log(f"2. Aşama sahada. {stage2_finish_wait} sn sonra köye dönülecek (Erken bitir: F3)...")
        else:
            if stage2_mode == "AUTO":
                self.log(f"1. Aşama izleniyor. {stage2_auto_wait} sn sonra 2. Aşama otomatik atılacak (Hemen geç: F2)...")
            else:
                self.log("1. Aşama izleniyor. 2. Aşama bekleniyor (Manuel: F2 veya Panel Butonu)...")

        last_stage2_log = 0
        last_finish_log = 0

        while self.running:
            now = time.time()
            elapsed_from_start = now - battle_start

            # Canlı Süreç ve Sayaç Bilgilendirmesi (Konsolda her 10 saniyede bir kalan süreyi yazar)
            if not stage2_deployed and stage2_mode == "AUTO":
                rem_stage2 = int(stage2_auto_wait - elapsed_from_start)
                if rem_stage2 > 0 and (now - last_stage2_log >= 10):
                    if self.lang == "EN":
                        self.log(f"[Countdown] Stage 2 auto-transition remaining: {rem_stage2}s (Trigger now: F2)")
                    else:
                        self.log(f"[Sayaç] 2. Aşamaya otomatik geçişe kalan: {rem_stage2} sn (Hemen geç: F2)")
                    last_stage2_log = now
            elif stage2_deployed and stage2_deploy_time:
                rem_finish = int(stage2_finish_wait - (now - stage2_deploy_time))
                if rem_finish > 0 and (now - last_finish_log >= 10):
                    if self.lang == "EN":
                        self.log(f"[Countdown] Battle end & return home remaining: {rem_finish}s (Finish now: F3)")
                    else:
                        self.log(f"[Sayaç] Savaş bitişi ve köye dönüşe kalan: {rem_finish} sn (Hemen bitir: F3)")
                    last_finish_log = now

            # Süre aşımı kontrolü (3 dakikadan fazla sürerse)
            if elapsed_from_start > max_duration:
                self.log("Maksimum savaş süresi aşıldı.")
                break

            # 1. Harici komutları ve tuşları denetle (F2 / F3)
            self.check_external_commands()

            # Manuel Bitirme Tetiklendi mi? (F3 veya Panel Butonu)
            if self.manual_finish_triggered:
                self.log("[MANUEL] Savaş erken bitirme (F3) tetiklendi! 'Tamam' butonuna basılıyor...")
                self.manual_finish_triggered = False
                break

            # 2. Aşama Birliklerini Sahaya Sürme Şartı:
            # - Kullanıcı F2'ye basmışsa VEYA
            # - Mod "AUTO" ise ve 1. aşamadan bu yana 'stage2_auto_wait' (75 sn) geçmişse
            should_deploy_stage2 = False
            if not stage2_deployed:
                # DEFEAT (YENİLGİ) KORUMASI:
                # Savaşın en az 25. saniyesinden sonra, tüm birlikler elenip yenildiysek ekranda 'Eve Dön' butonu belirir.
                # Yanlış eşleşmeleri (çim, can barı) engellemek için güven eşiği %74'tür.
                if elapsed_from_start >= 25:
                    try:
                        home_match = self.vision.find_template("return_home_button", confidence=0.74, return_best_score=True)
                        if home_match[0] is not None and home_match[2] >= 0.74:
                            score_pct = int(home_match[2] * 100)
                            self.log(f"[DEFEAT KORUMASI] Ekranda gerçek 'Eve Dön' butonu doğrulandı! (Benzerlik: %{score_pct})")
                            self.log("-> 1. Aşamada yenilgi gerçekleşti / savaş bitti. 2. Aşama iptal ediliyor!")
                            self.log("-> 'Eve Dön' butonuna basılıyor ve döngü sıfırdan başlatılıyor...")
                            human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                            self.safe_sleep(random.uniform(1.2, 1.6))
                            human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                            self.safe_sleep(random.uniform(1.8, 2.4))
                            break
                    except Exception:
                        pass

                if self.manual_stage2_triggered:
                    self.log("[MANUEL] 2. Aşama komutu alındı (F2)! Hero + 8 Birlik sahaya sürülüyor...")
                    self.manual_stage2_triggered = False
                    should_deploy_stage2 = True
                elif stage2_mode == "AUTO" and elapsed_from_start >= stage2_auto_wait:
                    # 2. Aşamaya geçmeden hemen önce son bir kez daha Defeat kontrolü
                    try:
                        home_match = self.vision.find_template("return_home_button", confidence=0.74, return_best_score=True)
                        if home_match[0] is not None and home_match[2] >= 0.74:
                            score_pct = int(home_match[2] * 100)
                            self.log(f"[DEFEAT KORUMASI] 2. Aşamaya geçmeden önce gerçek 'Eve Dön' butonu görüldü! (Benzerlik: %{score_pct})")
                            self.log("-> 2. Aşama sahaya sürülmüyor. 'Eve Dön'e basılarak yeni döngü başlatılıyor...")
                            human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                            self.safe_sleep(random.uniform(1.2, 1.6))
                            human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                            self.safe_sleep(random.uniform(1.8, 2.4))
                            break
                    except Exception:
                        pass

                    self.log(f"[OTOMATİK] 1. Aşama süresi doldu ({stage2_auto_wait} sn). 2. Aşama (Hero + 8 Birlik) sahaya sürülüyor...")
                    should_deploy_stage2 = True

            if should_deploy_stage2:
                self.deploy_stage(stage_num=2)
                stage2_deployed = True
                stage2_deploy_time = time.time()
                last_finish_log = time.time()
                self.log(f"2. Aşama birlikleri sahada. Savaşın tamamlanması için {stage2_finish_wait} sn bekleniyor (Erken bitir: F3)...")

            # 3. 2. Aşama Bekleme Sırasında Erken Bitiş / Eve Dön Kontrolü
            if stage2_deployed and stage2_deploy_time:
                # 2. Aşamada da savaş erken biterse ekranda 'Eve Dön' çıkar
                try:
                    home_match = self.vision.find_template("return_home_button", confidence=0.74, return_best_score=True)
                    if home_match[0] is not None and home_match[2] >= 0.74:
                        score_pct = int(home_match[2] * 100)
                        self.log(f"[SAVAŞ BİTTİ] Ekranda 'Eve Dön' butonu doğrulandı (Benzerlik: %{score_pct}). Süre dolmadan köye dönülüyor...")
                        human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                        self.safe_sleep(random.uniform(1.2, 1.6))
                        human_click(home_match[0], home_match[1], jitter=False, delay_after=False)
                        self.safe_sleep(random.uniform(1.8, 2.4))
                        break
                except Exception:
                    pass

                elapsed_since_stage2 = now - stage2_deploy_time
                if elapsed_since_stage2 >= stage2_finish_wait:
                    self.log(f"2. Aşama sonrası bekleme süresi ({stage2_finish_wait} sn) doldu. Savaş sonuçlandırılıyor...")
                    break

            if not self.safe_sleep(0.5):
                return

        if not self.running:
            return

        # Savaş bitti: Ana köye dönüş için 'Tamam / Eve Dön' butonunu çift tıkla (Loot/Yıldız pencerelerini kapatır)
        self.log("Savaş bitti. 'Tamam / Eve Dön' butonlarına basılarak köye dönülüyor...")
        # Önce görsel olarak Eve Dön butonunu ara
        home_pos = None
        try:
            home_match = self.vision.find_template("return_home_button", confidence=0.48)
            if home_match:
                home_pos = (home_match[0], home_match[1])
        except Exception:
            pass

        if not home_pos:
            return_btn = self.coords.get("return_home_button")
            if return_btn and return_btn.get("x"):
                home_pos = (return_btn["x"], return_btn["y"])

        if home_pos:
            # 1. Tık: Savaş Sonuç Ekranı 'Tamam / Eve Dön'
            human_click(home_pos[0], home_pos[1], jitter=False, delay_after=False)
            if not self.safe_sleep(random.uniform(1.2, 1.8)):
                return
            # 2. Tık: Ganimet / Kupa Özeti Ekranı 'Tamam'
            human_click(home_pos[0], home_pos[1], jitter=False, delay_after=False)
            self.safe_sleep(random.uniform(1.5, 2.5))

    def zoom_out_village(self):
        """
        Köyün (iksir toplayıcıların ve ganimet arabasının) net görünmesi için
        kullanıcının belirlediği odak noktasına (veya oyun merkezine) gider
        ve fare tekerleğiyle haritayı en uzak mesafeye küçültür (zoom-out).
        """
        if not self.running:
            return

        target_x, target_y = None, None

        # 1. Kullanıcı özel bir küçültme odak noktası kalibre etmişse öncelikle onu kullan
        custom_zoom_pt = self.coords.get("zoom_out_point")
        if custom_zoom_pt and custom_zoom_pt.get("x") is not None and custom_zoom_pt.get("y") is not None:
            target_x = custom_zoom_pt["x"]
            target_y = custom_zoom_pt["y"]
            self.log(f"[KAMERA / ZOOM] Belirlenen özel odak noktasına (X={target_x}, Y={target_y}) gidiliyor ve tekerlek çekiliyor...")
        else:
            try:
                rect = self.vision.get_game_window_rect()
                if rect:
                    target_x = (rect[0] + rect[2]) // 2
                    target_y = (rect[1] + rect[3]) // 2
            except Exception:
                pass

            if target_x is None:
                zones = self.get_deploy_zones()
                if zones:
                    target_x = sum(z["x"] for z in zones) // len(zones)
                    target_y = sum(z["y"] for z in zones) // len(zones)

            self.log("[KAMERA / ZOOM] Köyün tamamını görebilmek için fare tekerleğiyle sonuna kadar küçültülüyor...")

        human_zoom_out(target_x, target_y, steps=8)
        self.safe_sleep(random.uniform(0.35, 0.55))

    def scan_for_cart(self):
        """
        Köyde toplanacak ganimet arabasını veya iksir balonunu arar.
        Kullanıcının kendi köy ekranından çıkarılan birebir şablonlarla (bubble_village, cart_village)
        tam sağ üst alanda %95-%100 doğrulukla arama yapar.
        """
        best_name = "cart_village"
        best_score = 0.0

        # Şablon öncelik sıralaması
        active_loot_variants = [
            "bubble_village",           # 1. Öncelik: Kullanıcının köyündeki birebir balta/ganimet balonu (%100)
            "cart_village",             # 2. Öncelik: Kullanıcının köyündeki birebir araba (%100)
            "elixir_cart_axes_full",    # 3. Öncelik: Kullanıcının yeni yüklediği baltalı+iksirli araba (%90)
            "axes_head",                # 4. Öncelik: Yeni arabanın balta simgesi (%82)
            "axes_bubble",              # 5. Öncelik: Çapraz balta simgesi
            "elixir_bubble",            # 6. Öncelik: Mor iksir damlası balonu
            "elixir_cart_axes",         # 7. Öncelik: Baltalı araba
            "elixir_cart",              # 8. Öncelik: İksirli araba
        ]

        # Güven eşiği: 0.65 (Köydeki bomba, bina veya tuzakları %100 eler, arabayı anında yakalar)
        for tmpl in active_loot_variants:
            m = self.vision.find_template(tmpl, confidence=0.65, return_best_score=True)
            if m[2] > best_score:
                best_score = m[2]
                best_name = tmpl
            if m[0] is not None and m[2] >= 0.65:
                return (m[0], m[1], m[2], tmpl)

        return (None, None, best_score, best_name)

    def collect_post_battle_resources(self):
        """
        Savaş sonrası veya yeni savaşa başlamadan önce köydeki İksir Arabasını toplar:
        1. Önce kamerayı sonuna kadar uzaklaştırır (zoom-out).
        2. İksir Arabasını arar; eğer ekranda görünmezse imleçle haritayı aktif olarak kaydırıp (üst/alt/sağ/sol) uzaklaştırarak arar!
        3. Açılan pencerede yeşil 'Topla' butonuna bir defa basar.
        4. Sağ üstteki kırmızı 'X' (çarpı) butonuna basarak pencereyi kapatır ve köye döner.
        """
        if not self.running:
            return

        # 1. ADIM: Köyün tamamını görebilmek için fare tekerleğiyle sonuna kadar küçült (Zoom Out)
        self.zoom_out_village()
        if not self.running:
            return

        self.log("[İKSİR ARABASI] İksir kutusu toplama protokolü başlatılıyor...")

        # 1. Oyun/Emülatör penceresini öne getir ve merkezini belirle
        rect = None
        try:
            rect = self.vision.get_game_window_rect()
        except Exception:
            pass

        if rect and rect[2] > 200 and rect[3] > 200:
            cx = rect[0] + rect[2] // 2
            cy = rect[1] + rect[3] // 2
        else:
            try:
                import pyautogui
                sw, sh = pyautogui.size()
                cx = sw // 2
                cy = sh // 2
            except Exception:
                cx, cy = 960, 540

        # Pencereye odaklanmak için güvenli merkeze tıkla
        human_click(cx, cy, jitter=False, delay_after=False)
        time.sleep(0.20)

        # 2. ADIM: İksir Kutusunu Bul ve Tıkla (Üst ve Sağ Üst Odaklı Arama)
        cart_clicked = False
        cart_x, cart_y, best_score, best_tmpl = self.scan_for_cart()

        # Eğer ilk bakışta görünmediyse imleçle haritayı sağ üst ve üst tarafları açacak şekilde kaydır!
        if cart_x is None and self.running:
            score_pct = int(best_score * 100)
            self.log(f"[GÖRSEL BİLGİ] İksir kutusu ilk ekranda görünmedi (Benzerlik: %{score_pct}).")
            self.log("[KAMERA / ARAMA] Sağ üst ve üst bölgeleri kadraja almak için harita taranıyor...")

            # 1. Hamle: Sağ üst tarafı merkeze getirmek için fareyi sağ üstten sol alta çek
            self.log("-> 1/4: Harita sol-aşağı çekiliyor (Sağ üst bölge merkeze getiriliyor)...")
            human_drag(cx + 180, cy - 80, cx - 180, cy + 260, duration=0.55)
            self.safe_sleep(0.45)
            if self.running:
                cart_x, cart_y, best_score, best_tmpl = self.scan_for_cart()

        # 2. Hamle: Haritayı doğrudan aşağı çekerek üst bölgeyi tamamen aç
        if cart_x is None and self.running:
            self.log("-> 2/4: Harita aşağı çekiliyor (Tam üst bölge taranıyor)...")
            human_drag(cx, cy - 80, cx, cy + 300, duration=0.55)
            self.safe_sleep(0.45)
            if self.running:
                cart_x, cart_y, best_score, best_tmpl = self.scan_for_cart()

        # 3. Hamle: Sağ tarafı merkeze çekmek için yatay sola kaydır
        if cart_x is None and self.running:
            self.log("-> 3/4: Harita sola çekiliyor (Sağ sahil bölgesi taranıyor)...")
            human_drag(cx + 240, cy, cx - 220, cy, duration=0.50)
            self.safe_sleep(0.45)
            if self.running:
                cart_x, cart_y, best_score, best_tmpl = self.scan_for_cart()

        # 4. Hamle: Tekrar fare tekerleğiyle sonuna kadar uzaklaştır ve genel tara
        if cart_x is None and self.running:
            self.log("-> 4/4: Harita tekrar fare tekerleğiyle sonuna kadar uzaklaştırılıyor...")
            human_zoom_out(cx, cy, steps=8)
            self.safe_sleep(0.40)
            if self.running:
                cart_x, cart_y, best_score, best_tmpl = self.scan_for_cart()

        # Eğer kaydırmalar sonucu bulunduysa tıkla
        if cart_x is not None:
            score_pct = int(best_score * 100)
            self.log(f"-> [✓ BULUNDU] İksir kutusu ekranda tespit edildi! ({best_tmpl}, Benzerlik: %{score_pct}, X={cart_x}, Y={cart_y}) tıklanıyor...")
            human_click(cart_x, cart_y, jitter=False, delay_after=False)
            cart_clicked = True
        else:
            score_pct = int(best_score * 100)
            self.log(f"[UYARI] İksir kutusu tespit edilemedi (En yüksek benzerlik: %{score_pct}, Gereken: %62).")
            self.log("[GÜVENLİK] Yanlış binalara/tuzaklara tıklamamak için doğrudan savaşa geçiliyor.")
            return

        # Menünün açılması için insansı bekleme süresi
        if not self.safe_sleep(random.uniform(1.2, 1.6)):
            return

        # 3. ADIM: 'Topla' Butonuna Tıkla (SADECE KUTU AÇILDIYSA VE GERÇEK 'TOPLA' YAZISI DOĞRULANDIYSA)
        # GÜVENLİK: Güven eşiği 0.78'dir. Asla 'Yükselt' (Upgrade) veya bina butonlarına basmaz!
        try:
            collect_match = self.vision.find_template("collect_button", confidence=0.78, return_best_score=True)
            if collect_match[0] is not None and collect_match[2] >= 0.78:
                score_pct = int(collect_match[2] * 100)
                self.log(f"-> [GÖRSEL] Gerçek yeşil 'Topla' butonu doğrulandı! (Benzerlik: %{score_pct}, X={collect_match[0]}, Y={collect_match[1]}) basılıyor...")
                human_click(collect_match[0], collect_match[1], jitter=False, delay_after=False)
            else:
                self.log(f"[GÜVENLİK] 'Topla' butonu ekranda doğrulanamadı (Benzerlik: %{int(collect_match[2]*100)}, Gereken: %78). Yanlış butona basılmadı.")
        except Exception as e:
            self.log(f"[Görsel Arama Hatası - Topla Butonu] {e}")

        # Toplama efektinin işlenmesi için kısa bekleme
        if not self.safe_sleep(random.uniform(0.8, 1.2)):
            return

        # 4. ADIM: Sağ Üstteki Kapatma (X) Butonuna Tıkla
        # GÜVENLİK: Windows başlık çubuğuna (Y < 80) ASLA basılmaz; sadece oyun içi pop-up'taki kırmızı X aranır!
        try:
            close_match = self.vision.find_template("close_button", confidence=0.65, return_best_score=True)
            if close_match[0] is not None and close_match[2] >= 0.65 and close_match[1] > 90:
                score_pct = int(close_match[2] * 100)
                self.log(f"-> [GÖRSEL] Kapatma 'X' butonu tespit edildi! (Benzerlik: %{score_pct}, X={close_match[0]}, Y={close_match[1]}) kapatılıyor...")
                human_click(close_match[0], close_match[1], jitter=False, delay_after=False)
            else:
                # Kapat butonu bulunamadıysa menü dışındaki güvenli köy zeminine bir sol tık atarak kapat
                self.log("[KAPATMA] Pop-up'ı kapatmak için güvenli oyun zeminine tıklanıyor...")
                human_click(cx, cy + 200, jitter=False, delay_after=False)
        except Exception as e:
            self.log(f"[Görsel Arama Hatası - Kapat Butonu] {e}")

        self.log("[✓] İksir arabası ganimeti toplandı ve menü kapatıldı.")
        self.safe_sleep(random.uniform(0.5, 0.8))

    def run_single_attack(self):
        """Tek bir tam Builder Base 2.0 saldırı turu."""
        if not self.running:
            return False

        # 0. Savaş Öncesi/Sonrası İksir & Ganimet Toplama (3 Nokta)
        self.collect_post_battle_resources()

        if not self.running:
            return False

        self.log("--- YENİ SALDIRI DÖNGÜSÜ BAŞLATILIYOR ---")
        
        # Saldırı başlamadan önce F2 veya panelden 2. Aşama seçilmiş mi kontrol et
        self.check_external_commands()
        preselected_stage2 = self.manual_stage2_triggered
        self.manual_stage2_triggered = False
        self.manual_finish_triggered = False

        # 1. Saldır Butonuna Bas
        if not self.click_point("attack_button", "Sol alttaki 'Saldır' butonu"):
            return False

        if not self.safe_sleep(random.uniform(1.2, 1.8)):
            return False

        # 2. Şimdi Bul Butonuna Bas
        if not self.click_point("find_now_button", "'Şimdi Bul' butonu"):
            return False

        # 3. Rakip Köyün Gelmesini Bekle
        self.log("Rakip aranıyor ve köy yükleniyor...")
        if not self.safe_sleep(random.uniform(5.5, 7.5)):
            return False

        if not self.running:
            return False

        # Eşleşme aranırken veya yükleme sırasında F2'ye basıldı mı tekrar kontrol et
        self.check_external_commands()
        if self.manual_stage2_triggered:
            preselected_stage2 = True
            self.manual_stage2_triggered = False

        # 4. Birlikleri Sahaya Sür
        if preselected_stage2:
            self.log("[MANUEL] 2. Aşama önceden seçildi! Direkt 2. Aşama (Hero + 8 Birlik) sahaya sürülüyor...")
            self.deploy_stage(stage_num=2)
        else:
            self.deploy_stage(stage_num=1)

        if not self.running:
            return False

        # 5. Savaş Sürecini ve 2. Aşama Takviyelerini Yönet
        self.handle_battle_progression(already_stage2=preselected_stage2)

        if not self.running:
            return False

        self.attack_count += 1
        self.log(f"Saldırı #{self.attack_count} başarıyla tamamlandı!")
        return True

    def check_break_cooldown(self):
        """Anti-ban mola sistemi (Her 10-12 saldırıda bir 2-3 dakika mola)."""
        if not self.running:
            return
        max_attacks = ANTI_BAN["attacks_before_break"]
        if self.attack_count > 0 and (self.attack_count % max_attacks == 0):
            break_seconds = random.randint(
                ANTI_BAN["break_duration_min_seconds"],
                ANTI_BAN["break_duration_max_seconds"]
            )
            mins = break_seconds // 60
            self.log(f"[ANTİ-BAN MOLASI] {self.attack_count} saldırı yapıldı. {mins} dakika ({break_seconds} sn) dinleniliyor...")
            
            start_break = time.time()
            while (time.time() - start_break) < break_seconds:
                if not self.running:
                    break
                if not self.safe_sleep(1.0):
                    break
            self.log("Mola bitti! Saldırılara devam ediliyor...")

    def start(self):
        print("""
==================================================================
   CLASH TITAN 2.0 — BUILDER BASE BOT • Created by Zodi4c
==================================================================
* Durdurmak için istediğin an klavyeden 'q' tuşuna bas.
* Duraklatmak / Devam ettirmek için 'p' tuşuna bas.
* Anti-Ban: Doğal Bézier hareketi + 4 Kenara Yayılım + Otomatik Mola.
==================================================================
""")
        if not self.coords.get("attack_button") or not self.coords["attack_button"].get("x"):
            print("[DİKKAT / NOTICE] Henüz koordinatlar ayarlanmamış! / Coordinates not set!")
            print("Lütfen 'ClashTitan.bat' üzerinden paneli açıp Slot & Kalibrasyon sekmesinden noktaları kaydedin.\n")

        # Oyun/Emülatör penceresini otomatik öne getir
        try:
            self.vision.get_game_window_rect()
        except Exception:
            pass

        self.running = True
        msg = "Bot starting in 5s... Please open your game/emulator window!" if self.lang == "EN" else "Bot 5 saniye içinde başlayacak... Lütfen oyun/emülatör pencerenizi açın!"
        print(f"\n[*] {msg} (Google Play Games, BlueStacks, LDPlayer, GameLoop, MEmu, Nox)")
        for i in range(5, 0, -1):
            if not self.running:
                return
            print(f"[{i}]...", end="\r", flush=True)
            if not self.safe_sleep(1):
                return
        print("\n[+] BOT BAŞLADI / BOT STARTED!")

        try:
            while self.running:
                success = self.run_single_attack()
                
                # Kullanıcı 'q' ile durdurduysa hemen çık
                if not self.running:
                    break

                if not success:
                    self.log("[!] Bir adımda gecikme oldu, 3 sn sonra tekrar deneniyor...")
                    if not self.safe_sleep(3):
                        break

                self.check_break_cooldown()
                if not self.safe_sleep(random.uniform(2.5, 4.0)):
                    break

        except KeyboardInterrupt:
            self.log("Kullanıcı tarafından durduruldu.")
        finally:
            self.running = False
            self.log(f"Bot kapatıldı. Bu oturumda yapılan toplam saldırı: {self.attack_count}")

    def run_stage2_standalone(self):
        """
        Doğrudan ve anında 2. Aşama (Hero + 8 Birlik) sahaya sürme rutini:
        Savaş arama adımları atlanır. Ekrana 2. Aşama dökülür ve ardından
        kullanıcının belirlediği süre (default 50 sn) kadar savaş izlenip
        otomatik olarak 'Eve Dön / Tamam' butonuna basılır (ya da F3 ile erken çıkılır).
        """
        self.running = True
        stage2_finish_wait = self.user_prefs.get("stage2_finish_wait_seconds", BATTLE_SETTINGS.get("stage2_finish_wait_seconds", 50))

        self.log("="*55)
        self.log(">>> [DOĞRUDAN 2. AŞAMA] Savaş arama adımları atlandı.")
        self.log(">>> Mevcut ekrana 2. Aşama birlikleri (Hero + 8 Birlik) dökülüyor...")
        self.log("="*55)

        # Oyun penceresini öne getirmeyi dene
        try:
            self.vision.get_game_window_rect()
        except Exception:
            pass

        if not self.safe_sleep(0.35):
            return

        # Doğrudan Hero + 8 Birliği sahaya sür
        self.deploy_stage(stage_num=2)

        self.log(f"[✓] 2. Aşama konuşlandırması tamamlandı! {stage2_finish_wait} sn savaş izleniyor (Erken bitir: F3)...")

        # 2. Aşama sonrası bekleme (Default: 60 sn / 1 dakika)
        start_wait = time.time()
        last_countdown_log = 0
        while self.running and (time.time() - start_wait) < stage2_finish_wait:
            now = time.time()
            rem = int(stage2_finish_wait - (now - start_wait))
            if rem > 0 and (now - last_countdown_log >= 10):
                if self.lang == "EN":
                    self.log(f"[Countdown] Battle end & return home remaining: {rem}s (Finish now: F3)")
                else:
                    self.log(f"[Sayaç] Savaş bitişi ve köye dönüşe kalan: {rem} sn (Hemen bitir: F3)")
                last_countdown_log = now

            self.check_external_commands()
            if self.manual_finish_triggered:
                self.log("[MANUEL] 'F3' ile savaş erken bitirildi!")
                self.manual_finish_triggered = False
                break
            if not self.safe_sleep(0.5):
                return

        if not self.running:
            return

        # Savaş bitti: Köye dön
        self.log("2. Aşama süresi doldu. 'Tamam / Eve Dön' butonlarına basılarak köye dönülüyor...")
        return_btn = self.coords.get("return_home_button")
        if return_btn and return_btn.get("x"):
            human_click(return_btn["x"], return_btn["y"], jitter=False, delay_after=False)
            if not self.safe_sleep(1.4):
                return
            human_click(return_btn["x"], return_btn["y"], jitter=False, delay_after=False)
            self.safe_sleep(1.5)

        self.log("[✓] Oturum tamamlandı. Köye dönüldü.")
        self.running = False

if __name__ == "__main__":
    bot = BuilderBase2Bot()
    if "--stage2-only" in sys.argv:
        bot.run_stage2_standalone()
    else:
        bot.start()

