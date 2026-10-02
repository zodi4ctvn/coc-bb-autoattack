# -*- coding: utf-8 -*-
# TR/EN lokalizasyon paketi
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

STRINGS = {
    "TR": {
        # Başlık ve Üst Bilgi
        "app_title": "CLASH TITAN 2.0 • Created by Zodi4c",
        "brand_name": " CLASH TITAN",
        "brand_sub": "Builder Base 2.0 • by Zodi4c",
        "credit_footer": "CREATED BY ZODI4C",
        "status_ready": " SİSTEM HAZIR",
        "status_busy": " SALDIRIDA...",
        "status_stopped": " DURDURULDU",
        
        # Navigasyon
        "nav_dashboard": " Kontrol Merkezi",
        "nav_calibration": " Slot & Kalibrasyon",
        "nav_settings": " Anti-Ban & Strateji",
        "nav_logs": " Canlı Terminal",
        "mouse_hud": "Fare: X={x}, Y={y}",
        
        # Dashboard - Stat Kartları
        "stat_attacks": "TAMAMLANAN SALDIRI",
        "stat_session": "OTURUM SÜRESİ",
        "stat_stealth": "STEALTH KORUMA",
        "stat_stealth_val": "DONANIM DÜZEYİ",
        
        # Dashboard - Eylemler
        "sec_autonomous": "OTONOM SALDIRI KONTROLÜ",
        "btn_start": " SAVAŞI BAŞLAT",
        "btn_stop": " ACİL DURDUR (Q)",
        "btn_stage2": " 2. AŞAMAYA GEÇ (F2)",
        "btn_finish": " SAVAŞI BİTİR (F3)",
        "hint_hotkeys": "Kısayollar: 'q' -> Durdur | 'F2' -> 2. Aşamaya Geç | 'F3' -> Savaşı Bitir",
        "sec_feed": "CANLI ETKİNLİK AKIŞI",
        "init_log": "[✓] Clash Titan 2.0 hazır. Slotları kalibre ettiysen 'Savaşı Başlat'a basabilirsin.\n",
        
        # Kalibrasyon Sekmesi
        "calib_guide": "MANUEL KALİBRASYON: İstediğin kutunun 'Kaydet' butonuna bas, fareyi oyun ekranında o noktanın üzerine götürüp [SPACE] tuşuna bas. Atamayı silmek için [DELETE] veya çöp kutusuna, iptal için [ESC] tuşuna basabilirsin.",
        "calib_troops_head": "BİRLİK & HERO YUVALARI",
        "calib_map_head": "HARİTA & OYUN BUTONLARI",
        "btn_record": " Kaydet",
        "btn_test": " Test",
        "btn_space": " SPACE BAS",
        "badge_missing": "Eksik",
        "badge_waiting": "Space: Kaydet | Del: Sil | Esc: İptal",
        
        # Slot ve Buton Adları
        "slots": {
            "hero_slot": ("Hero Simgesi", "Alt çubuktaki Savaş Makinesi kutusu"),
            "troop_slot_1": ("1. Birlik Yuvası", "Alt çubuktaki 1. birlik kutusu"),
            "troop_slot_2": ("2. Birlik Yuvası", "Alt çubuktaki 2. birlik kutusu"),
            "troop_slot_3": ("3. Birlik Yuvası", "Alt çubuktaki 3. birlik kutusu"),
            "troop_slot_4": ("4. Birlik Yuvası", "Alt çubuktaki 4. birlik kutusu"),
            "troop_slot_5": ("5. Birlik Yuvası", "Alt çubuktaki 5. birlik kutusu"),
            "troop_slot_6": ("6. Birlik Yuvası", "Alt çubuktaki 6. birlik kutusu"),
            "troop_slot_7": ("Takviye 1 (2. Aşama)", "2. köy aşamasında açılan 1. takviye"),
            "troop_slot_8": ("Takviye 2 (2. Aşama)", "2. köy aşamasında açılan 2. takviye"),
            "attack_button": ("Saldır Butonu", "Yan Köy sol alttaki 'Saldır' butonu"),
            "find_now_button": ("Şimdi Bul Butonu", "Eşleşme arama 'Şimdi Bul' butonu"),
            "deploy_zone_1": ("1. Saldırı Konumu", "Haritadaki 1. birlik/hero bırakma alanı"),
            "deploy_zone_2": ("2. Saldırı Konumu", "Haritadaki 2. birlik/hero bırakma alanı"),
            "deploy_zone_3": ("3. Saldırı Konumu", "Haritadaki 3. birlik/hero bırakma alanı"),
            "deploy_zone_4": ("4. Saldırı Konumu", "Haritadaki 4. birlik/hero bırakma alanı"),
            "deploy_zone_5": ("5. Saldırı Konumu", "Haritadaki 5. birlik/hero bırakma alanı"),
            "deploy_zone_6": ("6. Saldırı Konumu", "Haritadaki 6. birlik/hero bırakma alanı"),
            "deploy_zone_7": ("7. Saldırı Konumu", "Haritadaki 7. birlik/hero bırakma alanı"),
            "return_home_button": ("Eve Dön / Tamam", "Savaş bitince çıkan yeşil Tamam butonu"),
            "collect_elixir_1": ("1. İksir Arabası Konumu", "Köydeki İksir Arabası (Görsel algılanamazsa yedek koordinat)"),
            "collect_elixir_2": ("2. 'Topla' Butonu Konumu", "Açılan menüdeki yeşil Topla butonu (Görsel yedeği)"),
            "collect_elixir_3": ("3. Kapatma (X) Butonu", "Pencerenin sağ üstündeki kırmızı X butonu (Görsel yedeği)"),
            "zoom_out_point": ("Kamera Küçültme Odak Noktası", "Köyü küçültürken farenin üzerinde duracağı odak noktası"),
        },
        
        # Ayarlar Sekmesi - Risk ve Önerilen Ayarlar
        "card_risk_head": "ANTİ-BAN RİSK & GÜVENLİK ANALİZİ",
        "card_risk_desc": "Mevcut ayarların Supercell algoritmalarına karşı ban riskini canlı hesaplar.",
        "btn_apply_preset": " ÖNERİLEN GÜVENLİ AYARLARI UYGULA",
        "lbl_stealth_score": "GÜVENLİK SKORU",
        "lbl_risk_score": "BAN RİSKİ",
        "auto_saved_hint": "Ayarlar anlık olarak otomatik kaydedilmektedir.",
        "risk_ultra_safe": "ULTRA GÜVENLİ (Gizlilik: %{pct})",
        "risk_moderate": "ORTA DÜZEY RİSK (Gizlilik: %{pct})",
        "risk_danger": "YÜKSEK BAN RİSKİ! (Gizlilik: %{pct})",
        "risk_tip_safe": "Mükemmel Güvenlik: Tüm ayarlar ideal insan biyometriği standartlarında. Ban riski minimumdur.",
        "risk_tip_break_high": "[DİKKAT] Mola sıklığı yüksek ({freq} saldırı). Güvenlik için 8-12 saldırı önerilir.",
        "risk_tip_break_danger": "[TEHLİKE] Çok seyrek mola ({freq} saldırı). Sunucu bot bayrağı düşürebilir!",
        "risk_tip_rush": "[DİKKAT] 2. Aşama çok erken atılıyor ({delay} sn). İdeal insan temposu için 70-85 sn önerilir.",
        "risk_tip_clicks": "[DİKKAT] Yuva başına ({clicks}) tık yapılıyor. Aşırı hızlı mikro tıklamalar şüphe çekebilir.",
        "preset_applied": "[+] Önerilen Güvenli Ayarlar uygulandı (Mola: 10, Aşama 2: 75s, Dönüş: 50s, Tık: 4, Mod: OTO).",
        
        # Ayarlar Sekmesi - Parametreler
        "card_break_head": "ANTİ-BAN MOLA ALGORİTMASI",
        "card_break_desc": "Supercell'in davranış tespit sistemini atlatmak için bot belirli aralıklarla insani mola verir.",
        "slider_break_title": "Kaç Saldırıda Bir Mola Versin?",
        "card_battle_head": "SAVAŞ & AŞAMA PARAMETRELERİ",
        "card_battle_desc": "1. aşama ve 2. aşama takviyelerinin sahaya sürülme zamanlamalarını yönetin.",
        "slider_stage2_title": "1. Aşama Bitişi / 2. Aşamaya Otomatik Geçiş Süresi:",
        "slider_stage2_finish_title": "2. Aşama Atıldıktan Sonra Kaç Saniye Sonra Dönsün?",
        "slider_clicks_title": "Her Birlik Yuvası İçin Haritaya Kaç Tık Yapılsın?",
        "lbl_stage2_mode": "2. Aşamaya Geçiş Tercihi:",
        "mode_auto": "OTOMATİK (Süreyle)",
        "mode_manual": "MANUEL (Sadece F2 / Tıkla)",
        "card_theme_head": "ÖZEL MENÜ & TİPOGRAFİ TEMASI",
        "card_theme_desc": "Menü, buton ve başlıkların yazı karakterini kendi zevkinize göre anında değiştirin.",
        "lbl_font_pack": "Yazı Tipi Paketi:",
        "card_color_head": "RENK TEMASI & NEON STİLİ",
        "card_color_desc": "Kontrol panelinin ana vurgu rengini, neon ışıklandırmalarını ve kart efektlerini değiştirin.",
        "lbl_color_choice": "Aktif Renk Teması:",
        "banner_dashboard_title": "OTONOM SAVAŞ ÜSSÜ • CLASH TITAN 2.0",
        "banner_dashboard_desc": "Builder Base 2.0 İki Aşamalı Gece Köyü Donanım Düzeyinde Harp Modülü",
        "banner_calib_title": "TAKTİK HARİTA & SLOT KOORDİNAT MERKEZİ",
        "banner_calib_desc": "Tüm emülatörler için hassas piksel hedefleme ve donanım tıklama haritası",
        "card_lang_head": "DİL & BÖLGE SEÇİMİ (LANGUAGE)",
        "card_lang_desc": "Arayüz dilini anında Türkçe veya İngilizce olarak değiştirin.",
        "lbl_lang_choice": "Aktif Dil:",
        "btn_save_config": " AYARLARI KAYDET VE UYGULA",
        "unit_attacks": "Saldırı",
        "unit_seconds": "Saniye",
        "unit_clicks": "Tıklama",
        
        # Loglar Sekmesi
        "sec_full_log": "TAM SALDIRI VE HATA GÜNLÜĞÜ",
        "btn_clear": "Temizle",
        "log_cleared": "[i] Günlük temizlendi.\n",
        
        # Mesajlar & Eksik Kalibrasyon Uyarısı
        "msg_saved": "[✓] Ayarlar Güncellendi: 2. Aşama Modu={mode}, Mola Sıklığı={break_freq} saldırı, Gecikme={delay} sn",
        "msg_recorded": "[✓] Kaydedildi: {key} -> (X: {x}, Y: {y})",
        "msg_cancelled": "[i] İptal edildi: {key}",
        "msg_slot_deleted": "[-] Tuş ataması silindi: {name} (Eksik olarak işaretlendi)",
        "msg_stage2_cmd": "[MANUEL] 2. Aşama komutu gönderildi (Takviyeler atılıyor...)",
        "msg_finish_cmd": "[MANUEL] Savaş bitirme komutu gönderildi (Eve dönülüyor...)",
        "calib_missing_title": "EKSİK TUŞ ATAMALARI",
        "calib_missing_header": "SAVAŞ BAŞLATILAMAZ!",
        "calib_missing_body": "Savaş motorunun sorunsuz ve ban riski olmadan çalışabilmesi için tüm 16 tuş atamasının yapılması zorunludur.\n\nEksik Kalan Noktalar ({count} adet):",
        "btn_calib_now": "ANLADIM, ŞİMDİ KALİBRE ET",
        "log_missing_slots": "[!] SAVAŞ BAŞLATILAMADI: {count} adet eksik tuş ataması var! Lütfen tüm slotları kalibre edin.",
        "calib_status_ready": "[✓] Tüm 16 tuş ataması yapıldı. Savaşa hazır.",
        "calib_status_missing": "[!] {count} adet eksik tuş ataması var. Başlatmadan önce kalibre edin.",
    },
    
    "EN": {
        # Title and Header
        "app_title": "CLASH TITAN 2.0 • Created by Zodi4c",
        "brand_name": " CLASH TITAN",
        "brand_sub": "Builder Base 2.0 • by Zodi4c",
        "credit_footer": "CREATED BY ZODI4C",
        "status_ready": " SYSTEM READY",
        "status_busy": " ATTACKING...",
        "status_stopped": " STOPPED",
        
        # Navigation
        "nav_dashboard": " Control Dashboard",
        "nav_calibration": " Slots & Calibration",
        "nav_settings": " Anti-Ban & Strategy",
        "nav_logs": " Live Terminal",
        "mouse_hud": "Mouse: X={x}, Y={y}",
        
        # Dashboard - Stat Cards
        "stat_attacks": "COMPLETED ATTACKS",
        "stat_session": "SESSION TIME",
        "stat_stealth": "STEALTH PROTECTION",
        "stat_stealth_val": "HARDWARE LEVEL",
        
        # Dashboard - Actions
        "sec_autonomous": "AUTONOMOUS ATTACK CONTROL",
        "btn_start": " START BATTLE",
        "btn_stop": " EMERGENCY STOP (Q)",
        "btn_stage2": " TRIGGER STAGE 2 (F2)",
        "btn_finish": " FINISH BATTLE (F3)",
        "hint_hotkeys": "Hotkeys: 'q' -> Stop | 'F2' -> Stage 2 | 'F3' -> Finish Battle",
        "sec_feed": "LIVE EVENT FEED",
        "init_log": "[✓] Clash Titan 2.0 ready. Calibrate slots and click 'Start Battle'.\n",
        
        # Calibration Tab
        "calib_guide": "MANUAL CALIBRATION: Click 'Record' on any slot, hover over the game target and press [SPACE] to save. Press [DELETE] or trash icon to clear/remove assignment, or [ESC] to cancel.",
        "calib_troops_head": "HERO & TROOP SLOTS",
        "calib_map_head": "MAP & GAME BUTTONS",
        "btn_record": " Record",
        "btn_test": " Test",
        "btn_space": " PRESS SPACE",
        "badge_missing": "Missing",
        "badge_waiting": "Space: Save | Del: Clear | Esc: Cancel",
        
        # Slot and Button Names
        "slots": {
            "hero_slot": ("Hero Slot", "Battle Machine slot on bottom bar"),
            "troop_slot_1": ("Troop Slot 1", "Troop box 1 on bottom bar"),
            "troop_slot_2": ("Troop Slot 2", "Troop box 2 on bottom bar"),
            "troop_slot_3": ("Troop Slot 3", "Troop box 3 on bottom bar"),
            "troop_slot_4": ("Troop Slot 4", "Troop box 4 on bottom bar"),
            "troop_slot_5": ("Troop Slot 5", "Troop box 5 on bottom bar"),
            "troop_slot_6": ("Troop Slot 6", "Troop box 6 on bottom bar"),
            "troop_slot_7": ("Reinforcement 1 (Stage 2)", "Stage 2 reinforcement slot 1"),
            "troop_slot_8": ("Reinforcement 2 (Stage 2)", "Stage 2 reinforcement slot 2"),
            "attack_button": ("Attack Button", "Bottom-left 'Attack' button in Builder Base"),
            "find_now_button": ("Find Now Button", "Matchmaking 'Find Now' button"),
            "deploy_zone_1": ("Attack Zone 1", "Map deploy position 1 for troop/hero"),
            "deploy_zone_2": ("Attack Zone 2", "Map deploy position 2 for troop/hero"),
            "deploy_zone_3": ("Attack Zone 3", "Map deploy position 3 for troop/hero"),
            "deploy_zone_4": ("Attack Zone 4", "Map deploy position 4 for troop/hero"),
            "deploy_zone_5": ("Attack Zone 5", "Map deploy position 5 for troop/hero"),
            "deploy_zone_6": ("Attack Zone 6", "Map deploy position 6 for troop/hero"),
            "deploy_zone_7": ("Attack Zone 7", "Map deploy position 7 for troop/hero"),
            "return_home_button": ("Return Home / OK", "Green 'OK / Return Home' button at battle end"),
            "collect_elixir_1": ("1. Elixir Cart Location", "Village Elixir Cart (Backup coordinate if visual fails)"),
            "collect_elixir_2": ("2. 'Collect' Button Location", "Green Collect button in popup (Backup coordinate)"),
            "collect_elixir_3": ("3. Close (X) Button", "Red X button in popup top-right (Backup coordinate)"),
            "zoom_out_point": ("Zoom-Out Anchor Point", "Pivot point where mouse rests while zooming out village"),
        },
        
        # Settings Tab - Risk & Recommended Settings
        "card_risk_head": "ANTI-BAN RISK & STEALTH ANALYZER",
        "card_risk_desc": "Real-time AI calculation of configuration safety against Supercell server algorithms.",
        "btn_apply_preset": " APPLY RECOMMENDED STEALTH PRESET",
        "lbl_stealth_score": "STEALTH RATING",
        "lbl_risk_score": "BAN RISK",
        "auto_saved_hint": "Settings are saved automatically in real-time.",
        "risk_ultra_safe": "ULTRA STEALTH (Safety: %{pct})",
        "risk_moderate": "MODERATE RISK (Safety: %{pct})",
        "risk_danger": "HIGH BAN RISK! (Safety: %{pct})",
        "risk_tip_safe": "Optimal Protection: All parameters match ideal human biometrics. Ban risk is minimal.",
        "risk_tip_break_high": "[NOTICE] Break interval is high ({freq} attacks). 8-12 attacks recommended.",
        "risk_tip_break_danger": "[CRITICAL] Extremely long sessions without breaks ({freq} attacks). Bot flagging risk!",
        "risk_tip_rush": "[NOTICE] Stage 2 triggered too early ({delay}s). Human pacing is typically 70-85s.",
        "risk_tip_clicks": "[NOTICE] ({clicks}) clicks per slot. Rapid repetitive micro-clicks may look suspicious.",
        "preset_applied": "[+] Recommended Stealth Preset applied (Break: 10, Stage 2: 75s, Return: 50s, Clicks: 4, Mode: AUTO).",

        # Settings Tab - Parameters
        "card_break_head": "ANTI-BAN BREAK ALGORITHM",
        "card_break_desc": "Prevents behavioral detection by taking human-like pauses between attack clusters.",
        "slider_break_title": "Attacks Before Cool-down Break?",
        "card_battle_head": "BATTLE & STAGE PARAMETERS",
        "card_battle_desc": "Configure timings and troop deployment pacing for Stage 1 & 2.",
        "slider_stage2_title": "Stage 1 End / Stage 2 Auto Transition Delay:",
        "slider_stage2_finish_title": "Wait Duration After Stage 2 Deploy Before Return:",
        "slider_clicks_title": "Deploy Clicks Per Troop Slot:",
        "lbl_stage2_mode": "Stage 2 Deployment Trigger:",
        "mode_auto": "AUTOMATIC (Timer)",
        "mode_manual": "MANUAL (F2 / Click Only)",
        "card_theme_head": "CUSTOM MENU & TYPOGRAPHY THEME",
        "card_theme_desc": "Instantly switch UI font themes between Tactical, Cyber, and Minimal.",
        "lbl_font_pack": "Font Theme:",
        "card_color_head": "COLOR THEME & NEON STYLE",
        "card_color_desc": "Instantly switch UI accent colors, neon glows, and card highlighting effects.",
        "lbl_color_choice": "Active Color Theme:",
        "banner_dashboard_title": "AUTONOMOUS WAR DECK • CLASH TITAN 2.0",
        "banner_dashboard_desc": "Builder Base 2.0 Dual-Stage Autonomous Hardware-Level Combat Deck",
        "banner_calib_title": "TACTICAL RADAR & SLOT COORDINATE DECK",
        "banner_calib_desc": "Sub-pixel targeting and hardware input mapping for all emulators",
        "card_lang_head": "LANGUAGE & LOCALIZATION",
        "card_lang_desc": "Instantly switch user interface language between English and Turkish.",
        "lbl_lang_choice": "Active Language:",
        "btn_save_config": " SAVE & APPLY SETTINGS",
        "unit_attacks": "Attacks",
        "unit_seconds": "Seconds",
        "unit_clicks": "Clicks",
        
        # Logs Tab
        "sec_full_log": "FULL BATTLE & EVENT LOG",
        "btn_clear": "Clear",
        "log_cleared": "[i] Log cleared.\n",
        
        # Messages & Missing Calibration Warning
        "msg_saved": "[✓] Settings Updated: Stage 2 Mode={mode}, Break Frequency={break_freq} attacks, Delay={delay}s",
        "msg_recorded": "[✓] Saved: {key} -> (X: {x}, Y: {y})",
        "msg_cancelled": "[i] Cancelled: {key}",
        "msg_slot_deleted": "[-] Slot assignment cleared: {name} (Marked as missing)",
        "msg_stage2_cmd": "[MANUAL] Stage 2 command sent (Deploying reinforcements...)",
        "msg_finish_cmd": "[MANUAL] Finish battle command sent (Returning home...)",
        "calib_missing_title": "MISSING KEY ASSIGNMENTS",
        "calib_missing_header": "CANNOT START BATTLE!",
        "calib_missing_body": "All 16 key slots must be calibrated to ensure flawless and anti-ban safe execution.\n\nMissing Slots ({count}):",
        "btn_calib_now": "UNDERSTOOD, CALIBRATE NOW",
        "log_missing_slots": "[!] CANNOT START BATTLE: {count} missing slot coordinates! Please calibrate all slots first.",
        "calib_status_ready": "[✓] All 16 slots assigned. Ready for battle.",
        "calib_status_missing": "[!] {count} missing slot coordinates. Calibrate before starting.",
    }
}

ACTIVE_LANG = "TR"

def get_text(key, lang=None, **kwargs):
    l = lang or ACTIVE_LANG
    s = STRINGS.get(l, STRINGS["TR"]).get(key, key)
    if isinstance(s, str) and kwargs:
        return s.format(**kwargs)
    return s

def get_slot_info(slot_key, lang=None):
    l = lang or ACTIVE_LANG
    slots = STRINGS.get(l, STRINGS["TR"]).get("slots", {})
    return slots.get(slot_key, (slot_key, ""))

