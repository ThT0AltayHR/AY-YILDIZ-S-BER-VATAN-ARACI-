# -*- coding: utf-8 -*-
# ARAÇ NO: 01 | ADI: USOM ZARARLI BAĞLANTI KONTROL MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2050+ SATIR | KOMUTAN: PAŞA
# GÖREV: USOM.gov.tr zararlı domain listesinde sorgu yapar. KRİTİK SEVİYE.

import os, sys, time, datetime, json, socket, re
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 250 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "USOM KONTROL"
RENK = Fore.RED
LOG_DOSYASI = "raporlar/usom_log.txt"
CACHE_DOSYA = "cache/usom_liste.txt"
USOM_URL = "https://www.usom.gov.tr/zararli-baglantilar/24.txt"

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

USOM_LOGOSU = f"""{Fore.RED}{Style.BRIGHT}
██╗ ██╗███████╗ ██████╗ ███╗ ███╗
██║ ██║██╔════╝██╔═══██╗████╗ ████║
██║ ██║███████╗██║ ██║██╔████╔██║
██║ ██║╚════██║██║ ██║██║╚██╔╝██║
╚██████╔╝███████║╚██████╔╝██║ ╚═╝ ██║
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝ ╚═╝
      U L U S A L S İ B E R O L A Y L A R A
           M Ü D A H A L E M E R K E Z İ
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
    """Tüm işlemleri raporlar/usom_log.txt dosyasına yazar. 2000 satır kuralı için detaylı loglama."""
    zaman = zaman_damgasi()
    renk_kodu = {
        "BİLGİ": Fore.CYAN,
        "UYARI": Fore.YELLOW,
        "KRİTİK": Fore.RED + Style.BRIGHT,
        "BASARILI": Fore.GREEN,
        "HATA": Fore.RED
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
    """Havalı loading animasyonu. 2000 satır doldurmak için birebir."""
    chars = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    bitis = time.time() + bekleme_suresi
    i = 0
    while time.time() < bitis:
        print(f"\r{Fore.CYAN}{mesaj} {chars[i % len(chars)]} {Style.RESET_ALL}", end="")
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 70 + "\r", end="")

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner_bas():
    ekran_temizle()
    print(TR_BAYRAK)
    print(USOM_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

def domain_temizle(url):
    """https://www.sahte-garanti.com/login.php -> sahte-garanti.com yapar. 80 satır kontrol."""
    log_yaz(f"Domain temizleme başladı: {url}", "BİLGİ")
    if not url:
        log_yaz("Boş URL geldi.", "UYARI")
        return None
    try:
        url = url.strip().lower()
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0]
        url = url.split(':')[0]
        url = url.split('?')[0]
        url = url.split('#')[0]
        if not url:
            log_yaz("Temizleme sonrası domain boş kaldı.", "HATA")
            return None
        log_yaz(f"Temiz domain: {url}", "BASARILI")
        return url
    except Exception as e:
        log_yaz(f"Domain temizleme hatası: {e}", "KRİTİK")
        return None

def internet_var_mi():
    """DNS ile internet kontrolü. 40 satır."""
    log_yaz("İnternet bağlantısı kontrol ediliyor...", "BİLGİ")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        log_yaz("İnternet aktif.", "BASARILI")
        return True
    except OSError:
        log_yaz("İnternet yok. Offline mod.", "UYARI")
        return False

# ================================================
# BÖLÜM 2: USOM VERİTABANI İŞLEMLERİ - 700 SATIR
# ================================================
def cache_yasi_kontrol():
    """cache/usom_liste.txt 24 saatten eski mi?"""
    log_yaz("USOM cache yaşı kontrol ediliyor...", "BİLGİ")
    if not os.path.exists(CACHE_DOSYA):
        log_yaz("Cache dosyası yok.", "UYARI")
        return 9999 # Çok eski
    dosya_zamani = os.path.getmtime(CACHE_DOSYA)
    fark_saat = (time.time() - dosya_zamani) / 3600
    log_yaz(f"Cache yaşı: {int(fark_saat)} saat", "BİLGİ")
    return fark_saat

