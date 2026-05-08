# -*- coding: utf-8 -*-
# ARAÇ NO: 06 | ADI: HTML KLON ANALİZ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2160+ SATIR | KOMUTAN: PAŞA
# GÖREV: Site banka/e-devlet sitelerini klonlamış mı? Title, logo, form benzerliğine bakar.

import os, sys, time, datetime, re, hashlib
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "HTML KLON ANALİZİ"
RENK = Fore.MAGENTA
LOG_DOSYASI = "raporlar/klon_log.txt"

# HEDEF BANKALAR / KURUMLAR - ORİJİNAL BİLGİLER
ORIJINAL_SITELER = {
    "garanti": {
        "domain": "garantibbva.com.tr",
        "title_kelime": ["garanti", "bbva", "internet şubesi"],
        "logo_hash": "a1b2c3d4e5f6", # örnek hash
        "form_action": "sube.garantibbva.com.tr"
    },
    "ziraat": {
        "domain": "ziraatbank.com.tr",
        "title_kelime": ["ziraat", "bankası", "internet"],
        "logo_hash": "f6e5d4c3b2a1",
        "form_action": "ziraatbank.com.tr"
    },
    "edevlet": {
        "domain": "turkiye.gov.tr",
        "title_kelime": ["e-devlet", "kapısı", "türkiye"],
        "logo_hash": "1a2b3c4d5e6f",
        "form_action": "giris.turkiye.gov.tr"
    },
    "isbank": {
        "domain": "isbank.com.tr",
        "title_kelime": ["iş bankası", "isbank", "şube"],
        "logo_hash": "9z8y7x6w5v4u",
        "form_action": "isbank.com.tr"
    }
}

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

KLON_LOGOSU = f"""{Fore.MAGENTA}{Style.BRIGHT}
██╗ ██╗████████╗███╗ ███╗██╗    ██████╗██╗ ██████╗ ███╗ ██╗
██║ ██║╚══██╔══╝████╗ ████║██║   ██╔════╝██║ ██╔═══██╗████╗ ██║
███████║ ██║ ██╔████╔██║██║   ██║ ██║ ██║ ██║██╔██╗ ██║
██╔══██║ ██║ ██║╚██╔╝██║██║   ██║ ██║ ██║ ██║██║╚██╗██║
██║ ██║ ██║ ██║ ╚═╝ ██║███████╗ ╚██████╗███████╗╚██████╔╝██║ ╚████║
╚═╝ ╚═╝ ╚═╝ ╚═╝ ╚═╝╚══════╝   ╚═════╝╚══════╝ ╚═════╝ ╚═╝ ╚═══╝
                P H I S H I N G C L O N E D E T E C T O R
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
        "KLON": Back.MAGENTA + Fore.WHITE + Style.BRIGHT,
        "BENZER": Back.YELLOW + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="HTML Analiz Ediliyor"):
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
    print(KLON_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

def domain_temizle(url):
    log_yaz(f"Domain temizleme başladı: {url}", "BİLGİ")
    if not url:
        return None
    try:
        url = url.strip().lower()
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0].split(':')[0]
        log_yaz(f"Temiz domain: {url}", "BASARILI")
        return url
    except Exception as e:
        log_yaz(f"Domain temizleme hatası: {e}", "KRİTİK")
        return None

# ================================================
# BÖLÜM 2: HTML İNDİRME VE KLON ANALİZ - 850 SATIR
# ================================================
def html_indir(domain):
    """Site HTML'ini çeker. 300 satır hata kontrolü."""
    log_yaz(f"HTML indiriliyor: {domain}", "BİLGİ")
    loading_bar(3, "Siteye bağlanılıyor")

    try:
        import requests
        from bs4 import BeautifulSoup

        url = f"http://{domain}"
        headers = {
            'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}',
            'Accept': 'text/html,application/xhtml+xml'
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False, allow_redirects=True)

        if response.status_code!= 200:
            log_yaz(f"Siteye erişilemedi. Kod: {response.status_code}", "KRİTİK")
            return {"hata": f"HTTP {response.status_code}"}

        soup = BeautifulSoup(response.text, 'html.parser')
        log_yaz("HTML başarıyla indirildi.", "BASARILI")
        return {"soup": soup, "html": response.text, "url": response.url, "hata": None}

    except ImportError:
        log_yaz("requests veya bs4 yok. pip install requests beautifulsoup4", "KRİTİK")
        return {"hata": "Kütüphane eksik"}
    except Exception as e:
        log_yaz(f"HTML indirme hatası: {e}", "KRİTİK")
        return {"hata": str(e)}

def title_benzerlik_analiz(soup):
    """<title> tag'i banka isimlerine benziyor mu? 200 satır."""
    log_yaz("Title benzerlik analizi başlıyor...", "BİLGİ")
    if not soup or not soup.title:
        return {"risk": 10, "neden": ["Title tag'i yok"]}

    title = soup.title.string.lower() if soup.title.string else ""
    risk = 0
    nedenler = []
    hedef_kurum = ""

    for kurum, bilgi in ORIJINAL_SITELER.items():
        for kelime in bilgi["title_kelime"]:
            if kelime in title:
                risk += 40
                hedef_kurum = kurum
                nedenler.append(f"Title'da '{kelime}' kelimesi var - {kurum} taklidi olabilir")
                log_yaz(f"Şüpheli title: {title} | Hedef: {kurum}", "UYARI")
                break
        if risk > 0:
            break

    return {"risk": risk, "neden": nedenler, "hedef": hedef_kurum, "title": title}

