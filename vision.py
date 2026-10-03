# -*- coding: utf-8 -*-
# Goruntu isleme modulu - OpenCV tabanli
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

import os
import cv2
import numpy as np
import pyautogui
from config import VISION_CONFIDENCE, WINDOW_TITLE_KEYWORDS

# Windows API için pencere yakalama (pywin32)
try:
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    win32gui = None
    win32con = None
    HAS_WIN32 = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

class VisionDetector:
    def __init__(self, templates_dir=None):
        self.templates_dir = templates_dir if templates_dir is not None else DEFAULT_TEMPLATES_DIR
        self.cached_templates = {}
        self.load_templates()

    def load_templates(self):
        """templates klasöründeki tüm png dosyalarını önbelleğe alır."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            return

        for filename in os.listdir(self.templates_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                name = os.path.splitext(filename)[0]
                filepath = os.path.join(self.templates_dir, filename)
                # BGR formatında yükle
                template_img = cv2.imread(filepath)
                if template_img is not None:
                    self.cached_templates[name] = template_img

    def get_all_detected_emulators(self):
        """Açık olan tüm Android emülatörlerini (Google Play Games, BlueStacks, LDPlayer, GameLoop vb.) listeler."""
        if not HAS_WIN32 or win32gui is None:
            return []

        emulators = []
        def enum_windows_callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).strip()
                if title:
                    for keyword in WINDOW_TITLE_KEYWORDS:
                        if keyword.lower() in title.lower():
                            rect = win32gui.GetWindowRect(hwnd)
                            w = rect[2] - rect[0]
                            h = rect[3] - rect[1]
                            if w > 250 and h > 250:
                                emulators.append({
                                    "hwnd": hwnd,
                                    "title": title,
                                    "type": keyword,
                                    "rect": (rect[0], rect[1], w, h)
                                })
                                break
            return True

        try:
            win32gui.EnumWindows(enum_windows_callback, None)
        except Exception:
            pass
        return emulators

    def get_game_window_rect(self):
        """
        Oyun/Emülatör penceresini (Google Play Games, BlueStacks, LDPlayer, GameLoop vb.) bulur ve odaklar.
        Dönüş: (left, top, width, height) veya bulunamazsa None
        """
        emulators = self.get_all_detected_emulators()
        if not emulators:
            return None

        # Clash of Clans başlığını içeren pencere varsa önceliklendir
        coc_window = next((e for e in emulators if "clash" in e["title"].lower()), emulators[0])
        hwnd = coc_window["hwnd"]
        rect = coc_window["rect"]

        # Pencereyi boyutunu ve konumunu bozmadan öne getir
        if HAS_WIN32 and win32gui and win32con:
            try:
                # Eğer pencere simge durumuna küçültülmüşse (minimized) geri yükle; 
                # aksi halde mevcut boyutunu (büyütülmüş veya özel boyutlandırılmış) asla bozma!
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                else:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass

        return rect

    def capture_screen(self, region=None):
        """Ekran görüntüsü alır ve OpenCV BGR formatında döndürür."""
        try:
            screenshot = pyautogui.screenshot(region=region)
            img_np = np.array(screenshot)
            return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        except Exception:
            try:
                from PIL import ImageGrab
                bbox = (region[0], region[1], region[0] + region[2], region[1] + region[3]) if region else None
                screenshot = ImageGrab.grab(bbox=bbox)
                img_np = np.array(screenshot)
                return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"[Vision Error] Screen grab failed: {e}")
                return None

    def find_template(self, template_name, region=None, confidence=None, multi_scale=True, return_best_score=False):
        """
        Şablon görselini ekranda arar.
        Farklı pencere ve ekran boyutlarını tolere etmek için multi-scale (0.25x - 1.30x) ve
        hem renkli hem gri tonlama (grayscale) taraması yapar.
        Dönüş: Bulunursa (merkez_x, merkez_y, eşleşme_skoru) veya (return_best_score=True ise (None, None, best_val))
        """
        if template_name not in self.cached_templates:
            filepath = os.path.join(self.templates_dir, f"{template_name}.png")
            if os.path.exists(filepath):
                self.cached_templates[template_name] = cv2.imread(filepath)
            else:
                return (None, None, 0.0) if return_best_score else None

        template = self.cached_templates[template_name]
        screen = self.capture_screen(region=region)
        if screen is None:
            return (None, None, 0.0) if return_best_score else None

        conf_threshold = confidence if confidence is not None else VISION_CONFIDENCE

        # UI Butonları (Eve Dön, Tamam, Topla, Kapat) sabit arayüz öğeleridir; harita gibi minyatür boyutlara (0.28x) küçülemez!
        is_ui_element = any(k in template_name for k in ["return_home", "ok_button", "collect_button", "close_button"])

        if is_ui_element:
            # Sadece doğal buton boyutları (±%20)
            scales = [1.0, 0.90, 0.80, 1.10, 1.20] if multi_scale else [1.0]
            # UI butonları için minimum güvenli eşik en az 0.72 olmalı
            if confidence is None:
                conf_threshold = 0.75
        else:
            # Harita içi öğeler (araba, iksir) zoom seviyesine göre minyatürleşebilir
            scales = [1.0, 0.90, 0.80, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 1.15] if multi_scale else [1.0]

        best_match = None
        best_val = -1.0

        sh, sw = screen.shape[:2]
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        for scale in scales:
            if scale != 1.0:
                new_w = int(template.shape[1] * scale)
                new_h = int(template.shape[0] * scale)
                if new_w >= sw or new_h >= sh or new_w < 20 or new_h < 20:
                    continue
                resized_gray = cv2.resize(gray_template, (new_w, new_h), interpolation=cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR)
            else:
                resized_gray = gray_template

            th, tw = resized_gray.shape[:2]
            if th >= sh or tw >= sw:
                continue

            result = cv2.matchTemplate(gray_screen, resized_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > best_val:
                center_x = max_loc[0] + tw // 2
                center_y = max_loc[1] + th // 2
                if region:
                    center_x += region[0]
                    center_y += region[1]

                # UI öğeleri için ek renk doğrulaması (çim veya can barı yanlış eşleşmesini engeller)
                valid = True
                if is_ui_element and max_val >= conf_threshold:
                    try:
                        # Ekrandaki bölgenin renkli görüntüsünü al
                        x1 = max(0, max_loc[0])
                        y1 = max(0, max_loc[1])
                        crop_scr = screen[y1:y1+th, x1:x1+tw]
                        resized_bgr = cv2.resize(template, (tw, th)) if scale != 1.0 else template
                        res_bgr = cv2.matchTemplate(crop_scr, resized_bgr, cv2.TM_CCOEFF_NORMED)
                        bgr_score = float(res_bgr[0][0]) if res_bgr.size > 0 else 0.0
                        if bgr_score < 0.65:
                            valid = False
                    except Exception:
                        pass

                if valid:
                    best_val = max_val
                    best_match = (center_x, center_y, max_val)

            if best_val >= 0.88:
                break

        if best_match and best_match[2] >= conf_threshold:
            return best_match

        if return_best_score:
            return (best_match[0] if best_match else None, best_match[1] if best_match else None, max(0.0, best_val))

        return None

    def find_all_matches(self, template_name, region=None, confidence=None, max_matches=5):
        """
        Belirli bir şablonun ekrandaki TÜM eşleşmelerini (örn. birden fazla iksir balonu) bulur.
        Dönüş: [{"x": x, "y": y, "score": score}, ...]
        """
        if template_name not in self.cached_templates:
            filepath = os.path.join(self.templates_dir, f"{template_name}.png")
            if os.path.exists(filepath):
                self.cached_templates[template_name] = cv2.imread(filepath)
            else:
                return []

        template = self.cached_templates[template_name]
        th, tw = template.shape[:2]
        screen = self.capture_screen(region=region)
        conf_threshold = confidence if confidence is not None else VISION_CONFIDENCE

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        y_locs, x_locs = np.where(result >= conf_threshold)

        matches = []
        for x, y in zip(x_locs, y_locs):
            score = float(result[y, x])
            center_x = int(x + tw // 2)
            center_y = int(y + th // 2)
            if region:
                center_x += region[0]
                center_y += region[1]

            # Yakın mükerrer pikselleri filtrele
            is_dup = any(abs(m["x"] - center_x) < 28 and abs(m["y"] - center_y) < 28 for m in matches)
            if not is_dup:
                matches.append({"name": template_name, "x": center_x, "y": center_y, "score": score})
                if len(matches) >= max_matches:
                    break

        return matches

    def find_resource_targets(self, confidence=0.72):
        """
        templates/ klasöründe bulunan tüm iksir, araba veya ganimet şablonlarını ekranda arar.
        Bulunan tüm benzersiz hedefleri liste olarak döndürür.
        """
        self.load_templates()
        targets = []
        for name in list(self.cached_templates.keys()):
            if any(k in name.lower() for k in ["elixir", "iksir", "loot", "cart", "araba", "bubble", "depo", "topla"]):
                found = self.find_all_matches(name, confidence=confidence)
                for item in found:
                    is_dup = any(abs(t["x"] - item["x"]) < 32 and abs(t["y"] - item["y"]) < 32 for t in targets)
                    if not is_dup:
                        targets.append(item)
        return targets

    def capture_and_save_template(self, template_name, center_x, center_y, crop_size=64):
        """
        Belirtilen pikselin etrafından bir kare kırparak templates/{template_name}.png olarak kaydeder.
        """
        half = crop_size // 2
        scr_w, scr_h = pyautogui.size()
        x1 = max(0, int(center_x - half))
        y1 = max(0, int(center_y - half))
        w = min(scr_w - x1, crop_size)
        h = min(scr_h - y1, crop_size)

        screen = self.capture_screen(region=(x1, y1, w, h))
        out_path = os.path.join(self.templates_dir, f"{template_name}.png")
        cv2.imwrite(out_path, screen)
        self.cached_templates[template_name] = screen
        return out_path

    def exists(self, template_name, region=None, confidence=None):
        """Şablonun ekranda var olup olmadığını boolean döndürür."""
        res = self.find_template(template_name, region, confidence)
        return res is not None

