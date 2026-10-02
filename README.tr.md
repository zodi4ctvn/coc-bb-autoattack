# Clash Titan 2.0 — Yan Köy Otomasyon Merkezi

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English-blue?style=for-the-badge)](README.md)
[![Language: Türkçe](https://img.shields.io/badge/Language-T%C3%BCrk%C3%A7e-red?style=for-the-badge)](README.tr.md)
[![Geliştirici](https://img.shields.io/badge/Geli%C5%9Ftirici-Zodi4c-10B981?style=for-the-badge)](https://github.com/Zodi4ctvn)

![Python Sürümü](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Arayüz](https://img.shields.io/badge/Aray%C3%BCz-CustomTkinter-10B981?style=for-the-badge)
![Lisans](https://img.shields.io/badge/Lisans-Ozel%20NC--Attribution-red?style=for-the-badge)
![Durum](https://img.shields.io/badge/Durum-G%C3%BCncel-success?style=for-the-badge)

**Tüm Android Emülatörleri (LDPlayer, BlueStacks, GameLoop, Google Play Games, MEmu, Nox vb.) için donanım düzeyinde, anti-ban korumalı otonom Builder Base 2.0 saldırı botu.**  
**Geliştirici: [Zodi4c](https://github.com/Zodi4ctvn).**

</div>


## Genel Bakışış


> [!NOTE]
> **Test Edilen Emülatör:** Bu bot yalnızca **Google Play Games (PC)** üzerinde test edilmiştir. Diğer emülatörler (LDPlayer, BlueStacks, MEmu vb.) teorik olarak uyumlu olmalıdır ancak **denenmemiştir**. Kullanım riski size aittir.
**Clash Titan 2.0**, Clash of Clans Yan Köy (Builder Base 2.0) için geliştirilmiş modern, donanım düzeyinde evrensel bir otomasyon yazılımıdır. **LDPlayer 9, BlueStacks 5, GameLoop, Google Play Games PC, MEmu Play, NoxPlayer, MuMu Player** ve Windows Subsystem for Android (WSA) dahil olmak üzere tüm platformlarla tam uyumludur. Oyun dosyalarına veya bellek alanlarına (RAM) müdahale etmez; işletim sistemi düzeyinde fiziksel fare hareketleri ve klavye sinyalleri üreterek tam insan simülasyonu uygular. **Türkçe ve İngilizce** tam çift dil desteğine sahiptir.

---

## Temel Özellikler

- **Evrensel Emülatör ve Oyun Desteği:** LDPlayer, BlueStacks, GameLoop, Google Play Games PC, MEmu, NoxPlayer, MuMu Player ve tüm Android pencere başlıklarını otomatik tanır, ön plana getirir ve kilitlenir.
- **Donanım Düzeyinde Giriş Motoru (DirectInput):** Windows `user32.mouse_event` API'si üzerinden donanım düzeyinde tıklama yapar. Tüm emülatörlerin yapay tıklama filtrelerini %100 aşar.
- **Biyometrik İnsan Faresi Simülasyonu:**
  - Kübik Bézier eğrileri ile hızlanma ve yavaşlama (ease-in / ease-out).
  - **Sapma ve Düzeltme (Overshoot & Correction):** İnsan eli gibi butonu %35 ihtimalle 4-10 piksel geçer ve milisaniyeler içinde geri toparlar.
  - **Gauss Dağılımı:** Tıklama süreleri ve tepki gecikmeleri rastgele değil, Gauss çan eğrisi standardındadır.
  - **Mikro Gezinme (Idle Micro-Drift):** Savaş izlenirken farenin hareketsiz kalmasını önleyerek AFK bot tespitlerini engeller.
- **Builder Base 2.0 İki Aşamalı Mimari:**
  - **Ayrı Slot Noktaları:** Hero ve 6 normal birlik yuvasına tek tek, sabit koordinatlarla basar; savaş ortasında asker yeteneklerini yanlışlıkla tetiklemez.
  - **Esnek 2. Aşama Geçişi:** İster süreye bağlı otomatik, ister `F2` kısayoluyla manuel geçiş imkanı.
  - **Erken Savaş Bitirme & Kupa/Ganimet Alma:** Savaş bittiğinde çıkan `Tamam / Eve Dön` ekranlarını çift tıklayarak loot'u kasaya aktarır.
- **Lüks CustomTkinter Kontrol Paneli:**
  - Vektörel SVG ikonlar (Windows emojileri yerine özel çizimler).
  - Özel Font Desteği: **Rajdhani** (Taktik HUD), **Orbitron** (Siber Fütüristik) ve **Outfit** (Minimalist Lüks).
  - **Dinamik Anti-Ban Risk Ölçer & Anlık Kayıt:** Ayarlar sekmesinde yapılan her değişiklik anında otomatik kaydedilir. Canlı risk analiz motoru, seçtiğiniz parametrelerin Supercell sunucu algoritmalarına karşı ban riskini canlı hesaplar (Yeşil / Sarı / Kırmızı göstergeler ve uyarılar). Tek tıkla **Önerilen Güvenli Ayarları Uygula** desteği mevcuttur.
  - Canlı fare koordinat paneli, oturum sayacı ve gerçek zamanlı saldırı istatistiği.
  - Sol tık veya `[SPACE]` ile kalibrasyon ve test tıklaması.
  - **Eksik Tuş Doğrulama Güvenliği:** 16 tuş noktasından herhangi biri eksikse savaşın başlatılmasını engeller, eksik noktaları şık bir uyarı penceresinde listeler ve kullanıcıyı doğrudan kalibrasyon sekmesine yönlendirir.
- **Genel Kısayollar:**
  - `q` — Acil Durdurma (Programı anında güvenle durdurur)
  - `p` — Duraklat / Devam Et
  - `F2` — 2. Aşamaya Manuel Geçiş (Takviyeleri hemen sahaya sürer)
  - `F3` — Savaşı Manuel Bitir (Erken biten savaşta hemen eve döner)

---

## Proje Dizini

```
coc-bb-autoattack/
├── ClashTitan.bat           # Tek tıkla çalıştırma ve otomatik kurulum betiği
├── main.py                  # Ana uygulama başlatıcı (GUI / CLI / Wizard)
├── gui.py                   # Lüks CustomTkinter kontrol paneli
├── bot.py                   # Ana savaş otomasyon motoru
├── locales.py               # Çift dilli lokalizasyon paketi (TR / EN)
├── human_mouse.py           # Donanım seviyesi DirectInput & Bézier fare motoru
├── icons.py                 # Vektörel ikon üretim motoru (supersampled)
├── vision.py                # OpenCV görsel eşleme modülü
├── setup_wizard.py          # Terminal kalibrasyon sihirbazı
├── config.py                # Merkezi strateji, anti-ban ve zamanlama ayarları
├── coordinates.example.json # Şablon kalibrasyon dosyası
├── coordinates.json         # Kullanıcıya ait kaydedilmiş ekran koordinatları
├── requirements.txt         # Gerekli Python kütüphaneleri
├── README.md                # İngilizce dokümantasyon
├── README.tr.md             # Türkçe dokümantasyon
├── .gitignore               # Git göz ardı kuralları
├── LICENSE                  # MIT açık kaynak lisansı
└── templates/               # Görsel şablon resimleri
```

---

## Kurulum

### Gereksinimler
- **İşletim Sistemi:** Windows 10 veya Windows 11 (64-bit)
- **Python:** Python 3.11 veya daha yenisi

### 1. Depoyu İndirin
```bash
git clone https://github.com/Zodi4ctvn/coc-bb-autoattack.git
cd coc-bb-autoattack
```

### 2. Kütüphaneleri Yükleyin
```bash
python -m pip install -r requirements.txt
```

---

## Hızlı Başlangıç

### Grafik Arayüzünü Başlatma (Önerilen)
Masaüstündeki **"Clash Yan Koy Botu"** kısayoluna veya **`ClashTitan.bat`** dosyasına çift tıklayın. Ya da terminalden:
```bash
python main.py
```

### Terminal (Arka Plan) Modu
```bash
python main.py --cli
```

### Hızlı Terminal Kalibrasyonu
```bash
python main.py --wizard
```

---

## Kalibrasyon Adımları

1. Oyun/Emülatör uygulamanızı (LDPlayer, BlueStacks, GameLoop, Google Play Games vb.) açın ve Clash of Clans Yan Köy ekranına gelin.
2. **Clash Titan 2.0** panelini açıp **Slot & Kalibrasyon** sekmesine geçin.
3. Her kutucuk için:
   - **`Kaydet`** butonuna basın.
   - Fareyi oyun ekranındaki ilgili butonun veya slotun üzerine götürün.
   - **`Sol Tık`** yapın veya klavyeden **`[SPACE]`** tuşuna basın (nokta kaydedilir ve bip sesi çalar).
   - *(İptal etmek için klavyeden **`[ESC]`** tuşuna basabilir veya butona tekrar tıklayabilirsiniz).*
4. **`Test`** butonuna basarak farenin o noktaya tıkladığını doğrulayın.
5. **Kontrol Merkezi** sekmesine dönüp **`SAVAŞI BAŞLAT`** butonuna tıklayın.

---

## Dil ve Tema Seçimi

- **Dil Değiştirme:** Sol menüdeki **`[ TR | EN ]`** hap butonuna tıklayarak arayüzü anında Türkçe veya İngilizce yapabilirsiniz.
- **Font Teması:** **Anti-Ban & Strateji** sekmesinden yazı karakterini **Taktik HUD (Rajdhani)**, **Siber Glitch (Orbitron)** veya **Minimalist Lüks (Outfit)** olarak canlı değiştirebilirsiniz.

---

## Sorumluluk Reddi (Fair Play Uyarısı)

> [!WARNING]
> Bu yazılım yalnızca **eğitim, araştırma ve arayüz otomasyon testleri** amacıyla hazırlanmıştır. Clash of Clans oyununda üçüncü parti otomasyon araçlarının kullanılması Supercell Hizmet Şartları'na (Terms of Service) aykırıdır. Doğabilecek hesap kısıtlamalarından kullanıcı sorumludur.

---

## Geliştirici & Yazar

Bu proje **[Zodi4c](https://github.com/Zodi4ctvn)** tarafından geliştirilmiş ve yayınlanmıştır.  
Soru, öneri ve hata bildirimleri için GitHub üzerinden Issue açabilirsiniz.

---

## Lisans

[![Lisans: Ozel NC-Attribution](https://img.shields.io/badge/Lisans-Ozel%20NC--Attribution-red?style=for-the-badge)](LICENSE)

Bu proje **Ozel Ticari Olmayan Atif Lisansi** ile lisanslanmistir.

**Temel kisitlamalar:**
- Kisisel ve egitim amacli kullanim serbesttir
- Ticari kullanim **yasaktir**
- Zodi4c yazar bilgisini silmek veya degistirmek **yasaktir**
- Projeyi kendi projeniz olarak dagitmak **yasaktir**
- Baska bir lisans altinda yayimlamak **yasaktir**

Tam metin icin [LICENSE](LICENSE) dosyasina bakiniz.


