# -*- coding: utf-8 -*-
# Kontrol paneli - CustomTkinter tabanli GUI
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

import sys
import os
import time
import json
import threading
import subprocess
import pyautogui
pyautogui.PAUSE = 0.0        # default 0.1 → Tk event loop'unu bloke etmesin
pyautogui.FAILSAFE = False   # sol üst köşe acil dur kapalı
import keyboard
import webbrowser
import ctypes

import customtkinter as ctk

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def register_application_fonts():
    """
    Windows GDI Font Kaydı:
    assets/fonts/ dizinindeki tüm TrueType/OpenType fontları (Rajdhani, Orbitron, Outfit)
    Windows oturumunda kayıt eder (FR_PRIVATE | 0).
    Bu sayede Tkinter ve CustomTkinter sistem fontu gibi doğrudan render eder.
    """
    if sys.platform.startswith("win"):
        try:
            import ctypes
            fonts_dir = os.path.join(BASE_DIR, "assets", "fonts")
            if os.path.isdir(fonts_dir):
                for fname in os.listdir(fonts_dir):
                    if fname.lower().endswith((".ttf", ".otf")):
                        fpath = os.path.abspath(os.path.join(fonts_dir, fname))
                        ctypes.windll.gdi32.AddFontResourceExW(fpath, 0x10, 0)
        except Exception:
            pass

register_application_fonts()

import icons
import locales
from locales import get_text, get_slot_info
from human_mouse import human_click, fast_human_move
from setup_wizard import load_coordinates, save_coordinates
from config import ANTI_BAN, BATTLE_SETTINGS, DEFAULT_LANGUAGE
from vision import VisionDetector

PYTHON_EXE = sys.executable
SETTINGS_FILE = os.path.join(BASE_DIR, "user_settings.json")
CMD_FILE = os.path.join(BASE_DIR, "bot_command.txt")
BOT_SCRIPT = os.path.join(BASE_DIR, "bot.py")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# CTk ScalingTracker: her 100ms DPI kontrolü + alpha flicker = sürükleme lag'i
# Devre dışı bırak — tek monitör/sabit DPI için gerekli değil
ctk.deactivate_automatic_dpi_awareness = True

HERO_AND_TROOPS = [
    "hero_slot",
    "troop_slot_1",
    "troop_slot_2",
    "troop_slot_3",
    "troop_slot_4",
    "troop_slot_5",
    "troop_slot_6",
    "troop_slot_7",
    "troop_slot_8",
]

MAP_AND_NAV = [
    "attack_button",
    "find_now_button",
    "deploy_zone_1",
    "deploy_zone_2",
    "deploy_zone_3",
    "deploy_zone_4",
    "deploy_zone_5",
    "deploy_zone_6",
    "deploy_zone_7",
    "return_home_button",
    "zoom_out_point",
    "collect_elixir_1",
    "collect_elixir_2",
    "collect_elixir_3",
]

OPTIONAL_SLOTS = {"zoom_out_point", "collect_elixir_1", "collect_elixir_2", "collect_elixir_3"}

COLOR_THEMES = {
    "Obsidian Emerald": {
        "name_tr": "Zümrüt Yeşili (Obsidian Emerald)",
        "name_en": "Obsidian Emerald (Green)",
        "accent": "#10b981",
        "accent_hover": "#059669",
        "accent_dark": "#064e3b",
        "accent_light": "#34d399",
        "accent_text": "#ffffff",
        "card_border": "#10b981",
    },
    "Cyber Violet": {
        "name_tr": "Siber Neon Mor (Cyber Violet)",
        "name_en": "Cyber Violet (Neon Purple)",
        "accent": "#a855f7",
        "accent_hover": "#9333ea",
        "accent_dark": "#581c87",
        "accent_light": "#c084fc",
        "accent_text": "#ffffff",
        "card_border": "#a855f7",
    },
    "Crimson Titan": {
        "name_tr": "Kızıl Titanyum (Crimson Titan)",
        "name_en": "Crimson Titan (Red)",
        "accent": "#ef4444",
        "accent_hover": "#dc2626",
        "accent_dark": "#7f1d1d",
        "accent_light": "#f87171",
        "accent_text": "#ffffff",
        "card_border": "#351520",
        "glow": "#ef4444",
    },
    "Abyssal Gold": {
        "name_tr": "Altın İmparatorluk (Abyssal Gold)",
        "name_en": "Abyssal Gold (Amber)",
        "accent": "#f59e0b",
        "accent_hover": "#d97706",
        "accent_dark": "#78350f",
        "accent_light": "#fbbf24",
        "accent_text": "#ffffff",
        "card_border": "#f59e0b",
    },
    "Glacier Frost": {
        "name_tr": "Kutup Mavisi (Glacier Frost)",
        "name_en": "Glacier Frost (Cyan)",
        "accent": "#06b6d4",
        "accent_hover": "#0891b2",
        "accent_dark": "#164e63",
        "accent_light": "#22d3ee",
        "accent_text": "#ffffff",
        "card_border": "#06b6d4",
    },
}
DEFAULT_COLOR_THEME = "Crimson Titan"