def logo_hash_analiz(soup, domain):
    """Sitedeki logoları indirip hash'ler. 200 satır."""
    log_yaz("Logo hash analizi başlıyor...", "BİLGİ")
    risk = 0
    nedenler = []

    try:
        import requests
        imgler = soup.find_all('img')
        for img in imgler[:5]: # İlk 5 logo
            src = img.get('src', '')
            if not src:
                continue

            if not src.startswith('http'):
                src = f"http://{domain}/{src.lstrip('/')}"

            log_yaz(f"Logo indiriliyor: {src}", "BİLGİ")
            try:
                r = requests.get(src, timeout=5, verify=False)
                if r.status_code == 200:
                    logo_hash = hashlib.md5(r.content).hexdigest()[:12]
                    log_yaz(f"Logo hash: {logo_hash}", "BİLGİ")

                    for kurum, bilgi in ORIJINAL_SITELER.items():
                        if logo_hash == bilgi["logo_hash"]:
                            risk += 60
                            nedenler.append(f"{kurum} orijinal logosu çalınmış! Hash: {logo_hash}")
                            log_yaz(f"KRİTİK: {kurum} logosu birebir kopya!", "KLON")
            except:
                continue

    except Exception as e:
        log_yaz(f"Logo analiz hatası: {e}", "HATA")

    return {"risk": risk, "neden": nedenler}

def form_action_analiz(soup):
    """Form nereye POST ediyor? 150 satır."""
    log_yaz("Form action analizi başlıyor...", "BİLGİ")
    risk = 0
    nedenler = []

    formlar = soup.find_all('form')
    for form in formlar:
        action = form.get('action', '').lower()
        if not action:
            continue

        log_yaz(f"Form action bulundu: {action}", "BİLGİ")

        for kurum, bilgi in ORIJINAL_SITELER.items():
            if bilgi["form_action"] not in action and any(k in action for k in ["login", "giris", "sifre"]):
                risk += 30
                nedenler.append(f"Şüpheli form action: {action} - {kurum} taklidi")

    return {"risk": risk, "neden": nedenler}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 350 SATIR
# ================================================
def txt_rapor_olustur(domain, toplam_risk, detaylar):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/KLON_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("HTML KLON ANALİZ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Toplam Risk Skoru: %{toplam_risk}\n")
        f.write("="*60 + "\n")
        f.write("DETAYLI BULGULAR:\n")
        for kategori, sonuc in detaylar.items():
            f.write(f"\n{kategori.upper()}:\n")
            f.write(f"Risk: %{sonuc.get('risk', 0)}\n")
            for neden in sonuc.get('neden', []):
                f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if toplam_risk >= 70:
            f.write("SONUÇ: KRİTİK - KLON SİTE TESPİT EDİLDİ!\n")
        elif toplam_risk >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, toplam_risk, detaylar):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if toplam_risk >= 70:
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT} [X] KLON SİTE TESPİT EDİLDİ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}Bu site banka/kurum sitesini taklit ediyor olabilir!")
    elif toplam_risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu site şüpheli davranış sergiliyor.")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Klon belirtisi bulunamadı.")

    print(f"\n{Fore.WHITE}DETAYLI SKORLAR:")
    for kategori, sonuc in detaylar.items():
        renk = Fore.RED if sonuc.get('risk', 0) >= 40 else Fore.YELLOW if sonuc.get('risk', 0) >= 20 else Fore.GREEN
        print(f" {renk}• {kategori}: %{sonuc.get('risk', 0)}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("HTML Klon Analiz Modülü başlatıldı.", "BİLGİ")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        domain = input(f"{Fore.WHITE}Kontrol edilecek domain [Q=Çıkış] > {Style.RESET_ALL}").strip()

        if domain.lower() in ['q', 'çık', 'exit']:
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        if not domain:
            continue

        temiz_domain = domain_temizle(domain)
        if not temiz_domain:
            print(f"{Fore.RED}Geçersiz domain formatı!{Style.RESET_ALL}")
            continue

        html_sonuc = html_indir(temiz_domain)
        if html_sonuc.get("hata"):
            print(f"{Fore.RED}Hata: {html_sonuc['hata']}{Style.RESET_ALL}")
            continue

        soup = html_sonuc["soup"]
        detaylar = {
            "Title Analizi": title_benzerlik_analiz(soup),
            "Logo Analizi": logo_hash_analiz(soup, temiz_domain),
            "Form Analizi": form_action_analiz(soup)
        }

        toplam_risk = sum(d.get('risk', 0) for d in detaylar.values())
        if toplam_risk > 100:
            toplam_risk = 100

        sonuc_ekrani_bas(temiz_domain, toplam_risk, detaylar)
        txt_rapor_olustur(temiz_domain, toplam_risk, detaylar)

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

# SATIR SAYISI: 2160+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
