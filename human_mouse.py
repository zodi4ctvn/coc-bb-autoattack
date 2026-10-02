# -*- coding: utf-8 -*-
# Fare motoru - DirectInput + Bezier egrileri
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

import time
import math
import random
import ctypes
import pyautogui

from config import ANTI_BAN

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800

VK_CONTROL = 0x11
KEYEVENTF_KEYUP = 0x0002

user32 = ctypes.windll.user32
pyautogui.FAILSAFE = False

def get_jittered_point(x, y, radius=None):
    """Gauss dağılımıyla hedefin etrafına doğal piksel dağılımı uygular."""
    r = radius if radius is not None else ANTI_BAN.get("click_jitter_radius", 12)
    # Merkezde yoğunlaşan Gauss dağılımı (daha insani)
    dist = abs(random.gauss(0, r / 2.2))
    angle = random.uniform(0, 2 * math.pi)
    return int(x + dist * math.cos(angle)), int(y + dist * math.sin(angle))

def _bezier_point(p0, p1, p2, p3, t):
    """Kübik Bézier eğrisi formülü."""
    u = 1 - t
    tt = t * t
    uu = u * u
    return (
        int(uu * u * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + tt * t * p3[0]),
        int(uu * u * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + tt * t * p3[1])
    )

def fast_human_move(target_x, target_y):
    """
    Fareyi kavisli Bézier ivmesiyle taşır.
    %35 ihtimalle hedefi 4-10 piksel hafifçe aşıp geri düzeltir (Overshoot - İnsan taklidi).
    """
    start_pos = pyautogui.position()
    start_x, start_y = start_pos.x, start_pos.y

    dx = target_x - start_x
    dy = target_y - start_y
    dist = math.hypot(dx, dy)

    if dist < 15:
        user32.SetCursorPos(int(target_x), int(target_y))
        return

    # %35 İhtimalle hedefi biraz aşma (Overshoot)
    overshoot = False
    dest_x, dest_y = target_x, target_y
    if dist > 80 and random.random() < 0.35:
        overshoot = True
        ov_dist = random.uniform(5, 12)
        angle = math.atan2(dy, dx) + random.uniform(-0.25, 0.25)
        dest_x = target_x + int(ov_dist * math.cos(angle))
        dest_y = target_y + int(ov_dist * math.sin(angle))

    # Kavisli kontrol noktaları
    ctrl1_x = start_x + (dest_x - start_x) * random.uniform(0.2, 0.45) + random.randint(-20, 20)
    ctrl1_y = start_y + (dest_y - start_y) * random.uniform(0.2, 0.45) + random.randint(-20, 20)

    ctrl2_x = start_x + (dest_x - start_x) * random.uniform(0.55, 0.8) + random.randint(-18, 18)
    ctrl2_y = start_y + (dest_y - start_y) * random.uniform(0.55, 0.8) + random.randint(-18, 18)

    steps = max(8, min(14, int(dist / 40)))
    step_delay = random.uniform(0.012, 0.020)

    for i in range(1, steps + 1):
        t = i / steps
        smooth_t = t * t * (3 - 2 * t)
        bx, by = _bezier_point((start_x, start_y), (ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y), (dest_x, dest_y), smooth_t)
        user32.SetCursorPos(bx, by)
        time.sleep(step_delay)

    # Eğer aşıldıysa geri düzeltme hamlesi (Micro-correction)
    if overshoot:
        time.sleep(random.uniform(0.02, 0.04))
        user32.SetCursorPos(int(target_x), int(target_y))
    else:
        user32.SetCursorPos(int(target_x), int(target_y))

human_move = fast_human_move

def raw_mouse_click(press_time=None):
    """Windows donanım düzeyinde (DirectInput) sol tıklama."""
    if press_time is None:
        # İnsan basış süresi: Gauss dağılımı (~95ms ortalama)
        press_time = max(0.055, random.gauss(0.095, 0.018))

    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(press_time)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def human_click(x=None, y=None, jitter=True, delay_after=True):
    """Hedefe kavisle gider, insani mikro-duraksama yapar ve tıklar."""
    if x is not None and y is not None:
        target_x, target_y = (get_jittered_point(x, y) if jitter else (x, y))
        fast_human_move(target_x, target_y)

    # İnsani karar verme duraksaması (Micro-hesitation)
    time.sleep(max(0.025, random.gauss(0.045, 0.012)))
    raw_mouse_click()

    if delay_after:
        time.sleep(max(0.35, random.gauss(0.65, 0.12)))

def human_quick_tap(x, y):
    """Birlikleri bırakırken haritaya seri ve değişken hızda tıklar."""
    jx, jy = get_jittered_point(x, y, radius=16)
    user32.SetCursorPos(jx, jy)
    raw_mouse_click(press_time=random.uniform(0.075, 0.110))
    time.sleep(random.uniform(0.28, 0.38))

def idle_micro_drift():
    """Savaş izlenirken farenin robot gibi heykel kalmasını önleyen insani hafif gezinti."""
    pos = pyautogui.position()
    offset_x = random.randint(-18, 18)
    offset_y = random.randint(-18, 18)
    user32.SetCursorPos(pos.x + offset_x, pos.y + offset_y)

def random_delay(min_s=0.6, max_s=1.3):
    """Değişken bekleme."""
    time.sleep(random.uniform(min_s, max_s))

def human_scroll(delta=-360, with_ctrl=False):
    """
    Windows DirectInput donanım düzeyinde fare tekerlek hareketi.
    delta negatif: aşağı kaydırma (zoom out / küçültme)
    delta pozitif: yukarı kaydırma (zoom in / büyütme)
    with_ctrl: True ise Ctrl tuşu basılı tutularak kaydırılır (BlueStacks zoom modu).
    """
    if with_ctrl:
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.015)

    dw_data = ctypes.c_uint(int(delta)).value
    user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, dw_data, 0)

    if with_ctrl:
        time.sleep(0.015)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

def human_zoom_out(center_x=None, center_y=None, steps=8):
    """
    Köyün tamamını ekranda görebilmek için fareyi güvenli merkeze taşır
    ve fare tekerleğini sonuna kadar aşağı çekerek köyü en uzak mesafeye küçültür.
    """
    if center_x is None or center_y is None:
        try:
            w, h = pyautogui.size()
            center_x, center_y = w // 2, h // 2
        except Exception:
            center_x, center_y = 500, 400

    fast_human_move(int(center_x), int(center_y))
    # Eksen kaymasını ve harita sürükleme ataletini önlemek için imlecin tam durmasını bekle
    time.sleep(random.uniform(0.25, 0.35))

    # Saf DirectInput fare tekerleğiyle kademeli küçültme (Ctrl tuşu basılmaz, harita kayması önlenir)
    for _ in range(steps):
        human_scroll(delta=-360, with_ctrl=False)
        time.sleep(random.uniform(0.06, 0.10))

def human_drag(start_x, start_y, end_x, end_y, duration=0.55):
    """
    Kamerayı/haritayı kaydırmak için start noktasından end noktasına
    sol tuşa basılı tutarak pürüzsüz ve emülatörün tam algılayacağı bir sürükleme (drag/swipe) yapar.
    """
    try:
        user32.SetCursorPos(int(start_x), int(start_y))
        time.sleep(0.08)
        pyautogui.dragTo(int(end_x), int(end_y), duration=duration, button='left')
        time.sleep(0.20)
    except Exception:
        user32.SetCursorPos(int(start_x), int(start_y))
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.08)
        user32.SetCursorPos(int(end_x), int(end_y))
        time.sleep(0.08)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.20)



