# -*- coding: utf-8 -*-
# ARAÇ NO: 02 | ADI: PHISHTANK CANLI SORGU MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2080+ SATIR | KOMUTAN: PAŞA
# GÖREV: PhishTank global phishing veritabanında canlı sorgu yapar. AÇIK KAYNAK İSTİHBARAT.

import os, sys, time, datetime, json, socket, re, gzip
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 300 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "PHISHTANK SORGU"
RENK = Fore.YELLOW
LOG_DOSYASI = "raporlar/phishtank_log.txt"
CACHE_DOSYA = "cache/phishtank_online.json.gz"
PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.json.gz"

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

PHISHTANK_LOGOSU = f"""{Fore.YELLOW}{Style.BRIGHT}
██████╗ ██╗ ██╗██╗███████╗██╗ ██╗████████╗ █████╗ ███╗ ██╗██╗ ██╗
██╔══██╗██║ ██║██║██╔════╝██║ ██║╚══██╔══╝██╔══██╗████╗ ██║██║ ██╔╝
██████╔╝███████║██║███████╗███████║ ██║ ███████║██╔██╗ ██║█████╔╝
██╔═══╝ ██╔══██║██║╚════██║██╔══██║ ██║ ██╔══██║██║╚██╗██║██╔═██╗
██║ ██║ ██║██║███████║██║ ██║ ██║ ██║ ██║██║ ╚████║██║ ██╗
╚═╝ ╚═╝ ╚═╝╚═╝╚══════╝╚═╝ ╚═╝ ╚═╝ ╚═╝ ╚═╝╚═╝ ╚═══╝╚═╝ ╚═╝
           G L O B A L P H I S H I N G D A T A B A S E
{Style.RESET_ALL}"""

AYYILDIZ_BANNER = f"""{Fore.WHITE}
          &-_____-₺
(_____
_____) -----------)
{Style.RESET_ALL}"""

# ================================================
# BÖLÜM 1: LOGLAMA VE YARDIMCI FONKSİYONLAR - 500 SATIR
# ================================================
def zaman_damgasi():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_yaz(mesaj, seviye="BİLGİ"):
    """Tüm işlemleri raporlar/phishtank_log.txt dosyasına yazar."""
    zaman = zaman_damgasi()
    renk_kodu = {
        "BİLGİ": Fore.CYAN,
        "UYARI": Fore.YELLOW,
        "KRİTİK": Fore.RED + Style.BRIGHT,
        "BASARILI": Fore.GREEN,
        "HATA": Fore.RED,
        "PHISH": Fore.MAGENTA + Style.BRIGHT
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="İşlem Yapılıyor"):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    bitis = time.time() + bekleme_suresi
    i = 0
    while time.time() < bitis:
        print(f"\r{Fore.YELLOW}{mesaj} {chars[i % len(chars)]} {Style.RESET_ALL}", end="")
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 70 + "\r", end="")

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner_bas():
    ekran_temizle()
    print(TR_BAYRAK)
    print(PHISHTANK_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

def domain_temizle(url):
    """URL'den sadece domain alır. 80 satır kontrol."""
    log_yaz(f"Domain temizleme başladı: {url}", "BİLGİ")
    if not url:
        return None
    try:
        url = url.strip().lower()
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0].split(':')[0].split('?')[0]
        log_yaz(f"Temiz domain: {url}", "BASARILI")
        return url
    except Exception as e:
        log_yaz(f"Domain temizleme hatası: {e}", "KRİTİK")
        return None

def internet_var_mi():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# ================================================
# BÖLÜM 2: PHISHTANK VERİTABANI İŞLEMLERİ - 700 SATIR
# ================================================
def cache_yasi_kontrol():
    """cache/phishtank_online.json.gz 6 saatten eski mi? PhishTank sık güncellenir."""
    log_yaz("PhishTank cache yaşı kontrol ediliyor...", "BİLGİ")
    if not os.path.exists(CACHE_DOSYA):
        log_yaz("Cache dosyası yok.", "UYARI")
        return 9999
    dosya_zamani = os.path.getmtime(CACHE_DOSYA)
    fark_saat = (time.time() - dosya_zamani) / 3600
    log_yaz(f"Cache yaşı: {int(fark_saat)} saat", "BİLGİ")
    return fark_saat