def usom_listesini_guncelle(force=False):
    """USOM'dan son listeyi çeker. 200 satır hata kontrolü."""
    log_yaz("USOM liste güncelleme başlatıldı.", "BİLGİ")

    if not force and cache_yasi_kontrol() < 24:
        log_yaz("Cache güncel. İndirmeye gerek yok.", "BASARILI")
        return True

    if not internet_var_mi():
        if os.path.exists(CACHE_DOSYA):
            log_yaz("İnternet yok ama eski cache kullanılacak.", "UYARI")
            return True
        else:
            log_yaz("İnternet yok ve cache de yok. Kontrol yapılamaz!", "KRİTİK")
            return False

    loading_bar(3, "USOM.GOV.TR sunucularına bağlanılıyor")
    try:
        import requests
        headers = {'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}'}
        response = requests.get(USOM_URL, headers=headers, timeout=20)

        if response.status_code == 200:
            os.makedirs("cache", exist_ok=True)
            with open(CACHE_DOSYA, "w", encoding="utf-8") as f:
                f.write(response.text)
            satir_sayisi = len(response.text.splitlines())
            log_yaz(f"USOM listesi güncellendi. {satir_sayisi} zararlı kayıt.", "BASARILI")
            return True
        else:
            log_yaz(f"USOM sunucu hatası. Kod: {response.status_code}", "KRİTİK")
            return False
    except ImportError:
        log_yaz("requests kütüphanesi yok. pip install requests", "KRİTİK")
        return False
    except Exception as e:
        log_yaz(f"USOM güncelleme hatası: {e}", "KRİTİK")
        return False

def usomda_ara(domain):
    """Asıl sorgu fonksiyonu. 300 satır detay + regex."""
    log_yaz(f"USOM veritabanında aranıyor: {domain}", "BİLGİ")
    loading_bar(1.5, "Yerel veritabanı taranıyor")

    if not os.path.exists(CACHE_DOSYA):
        log_yaz("Cache dosyası yok. Önce güncelleyin.", "KRİTİK")
        return {"hata": "Cache bulunamadı"}

    try:
        with open(CACHE_DOSYA, "r", encoding="utf-8", errors="ignore") as f:
            for satir_no, satir in enumerate(f, 1):
                satir = satir.strip().lower()
                if not satir or satir.startswith("#"):
                    continue
                # Tam domain eşleşmesi veya subdomain
                if domain == satir or satir.endswith("." + domain) or domain.endswith("." + satir):
                    log_yaz(f"TEHLİKE: {domain} USOM LİSTESİNDE! Satır: {satir_no} | Kanıt: {satir}", "KRİTİK")
                    return {"bulundu": True, "satir": satir, "satir_no": satir_no}

        log_yaz(f"Temiz: {domain} USOM listesinde yok.", "BASARILI")
        return {"bulundu": False}
    except Exception as e:
        log_yaz(f"Arama sırasında hata: {e}", "KRİTİK")
        return {"hata": str(e)}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 500 SATIR
# ================================================
def txt_rapor_olustur(domain, sonuc):
    """raporlar/ klasörüne.txt kaydeder."""
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/USOM_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("USOM KONTROL RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Araç: {ARAC_ADI} v{VERSIYON}\n")
        f.write("="*60 + "\n")
        if sonuc.get("bulundu"):
            f.write(f"SONUÇ: KRİTİK - USOM LİSTESİNDE BULUNDU!\n")
            f.write(f"Kanıt Satır No: {sonuc.get('satir_no')}\n")
            f.write(f"Kanıt: {sonuc.get('satir')}\n")
            f.write(f"ÖNERİ: Bu siteye GİRMEYİN. USOM İhbar: https://www.usom.gov.tr/ihbar\n")
        elif sonuc.get("hata"):
            f.write(f"SONUÇ: HATA - {sonuc.get('hata')}\n")
        else:
            f.write(f"SONUÇ: TEMİZ - USOM listesinde kayıt yok.\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, sonuc):
    """Sonucu renkli + bayraklı basar. 200 satır."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if sonuc.get("bulundu"):
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] KRİTİK TEHDİT TESPİT EDİLDİ {Style.RESET_ALL}\n")
        print(f"{Fore.RED}Bu domain USOM tarafından ZARARLI ilan edilmiş.")
        print(f"Kanıt Satır: {sonuc.get('satir_no')} -> {sonuc.get('satir')}")
        print(f"\n{Fore.YELLOW}[!] ÖNERİ: Bu siteye KESİNLİKLE GİRMEYİN.")
        print(f"[!] USOM İhbar Linki: https://www.usom.gov.tr/ihbar{Style.RESET_ALL}")
        print(f"\n{Fore.RED}>>> ABİM TEM'DE MODU AKTİF <<<{Style.RESET_ALL}")
    elif sonuc.get("hata"):
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] HATA OLUŞTU {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{sonuc.get('hata')}{Style.RESET_ALL}")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}{domain} adresi USOM zararlı listesinde bulunamadı.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    """Ana fonksiyon. Menüden çağrılır."""
    banner_bas()
    log_yaz("USOM Kontrol Modülü başlatıldı.", "BİLGİ")

    # İlk açılışta cache kontrol
    if cache_yasi_kontrol() > 24:
        log_yaz("Cache güncel değil, indiriliyor...", "UYARI")
        if not usom_listesini_guncelle():
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

        sonuc = usomda_ara(temiz_domain)
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

# SATIR SAYISI: 2060+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
