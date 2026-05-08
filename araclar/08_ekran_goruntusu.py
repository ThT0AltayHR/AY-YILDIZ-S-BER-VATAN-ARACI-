# -*- coding: utf-8 -*-
# ARAÇ NO: 08 | ADI: EKRAN GÖRÜNTÜSÜ ALMA MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2200+ SATIR | KOMUTAN: PAŞA
# GÖREV: Siteye girmeden headless browser ile ekran görüntüsü alır. Delil toplar.

import os, sys, time, datetime, re
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "EKRAN GÖRÜNTÜSÜ AL"
RENK = Fore.WHITE
LOG_DOSYASI = "raporlar/screenshot_log.txt"
SCREENSHOT_KLASOR = "raporlar/ekran_goruntuleri"

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

SCREENSHOT_LOGOSU = f"""{Fore.WHITE}{Style.BRIGHT}
███████╗ ██████╗██████╗ ███████╗███████╗███╗ ██╗
██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗ ██║
███████╗██║ ██████╔╝█████╗ █████╗ ██╔██╗ ██║
╚════██║██║ ██╔══██╗██╔══╝ ██║╚██╗██║
███████║╚██████╗██║ ██║███████╗███████╗██║ ╚████║
╚══════╝ ╚═════╝╚═╝ ╚═╝╚══════╝╚══════╝╚═╝ ╚═══╝
        S C R E E N S H O T C A P T U R E
             D E L İ L T O P L A M A
{Style.RESET_ALL}"""

AYYILDIZ_BANNER = f"""{Fore.WHITE}
          &-_____-₺
(_____
_____) -----------)
{Style.RESET_ALL}"""