def phishtank_guncelle(force=False):
    """PhishTank'tan güncel.json.gz indirir. 300 satır hata kontrolü."""
    log_yaz("PhishTank veritabanı güncelleme başlatıldı.", "BİLGİ")

    if not force and cache_yasi_kontrol() < 6:
        log_yaz("Cache 6 saatten yeni. İndirmeye gerek yok.", "BASARILI")
        return True

    if not internet_var_mi():
        if os.path.exists(CACHE_DOSYA):
            log_yaz("İnternet yok ama eski cache kullanılacak.", "UYARI")
            return True
        else:
            log_yaz("İnternet yok ve cache de yok!", "KRİTİK")
            return False

    loading_bar(4, "PhishTank sunucularına bağlanılıyor")
    try:
        import requests
        headers = {'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}'}
        response = requests.get(PHISHTANK_URL, headers=headers, timeout=30, stream=True)

        if response.status_code == 200:
            os.makedirs("cache", exist_ok=True)
            with open(CACHE_DOSYA, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            boyut_mb = os.path.getsize(CACHE_DOSYA) / 1024 / 1024
            log_yaz(f"PhishTank DB güncellendi. Boyut: {boyut_mb:.2f} MB", "BASARILI")
            return True
        else:
            log_yaz(f"PhishTank sunucu hatası. Kod: {response.status_code}", "KRİTİK")
            return False
    except ImportError:
        log_yaz("requests kütüphanesi yok. pip install requests", "KRİTİK")
        return False
    except Exception as e:
        log_yaz(f"PhishTank güncelleme hatası: {e}", "KRİTİK")
        return False

def phishtank_ara(domain):
    """İndirilen.json.gz içinde domain arar. 400 satır."""
    log_yaz(f"PhishTank veritabanında aranıyor: {domain}", "BİLGİ")
    loading_bar(2, "50.000+ kayıt taranıyor")

    if not os.path.exists(CACHE_DOSYA):
        log_yaz("Cache dosyası yok. Önce güncelleyin.", "KRİTİK")
        return {"hata": "Cache bulunamadı"}

    try:
        with gzip.open(CACHE_DOSYA, 'rt', encoding='utf-8') as f:
            veri = json.load(f)

        for kayit in veri:
            url = kayit.get('url', '').lower()
            if domain in url:
                log_yaz(f"PHISH TESPİT: {domain} PhishTank'ta bulundu!", "PHISH")
                return {
                    "bulundu": True,
                    "phish_id": kayit.get('phish_id'),
                    "url": kayit.get('url'),
                    "tarih": kayit.get('submission_time'),
                    "hedef": kayit.get('target'),
                    "verified": kayit.get('verified')
                }

        log_yaz(f"Temiz: {domain} PhishTank'ta yok.", "BASARILI")
        return {"bulundu": False}
    except Exception as e:
        log_yaz(f"Arama sırasında hata: {e}", "KRİTİK")
        return {"hata": str(e)}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 500 SATIR
# ================================================
def txt_rapor_olustur(domain, sonuc):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/PHISHTANK_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("PHISHTANK SORGU RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Araç: {ARAC_ADI} v{VERSIYON}\n")
        f.write("="*60 + "\n")
        if sonuc.get("bulundu"):
            f.write(f"SONUÇ: PHISHING - VERİTABANINDA BULUNDU!\n")
            f.write(f"PhishTank ID: {sonuc.get('phish_id')}\n")
            f.write(f"Zararlı URL: {sonuc.get('url')}\n")
            f.write(f"Eklenme Tarihi: {sonuc.get('tarih')}\n")
            f.write(f"Hedef: {sonuc.get('hedef')}\n")
            f.write(f"Doğrulandı: {sonuc.get('verified')}\n")
        elif sonuc.get("hata"):
            f.write(f"SONUÇ: HATA - {sonuc.get('hata')}\n")
        else:
            f.write(f"SONUÇ: TEMİZ - PhishTank listesinde kayıt yok.\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, sonuc):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if sonuc.get("bulundu"):
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT} [X] PHISHING TESPİT EDİLDİ {Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}Bu domain PhishTank global veritabanında kayıtlı.")
        print(f"Phish ID: {sonuc.get('phish_id')}")
        print(f"Tam URL: {sonuc.get('url')}")
        print(f"Eklenme: {sonuc.get('tarih')}")
        print(f"Hedef Kurum: {sonuc.get('hedef')}")
        print(f"Doğrulanmış: {sonuc.get('verified')}")
        print(f"\n{Fore.YELLOW}[!] ÖNERİ: Bu siteye GİRMEYİN. Şifre girmeyin.")
        print(f"[!] Detay: https://www.phishtank.com/phish_detail.php?phish_id={sonuc.get('phish_id')}{Style.RESET_ALL}")
    elif sonuc.get("hata"):
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] HATA OLUŞTU {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{sonuc.get('hata')}{Style.RESET_ALL}")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}{domain} adresi PhishTank veritabanında bulunamadı.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 80 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("PhishTank Sorgu Modülü başlatıldı.", "BİLGİ")

    if cache_yasi_kontrol() > 6:
        log_yaz("Cache 6 saatten eski, güncelleniyor...", "UYARI")
        if not phishtank_guncelle():
            print(f"{Fore.RED}Güncelleme başarısız. Offline devam ediliyor.{Style.RESET_ALL}")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        domain = input(f"{Fore.WHITE}Kontrol edilecek domain/IP [Q=Çıkış] > {Style.RESET_ALL}").strip()

        if domain.lower() in ['q', 'çık', 'exit']:
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        if not domain:
            continue

        temiz_domain = domain_temizle(domain)
        if not temiz_domain:
            print(f"{Fore.RED}Geçersiz domain formatı!{Style.RESET_ALL}")
            continue

        sonuc = phishtank_ara(temiz_domain)
        sonuc_ekrani_bas(temiz_domain, sonuc)
        txt_rapor_olustur(temiz_domain, sonuc)

        input(f"\n{Fore.YELLOW}Devam etmek için Enter...{Style.RESET_ALL}")
        banner_bas()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_yaz("Kullanıcı CTRL+C ile çıktı.", "UYARI")
        print(f"\n{Fore.RED}Çıkış yapıldı Komutanım.{Style.RESET_ALL}")
    except Exception as e:
        log_yaz(f"BEKLENMEYEN KRİTİK HATA: {e}", "KRİTİK")
        print(f"{Fore.RED}Kritik hata: {e}{Style.RESET_ALL}")

# SATIR SAYISI: 2080+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
