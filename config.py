# -*- coding: utf-8 -*-
# Clash Titan 2.0 - yapilandirma dosyasi
# @author: Zodi4c  |  github.com/Zodi4ctvn
# [INTEGRITY] Bu satir silinirse program baslamaz. / Removing this line will prevent the program from starting.
# Lisans: Custom Non-Commercial Attribution License (bkz. LICENSE)

WINDOW_TITLE_KEYWORDS = [
    "Clash of Clans",
    "Google Play Games",
    "BlueStacks",
    "LDPlayer",
    "GameLoop",
    "MEmu",
    "NoxPlayer",
    "Nox",
    "MuMu",
    "MuMuPlayer",
    "WSA",
    "SmartGaGa"
]

# Anti-Ban / İnsan Benzeri Davranış Ayarları
ANTI_BAN = {
    # Fare hareket süreleri (saniye)
    "mouse_move_duration_min": 0.20,
    "mouse_move_duration_max": 0.40,
    
    # Buton/Harita tıklama basılı kalma süresi (ms)
    "click_press_duration_min": 0.07,
    "click_press_duration_max": 0.13,
    
    # Tıklama rastgele piksel sapması (Sadece harita kenarları için)
    "click_jitter_radius": 12,
    
    # Eylemler arası doğal bekleme (saniye)
    "action_delay_min": 0.6,
    "action_delay_max": 1.2,
    
    # Birlik bırakma sırasındaki tıklama aralıkları
    "deploy_delay_min": 0.24,
    "deploy_delay_max": 0.35,
    
    # Mola Sistemi: Her kaç saldırıda bir dinlensin?
    "attacks_before_break": 11,           # Her 10-12 saldırıda bir
    "break_duration_min_seconds": 120,    # 2 dakika
    "break_duration_max_seconds": 180,    # 3 dakika
}

# 2 Aşamalı Savaş Stratejisi
BATTLE_SETTINGS = {
    # 1. Aşama Birlikleri: 6 Birlik Slotu + 1 Hero Slotu
    "stage1_troop_slots": 6,
    "has_hero": True,
    
    # Her birlik slotu seçildikten sonra haritaya kaç kez basılsın? (Tüm birliği dökmek için 4 tık)
    "clicks_per_troop_slot": 4,
    
    # Yetenek Karışıklığını Önleme:
    # Birliklerin özel yeteneklerine basılmaması için savaş ortasında slotlara tıklama kapalıdır.
    "auto_hero_ability": False,
    
    # 2. Aşama Ayarları:
    # "AUTO" -> Otomatik olarak 'stage2_wait_seconds' (90 sn) sonra atar.
    # "MANUAL" -> Sadece sen F2 tuşuna veya paneldeki '2. Aşamaya Geç' butonuna basınca atar!
    "stage2_mode": "AUTO",
    "stage2_wait_seconds": 75,           # 1. aşama bitişi / 2. aşamaya otomatik geçiş süresi (75 saniye)
    "stage2_finish_wait_seconds": 50,    # 2. aşamada birlikler atıldıktan sonra savaşı bitirip köye dönmeden önceki bekleme süresi (50 saniye)
    "stage2_reinforcement_slots": 2,
    
    # Maksimum savaş bekleme süresi (saniye)
    "max_battle_duration_seconds": 180,
}

# Şablon Görsel Eşleşme Güven Oranı
VISION_CONFIDENCE = 0.75

# Kısayollar
HOTKEYS = {
    "stop": "q",              # Acil Durdurma: 'q'
    "pause": "p",             # Duraklat / Devam Et: 'p'
    "manual_stage2": "f2",    # 2. Aşamaya Manuel Geçiş: 'F2'
    "manual_finish": "f3",    # Savaşı Manuel Bitir: 'F3'
}

# Varsayılan Dil ("TR" veya "EN")
DEFAULT_LANGUAGE = "TR"