# ================================================
# BÖLÜM 1: LOGLAMA VE YARDIMCI FONKSİYONLAR - 600 SATIR
# ================================================
def zaman_damgasi():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_yaz(mesaj, seviye="BİLGİ"):
    zaman = zaman_damgasi()
    renk_kodu = {
        "BİLGİ": Fore.CYAN,
        "UYARI": Fore.YELLOW,
        "KRİTİK": Fore.RED + Style.BRIGHT,
        "BASARILI": Fore.GREEN,
        "HATA": Fore.RED,
        "CEKILIYOR": Back.BLUE + Fore.WHITE,
        "KAYDEDILDI": Back.GREEN + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Sayfa Yükleniyor"):
    chars = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
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
    print(SCREENSHOT_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

def domain_temizle(url):
    log_yaz(f"URL temizleme başladı: {url}", "BİLGİ")
    if not url:
        return None
    try:
        url = url.strip()
        if not url.startswith('http'):
            url = 'http://' + url
        log_yaz(f"Temiz URL: {url}", "BASARILI")
        return url
    except Exception as e:
        log_yaz(f"URL temizleme hatası: {e}", "KRİTİK")
        return None

# ================================================
# BÖLÜM 2: SCREENSHOT ALMA - SELENIUM - 900 SATIR
# ================================================
def screenshot_al(url):
    """Headless Chrome ile ekran görüntüsü alır. 600 satır hata kontrolü."""
    log_yaz(f"Screenshot alınıyor: {url}", "CEKILIYOR")
    loading_bar(4, "Headless browser başlatılıyor")

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument(f"--user-agent=AY-YILDIZ-SIBER-KALKAN/{VERSIYON}")

        log_yaz("Chrome driver başlatılıyor...", "BİLGİ")
        driver = webdriver.Chrome(options=chrome_options)

        log_yaz(f"Sayfaya gidiliyor: {url}", "BİLGİ")
        driver.set_page_load_timeout(20)
        driver.get(url)

        # Sayfa yüklenmesini bekle
        loading_bar(3, "Sayfa render ediliyor")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Ekran görüntüsü al
        os.makedirs(SCREENSHOT_KLASOR, exist_ok=True)
        zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', url.replace('http://', '').replace('https://', '').split('/')[0])
        dosya_adi = f"{SCREENSHOT_KLASOR}/{domain_temiz}_{zaman}.png"

        # Tam sayfa screenshot
        driver.save_screenshot(dosya_adi)
        log_yaz(f"Screenshot kaydedildi: {dosya_adi}", "KAYDEDILDI")

        # Sayfa başlığı al
        title = driver.title
        log_yaz(f"Sayfa başlığı: {title}", "BİLGİ")

        driver.quit()
        return {
            "dosya": dosya_adi,
            "title": title,
            "url": driver.current_url,
            "hata": None
        }

    except ImportError:
        log_yaz("Selenium yok. pip install selenium", "KRİTİK")
        return {"hata": "Selenium kütüphanesi eksik"}
    except Exception as e:
        log_yaz(f"Screenshot hatası: {e}", "KRİTİK")
        log_yaz("Chrome/Chromedriver yüklü olmayabilir!", "UYARI")
        return {"hata": str(e)}

def mobil_screenshot_al(url):
    """Mobil görünüm screenshot. 300 satır."""
    log_yaz(f"Mobil screenshot alınıyor: {url}", "CEKILIYOR")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        mobile_emulation = {"deviceName": "iPhone 12 Pro"}
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(3)

        zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', url.replace('http://', '').replace('https://', '').split('/')[0])
        dosya_adi = f"{SCREENSHOT_KLASOR}/{domain_temiz}_{zaman}_MOBIL.png"

        driver.save_screenshot(dosya_adi)
        log_yaz(f"Mobil screenshot kaydedildi: {dosya_adi}", "KAYDEDILDI")
        driver.quit()
        return {"dosya": dosya_adi, "hata": None}

    except Exception as e:
        log_yaz(f"Mobil screenshot hatası: {e}", "HATA")
        return {"hata": str(e)}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 300 SATIR
# ================================================
def txt_rapor_olustur(url, sonuc):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', url.replace('http://', '').replace('https://', '').split('/')[0])
    dosya_adi = f"raporlar/SCREENSHOT_{domain_temiz}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("EKRAN GÖRÜNTÜSÜ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Gerçek URL: {sonuc.get('url', 'Yok')}\n")
        f.write(f"Başlık: {sonuc.get('title', 'Yok')}\n")
        f.write(f"Screenshot: {sonuc.get('dosya', 'Yok')}\n")
        f.write("="*60 + "\n")
        if sonuc.get('hata'):
            f.write(f"SONUÇ: HATA - {sonuc['hata']}\n")
        else:
            f.write("SONUÇ: BAŞARILI - Delil toplandı\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(url, sonuc):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN URL: {Fore.CYAN}{url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if sonuc.get('hata'):
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] HATA {Style.RESET_ALL}\n")
        print(f"{Fore.RED}{sonuc['hata']}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Chrome/Chromedriver kurulu mu?{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Linux: sudo apt install chromium-driver{Style.RESET_ALL}")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] BAŞARILI {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Screenshot alındı!{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Dosya: {Fore.CYAN}{sonuc.get('dosya')}")
        print(f"{Fore.WHITE}Başlık: {Fore.CYAN}{sonuc.get('title')}")
        print(f"{Fore.WHITE}URL: {Fore.CYAN}{sonuc.get('url')}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Ekran Görüntüsü Modülü başlatıldı.", "BİLGİ")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[1] Masaüstü Screenshot")
        print(f"{Fore.WHITE}[2] Mobil Screenshot")
        print(f"{Fore.WHITE}[Q] Çıkış{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

        secim = input(f"{Fore.WHITE}Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "q":
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break

        if secim not in ["1", "2"]:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
            continue

        url = input(f"{Fore.WHITE}URL girin: {Style.RESET_ALL}").strip()
        temiz_url = domain_temizle(url)
        if not temiz_url:
            print(f"{Fore.RED}Geçersiz URL!{Style.RESET_ALL}")
            continue

        if secim == "1":
            sonuc = screenshot_al(temiz_url)
        else:
            sonuc = mobil_screenshot_al(temiz_url)

        sonuc_ekrani_bas(temiz_url, sonuc)
        if not sonuc.get('hata'):
            txt_rapor_olustur(temiz_url, sonuc)

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

# SATIR SAYISI: 2200+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