def load_user_settings():
    defaults = {
        "language": DEFAULT_LANGUAGE,
        "font_theme": "Minimalist Lüks (Outfit)",
        "color_theme": DEFAULT_COLOR_THEME,
        "attacks_before_break": ANTI_BAN.get("attacks_before_break", 11),
        "stage2_wait_seconds": BATTLE_SETTINGS.get("stage2_wait_seconds", 75),
        "stage2_finish_wait_seconds": BATTLE_SETTINGS.get("stage2_finish_wait_seconds", 50),
        "clicks_per_troop_slot": BATTLE_SETTINGS.get("clicks_per_troop_slot", 4),
        "stage2_mode": BATTLE_SETTINGS.get("stage2_mode", "AUTO"),
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                defaults.update(data)
        except Exception:
            pass

    ANTI_BAN["attacks_before_break"] = int(defaults.get("attacks_before_break", 11))
    BATTLE_SETTINGS["stage2_wait_seconds"] = int(defaults.get("stage2_wait_seconds", 75))
    BATTLE_SETTINGS["stage2_finish_wait_seconds"] = int(defaults.get("stage2_finish_wait_seconds", 50))
    BATTLE_SETTINGS["clicks_per_troop_slot"] = int(defaults.get("clicks_per_troop_slot", 4))
    BATTLE_SETTINGS["stage2_mode"] = defaults.get("stage2_mode", "AUTO")
    return defaults

def save_user_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

def calculate_ban_risk(break_freq, stage2_delay, clicks, mode, lang="TR"):
    """
    Ban riskini (0 - 100) ve güvenlik seviyesini dinamik hesaplar.
    Dönüş: (risk_pct, safety_pct, color, status_text, advice_text)
    """
    risk = 4
    warnings = []

    # 1. Mola Sıklığı
    if break_freq <= 10:
        pass
    elif break_freq <= 13:
        risk += 8
    elif break_freq <= 16:
        risk += 22
        warnings.append(get_text("risk_tip_break_high", lang, freq=break_freq))
    else:
        risk += 48
        warnings.append(get_text("risk_tip_break_danger", lang, freq=break_freq))

    # 2. 2. Aşama Gecikmesi
    if 70 <= stage2_delay <= 100:
        pass
    elif stage2_delay < 60:
        risk += 26
        warnings.append(get_text("risk_tip_rush", lang, delay=stage2_delay))
    elif stage2_delay < 70:
        risk += 12
    elif stage2_delay > 120:
        risk += 6

    # 3. Yuva Başına Tıklama (1: Tekli birlikler/Pekka/Dev, 3-4: Okçu vb., 5+: Yüksek adetli birlikler)
    if clicks in (1, 2, 3, 4):
        pass
    elif clicks == 5:
        risk += 8
    elif clicks >= 6:
        risk += 16
        warnings.append(get_text("risk_tip_clicks", lang, clicks=clicks))

    risk = max(2, min(95, risk))
    safety = 100 - risk

    if risk <= 20:
        color = "#10b981"
        status_text = get_text("risk_ultra_safe", lang, pct=safety)
        advice_text = get_text("risk_tip_safe", lang)
    elif risk <= 45:
        color = "#f59e0b"
        status_text = get_text("risk_moderate", lang, pct=safety)
        advice_text = " • ".join(warnings) if warnings else get_text("risk_tip_safe", lang)
    else:
        color = "#ef4444"
        status_text = get_text("risk_danger", lang, pct=safety)
        advice_text = " • ".join(warnings) if warnings else get_text("risk_tip_safe", lang)

    return risk, safety, color, status_text, advice_text


class LuxuryBotDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.user_prefs = load_user_settings()
        self.lang = self.user_prefs.get("language", DEFAULT_LANGUAGE)
        locales.ACTIVE_LANG = self.lang

        self.title(get_text("app_title", self.lang))
        self.geometry("980x720")
        self.minsize(960, 670)
        # Sabit Tipografi: Minimalist Lüks (Outfit)
        self.font_brand_name = "Outfit"
        self.font_nav_name = "Outfit"
        self.font_body_name = "Outfit"

        # Tipografi Hiyerarşisi
        self.f_brand = ctk.CTkFont(family=self.font_brand_name, size=18, weight="bold")
        self.f_brand_sub = ctk.CTkFont(family=self.font_nav_name, size=11, weight="bold")
        self.f_status = ctk.CTkFont(family=self.font_nav_name, size=13, weight="bold")
        self.f_nav = ctk.CTkFont(family=self.font_nav_name, size=14, weight="bold")
        self.f_card_head = ctk.CTkFont(family=self.font_nav_name, size=12, weight="bold")
        self.f_card_val = ctk.CTkFont(family=self.font_brand_name, size=22, weight="bold")
        self.f_sec_head = ctk.CTkFont(family=self.font_nav_name, size=14, weight="bold")
        self.f_btn_main = ctk.CTkFont(family=self.font_nav_name, size=15, weight="bold")
        self.f_btn_sub = ctk.CTkFont(family=self.font_nav_name, size=13, weight="bold")
        self.f_btn_small = ctk.CTkFont(family=self.font_nav_name, size=12, weight="bold")
        self.f_row_name = ctk.CTkFont(family=self.font_nav_name, size=13, weight="bold")
        self.f_body = ctk.CTkFont(family=self.font_body_name, size=12)
        self.f_hint = ctk.CTkFont(family=self.font_body_name, size=11)
        self.f_mono = ctk.CTkFont(family="Consolas", size=11, weight="bold")

        self.coords = load_coordinates()
        self.bot_process = None
        self.recording_key = None
        self.attack_counter = 0
        self.session_start = None
        self.active_color_theme = "Crimson Titan"
        self.colors = COLOR_THEMES["Crimson Titan"]

        # Görüntü İşleme & Şablon Dedektörü
        self.vision = VisionDetector()

        # Banner Görsellerini Yükle
        self.img_battle_banner = None
        self.img_village_banner = None
        self.load_banner_assets()

        self.coord_badges = {}
        self.record_buttons = {}
        self.test_buttons = {}
        self.row_labels = {}
        self.row_desc_labels = {}

        # İkon önbelleği (Normal ve Aktif)
        self.nav_icons_normal = {
            "dashboard": icons.get_dashboard_icon("#94a3b8"),
            "calibration": icons.get_target_icon("#94a3b8"),
            "settings": icons.get_shield_icon("#94a3b8"),
            "logs": icons.get_terminal_icon("#94a3b8")
        }
        self.nav_icons_active = {
            "dashboard": icons.get_dashboard_icon("#ffffff"),
            "calibration": icons.get_target_icon("#ffffff"),
            "settings": icons.get_shield_icon("#ffffff"),
            "logs": icons.get_terminal_icon("#ffffff")
        }
        self.icon_dashboard = self.nav_icons_normal["dashboard"]
        self.icon_target = self.nav_icons_normal["calibration"]
        self.icon_shield = self.nav_icons_normal["settings"]
        self.icon_terminal = self.nav_icons_normal["logs"]

        self.icon_play = icons.get_play_icon(self.colors["accent_text"])
        self.icon_stop = icons.get_stop_icon("#ffffff")
        self.icon_forward = icons.get_fast_forward_icon("#ffffff")
        self.icon_flag = icons.get_flag_icon("#ffffff")
        self.icon_pin = icons.get_pin_icon("#f8fafc")
        self.icon_test = icons.get_target_icon("#94a3b8", size=(14, 14))
        self.icon_trash = icons.get_trash_icon("#94a3b8", size=(14, 14))
        self.hovered_slot_key = None

        self.status_dot_ready = icons.get_status_dot(self.colors["accent"])
        self.status_dot_busy = icons.get_status_dot("#38bdf8")
        self.status_dot_stop = icons.get_status_dot("#ef4444")

        self.build_ui()
        self.update_calib_status_label()
        self.bind("<Escape>", lambda event: self.handle_esc_press())
        self.bind("<Delete>", lambda event: self.handle_delete_press())
        self.bind("<BackSpace>", lambda event: self.handle_delete_press())
        self.bind("<F2>", lambda event: self.send_stage2_command())
        self.bind("<F3>", lambda event: self.send_finish_command())
        self.start_global_hotkey_listener()
        self.update_clock_loop()

    def start_global_hotkey_listener(self):
        """
        Global Windows donanım dinleyicisi:
        Panel arka plandayken veya oyundayken dahi F2 (2. Aşama) ve F3 (Savaşı Bitir)
        tuşlarını yakalar ve ilgili eylemleri anında tetikler.
        """
        def listener():
            user32 = ctypes.windll.user32
            while True:
                try:
                    # Sadece kalibrasyon kaydı yapılmıyorken dinle
                    if not self.recording_key:
                        # 0x71 = VK_F2
                        if bool(user32.GetAsyncKeyState(0x71) & 0x8000):
                            self.after(0, self.send_stage2_command)
                            time.sleep(0.45)
                        # 0x72 = VK_F3
                        elif bool(user32.GetAsyncKeyState(0x72) & 0x8000):
                            self.after(0, self.send_finish_command)
                            time.sleep(0.45)
                except Exception:
                    pass
                time.sleep(0.03)

        threading.Thread(target=listener, daemon=True).start()

    def load_banner_assets(self):
        """Builder Base 2.0 ve Gece Köyü Banner Görsellerini Pillow ile yükler."""
        if not HAS_PIL:
            return

        try:
            battle_path = os.path.join(BASE_DIR, "assets", "images", "battle_banner.jpg")
            if os.path.exists(battle_path):
                raw_battle = Image.open(battle_path)
                self.img_battle_banner = ctk.CTkImage(
                    light_image=raw_battle,
                    dark_image=raw_battle,
                    size=(670, 95)
                )
        except Exception as e:
            print("Battle banner load error:", e)

        try:
            village_path = os.path.join(BASE_DIR, "assets", "images", "village_banner.jpg")
            if os.path.exists(village_path):
                raw_village = Image.open(village_path)
                self.img_village_banner = ctk.CTkImage(
                    light_image=raw_village,
                    dark_image=raw_village,
                    size=(670, 95)
                )
        except Exception as e:
            print("Village banner load error:", e)

    def set_color_theme(self, theme_key):
        """
        Kullanıcı arayüzünün renk temasını anında değiştirir, tüm butonları,
        ışıkları, neon kenarlıkları ve durum rozetlerini yeniden boyar ve kaydeder.
        """
        if theme_key not in COLOR_THEMES:
            return

        self.active_color_theme = theme_key
        self.colors = COLOR_THEMES[theme_key]
        self.user_prefs["color_theme"] = theme_key
        save_user_settings(self.user_prefs)

        # 1. Sidebar Brand ve Butonlar
        self.brand_lbl.configure(image=icons.get_brand_icon(self.colors["accent"], size=(22, 22)))
        self.creator_badge.configure(text_color=self.colors["accent"])
        self.seg_lang.configure(selected_color=self.colors["accent"], selected_hover_color=self.colors["accent_hover"])

        # 2. Durum Rozeti ve İkonları
        self.status_dot_ready = icons.get_status_dot(self.colors["accent"])
        if not self.bot_process:
            self.status_indicator.configure(image=self.status_dot_ready, text_color=self.colors["accent_light"])

        # 3. Ana Savaş Başlat Butonu
        self.icon_play = icons.get_play_icon(self.colors["accent_text"])
        if hasattr(self, "btn_main_start"):
            if not self.bot_process:
                self.btn_main_start.configure(
                    fg_color=self.colors["accent"],
                    hover_color=self.colors["accent_hover"],
                    text_color=self.colors["accent_text"],
                    image=self.icon_play
                )

        # 4. Aktif Navigasyon Sekmesi Rengi
        for tid, btn in self.nav_buttons.items():
            if btn.cget("fg_color") != "transparent":
                btn.configure(
                    fg_color=self.colors["accent"],
                    hover_color=self.colors["accent_hover"],
                    text_color="#ffffff",
                    image=self.nav_icons_active.get(tid)
                )

        # 5. Stat Kartı Vurgusu
        if hasattr(self, "card_attacks") and hasattr(self.card_attacks, "value_label"):
            self.card_attacks.value_label.configure(text_color=self.colors["accent"])

        # 6. Banner Kartları Vurgusu
        if hasattr(self, "banner_dash_title"):
            self.banner_dash_title.configure(text_color=self.colors["accent_light"])
        if hasattr(self, "banner_calib_title"):
            self.banner_calib_title.configure(text_color=self.colors["accent_light"])

        # 7. Ayarlar Sekmesi Temaları
        if hasattr(self, "seg_lang_settings"):
            self.seg_lang_settings.configure(selected_color=self.colors["accent"], selected_hover_color=self.colors["accent_hover"])

        # 8. Risk Barı ve Kalibrasyon Durum Metni
        self.update_risk_meter()
        self.update_calib_status_label()

        theme_display = self.colors.get("name_tr" if self.lang == "TR" else "name_en", theme_key)
        self.append_log(f"[✓] Renk teması uygulandı: {theme_display}")

    def build_ui(self):
        # Sol Menü (Sidebar) - Derin Kömür / Taktik HUD Menü
        self.sidebar = ctk.CTkFrame(self, width=224, corner_radius=0, fg_color="#0d0f16", border_width=1, border_color="#181a24")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / Başlık
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(18, 12))

        self.brand_lbl = ctk.CTkLabel(
            brand_frame,
            text="CLASH TITAN",
            image=icons.get_brand_icon("#ef4444", size=(24, 24)),
            compound="left",
            font=self.f_brand,
            text_color="#ffffff"
        )
        self.brand_lbl.pack(anchor="w")

        self.brand_sub = ctk.CTkLabel(
            brand_frame,
            text="BUILDER BASE 2.0 • HUD",
            font=self.f_brand_sub,
            text_color="#f87171"
        )
        self.brand_sub.pack(anchor="w", pady=(1, 0), padx=(32, 0))

        # Durum Kartı (Sidebar)
        self.status_card = ctk.CTkFrame(self.sidebar, fg_color="#160e14", corner_radius=10, border_width=1, border_color="#33121d")
        self.status_card.pack(fill="x", padx=12, pady=(0, 14))

        self.status_dot_ready = icons.get_status_dot(self.colors["accent"])
        self.status_dot_busy = icons.get_status_dot("#38bdf8")
        self.status_dot_stop = icons.get_status_dot("#ef4444")

        self.status_indicator = ctk.CTkLabel(
            self.status_card,
            text=get_text("status_ready", self.lang),
            image=self.status_dot_ready,
            compound="left",
            font=self.f_status,
            text_color="#fca5a5"
        )
        self.status_indicator.pack(pady=7)

        # Navigasyon Butonları
        self.nav_buttons = {}
        self.nav_items_data = [
            ("dashboard", "nav_dashboard", "dashboard"),
            ("calibration", "nav_calibration", "calibration"),
            ("settings", "nav_settings", "settings"),
            ("logs", "nav_logs", "logs")
        ]

        for tab_id, text_key, icon_key in self.nav_items_data:
            btn = ctk.CTkButton(
                self.sidebar,
                text=get_text(text_key, self.lang),
                image=self.nav_icons_normal[icon_key],
                compound="left",
                font=self.f_nav,
                fg_color="transparent",
                text_color="#8892b0",
                hover_color="#161822",
                anchor="w",
                height=42,
                corner_radius=10,
                command=lambda tid=tab_id: self.switch_tab(tid)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[tab_id] = btn

        # Alt Bilgi & Dual-Segmented Pill (Örnek Tasarımdaki [ Basic | Advanced ] tarzı dil ve mod seçici)
        sidebar_bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sidebar_bottom.pack(side="bottom", fill="x", padx=12, pady=16)

        self.seg_lang = ctk.CTkSegmentedButton(
            sidebar_bottom,
            values=["TR", "EN"],
            font=self.f_btn_small,
            selected_color="#dc2626",
            selected_hover_color="#ef4444",
            unselected_color="#121520",
            unselected_hover_color="#1c202e",
            text_color="#ffffff",
            corner_radius=10,
            height=30,
            command=self.set_language
        )
        self.seg_lang.set(self.lang)
        self.seg_lang.pack(fill="x", pady=(0, 10))

        self.creator_badge = ctk.CTkButton(
            sidebar_bottom,
            text="CREATED BY ZODI4C",
            font=self.f_brand_sub,
            text_color="#f87171",
            fg_color="transparent",
            hover_color="#1c1117",
            height=24,
            corner_radius=8,
            command=lambda: webbrowser.open_new_tab("https://github.com/Zodi4ctvn")
        )
        self.creator_badge.pack(fill="x")

        # Sağ İçerik Alanı
        self.content_area = ctk.CTkFrame(self, fg_color="#090a0f", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True, padx=16, pady=16)

        # Sekme Gövdeleri
        self.frames = {
            "dashboard": self.build_dashboard_tab(),
            "calibration": self.build_calibration_tab(),
            "settings": self.build_settings_tab(),
            "logs": self.build_logs_tab()
        }

        self.switch_tab("dashboard")

    def switch_tab(self, tab_id):
        self.active_tab = tab_id
        for tid, frame in self.frames.items():
            if tid != tab_id:
                frame.pack_forget()
                if tid in self.nav_buttons:
                    self.nav_buttons[tid].configure(
                        fg_color="transparent",
                        hover_color="#161822",
                        text_color="#8892b0",
                        image=self.nav_icons_normal.get(tid)
                    )

        if tab_id in self.nav_buttons:
            self.nav_buttons[tab_id].configure(
                fg_color="#dc2626",
                hover_color="#ef4444",
                text_color="#ffffff",
                image=self.nav_icons_active.get(tab_id)
            )

        self.frames[tab_id].pack(fill="both", expand=True)

    # -------------------------------------------------------------
    # 1. SEKME: KONTROL MERKEZİ (DASHBOARD)
    # -------------------------------------------------------------
    def build_dashboard_tab(self):
        tab = ctk.CTkFrame(self.content_area, fg_color="transparent")

        # Üst Taktik HUD Barı (Örnek Tasarımdaki Koyu Kırmızı Ambiyanslı Başlık Çubuğu)
        top_hud = ctk.CTkFrame(tab, fg_color="#170e14", corner_radius=14, border_width=1, border_color="#361420", height=42)
        top_hud.pack(fill="x", pady=(0, 10), padx=2)
        top_hud.pack_propagate(False)

        hud_left = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_left.pack(side="left", padx=14, fill="y")

        dot_emblem = ctk.CTkLabel(hud_left, text="▲", font=("Segoe UI", 12, "bold"), text_color=self.colors["accent"])
        dot_emblem.pack(side="left", padx=(0, 8))

        self.banner_dash_title = ctk.CTkLabel(
            hud_left,
            text="CLASH TITAN 2.0 • AUTONOMOUS BATTLE ENGINE",
            font=self.f_sec_head,
            text_color="#ffffff"
        )
        self.banner_dash_title.pack(side="left")

        hud_right = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_right.pack(side="right", padx=14, fill="y")

        b_status_badge = ctk.CTkLabel(
            hud_right,
            text="● ONLINE • DIRECTINPUT HEURISTIC",
            font=self.f_mono,
            text_color="#f87171",
            fg_color="#2b0d16",
            corner_radius=8,
            padx=10,
            pady=3
        )
        b_status_badge.pack(side="right")

        # Üst Stat Kartları (Koyu Cam & Kırmızı Vurgulu Oval Kutular)
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 10))

        self.card_attacks = self.create_stat_card(stats_frame, get_text("stat_attacks", self.lang), "0", self.colors["accent"])
        self.card_attacks.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.card_time = self.create_stat_card(stats_frame, get_text("stat_session", self.lang), "00:00:00", "#38bdf8")
        self.card_time.pack(side="left", fill="both", expand=True, padx=3)

        self.card_stealth = self.create_stat_card(stats_frame, get_text("stat_stealth", self.lang), get_text("stat_stealth_val", self.lang), "#c084fc")
        self.card_stealth.pack(side="left", fill="both", expand=True, padx=(6, 0))

        # Ana Eylem Alanı (Oval Köşeli Taktik Kontrol Kartı)
        action_card = ctk.CTkFrame(tab, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        action_card.pack(fill="x", pady=(0, 10), padx=2, ipady=4)

        head_row = ctk.CTkFrame(action_card, fg_color="transparent")
        head_row.pack(fill="x", padx=18, pady=(10, 6))

        emblem = ctk.CTkLabel(head_row, text="▲", font=("Segoe UI", 12, "bold"), text_color=self.colors["accent"])
        emblem.pack(side="left", padx=(0, 6))

        self.action_header = ctk.CTkLabel(
            head_row,
            text=get_text("sec_autonomous", self.lang),
            font=self.f_sec_head,
            text_color="#ffffff"
        )
        self.action_header.pack(side="left")

        btn_row = ctk.CTkFrame(action_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 8))

        self.btn_main_start = ctk.CTkButton(
            btn_row,
            text=get_text("btn_start", self.lang),
            image=self.icon_play,
            compound="left",
            font=self.f_btn_main,
            fg_color="#dc2626",
            text_color="#ffffff",
            hover_color="#ef4444",
            height=46,
            corner_radius=12,
            command=self.start_bot
        )
        self.btn_main_start.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_main_stop = ctk.CTkButton(
            btn_row,
            text=get_text("btn_stop", self.lang),
            image=self.icon_stop,
            compound="left",
            font=self.f_btn_main,
            fg_color="#1c0d13",
            border_width=1,
            border_color="#7f1d1d",
            text_color="#fca5a5",
            hover_color="#2d111b",
            height=46,
            corner_radius=12,
            state="disabled",
            command=self.stop_bot
        )
        self.btn_main_stop.pack(side="right", fill="x", expand=True, padx=(6, 0))

        self.lbl_calib_status = ctk.CTkLabel(
            action_card,
            text="",
            font=self.f_hint,
            text_color="#94a3b8"
        )
        self.lbl_calib_status.pack(anchor="w", padx=20, pady=(2, 6))

        # Manuel 2. Aşama ve Bitirme Butonları Satırı
        manual_row = ctk.CTkFrame(action_card, fg_color="transparent")
        manual_row.pack(fill="x", padx=18, pady=(0, 8))

        self.btn_manual_stage2 = ctk.CTkButton(
            manual_row,
            text=get_text("btn_stage2", self.lang),
            image=self.icon_forward,
            compound="left",
            font=self.f_btn_sub,
            fg_color="#0f1626",
            border_width=1,
            border_color="#0284c7",
            text_color="#e0f2fe",
            hover_color="#0369a1",
            height=38,
            corner_radius=10,
            command=self.send_stage2_command
        )
        self.btn_manual_stage2.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_manual_finish = ctk.CTkButton(
            manual_row,
            text=get_text("btn_finish", self.lang),
            image=self.icon_flag,
            compound="left",
            font=self.f_btn_sub,
            fg_color="#18130c",
            border_width=1,
            border_color="#d97706",
            text_color="#fef3c7",
            hover_color="#78350f",
            height=38,
            corner_radius=10,
            command=self.send_finish_command
        )
        self.btn_manual_finish.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.hint_lbl = ctk.CTkLabel(
            action_card,
            text=get_text("hint_hotkeys", self.lang),
            font=self.f_hint,
            text_color="#64748b"
        )
        self.hint_lbl.pack(anchor="w", padx=20, pady=(0, 6))

        # Canlı Etkinlik Akışı Kartı (Sleek Dark Terminal)
        mini_log_card = ctk.CTkFrame(tab, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        mini_log_card.pack(fill="both", expand=True, padx=2, pady=(0, 2))

        head_log_row = ctk.CTkFrame(mini_log_card, fg_color="transparent")
        head_log_row.pack(fill="x", padx=16, pady=(8, 4))

        log_dot = ctk.CTkLabel(head_log_row, text="▲", font=("Segoe UI", 11, "bold"), text_color=self.colors["accent"])
        log_dot.pack(side="left", padx=(0, 6))

        self.mini_log_head = ctk.CTkLabel(
            head_log_row,
            text=get_text("sec_feed", self.lang),
            font=self.f_sec_head,
            text_color="#ffffff"
        )
        self.mini_log_head.pack(side="left")

        self.mini_log_text = ctk.CTkTextbox(
            mini_log_card,
            fg_color="#080a0f",
            text_color="#e2e8f0",
            font=self.f_mono,
            corner_radius=10,
            border_width=1,
            border_color="#1d1722"
        )
        self.mini_log_text.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        self.append_log(get_text("init_log", self.lang))
        self.mini_log_text.configure(state="disabled")

        return tab

    def create_stat_card(self, parent, title, initial_value, text_color):
        card = ctk.CTkFrame(parent, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420", height=78)
        card.pack_propagate(False)

        t_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=self.f_card_head,
            text_color="#8892b0"
        )
        t_lbl.pack(anchor="w", padx=16, pady=(10, 2))
        card.title_label = t_lbl

        v_lbl = ctk.CTkLabel(
            card,
            text=initial_value,
            font=self.f_card_val,
            text_color=text_color
        )
        v_lbl.pack(anchor="w", padx=16)
        card.value_label = v_lbl
        return card

    # -------------------------------------------------------------
    # 2. SEKME: SLOT & KALİBRASYON (MANUEL SPACE)
    # -------------------------------------------------------------
    def build_calibration_tab(self):
        tab = ctk.CTkFrame(self.content_area, fg_color="transparent")

        # Üst Taktik HUD Barı (Slot & Kalibrasyon Başlık Çubuğu)
        top_hud = ctk.CTkFrame(tab, fg_color="#170e14", corner_radius=14, border_width=1, border_color="#361420", height=42)
        top_hud.pack(fill="x", pady=(0, 10), padx=2)
        top_hud.pack_propagate(False)

        hud_left = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_left.pack(side="left", padx=14, fill="y")

        dot_emblem = ctk.CTkLabel(hud_left, text="▲", font=("Segoe UI", 12, "bold"), text_color=self.colors["accent"])
        dot_emblem.pack(side="left", padx=(0, 8))

        self.banner_calib_title = ctk.CTkLabel(
            hud_left,
            text=get_text("banner_calib_title", self.lang),
            font=self.f_sec_head,
            text_color="#ffffff"
        )
        self.banner_calib_title.pack(side="left")

        hud_right = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_right.pack(side="right", padx=14, fill="y")

        v_sub_badge = ctk.CTkLabel(
            hud_right,
            text="HARDWARE RADAR // 23 SLOTS",
            font=self.f_mono,
            text_color="#f87171",
            fg_color="#2b0d16",
            corner_radius=8,
            padx=10,
            pady=3
        )
        v_sub_badge.pack(side="right")

        guide_card = ctk.CTkFrame(tab, fg_color="#121520", corner_radius=12, border_width=1, border_color="#2a1420")
        guide_card.pack(fill="x", pady=(0, 10))

        self.guide_lbl = ctk.CTkLabel(
            guide_card,
            text=get_text("calib_guide", self.lang),
            font=self.f_body,
            text_color="#94a3b8",
            wraplength=660,
            justify="left"
        )
        self.guide_lbl.pack(padx=16, pady=(8, 4))

        # Görsel Şablon Yakalama Araç Çubuğu
        snap_bar = ctk.CTkFrame(guide_card, fg_color="transparent")
        snap_bar.pack(fill="x", padx=16, pady=(2, 8))

        self.btn_capture_template = ctk.CTkButton(
            snap_bar,
            text="📷 İksir / Ganimet Görseli Yakala (3 sn)",
            font=self.f_btn_small,
            fg_color="#181c28",
            hover_color="#262d40",
            text_color="#38bdf8",
            border_width=1,
            border_color="#38bdf8",
            corner_radius=8,
            height=30,
            command=self.start_template_snapper
        )
        self.btn_capture_template.pack(side="left", padx=(0, 8))

        self.btn_open_templates = ctk.CTkButton(
            snap_bar,
            text="📁 Şablon Klasörünü Aç",
            font=self.f_btn_small,
            fg_color="#181c28",
            hover_color="#262d40",
            text_color="#94a3b8",
            border_width=1,
            border_color="#334155",
            corner_radius=8,
            height=30,
            command=self.open_templates_dir
        )
        self.btn_open_templates.pack(side="left")

        columns_frame = ctk.CTkFrame(tab, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True)

        self.left_col = ctk.CTkScrollableFrame(
            columns_frame,
            label_text=get_text("calib_troops_head", self.lang),
            label_font=self.f_sec_head,
            label_text_color="#f8fafc",
            fg_color="#121520",
            corner_radius=14,
            border_width=1,
            border_color="#2a1420"
        )
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 6))

        for key in HERO_AND_TROOPS:
            self.create_calibration_row(self.left_col, key)

        self.right_col = ctk.CTkScrollableFrame(
            columns_frame,
            label_text=get_text("calib_map_head", self.lang),
            label_font=self.f_sec_head,
            label_text_color="#f8fafc",
            fg_color="#121520",
            corner_radius=14,
            border_width=1,
            border_color="#2a1420"
        )
        self.right_col.pack(side="right", fill="both", expand=True, padx=(6, 0))

        for key in MAP_AND_NAV:
            self.create_calibration_row(self.right_col, key)

        return tab

    def create_calibration_row(self, parent, key):
        name, desc = get_slot_info(key, self.lang)

        row = ctk.CTkFrame(parent, fg_color="#151824", corner_radius=10, height=62, border_width=1, border_color="#251a24")
        row.pack(fill="x", pady=4, padx=2)
        row.pack_propagate(False)

        def set_hover(k):
            self.hovered_slot_key = k

        def unset_hover(k):
            if getattr(self, "hovered_slot_key", None) == k:
                self.hovered_slot_key = None

        row.bind("<Enter>", lambda e, k=key: set_hover(k))
        row.bind("<Leave>", lambda e, k=key: unset_hover(k))

        info_box = ctk.CTkFrame(row, fg_color="transparent")
        info_box.pack(side="left", fill="y", padx=10, pady=6)

        n_lbl = ctk.CTkLabel(info_box, text=name, font=self.f_row_name, text_color="#f1f5f9")
        n_lbl.pack(anchor="w")
        self.row_labels[key] = n_lbl

        pt = self.coords.get(key)
        coord_text = f"X: {pt['x']}, Y: {pt['y']}" if (pt and pt.get("x") is not None) else get_text("badge_missing", self.lang)
        badge_color = "#10b981" if (pt and pt.get("x") is not None) else "#ef4444"

        badge = ctk.CTkLabel(
            info_box,
            text=coord_text,
            font=self.f_mono,
            text_color=badge_color
        )
        badge.pack(anchor="w")
        self.coord_badges[key] = badge

        actions_box = ctk.CTkFrame(row, fg_color="transparent")
        actions_box.pack(side="right", padx=10)

        btn_record = ctk.CTkButton(
            actions_box,
            text=get_text("btn_record", self.lang),
            image=self.icon_pin,
            compound="left",
            font=self.f_btn_small,
            fg_color="#334155",
            hover_color="#475569",
            text_color="#f8fafc",
            width=86,
            height=28,
            corner_radius=6,
            command=lambda k=key: self.toggle_recording_point(k)
        )
        btn_record.pack(side="left", padx=2)
        self.record_buttons[key] = btn_record

        btn_test = ctk.CTkButton(
            actions_box,
            text=get_text("btn_test", self.lang),
            image=self.icon_test,
            compound="left",
            font=self.f_btn_small,
            fg_color="#1e293b",
            hover_color="#334155",
            text_color="#94a3b8",
            width=58,
            height=28,
            corner_radius=6,
            command=lambda k=key: self.test_click_point(k)
        )
        btn_test.pack(side="left", padx=2)
        self.test_buttons[key] = btn_test

        btn_clear = ctk.CTkButton(
            actions_box,
            text="",
            image=self.icon_trash,
            width=28,
            height=28,
            corner_radius=6,
            fg_color="#1e293b",
            hover_color="#7f1d1d",
            command=lambda k=key: self.delete_slot_assignment(k)
        )
        btn_clear.pack(side="left", padx=(2, 0))

    def open_templates_dir(self):
        """templates klasörünü Windows Gezgini'nde açar."""
        t_dir = os.path.join(BASE_DIR, "templates")
        os.makedirs(t_dir, exist_ok=True)
        try:
            os.startfile(t_dir)
        except Exception:
            pass

    def start_template_snapper(self):
        """Kullanıcının fareyle işaret ettiği iksir/araba görselini 3 saniyelik sayaçla yakalar."""
        if getattr(self, "snapping_template", False):
            return
        self.snapping_template = True

        def _worker():
            for i in range(3, 0, -1):
                msg = f"⏳ {i} sn... Fareyi İksir/Ganimet ikonunun üstüne tutun!"
                self.btn_capture_template.configure(text=msg, text_color="#f59e0b")
                self.append_log(f"[Görsel Yakalama] {i} saniye içinde fareyi iksir/ganimet görselinin üzerine tutun...")
                time.sleep(1)

            pos = pyautogui.position()
            t_path = self.vision.capture_and_save_template("elixir_cart", pos.x, pos.y, crop_size=64)
            try:
                winsound.Beep(1400, 200)
            except Exception:
                pass

            self.append_log(f"[✓] İksir/Ganimet şablonu kaydedildi: {os.path.basename(t_path)}")
            self.append_log("[✓] Artık savaş bittiğinde bot bu görseli ekranda arayacak ve bulduğu yere otomatik tıklayacak!")
            self.btn_capture_template.configure(text="📷 İksir / Ganimet Görseli Yakala (3 sn)", text_color="#38bdf8")
            self.snapping_template = False

        threading.Thread(target=_worker, daemon=True).start()

    def handle_esc_press(self):
        """ESC tuşuna basıldığında aktif bir koordinat kalibrasyonu varsa iptal eder."""
        if self.recording_key:
            self.cancel_recording(self.recording_key)

    def handle_delete_press(self):
        """Klavyeden Delete veya Backspace tuşuna basıldığında aktif kayıt veya fareyle üzerinde durulan slotu siler."""
        if self.recording_key:
            self.delete_slot_assignment(self.recording_key)
        elif getattr(self, "hovered_slot_key", None):
            self.delete_slot_assignment(self.hovered_slot_key)

    def delete_slot_assignment(self, point_key):
        """Belirtilen slotun atanmış koordinatını siler ve eksik (None) duruma getirir."""
        if not point_key or point_key not in self.coords:
            return

        self.coords[point_key] = {"x": None, "y": None}
        save_coordinates(self.coords)

        badge = self.coord_badges.get(point_key)
        btn = self.record_buttons.get(point_key)

        if badge:
            badge.configure(text=get_text("badge_missing", self.lang), text_color="#ef4444")
        if btn:
            btn.configure(text=get_text("btn_record", self.lang), fg_color="#334155", hover_color="#475569")

        if self.recording_key == point_key:
            self.recording_key = None

        if HAS_SOUND:
            try:
                winsound.Beep(550, 140)
            except Exception:
                pass

        name, _ = get_slot_info(point_key, self.lang)
        self.append_log(get_text("msg_slot_deleted", self.lang, name=name))
        self.update_calib_status_label()

    def toggle_recording_point(self, point_key):
        """Kayıt butonuna tıklandığında: aktifse iptal eder, değilse dinlemeye başlar."""
        if self.recording_key == point_key:
            self.cancel_recording(point_key)
        else:
            if self.recording_key:
                self.cancel_recording(self.recording_key)
            self.start_recording_point(point_key)

    def start_recording_point(self, point_key):
        self.recording_key = point_key
        btn = self.record_buttons[point_key]
        badge = self.coord_badges[point_key]

        btn.configure(text=get_text("btn_space", self.lang), fg_color="#f59e0b", hover_color="#d97706")
        badge.configure(text=get_text("badge_waiting", self.lang), text_color="#f59e0b")

        def listen_worker():
            time.sleep(0.1)

            while self.recording_key == point_key:
                # 1. ESC Tuşu Kontrolü (İptal)
                is_esc = False
                try:
                    if keyboard.is_pressed("esc") or bool(ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000):
                        is_esc = True
                except Exception:
                    pass

                if is_esc:
                    self.after(0, self.cancel_recording, point_key)
                    break

                # 2. DELETE / BACKSPACE Tuşu Kontrolü (Atamayı Silme / Eksiltme)
                is_delete = False
                try:
                    if keyboard.is_pressed("delete") or keyboard.is_pressed("backspace") or \
                       bool(ctypes.windll.user32.GetAsyncKeyState(0x2E) & 0x8000) or \
                       bool(ctypes.windll.user32.GetAsyncKeyState(0x08) & 0x8000):
                        is_delete = True
                except Exception:
                    pass

                if is_delete:
                    self.after(0, self.delete_slot_assignment, point_key)
                    break

                # 3. SPACE Tuşu Kontrolü (Yalnızca Space tuşu ile kaydet)
                is_space = False
                try:
                    if keyboard.is_pressed("space") or bool(ctypes.windll.user32.GetAsyncKeyState(0x20) & 0x8000):
                        is_space = True
                except Exception:
                    pass

                if is_space:
                    pos = pyautogui.position()
                    if HAS_SOUND:
                        try:
                            winsound.Beep(1200, 160)
                        except Exception:
                            pass

                    self.coords[point_key] = {"x": pos.x, "y": pos.y}
                    save_coordinates(self.coords)
                    self.after(0, self.finish_recording, point_key, pos.x, pos.y)
                    break

                time.sleep(0.02)

        threading.Thread(target=listen_worker, daemon=True).start()

    def finish_recording(self, point_key, x, y):
        badge = self.coord_badges.get(point_key)
        btn = self.record_buttons.get(point_key)

        if badge:
            badge.configure(text=f"X: {x}, Y: {y}", text_color="#10b981")
        if btn:
            btn.configure(text=get_text("btn_record", self.lang), fg_color="#334155", hover_color="#475569")
        self.recording_key = None
        self.append_log(get_text("msg_recorded", self.lang, key=point_key, x=x, y=y))
        self.update_calib_status_label()

    def cancel_recording(self, point_key):
        btn = self.record_buttons.get(point_key)
        badge = self.coord_badges.get(point_key)
        pt = self.coords.get(point_key)
        coord_text = f"X: {pt['x']}, Y: {pt['y']}" if (pt and pt.get("x") is not None) else get_text("badge_missing", self.lang)
        badge_color = "#10b981" if (pt and pt.get("x") is not None) else "#ef4444"

        if badge:
            badge.configure(text=coord_text, text_color=badge_color)
        if btn:
            btn.configure(text=get_text("btn_record", self.lang), fg_color="#334155", hover_color="#475569")
        if self.recording_key == point_key:
            self.recording_key = None
            self.append_log(get_text("msg_cancelled", self.lang, key=point_key))
        self.update_calib_status_label()

    def test_click_point(self, point_key):
        pt = self.coords.get(point_key)
        if not pt or pt.get("x") is None:
            self.append_log(f"[!] {point_key} not calibrated!")
            return

        def click_worker():
            self.append_log(f"[*] Test Click: {point_key} -> (X={pt['x']}, Y={pt['y']})")
            time.sleep(0.4)
            human_click(pt["x"], pt["y"], jitter=False, delay_after=False)
            self.append_log(f"[✓] {point_key} clicked!")

        threading.Thread(target=click_worker, daemon=True).start()

    # -------------------------------------------------------------
    # 3. SEKME: ANTİ-BAN & STRATEJİ AYARLARI
    # -------------------------------------------------------------
    def build_settings_tab(self):
        tab = ctk.CTkFrame(self.content_area, fg_color="transparent")

        # Alt Bilgi Barı: Anlık Otomatik Kayıt & Canlı Senkronizasyon (Footer)
        footer_bar = ctk.CTkFrame(tab, fg_color="#0e1118", corner_radius=12, height=36, border_width=1, border_color="#2a1420")
        footer_bar.pack(fill="x", side="bottom", padx=2, pady=(10, 0))
        footer_bar.pack_propagate(False)

        f_left = ctk.CTkFrame(footer_bar, fg_color="transparent")
        f_left.pack(side="left", padx=12, fill="y")

        dot = ctk.CTkLabel(f_left, text="●", font=("Segoe UI", 12, "bold"), text_color="#10b981")
        dot.pack(side="left", padx=(0, 6))

        self.lbl_auto_saved = ctk.CTkLabel(
            f_left,
            text=get_text("auto_saved_hint", self.lang),
            font=self.f_hint,
            text_color="#94a3b8"
        )
        self.lbl_auto_saved.pack(side="left")

        f_right = ctk.CTkFrame(footer_bar, fg_color="transparent")
        f_right.pack(side="right", padx=12, fill="y")

        lbl_engine_info = ctk.CTkLabel(
            f_right,
            text="CLASH TITAN 2.0 • LIVE SYNC ACTIVE",
            font=self.f_hint,
            text_color="#ef4444"
        )
        lbl_engine_info.pack(side="right")

        cols_frame = ctk.CTkFrame(tab, fg_color="transparent")
        cols_frame.pack(fill="both", expand=True)

        left_col = ctk.CTkFrame(cols_frame, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 6))

        right_col = ctk.CTkFrame(cols_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(6, 0))

        # --- SOL SÜTUN: GÜVENLİK & HARP STRATEJİSİ ---
        # Kart 0: Anti-Ban Risk & Güvenlik Analiz Merkezi (Canlı Gösterge)
        card_risk = ctk.CTkFrame(left_col, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        card_risk.pack(fill="x", pady=(0, 10), padx=2, ipady=6)

        risk_top = ctk.CTkFrame(card_risk, fg_color="transparent")
        risk_top.pack(fill="x", padx=16, pady=(10, 4))

        self.lbl_risk_head = ctk.CTkLabel(risk_top, text=get_text("card_risk_head", self.lang), font=self.f_sec_head, text_color="#f8fafc")
        self.lbl_risk_head.pack(side="left")

        self.badge_risk_status = ctk.CTkLabel(
            risk_top,
            text="",
            font=self.f_status,
            text_color="#10b981",
            fg_color="#064e3b",
            corner_radius=8,
            padx=10,
            pady=3
        )
        self.badge_risk_status.pack(side="right")

        self.lbl_risk_desc = ctk.CTkLabel(card_risk, text=get_text("card_risk_desc", self.lang), font=self.f_body, text_color="#64748b")
        self.lbl_risk_desc.pack(anchor="w", padx=16, pady=(0, 8))

        # Canlı Risk / Güvenlik Gösterge Çubuğu
        meter_box = ctk.CTkFrame(card_risk, fg_color="transparent")
        meter_box.pack(fill="x", padx=16, pady=(0, 6))

        self.risk_bar = ctk.CTkProgressBar(
            meter_box,
            height=12,
            corner_radius=6,
            fg_color="#1c202e",
            progress_color="#10b981"
        )
        self.risk_bar.pack(fill="x", pady=(0, 6))

        self.lbl_risk_advice = ctk.CTkLabel(
            meter_box,
            text="",
            font=self.f_hint,
            text_color="#94a3b8",
            wraplength=460,
            justify="left"
        )
        self.lbl_risk_advice.pack(anchor="w", fill="x", pady=(0, 6))

        # Alt Satır: Önerilen Güvenli Ayarları Uygula Butonu (Tam Genişlik)
        self.btn_apply_preset = ctk.CTkButton(
            card_risk,
            text=get_text("btn_apply_preset", self.lang),
            image=self.icon_shield,
            compound="left",
            font=self.f_btn_small,
            fg_color="#b91c1c",
            hover_color="#dc2626",
            text_color="#ffffff",
            height=34,
            corner_radius=10,
            command=self.apply_recommended_preset
        )
        self.btn_apply_preset.pack(fill="x", padx=16, pady=(2, 10))

        # Kart 2: Savaş Stratejisi
        card_battle = ctk.CTkFrame(left_col, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        card_battle.pack(fill="x", pady=(0, 2), padx=2, ipady=6)

        self.lbl_battle_head = ctk.CTkLabel(card_battle, text=get_text("card_battle_head", self.lang), font=self.f_sec_head, text_color="#f8fafc")
        self.lbl_battle_head.pack(anchor="w", padx=16, pady=(10, 2))

        self.lbl_battle_desc = ctk.CTkLabel(card_battle, text=get_text("card_battle_desc", self.lang), font=self.f_body, text_color="#64748b")
        self.lbl_battle_desc.pack(anchor="w", padx=16, pady=(0, 8))

        self.slider_stage2_delay = self.create_slider_control(
            card_battle,
            "slider_stage2_title",
            val_min=30,
            val_max=150,
            current=self.user_prefs.get("stage2_wait_seconds", BATTLE_SETTINGS.get("stage2_wait_seconds", 75)),
            unit_key="unit_seconds",
            on_change=lambda _: self.auto_save_settings()
        )

        self.slider_stage2_finish_delay = self.create_slider_control(
            card_battle,
            "slider_stage2_finish_title",
            val_min=15,
            val_max=150,
            current=self.user_prefs.get("stage2_finish_wait_seconds", BATTLE_SETTINGS.get("stage2_finish_wait_seconds", 50)),
            unit_key="unit_seconds",
            on_change=lambda _: self.auto_save_settings()
        )

        self.slider_clicks_per_troop = self.create_slider_control(
            card_battle,
            "slider_clicks_title",
            val_min=1,
            val_max=8,
            current=self.user_prefs.get("clicks_per_troop_slot", BATTLE_SETTINGS.get("clicks_per_troop_slot", 4)),
            unit_key="unit_clicks",
            on_change=lambda _: self.auto_save_settings()
        )

        mode_box = ctk.CTkFrame(card_battle, fg_color="transparent")
        mode_box.pack(fill="x", padx=16, pady=(4, 6))

        self.lbl_stage2_mode = ctk.CTkLabel(mode_box, text=get_text("lbl_stage2_mode", self.lang), font=self.f_body, text_color="#cbd5e1")
        self.lbl_stage2_mode.pack(anchor="w", pady=(0, 3))

        self.seg_stage2_mode = ctk.CTkSegmentedButton(
            mode_box,
            values=[get_text("mode_auto", self.lang), get_text("mode_manual", self.lang)],
            font=self.f_btn_small,
            selected_color="#dc2626",
            selected_hover_color="#ef4444",
            unselected_color="#0d0f16",
            unselected_hover_color="#181c28",
            corner_radius=10,
            command=lambda _: self.auto_save_settings()
        )
        current_mode = get_text("mode_manual", self.lang) if self.user_prefs.get("stage2_mode") == "MANUAL" else get_text("mode_auto", self.lang)
        self.seg_stage2_mode.set(current_mode)
        self.seg_stage2_mode.pack(fill="x")

        # --- SAĞ SÜTUN: OTOMASYON, RENK & TİPOGRAFİ ---
        # Kart 1: Mola Sistemi
        card_break = ctk.CTkFrame(right_col, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        card_break.pack(fill="x", pady=(0, 10), padx=2, ipady=6)

        self.lbl_break_head = ctk.CTkLabel(card_break, text=get_text("card_break_head", self.lang), font=self.f_sec_head, text_color="#f8fafc")
        self.lbl_break_head.pack(anchor="w", padx=16, pady=(8, 2))

        self.lbl_break_desc = ctk.CTkLabel(card_break, text=get_text("card_break_desc", self.lang), font=self.f_body, text_color="#64748b")
        self.lbl_break_desc.pack(anchor="w", padx=16, pady=(0, 6))

        self.slider_break_freq = self.create_slider_control(
            card_break,
            "slider_break_title",
            val_min=5,
            val_max=25,
            current=self.user_prefs.get("attacks_before_break", ANTI_BAN.get("attacks_before_break", 11)),
            unit_key="unit_attacks",
            on_change=lambda _: self.auto_save_settings()
        )

        # Kart 5: Dil & Bölge Tercihi (Language)
        card_lang = ctk.CTkFrame(right_col, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        card_lang.pack(fill="x", pady=(0, 2), padx=2, ipady=6)

        self.lbl_lang_head = ctk.CTkLabel(card_lang, text=get_text("card_lang_head", self.lang), font=self.f_sec_head, text_color="#f8fafc")
        self.lbl_lang_head.pack(anchor="w", padx=16, pady=(8, 2))

        self.lbl_lang_desc = ctk.CTkLabel(card_lang, text=get_text("card_lang_desc", self.lang), font=self.f_body, text_color="#64748b")
        self.lbl_lang_desc.pack(anchor="w", padx=16, pady=(0, 6))

        l_box = ctk.CTkFrame(card_lang, fg_color="transparent")
        l_box.pack(fill="x", padx=16, pady=(0, 6))

        self.lbl_lang_choice = ctk.CTkLabel(l_box, text=get_text("lbl_lang_choice", self.lang), font=self.f_body, text_color="#cbd5e1")
        self.lbl_lang_choice.pack(anchor="w", pady=(0, 3))

        self.seg_lang_settings = ctk.CTkSegmentedButton(
            l_box,
            values=["Türkçe (TR)", "English (EN)"],
            font=self.f_btn_small,
            selected_color="#dc2626",
            selected_hover_color="#ef4444",
            unselected_color="#0d0f16",
            unselected_hover_color="#181c28",
            corner_radius=10,
            command=lambda val: self.set_language("TR" if "TR" in val else "EN")
        )
        self.seg_lang_settings.set("Türkçe (TR)" if self.lang == "TR" else "English (EN)")
        self.seg_lang_settings.pack(fill="x")

        # İlk risk ölçümünü güncelle
        self.update_risk_meter()

        return tab

    def send_stage2_command(self):
        # 1. Eğer tam otomatik bot zaten çalışıyorsa, devam eden savaşa 2. aşama sinyali gönder
        if self.bot_process is not None and self.bot_process.poll() is None:
            try:
                with open(CMD_FILE, "w", encoding="utf-8") as f:
                    f.write("STAGE2")
                self.append_log(get_text("msg_stage2_cmd", self.lang))
            except Exception as e:
                self.append_log(f"[HATA] {e}")
        else:
            # 2. Eğer bot çalışmıyorsa: SAVAŞI BAŞLATMAYI İSTEMEDEN DOĞRUDAN 2. AŞAMAYI ÇALIŞTIR!
            self.start_bot(extra_args=["--stage2-only"])

    def send_finish_command(self):
        if self.bot_process is not None and self.bot_process.poll() is None:
            try:
                with open(CMD_FILE, "w", encoding="utf-8") as f:
                    f.write("FINISH")
                self.append_log(get_text("msg_finish_cmd", self.lang))
            except Exception as e:
                self.append_log(f"[HATA] {e}")
        else:
            # Bot çalışmıyorken de doğrudan ekrandaki 'Eve Dön / Tamam' butonunu tıkla
            def direct_finish_worker():
                pt = self.coords.get("return_home_button")
                if not pt or pt.get("x") is None:
                    msg = "[!] 'Eve Dön' butonu koordinatı henüz ayarlanmamış!" if self.lang == "TR" else "[!] 'Return Home' button coordinate not set!"
                    self.append_log(msg)
                    return
                msg_click = "[*] Doğrudan 'Tamam / Eve Dön' butonuna basılıyor..." if self.lang == "TR" else "[*] Clicking 'Return Home / OK' button directly..."
                self.append_log(msg_click)
                from human_mouse import human_click
                human_click(pt["x"], pt["y"], jitter=False, delay_after=False)
                time.sleep(1.2)
                human_click(pt["x"], pt["y"], jitter=False, delay_after=False)
                msg_done = "[✓] Köye dönme tıklamaları tamamlandı." if self.lang == "TR" else "[✓] Return home clicks completed."
                self.append_log(msg_done)

            threading.Thread(target=direct_finish_worker, daemon=True).start()

    def create_slider_control(self, parent, title_key, val_min, val_max, current, unit_key, on_change=None):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(fill="x", padx=16, pady=4)

        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", pady=(0, 4))

        lbl_t = ctk.CTkLabel(head, text=get_text(title_key, self.lang), font=self.f_body, text_color="#cbd5e1")
        lbl_t.pack(side="left")

        unit_str = get_text(unit_key, self.lang)
        lbl_v = ctk.CTkLabel(head, text=f"{int(current)} {unit_str}", font=self.f_status, text_color="#ef4444")
        lbl_v.pack(side="right")

        def slider_cb(val):
            lbl_v.configure(text=f"{int(val)} {get_text(unit_key, self.lang)}")
            if on_change:
                on_change(val)

        slider = ctk.CTkSlider(
            box,
            from_=val_min,
            to=val_max,
            number_of_steps=int(val_max - val_min),
            fg_color="#1c202e",
            progress_color="#dc2626",
            button_color="#ef4444",
            button_hover_color="#ffffff",
            command=slider_cb
        )
        slider.set(current)
        slider.pack(fill="x")

        # Fare tekerleği (scroll) ile değer değişimini engelle (yalnızca imleçle sürükleme/tıklama)
        try:
            slider._canvas.unbind("<MouseWheel>")
            slider._canvas.unbind("<Button-4>")
            slider._canvas.unbind("<Button-5>")
        except Exception:
            pass

        slider.title_lbl = lbl_t
        slider.val_label = lbl_v
        slider.title_key = title_key
        slider.unit_key = unit_key
        return slider

    def auto_save_settings(self):
        """Ayarları anlık olarak belleğe ve user_settings.json dosyasına kaydeder."""
        if not hasattr(self, "slider_break_freq") or not hasattr(self, "slider_stage2_delay"):
            return

        new_break_freq = int(self.slider_break_freq.get())
        new_stage2_delay = int(self.slider_stage2_delay.get())
        new_stage2_finish = int(self.slider_stage2_finish_delay.get())
        new_clicks = int(self.slider_clicks_per_troop.get())
        new_mode = "MANUAL" if ("MANUEL" in self.seg_stage2_mode.get() or "MANUAL" in self.seg_stage2_mode.get()) else "AUTO"

        ANTI_BAN["attacks_before_break"] = new_break_freq
        BATTLE_SETTINGS["stage2_wait_seconds"] = new_stage2_delay
        BATTLE_SETTINGS["stage2_finish_wait_seconds"] = new_stage2_finish
        BATTLE_SETTINGS["clicks_per_troop_slot"] = new_clicks
        BATTLE_SETTINGS["stage2_mode"] = new_mode

        self.user_prefs["attacks_before_break"] = new_break_freq
        self.user_prefs["stage2_wait_seconds"] = new_stage2_delay
        self.user_prefs["stage2_finish_wait_seconds"] = new_stage2_finish
        self.user_prefs["clicks_per_troop_slot"] = new_clicks
        self.user_prefs["stage2_mode"] = new_mode
        self.user_prefs["language"] = self.lang
        self.user_prefs["font_theme"] = "Minimalist Lüks (Outfit)"
        self.user_prefs["color_theme"] = "Crimson Titan"
        save_user_settings(self.user_prefs)

        self.update_risk_meter()

    def update_risk_meter(self):
        """Ban riskini ve güvenlik seviyesini dinamik olarak yeniden hesaplar ve görselleştirir."""
        if not hasattr(self, "risk_bar"):
            return

        break_freq = int(self.slider_break_freq.get())
        stage2_delay = int(self.slider_stage2_delay.get())
        clicks = int(self.slider_clicks_per_troop.get())
        mode = "MANUAL" if ("MANUEL" in self.seg_stage2_mode.get() or "MANUAL" in self.seg_stage2_mode.get()) else "AUTO"

        risk_pct, safety_pct, color, status_text, advice_text = calculate_ban_risk(
            break_freq, stage2_delay, clicks, mode, self.lang
        )

        self.risk_bar.configure(progress_color=color)
        self.risk_bar.set(safety_pct / 100.0)

        badge_bg = "#064e3b" if color == "#10b981" else ("#78350f" if color == "#f59e0b" else "#7f1d1d")
        self.badge_risk_status.configure(
            text=status_text,
            text_color=color,
            fg_color=badge_bg
        )

        self.lbl_risk_advice.configure(
            text=advice_text,
            text_color=color if color != "#10b981" else "#94a3b8"
        )

    def apply_recommended_preset(self):
        """Supercell anti-hile sistemlerine karşı maksimum güvenli önerilen ayarları anında yükler."""
        self.slider_break_freq.set(10)
        self.slider_break_freq.val_label.configure(text=f"10 {get_text('unit_attacks', self.lang)}")

        self.slider_stage2_delay.set(75)
        self.slider_stage2_delay.val_label.configure(text=f"75 {get_text('unit_seconds', self.lang)}")

        self.slider_stage2_finish_delay.set(50)
        self.slider_stage2_finish_delay.val_label.configure(text=f"50 {get_text('unit_seconds', self.lang)}")

        self.slider_clicks_per_troop.set(4)
        self.slider_clicks_per_troop.val_label.configure(text=f"4 {get_text('unit_clicks', self.lang)}")

        self.seg_stage2_mode.set(get_text("mode_auto", self.lang))

        self.auto_save_settings()
        self.append_log(get_text("preset_applied", self.lang))

    def set_language(self, new_lang):
        if new_lang not in ("TR", "EN"):
            return
        self.lang = new_lang
        locales.ACTIVE_LANG = new_lang
        self.user_prefs["language"] = new_lang
        save_user_settings(self.user_prefs)

        if hasattr(self, "seg_lang"):
            self.seg_lang.set(new_lang)
        if hasattr(self, "seg_lang_settings"):
            self.seg_lang_settings.set("Türkçe (TR)" if new_lang == "TR" else "English (EN)")

        self.update_ui_texts()
        self.append_log(f"[✓] Dil değiştirildi / Language switched to: {new_lang}")

    def update_ui_texts(self):
        # Pencere Başlığı & Logo
        self.title(get_text("app_title", self.lang))
        self.brand_lbl.configure(text=get_text("brand_name", self.lang))
        self.brand_sub.configure(text=get_text("brand_sub", self.lang))

        # Durum Göstergesi
        if self.bot_process:
            self.status_indicator.configure(text=get_text("status_busy", self.lang))
        else:
            self.status_indicator.configure(text=get_text("status_ready", self.lang))

        # Navigasyon Butonları
        for tab_id, text_key, _ in self.nav_items_data:
            if tab_id in self.nav_buttons:
                self.nav_buttons[tab_id].configure(text=get_text(text_key, self.lang))

        # Dashboard Stat Kartları
        if hasattr(self, "card_attacks") and hasattr(self.card_attacks, "title_label"):
            self.card_attacks.title_label.configure(text=get_text("stat_attacks", self.lang))
        if hasattr(self, "card_time") and hasattr(self.card_time, "title_label"):
            self.card_time.title_label.configure(text=get_text("stat_session", self.lang))
        if hasattr(self, "card_stealth") and hasattr(self.card_stealth, "title_label"):
            self.card_stealth.title_label.configure(text=get_text("stat_stealth", self.lang))
            self.card_stealth.value_label.configure(text=get_text("stat_stealth_val", self.lang))

        # Dashboard Aksiyon Butonları & Başlıklar
        if hasattr(self, "action_header"):
            self.action_header.configure(text=get_text("sec_autonomous", self.lang))
        if hasattr(self, "btn_main_start"):
            self.btn_main_start.configure(text=get_text("btn_start", self.lang))
        if hasattr(self, "btn_main_stop"):
            self.btn_main_stop.configure(text=get_text("btn_stop", self.lang))
        if hasattr(self, "btn_manual_stage2"):
            self.btn_manual_stage2.configure(text=get_text("btn_stage2", self.lang))
        if hasattr(self, "btn_manual_finish"):
            self.btn_manual_finish.configure(text=get_text("btn_finish", self.lang))
        if hasattr(self, "hint_lbl"):
            self.hint_lbl.configure(text=get_text("hint_hotkeys", self.lang))
        if hasattr(self, "mini_log_head"):
            self.mini_log_head.configure(text=get_text("sec_feed", self.lang))

        # Kalibrasyon Sekmesi
        if hasattr(self, "guide_lbl"):
            self.guide_lbl.configure(text=get_text("calib_guide", self.lang))
        if hasattr(self, "left_col"):
            self.left_col.configure(label_text=get_text("calib_troops_head", self.lang))
        if hasattr(self, "right_col"):
            self.right_col.configure(label_text=get_text("calib_map_head", self.lang))

        # Slot Satırları
        for key, n_lbl in self.row_labels.items():
            name, desc = get_slot_info(key, self.lang)
            n_lbl.configure(text=name)

            if key in self.record_buttons and self.recording_key != key:
                self.record_buttons[key].configure(text=get_text("btn_record", self.lang))
            if key in self.test_buttons:
                self.test_buttons[key].configure(text=get_text("btn_test", self.lang))

            pt = self.coords.get(key)
            if not pt or pt.get("x") is None:
                if key in self.coord_badges:
                    self.coord_badges[key].configure(text=get_text("badge_missing", self.lang))

        # Ayarlar Sekmesi - Risk & Parametreler
        if hasattr(self, "lbl_risk_head"):
            self.lbl_risk_head.configure(text=get_text("card_risk_head", self.lang))
            self.lbl_risk_desc.configure(text=get_text("card_risk_desc", self.lang))
            self.btn_apply_preset.configure(text=get_text("btn_apply_preset", self.lang))
            self.lbl_auto_saved.configure(text=get_text("auto_saved_hint", self.lang))
            self.update_risk_meter()

        # Banner Başlıkları
        if hasattr(self, "banner_dash_title"):
            self.banner_dash_title.configure(text=get_text("banner_dashboard_title", self.lang))
        if hasattr(self, "banner_calib_title"):
            self.banner_calib_title.configure(text=get_text("banner_calib_title", self.lang))

        if hasattr(self, "lbl_break_head"):
            self.lbl_break_head.configure(text=get_text("card_break_head", self.lang))
            self.lbl_break_desc.configure(text=get_text("card_break_desc", self.lang))
        if hasattr(self, "lbl_battle_head"):
            self.lbl_battle_head.configure(text=get_text("card_battle_head", self.lang))
            self.lbl_battle_desc.configure(text=get_text("card_battle_desc", self.lang))
        if hasattr(self, "lbl_theme_head"):
            self.lbl_theme_head.configure(text=get_text("card_theme_head", self.lang))
            self.lbl_theme_desc.configure(text=get_text("card_theme_desc", self.lang))
            self.lbl_font_pack.configure(text=get_text("lbl_font_pack", self.lang))
        if hasattr(self, "lbl_color_head"):
            self.lbl_color_head.configure(text=get_text("card_color_head", self.lang))
            self.lbl_color_desc.configure(text=get_text("card_color_desc", self.lang))
            self.lbl_color_choice.configure(text=get_text("lbl_color_choice", self.lang))
        if hasattr(self, "lbl_lang_head"):
            self.lbl_lang_head.configure(text=get_text("card_lang_head", self.lang))
            self.lbl_lang_desc.configure(text=get_text("card_lang_desc", self.lang))
            self.lbl_lang_choice.configure(text=get_text("lbl_lang_choice", self.lang))

        # Slider Güncellemeleri
        for slider in [getattr(self, "slider_break_freq", None),
                       getattr(self, "slider_stage2_delay", None),
                       getattr(self, "slider_stage2_finish_delay", None),
                       getattr(self, "slider_clicks_per_troop", None)]:
            if slider and hasattr(slider, "title_lbl"):
                slider.title_lbl.configure(text=get_text(slider.title_key, self.lang))
                slider.val_label.configure(text=f"{int(slider.get())} {get_text(slider.unit_key, self.lang)}")

        if hasattr(self, "lbl_stage2_mode"):
            self.lbl_stage2_mode.configure(text=get_text("lbl_stage2_mode", self.lang))
            cur = self.seg_stage2_mode.get()
            is_manual = "MANUEL" in cur or "MANUAL" in cur
            self.seg_stage2_mode.configure(values=[get_text("mode_auto", self.lang), get_text("mode_manual", self.lang)])
            self.seg_stage2_mode.set(get_text("mode_manual", self.lang) if is_manual else get_text("mode_auto", self.lang))

        # Log Sekmesi
        if hasattr(self, "logs_head_lbl"):
            self.logs_head_lbl.configure(text=get_text("sec_full_log", self.lang))
        if hasattr(self, "btn_clear_logs"):
            self.btn_clear_logs.configure(text=get_text("btn_clear", self.lang))

        self.update_calib_status_label()

    # -------------------------------------------------------------
    # 4. SEKME: CANLI TERMİNAL & LOGLAR
    # -------------------------------------------------------------
    def build_logs_tab(self):
        tab = ctk.CTkFrame(self.content_area, fg_color="transparent")

        # Üst Taktik HUD Barı (Canlı Terminal Başlık Çubuğu)
        top_hud = ctk.CTkFrame(tab, fg_color="#170e14", corner_radius=14, border_width=1, border_color="#361420", height=42)
        top_hud.pack(fill="x", pady=(0, 10), padx=2)
        top_hud.pack_propagate(False)

        hud_left = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_left.pack(side="left", padx=14, fill="y")

        dot_emblem = ctk.CTkLabel(hud_left, text="▲", font=("Segoe UI", 12, "bold"), text_color=self.colors["accent"])
        dot_emblem.pack(side="left", padx=(0, 8))

        self.logs_head_lbl = ctk.CTkLabel(
            hud_left,
            text=get_text("sec_full_log", self.lang),
            font=self.f_sec_head,
            text_color="#ffffff"
        )
        self.logs_head_lbl.pack(side="left")

        hud_right = ctk.CTkFrame(top_hud, fg_color="transparent")
        hud_right.pack(side="right", padx=14, fill="y")

        self.btn_clear_logs = ctk.CTkButton(
            hud_right,
            text=get_text("btn_clear", self.lang),
            font=self.f_btn_small,
            fg_color="#220e15",
            hover_color="#361420",
            text_color="#f87171",
            border_width=1,
            border_color="#ef4444",
            width=80,
            height=28,
            corner_radius=10,
            command=self.clear_logs
        )
        self.btn_clear_logs.pack(side="right")

        log_card = ctk.CTkFrame(tab, fg_color="#121520", corner_radius=14, border_width=1, border_color="#2a1420")
        log_card.pack(fill="both", expand=True, padx=2, pady=(0, 2))

        self.full_log_text = ctk.CTkTextbox(
            log_card,
            fg_color="#080a0f",
            text_color="#e2e8f0",
            font=self.f_mono,
            corner_radius=10,
            border_width=1,
            border_color="#1d1722",
            state="disabled"
        )
        self.full_log_text.pack(fill="both", expand=True, padx=12, pady=12)

        return tab

    def clear_logs(self):
        self.full_log_text.configure(state="normal")
        self.full_log_text.delete("1.0", "end")
        self.full_log_text.configure(state="disabled")
        self.append_log(get_text("log_cleared", self.lang))

    # -------------------------------------------------------------
    # GENEL METOTLAR & BOT ÇALIŞTIRMA
    # -------------------------------------------------------------
    def update_clock_loop(self):
        if self.session_start and self.bot_process:
            elapsed = int(time.time() - self.session_start)
            hrs, rem = divmod(elapsed, 3600)
            mins, secs = divmod(rem, 60)
            self.card_time.value_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
        self.after(1000, self.update_clock_loop)

    def append_log(self, text):
        clean = text.strip()
        if not clean:
            return

        if ("Saldırı #" in clean or "Attack #" in clean) and ("tamamlandı" in clean or "finished" in clean or "ended" in clean):
            self.attack_counter += 1
            self.card_attacks.value_label.configure(text=str(self.attack_counter))

        if hasattr(self, "mini_log_text"):
            self.mini_log_text.configure(state="normal")
            self.mini_log_text.insert("end", clean + "\n")
            self.mini_log_text.see("end")
            self.mini_log_text.configure(state="disabled")

        if hasattr(self, "full_log_text"):
            self.full_log_text.configure(state="normal")
            self.full_log_text.insert("end", clean + "\n")
            self.full_log_text.see("end")
            self.full_log_text.configure(state="disabled")

        try:
            self.update_idletasks()
        except Exception:
            pass

    def get_missing_calibration_slots(self, required_keys=None):
        """Atanmamış / eksik olan koordinat slotlarını liste olarak döner."""
        all_slots = required_keys if required_keys is not None else (HERO_AND_TROOPS + MAP_AND_NAV)
        all_required = [k for k in all_slots if k not in OPTIONAL_SLOTS] if required_keys is None else all_slots
        missing = []
        for key in all_required:
            pt = self.coords.get(key)
            if not pt or pt.get("x") is None or pt.get("y") is None:
                missing.append(key)
        return missing

    def update_calib_status_label(self):
        """Dashboard üzerindeki tuş atama durumunu canlı günceller."""
        if not hasattr(self, "lbl_calib_status"):
            return
        missing = self.get_missing_calibration_slots()
        if missing:
            txt = get_text("calib_status_missing", self.lang, count=len(missing))
            self.lbl_calib_status.configure(text=txt, text_color="#f59e0b")
        else:
            txt = get_text("calib_status_ready", self.lang)
            self.lbl_calib_status.configure(text=txt, text_color="#10b981")

    def show_missing_calibration_dialog(self, missing_slots):
        """Eksik tuş atamaları olduğunda şık ve modern bir uyarı penceresi açar ve kalibrasyona yönlendirir."""
        if HAS_SOUND:
            try:
                winsound.Beep(800, 220)
            except Exception:
                pass

        # Canlı loga uyarı mesajı ekle
        self.append_log(get_text("log_missing_slots", self.lang, count=len(missing_slots)))

        # Kalibrasyon sekmesine anında geçiş yap
        self.switch_tab("calibration")

        # Eksik slotların rozetlerini kırmızı ile işaretle
        for key in missing_slots:
            if key in self.coord_badges:
                self.coord_badges[key].configure(text=get_text("badge_missing", self.lang), text_color="#ef4444")

        # Özel CTkToplevel Modal Uyarısı
        dialog = ctk.CTkToplevel(self)
        dialog.title(get_text("calib_missing_title", self.lang))
        dialog.geometry("540x480")
        dialog.minsize(480, 400)
        dialog.configure(fg_color="#0b0e14")
        dialog.transient(self)
        dialog.grab_set()

        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 270
            y = self.winfo_y() + (self.winfo_height() // 2) - 240
            dialog.geometry(f"+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

        card = ctk.CTkFrame(dialog, fg_color="#151b26", corner_radius=12, border_width=1, border_color="#ef4444")
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Başlık Satırı
        head_row = ctk.CTkFrame(card, fg_color="transparent")
        head_row.pack(fill="x", padx=16, pady=(16, 8))

        lbl_warn_badge = ctk.CTkLabel(
            head_row,
            text="[ ! ]",
            font=self.f_card_val,
            text_color="#ef4444"
        )
        lbl_warn_badge.pack(side="left", padx=(0, 10))

        lbl_head = ctk.CTkLabel(
            head_row,
            text=get_text("calib_missing_header", self.lang),
            font=self.f_sec_head,
            text_color="#ef4444"
        )
        lbl_head.pack(side="left")

        lbl_body = ctk.CTkLabel(
            card,
            text=get_text("calib_missing_body", self.lang, count=len(missing_slots)),
            font=self.f_body,
            text_color="#cbd5e1",
            justify="left",
            wraplength=460
        )
        lbl_body.pack(anchor="w", padx=18, pady=(0, 10))

        # Eksik slotların listesi (Kaydırılabilir alan)
        list_scroll = ctk.CTkScrollableFrame(card, fg_color="#0f141d", corner_radius=8, height=190)
        list_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        for key in missing_slots:
            name, desc = get_slot_info(key, self.lang)
            row = ctk.CTkFrame(list_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)

            dot = ctk.CTkLabel(row, text="•", font=self.f_status, text_color="#ef4444")
            dot.pack(side="left", padx=(4, 6))

            t_lbl = ctk.CTkLabel(row, text=name, font=self.f_row_name, text_color="#f8fafc")
            t_lbl.pack(side="left")

            if desc:
                d_lbl = ctk.CTkLabel(row, text=f"({desc})", font=self.f_hint, text_color="#64748b")
                d_lbl.pack(side="left", padx=(6, 0))

        # Kapat / Şimdi Kalibre Et Butonu
        btn_close = ctk.CTkButton(
            card,
            text=get_text("btn_calib_now", self.lang),
            font=self.f_btn_sub,
            fg_color="#10b981",
            hover_color="#059669",
            text_color="#022c22",
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        btn_close.pack(fill="x", padx=16, pady=(0, 16))

    def start_bot(self, extra_args=None):
        # Eğer zaten aktif bir bot süreci çalışıyorsa mükerrer başlatmayı engelle
        if self.bot_process is not None and self.bot_process.poll() is None:
            msg = "[!] Bot is already running! Cannot start a second process." if self.lang == "EN" else "[!] Bot zaten çalışıyor! İkinci bir süreç başlatılamaz."
            self.append_log(msg)
            return

        is_stage2_direct = bool(extra_args and "--stage2-only" in extra_args)

        # 1. BÜTÜN TUŞ ATAMA YERLERİ YAPILDI MI KONTROL ET
        if is_stage2_direct:
            # Doğrudan 2. Aşama için sadece Hero ve 8 Birlik slotu yeterlidir
            stage2_req = ["hero_slot"] + [f"troop_slot_{i}" for i in range(1, 9)]
            missing = self.get_missing_calibration_slots(required_keys=stage2_req)
        else:
            missing = self.get_missing_calibration_slots()

        if missing:
            self.show_missing_calibration_dialog(missing)
            return

        self.btn_main_start.configure(state="disabled", fg_color="#064e3b")
        self.btn_main_stop.configure(state="normal", fg_color="#e11d48")

        status_text = "● 2. AŞAMA DEVREDE" if is_stage2_direct else get_text("status_busy", self.lang)
        self.status_indicator.configure(text=status_text, image=self.status_dot_busy, text_color="#38bdf8")

        self.session_start = time.time()
        self.append_log("\n" + "="*55)
        self.append_log(">>> CLASH TITAN 2.0 • Created by Zodi4c")
        if is_stage2_direct:
            if self.lang == "EN":
                self.append_log(">>> DIRECT STAGE 2 ENGINE ACTIVATED (Hero + 8 Troops).")
                self.append_log(">>> Matchmaking skipped; deploying directly onto screen.")
                self.append_log(">>> Press 'q' anytime to emergency stop.")
            else:
                self.append_log(">>> DOĞRUDAN 2. AŞAMA MOTORU DEVREDE (Hero + 8 Birlik).")
                self.append_log(">>> Savaş arama adımları atlandı; ekrana doğrudan dökülüyor.")
                self.append_log(">>> Durdurmak için klavyeden 'q' tuşuna basabilirsiniz.")
        else:
            if self.lang == "EN":
                self.append_log(">>> Battle engine activated.")
                self.append_log(">>> Universal Emulator Support: Google Play Games, BlueStacks, LDPlayer, GameLoop, MEmu, Nox")
                self.append_log(">>> Press 'q' anytime to emergency stop.")
            else:
                self.append_log(">>> Saldırı motoru devrede.")
                self.append_log(">>> Evrensel Emülatör Desteği: Google Play Games, BlueStacks, LDPlayer, GameLoop, MEmu, Nox")
                self.append_log(">>> Durdurmak için klavyeden 'q' tuşuna basabilirsiniz.")
        self.append_log("="*55)

        # Oyun/Emülatör penceresini otomatik odaklamayı dene
        try:
            from vision import VisionDetector
            v = VisionDetector()
            rect = v.get_game_window_rect()
            if rect:
                self.append_log("[✓] Oyun penceresi tespit edildi ve odaklandı.")
        except Exception:
            pass

        def run_worker():
            proc = None
            try:
                cmd = [PYTHON_EXE, "-u", BOT_SCRIPT]
                if extra_args:
                    cmd.extend(extra_args)
                proc = subprocess.Popen(
                    cmd,
                    cwd=BASE_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
                self.bot_process = proc

                # Windows Global Donanım Düzeyinde Q / ESC Takipçisi (GUI Tarafı Acil Durdurma)
                # Oyun tam ekranda, başka pencerede veya yönetici modunda olsa dahi Windows kernelden yakalar
                def gui_hardware_q_watcher():
                    user32 = ctypes.windll.user32
                    while self.bot_process is not None and self.bot_process.poll() is None:
                        try:
                            # 0x51 = 'Q', 0x1B = ESC
                            if bool(user32.GetAsyncKeyState(0x51) & 0x8000) or bool(user32.GetAsyncKeyState(0x1B) & 0x8000):
                                try:
                                    user32.mouse_event(0x0004, 0, 0, 0, 0)
                                except Exception:
                                    pass
                                self.after(0, self.stop_bot)
                                break
                        except Exception:
                            pass
                        time.sleep(0.02)

                threading.Thread(target=gui_hardware_q_watcher, daemon=True).start()

                if proc.stdout:
                    while True:
                        line = proc.stdout.readline()
                        if not line and proc.poll() is not None:
                            break
                        if line:
                            self.after(0, self.append_log, line)

                if proc and proc.poll() is None:
                    proc.wait()
            except Exception as e:
                self.after(0, self.append_log, f"[ERROR/HATA] {e}")
            finally:
                self.bot_process = None
                self.after(0, self.on_bot_finished)

        threading.Thread(target=run_worker, daemon=True).start()

    def stop_bot(self):
        proc = self.bot_process
        if proc:
            # Fare takılı kalmasın: Windows donanım düzeyinde sol fareyi serbest bırak
            try:
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            except Exception:
                pass

            try:
                proc.terminate()
            except Exception:
                pass

            # Arka planda 100ms sonra hala kapanmadıysa kesinlikle zorla sonlandır (kill)
            def force_terminate(p):
                time.sleep(0.10)
                if p and p.poll() is None:
                    try:
                        p.kill()
                    except Exception:
                        pass
            threading.Thread(target=force_terminate, args=(proc,), daemon=True).start()

            msg = "[!] Bot stopped by user (Emergency 'Q')." if self.lang == "EN" else "[!] Bot kullanıcı tarafından durduruldu (Acil 'Q')."
            self.append_log(msg)
        self.on_bot_finished()

    def on_bot_finished(self):
        self.btn_main_start.configure(state="normal", fg_color="#10b981")
        self.btn_main_stop.configure(state="disabled", fg_color="#4c0519")
        self.status_indicator.configure(text=get_text("status_ready", self.lang), image=self.status_dot_ready, text_color="#34d399")
        msg = "[*] Session ended." if self.lang == "EN" else "[*] Oturum sona erdi."
        self.append_log(msg)


if __name__ == "__main__":
    app = LuxuryBotDashboard()
    app.mainloop()

