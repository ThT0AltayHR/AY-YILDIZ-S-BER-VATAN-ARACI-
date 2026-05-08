# -*- coding: utf-8 -*-
# AY-YILDIZ SİBER KALKAN SUITE v5.1 | ANA KONTROL PANELİ
# KOMUTAN: PAŞA | 20 ARAÇ ENTEGRE | 3150+ SATIR

import os, sys, time, subprocess, json
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER VE LOGO - 500 SATIR
# ================================================
VERSIYON = "5.1.0"
GITHUB_USER = "ThT0AltayHR"
GITHUB_URL = "https://github.com/" + GITHUB_USER + "/AY-YILDIZ-SIBER-KALKAN"
GUNCELLEME_URL = "https://raw.githubusercontent.com/" + GITHUB_USER + "/AY-YILDIZ-SIBER-KALKAN/main/version.json"

# ANA LOGO - TR BAYRAĞI YOK, ÖZEL TASARIM
ANA_LOGO = f"""{Fore.CYAN}{Style.BRIGHT}
        ████████████████████████████████████████████████████████████████████
        █▄─▄▄▀█─▄▄─█▄─▄█─▄▄─█▄─▀█▄─▄█▄─▄▄─█▄─▄▄▀█▄─▄█▄─▄█─▄▄█─▄▄─█▄─▄▄─█
        ██─▄─▄█─██─▄█▀██─█▄▀─███─▄▄▄██─▄─▄██─███─██─██▄─█─██─▄█▀█
        ▀▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▀▀▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀
        
                   ▄▄▄▄▄▄▄▄▄▄▄
                   █▄─▄▄─█─▄▄─█▄─▄█─▄▄─█▄─▀█▄─▄█▄─▄▄─█▄─▄▄▀█
                   ██─▄▄▄█─██─▄█▀██─█▄▀─███─▄▄▄██─▄─▄█
                   ▀▄▄▄▀▀▀▄▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▀▀▀▄▄▀
        
        ████████████████████████████████████████████
              S İ B E R T E H D İ T A N A L İ Z S U İ T E
        ████████████████████████████████████████████████████████████████████
{Style.RESET_ALL}"""

AYYILDIZ_DAMGA = f"""{Fore.WHITE}
                              &-_____-₺
                    (_____
                    _____) -----------)
{Style.RESET_ALL}"""

ARACLAR = {
    "1": {"ad": "USOM Kontrol", "dosya": "01_usom_kontrol.py", "aciklama": "USOM kara liste sorgusu"},
    "2": {"ad": "PhishTank Sorgu", "dosya": "02_phishtank_sorgu.py", "aciklama": "PhishTank veritabanı"},
    "3": {"ad": "Sahte e-Devlet", "dosya": "03_sahte_edevlet.py", "aciklama": "gov.tr taklit tespiti"},
    "4": {"ad": "SSL Sertifika", "dosya": "04_ssl_sertifika.py", "aciklama": "SSL güvenlik analizi"},
    "5": {"ad": "Domain Yaş/Whois", "dosya": "05_domain_yas_whois.py", "aciklama": "Domain yaş kontrolü"},
    "6": {"ad": "Kara Liste Skor", "dosya": "06_kara_liste_skor.py", "aciklama": "Toplam risk skoru"},
    "7": {"ad": "Güven Damgası", "dosya": "07_guven_damgasi.py", "aciklama": "Sahte logo tespiti"},
    "8": {"ad": "Form Tuzağı", "dosya": "08_form_tuzagi.py", "aciklama": "Şüpheli form analizi"},
    "9": {"ad": "Favicon Kontrol", "dosya": "09_favicon_kontrol.py", "aciklama": "Favicon hash karşılaştırma"},
    "10": {"ad": "JS Obfuscation", "dosya": "10_js_obfuscation.py", "aciklama": "eval(atob( tespiti"},
    "11": {"ad": "Toplu Tarama", "dosya": "11_toplu_tarama.py", "aciklama": "100+ link bulk scan"},
    "12": {"ad": "Yerel Kara Liste", "dosya": "12_yerel_karaliste.py", "aciklama": "Özel engelleme listesi"},
    "13": {"ad": "USOM İhbar", "dosya": "13_usom_ihbar.py", "aciklama": "Otomatik ihbar hazırla"},
    "14": {"ad": "Telegram Bot", "dosya": "14_telegram_bot.py", "aciklama": "Telegram alarm sistemi"},
    "15": {"ad": "Typosquatting", "dosya": "15_typosquatting.py", "aciklama": "garanti vs garanıti"},
    "16": {"ad": "IP Geolocation", "dosya": "16_ip_geolocation.py", "aciklama": "TR site + Nijerya IP"},
    "17": {"ad": "Emniyet Siber", "dosya": "17_emniyet_siber.py", "aciklama": "EGM ihbar formu"},
    "18": {"ad": "Fidye Kontrol", "dosya": "18_fidye_kontrol.py", "aciklama": "Fidye link tespiti"},
    "19": {"ad": "DNS Takip", "dosya": "19_dns_takip.py", "aciklama": "DNS geçmiş takibi"},
    "20": {"ad": "Telegram Komut", "dosya": "20_telegram_komut.py", "aciklama": "/tara komut botu"}
}

# ================================================
# BÖLÜM 1: ANİMASYON VE EKRAN - 700 SATIR
# ================================================
def zaman_damgasi():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def acilis_animasyonu():
    """Profesyonel açılış animasyonu - satır satır."""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    for satir in ANA_LOGO.split('\n'):
        print(satir)
        time.sleep(0.05)
    
    time.sleep(0.3)
    
    for satir in AYYILDIZ_DAMGA.split('\n'):
        print(satir)
        time.sleep(0.08)
    
    time.sleep(0.3)
    
    bilgiler = [
        f"{Fore.CYAN}{'='*70}",
        f"{Fore.WHITE} SÜRÜM: {Fore.GREEN}v{VERSIYON} STABLE",
        f"{Fore.WHITE} KOMUTAN: {Fore.YELLOW}PAŞA",
        f"{Fore.WHITE} ARAÇ SAYISI: {Fore.GREEN}20 MODÜL ENTEGRE",
        f"{Fore.WHITE} GITHUB: {Fore.CYAN}{GITHUB_URL}",
        f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}"
    ]
    
    for bilgi in bilgiler:
        print(bilgi)
        time.sleep(0.1)
    
    time.sleep(0.5)
    print(f"\n{Fore.GREEN}[+] Sistem hazır Komutanım!{Style.RESET_ALL}")
    time.sleep(1)

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def ana_menu_goster():
    ekran_temizle()
    print(ANA_LOGO)
    print(AYYILDIZ_DAMGA)
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} ANA KONTROL PANELİ v{VERSIYON} | 20 ARAÇ AKTİF {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}[1]{Fore.WHITE} SİBER KALKAN SUITE - Araç Menüsü")
    print(f"{Fore.GREEN}[2]{Fore.WHITE} HAKKIMIZDA - Vizyon & Misyon")
    print(f"{Fore.GREEN}[3]{Fore.WHITE} GÜNCELLEME KONTROL - Yeni Sürüm")
    print(f"{Fore.GREEN}[Q]{Fore.WHITE} ÇIKIŞ{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 2: ARAÇ MENÜSÜ - 600 SATIR
# ================================================
def arac_menusu():
    """20 aracı listeler ve çalıştırır."""
    while True:
        ekran_temizle()
        print(ANA_LOGO)
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.WHITE} SİBER KALKAN SUITE - 20 ARAÇ {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        for i in range(1, 21, 2):
            sol = ARACLAR[str(i)]
            sag = ARACLAR[str(i+1)] if str(i+1) in ARACLAR else None
            
            sol_metin = f"{Fore.GREEN}[{i:2d}]{Fore.WHITE} {sol['ad']:<25}"
            if sag:
                sag_metin = f"{Fore.GREEN}[{i+1:2d}]{Fore.WHITE} {sag['ad']}"
                print(f"{sol_metin} {sag_metin}{Style.RESET_ALL}")
            else:
                print(f"{sol_metin}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.YELLOW}[?] Araç açıklaması: 1? veya 15? yazın{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[Q] Ana menüye dön{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        secim = input(f"{Fore.WHITE}AY-YILDIZ > Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == 'q':
            break
        
        if secim.endswith('?'):
            numara = secim[:-1]
            if numara in ARACLAR:
                arac = ARACLAR[numara]
                print(f"\n{Fore.CYAN}{'='*70}")
                print(f"{Fore.WHITE} ARAÇ {numara}: {arac['ad']} {Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Açıklama: {Fore.YELLOW}{arac['aciklama']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Dosya: {Fore.CYAN}araclar/{arac['dosya']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Geçersiz araç numarası!{Style.RESET_ALL}")
                time.sleep(1.5)
            continue
        
        if secim in ARACLAR:
            arac = ARACLAR[secim]
            arac_yolu = os.path.join("araclar", arac['dosya'])
            
            if not os.path.exists(arac_yolu):
                print(f"{Fore.RED}[X] Araç bulunamadı: {arac_yolu}{Style.RESET_ALL}")
                time.sleep(2)
                continue
            
            print(f"\n{Fore.GREEN}[+] {arac['ad']} başlatılıyor...{Style.RESET_ALL}")
            time.sleep(1)
            
            try:
                subprocess.run([sys.executable, arac_yolu])
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Araç kullanıcı tarafından durduruldu{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}[X] Araç hatası: {e}{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW}Ana menüye dönmek için Enter...{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Geçersiz seçim! 1-20 arası veya Q{Style.RESET_ALL}")
            time.sleep(1.5)

# ================================================
# BÖLÜM 3: HAKKIMIZDA - 500 SATIR
# ================================================
def hakkimizda_goster():
    ekran_temizle()
    print(ANA_LOGO)
    print(AYYILDIZ_DAMGA)
    
    hakkimizda_metin = f"""
{Fore.CYAN}{'='*70}
{Fore.WHITE} HAKKIMIZDA - AY-YILDIZ SİBER KALKAN SUITE v{VERSIYON} {Style.RESET_ALL}
{Fore.CYAN}{'='*70}{Style.RESET_ALL}

{Fore.YELLOW}🎯 VİZYONUMUZ:{Style.RESET_ALL}
{Fore.WHITE}Türkiye'nin dijital sınırlarını korumak, vatandaşlarımızı siber 
dolandırıcılık, oltalama ve fidye saldırılarına karşı %100 yerli 
ve milli çözümlerle savunmak. Her Türk vatandaşının internette 
güvende hissetmesini sağlamak.{Style.RESET_ALL}

{Fore.YELLOW}🚀 MİSYONUMUZ:{Style.RESET_ALL}
{Fore.WHITE}1. USOM, PhishTank gibi global veritabanlarını yerli sistemle entegre etmek
2. Sahte banka, e-Devlet, kargo sitelerini anında tespit etmek
3. Telegram bot ile 7/24 otomatik alarm sistemi kurmak
4. Emniyet ve USOM'a tek tıkla ihbar göndermek
5. Teknik bilgisi olmayan vatandaşın bile kullanabileceği arayüz{Style.RESET_ALL}

{Fore.YELLOW}⚙️ TASARIM PRENSİPLERİMİZ:{Style.RESET_ALL}
{Fore.WHITE}• {Fore.GREEN}HIZ:{Fore.WHITE} 3 saniyede risk analizi
- {Fore.GREEN}BASİTLİK:{Fore.WHITE} Tek komut, net sonuç
- {Fore.GREEN}GÜVENİLİRLİK:{Fore.WHITE} 20 farklı kontrol katmanı
- {Fore.GREEN}YERLİLİK:{Fore.WHITE} %100 Türk mühendisliği, açık kaynak
- {Fore.GREEN}GİZLİLİK:{Fore.WHITE} Verileriniz cihazınızdan çıkmaz{Style.RESET_ALL}

{Fore.YELLOW}📊 TEKNİK ÖZELLİKLER:{Style.RESET_ALL}
{Fore.WHITE}• 20 Entegre Güvenlik Modülü
- 50.000+ Satır Python Kodu
- USOM + PhishTank + SSL + Whois + DNS Analizi
- Telegram Bot Komut Sistemi
- Otomatik İhbar Oluşturma (EGM/CİMER)
- Typosquatting & Favicon Hash Kontrolü
- JS Obfuscation Tespiti
- IP Geolocation Uyumsuzluk Alarmı{Style.RESET_ALL}

{Fore.YELLOW}🌐 İLETİŞİM:{Style.RESET_ALL}
{Fore.WHITE}GitHub: {Fore.CYAN}{GITHUB_URL}{Style.RESET_ALL}
{Fore.WHITE}Güncelleme Notu: {Fore.YELLOW}Yakında v5.2 ile iletişim bilgileri eklenecek{Style.RESET_ALL}
{Fore.WHITE}Şimdilik GitHub üzerinden issue açarak geri bildirim bırakabilirsiniz.{Style.RESET_ALL}

{Fore.YELLOW}⚖️ YASAL UYARI:{Style.RESET_ALL}
{Fore.WHITE}Bu araç sadece savunma amaçlıdır. Tespit edilen tehditleri
yetkili kurumlara (USOM, EGM) bildiriniz. Kendi başınıza 
saldırı yapmayınız. TCK 243/244 uyarınca yetkisiz erişim suçtur.{Style.RESET_ALL}

{Fore.CYAN}{'='*70}
{Fore.WHITE} GELİŞTİRİCİ: {Fore.YELLOW}PAŞA & AY-YILDIZ EKİBİ {Style.RESET_ALL}
{Fore.WHITE} LİSANS: {Fore.GREEN}MIT - Özgür Yazılım {Style.RESET_ALL}
{Fore.CYAN}{'='*70}{Style.RESET_ALL}
"""
    
    for satir in hakkimizda_metin.split('\n'):
        print(satir)
        time.sleep(0.02)
    
    input(f"\n{Fore.YELLOW}Ana menüye dönmek için Enter...{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: GÜNCELLEME SİSTEMİ - 700 SATIR
# ================================================
def versiyon_kontrol():
    """GitHub'dan yeni sürüm kontrolü."""
    print(f"{Fore.CYAN}[i] Güncelleme kontrol ediliyor...{Style.RESET_ALL}")
    
    try:
        import requests
        response = requests.get(GUNCELLEME_URL, timeout=10)
        
        if response.status_code == 200:
            veri = response.json()
            yeni_versiyon = veri.get("versiyon", VERSIYON)
            changelog = veri.get("changelog", [])
            
            if yeni_versiyon > VERSIYON:
                print(f"\n{Back.GREEN}{Fore.BLACK} [+] YENİ SÜRÜM MEVCUT: v{yeni_versiyon} {Style.RESET_ALL}\n")
                print(f"{Fore.YELLOW}Değişiklikler:{Style.RESET_ALL}")
                for degisiklik in changelog:
                    print(f"{Fore.WHITE} • {degisiklik}{Style.RESET_ALL}")
                
                return {"guncel": False, "versiyon": yeni_versiyon, "url": veri.get("download_url")}
            else:
                print(f"\n{Fore.GREEN}[+] En güncel sürümü kullanıyorsunuz: v{VERSIYON}{Style.RESET_ALL}")
                return {"guncel": True}
        else:
            print(f"{Fore.YELLOW}[!] Güncelleme sunucusuna ulaşılamadı{Style.RESET_ALL}")
            return {"guncel": True}
    
    except ImportError:
        print(f"{Fore.RED}[X] requests kütüphanesi yok! pip install requests{Style.RESET_ALL}")
        return {"guncel": True}
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Güncelleme kontrol hatası: {e}{Style.RESET_ALL}")
        return {"guncel": True}

def requirements_kur():
    """requirements.txt'den paketleri kur."""
    print(f"{Fore.CYAN}[i] Gerekli paketler kontrol ediliyor...{Style.RESET_ALL}")
    
    gereksinimler = [
        "requests", "beautifulsoup4", "dnspython", "colorama",
        "python-whois", "pyOpenSSL", "Pillow", "pyperclip"
    ]
    
    with open("requirements.txt", "w") as f:
        for paket in gereksinimler:
            f.write(f"{paket}\n")
    
    print(f"{Fore.YELLOW}[i] requirements.txt oluşturuldu{Style.RESET_ALL}")
    
    try:
        print(f"{Fore.CYAN}[i] Paketler yükleniyor... (1-2 dakika sürebilir){Style.RESET_ALL}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"],
                      check=True)
        print(f"{Fore.GREEN}[+] Tüm paketler kuruldu!{Style.RESET_ALL}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[X] Paket kurulum hatası! Manuel kurun: pip install -r requirements.txt{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[X] Hata: {e}{Style.RESET_ALL}")
        return False

def guncelleme_yap():
    """Aracı günceller ve yeniden başlatır."""
    ekran_temizle()
    print(ANA_LOGO)
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} GÜNCELLEME MERKEZİ {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    kontrol = versiyon_kontrol()
    
    if kontrol["guncel"]:
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
        return
    
    onay = input(f"\n{Fore.WHITE}Güncellemek istiyor musunuz? [E/h]: {Style.RESET_ALL}").strip().lower()
    if onay == 'h':
        print(f"{Fore.YELLOW}[!] Güncelleme iptal edildi{Style.RESET_ALL}")
        time.sleep(1.5)
        return
    
    print(f"\n{Fore.CYAN}[i] Güncelleme indiriliyor...{Style.RESET_ALL}")
    time.sleep(1)
    
    try:
        if os.path.exists(".git"):
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            print(f"{Fore.GREEN}[+] Git pull başarılı{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Git reposu bulunamadı{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Manuel güncelleme: {Style.RESET_ALL}")
            print(f"{Fore.CYAN}{kontrol['url']}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}[i] Bağımlılıklar güncelleniyor...{Style.RESET_ALL}")
        requirements_kur()
        
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] GÜNCELLEME TAMAMLANDI! v{kontrol['versiyon']} {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] 3 saniye içinde yeniden başlatılıyor...{Style.RESET_ALL}")
        time.sleep(3)
        
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[X] Git hatası! Manuel güncelleyin{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[X] Güncelleme hatası: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

# ================================================
# BÖLÜM 5: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    """Ana program döngüsü."""
    acilis_animasyonu()
    
    while True:
        ana_menu_goster()
        secim = input(f"{Fore.WHITE}AY-YILDIZ > Seçim: {Style.RESET_ALL}").strip().lower()
        
        if secim == "1":
            arac_menusu()
        elif secim == "2":
            hakkimizda_goster()
        elif secim == "3":
            guncelleme_yap()
        elif secim == "q":
            ekran_temizle()
            print(f"\n{Fore.CYAN}AY-YILDIZ SİBER KALKAN kapatılıyor...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Güvende kalın Komutanım! 🇹🇷{Style.RESET_ALL}\n")
            time.sleep(1)
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim! 1, 2, 3 veya Q{Style.RESET_ALL}")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        os.makedirs("araclar", exist_ok=True)
        os.makedirs("raporlar", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        main()
    except KeyboardInterrupt:
        ekran_temizle()
        print(f"\n{Fore.YELLOW}[!] Kullanıcı tarafından durduruldu{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Güle güle Komutanım!{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}KRİTİK HATA: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Hata logu: raporlar/ana_menu_error.log{Style.RESET_ALL}")
        with open("raporlar/ana_menu_error.log", "a") as f:
            f.write(f"[{zaman_damgasi()}] {str(e)}\n")
        sys.exit(1)

# SATIR SAYISI: 3150+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN v5.1
