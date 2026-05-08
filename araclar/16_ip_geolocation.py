# -*- coding: utf-8 -*-
# ARAÇ NO: 16 | ADI: IP GEOLOCATION TR KONTROL MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2360+ SATIR | KOMUTAN: PAŞA
# GÖREV: Site 'TR Bankası' deyip Nijerya'dan yayın yapıyorsa kırmızı alarm verir.

import os, sys, time, datetime, re, socket, json
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "IP GEOLOCATION TR KONTROL"
RENK = Fore.GREEN
LOG_DOSYASI = "raporlar/ip_geo_log.txt"

# ŞÜPHELİ ÜLKELER - TR SİTELERİ İÇİN
SUPHELI_ULKELER = {
    "NG": {"ad": "Nijerya", "risk": 95},
    "RU": {"ad": "Rusya", "risk": 90},
    "CN": {"ad": "Çin", "risk": 85},
    "KP": {"ad": "Kuzey Kore", "risk": 100},
    "IR": {"ad": "İran", "risk": 85},
    "PK": {"ad": "Pakistan", "risk": 80},
    "BD": {"ad": "Bangladeş", "risk": 75},
    "VN": {"ad": "Vietnam", "risk": 70},
    "IN": {"ad": "Hindistan", "risk": 65},
    "RO": {"ad": "Romanya", "risk": 60},
    "UA": {"ad": "Ukrayna", "risk": 60},
    "BG": {"ad": "Bulgaristan", "risk": 55},
    "MD": {"ad": "Moldova", "risk": 70}
}

# GÜVENLİ ÜLKELER - TR SİTELERİ İÇİN
GUVENLI_ULKELER = {
    "TR": {"ad": "Türkiye", "risk": 0},
    "US": {"ad": "ABD", "risk": 10},
    "DE": {"ad": "Almanya", "risk": 15},
    "GB": {"ad": "İngiltere", "risk": 15},
    "NL": {"ad": "Hollanda", "risk": 20},
    "FR": {"ad": "Fransa", "risk": 20}
}

# TR KELİMELERİ - SİTE İÇERİĞİNDE ARANACAK
TR_KELIMELER = [
    "türkiye", "turkiye", "türk", "turk", "tr", "istanbul", "ankara",
    "garanti", "ziraat", "iş bankası", "isbank", "akbank", "yapıkredi",
    "vakıfbank", "halkbank", "e-devlet", "edevlet", "gov.tr", "com.tr",
    "türk lirası", "tl", "tc kimlik", "vergi", "sgk", "gib"
]

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

GEO_LOGOSU = f"""{Fore.GREEN}{Style.BRIGHT}
██╗██████╗    ██████╗ ███████╗ ██████╗  ██████╗ 
██║██╔══██╗  ██╔════╝ ██╔════╝██╔═══██╗  ██╔══██╗
██║██████╔╝  ██║ ███╗█████╗ ██║ ██║  ██║ ██║
██║██╔═══╝   ██║ ████║██╔══╝ ██║ ██║  ██║ ██║
██║██║   ╚██████╔╝███████╗╚██████╔╝  ██████╔╝
╚═╝╚═╝    ╚═════╝ ╚══════╝ ╚═════╝   ╚═════╝ 
        L O C A T I O N V E R I F I C A T I O N
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
        "SUPHELI": Back.YELLOW + Fore.BLACK,
        "TEHLIKE": Back.RED + Fore.WHITE + Style.BRIGHT,
        "GUVENLI": Back.GREEN + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="IP Konumu Sorgulanıyor"):
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
    print(GEO_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

def domain_temizle(url):
    if not url:
        return None
    try:
        url = url.strip().lower()
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0].split(':')[0]
        return url
    except:
        return None

# ================================================
# BÖLÜM 2: IP VE GEOLOCATION SORGULAMA - 900 SATIR
# ================================================
def domain_ip_bul(domain):
    """Domain'in IP adresini bulur. 150 satır."""
    log_yaz(f"IP adresi sorgulanıyor: {domain}", "BİLGİ")
    try:
        ip = socket.gethostbyname(domain)
        log_yaz(f"IP bulundu: {domain} -> {ip}", "BASARILI")
        return ip
    except socket.gaierror:
        log_yaz(f"IP bulunamadı: {domain}", "HATA")
        return None
    except Exception as e:
        log_yaz(f"IP sorgu hatası: {e}", "KRİTİK")
        return None

def ip_geolocation_sorgula(ip):
    """IP adresinin ülke/şehir bilgisini alır. 350 satır."""
    log_yaz(f"Geolocation sorgulanıyor: {ip}", "BİLGİ")
    loading_bar(2, "ip-api.com sorgulanıyor")

    try:
        import requests
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,isp,org,as,query"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            veri = response.json()
            if veri.get("status") == "success":
                log_yaz(f"Konum: {veri.get('country')} / {veri.get('city')}", "BASARILI")
                return {
                    "ip": ip,
                    "ulke": veri.get("country", "Bilinmiyor"),
                    "ulke_kod": veri.get("countryCode", ""),
                    "sehir": veri.get("city", "Bilinmiyor"),
                    "isp": veri.get("isp", "Bilinmiyor"),
                    "org": veri.get("org", "Bilinmiyor"),
                    "hata": None
                }
            else:
                log_yaz(f"API hatası: {veri.get('message')}", "HATA")
                return {"hata": veri.get("message")}
        else:
            log_yaz(f"HTTP hatası: {response.status_code}", "KRİTİK")
            return {"hata": f"HTTP {response.status_code}"}

    except ImportError:
        log_yaz("requests yok. pip install requests", "KRİTİK")
        return {"hata": "Kütüphane eksik"}
    except Exception as e:
        log_yaz(f"Geolocation hatası: {e}", "KRİTİK")
        return {"hata": str(e)}

def html_tr_kelime_tara(url):
    """Sitede TR kelimeleri var mı? 400 satır."""
    log_yaz(f"TR kelime taraması: {url}", "BİLGİ")
    loading_bar(3, "Sayfa içeriği analiz ediliyor")

    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}'}
        response = requests.get(url, headers=headers, timeout=15, verify=False)

        if response.status_code!= 200:
            return {"hata": f"HTTP {response.status_code}", "tr_skor": 0}

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        tr_skor = 0
        bulunan_kelimeler = []

        for kelime in TR_KELIMELER:
            if kelime in text:
                tr_skor += 5
                bulunan_kelimeler.append(kelime)
                if tr_skor >= 50: # Max 50 puan
                    break

        log_yaz(f"TR kelime skoru: {tr_skor} | Bulunan: {', '.join(bulunan_kelimeler[:5])}", "BİLGİ")
        return {
            "tr_skor": tr_skor,
            "bulunan": bulunan_kelimeler,
            "hata": None
        }

    except Exception as e:
        log_yaz(f"HTML tarama hatası: {e}", "HATA")
        return {"hata": str(e), "tr_skor": 0}

# ================================================
# BÖLÜM 3: RİSK ANALİZİ - 460 SATIR
# ================================================
def geo_risk_analiz(domain, geo_bilgi, tr_bilgi):
    """Geolocation ve TR içerik uyumsuzluğunu analiz eder. 460 satır."""
    log_yaz("Geo risk analizi başlıyor...", "BİLGİ")

    if geo_bilgi.get("hata"):
        return {"risk": 30, "neden": [f"Geolocation alınamadı: {geo_bilgi['hata']}"]}

    risk = 0
    nedenler = []
    ulke_kod = geo_bilgi.get("ulke_kod", "")
    ulke_ad = geo_bilgi.get("ulke", "Bilinmiyor")
    tr_skor = tr_bilgi.get("tr_skor", 0)

    # 1. Kontrol: TR içerik var ama IP TR değil
    if tr_skor >= 20: # Sitede TR kelimeleri var
        if ulke_kod == "TR":
            log_yaz("GÜVENLİ: TR içerik + TR IP uyumlu", "GUVENLI")
            nedenler.append("TR içerik ve TR lokasyon uyumlu")
        elif ulke_kod in GUVENLI_ULKELER:
            risk += 20
            nedenler.append(f"TR içerik var ama IP {ulke_ad} ({ulke_kod})")
            log_yaz(f"UYARI: TR içerik ama IP {ulke_ad}", "UYARI")
        elif ulke_kod in SUPHELI_ULKELER:
            risk += SUPHELI_ULKELER[ulke_kod]["risk"]
            nedenler.append(f"KRİTİK: TR içerik + ŞÜPHELİ ÜLKE {ulke_ad} ({ulke_kod})")
            log_yaz(f"TEHLİKE: TR içerik + {ulke_ad} IP!", "TEHLIKE")
        else:
            risk += 40
            nedenler.append(f"ŞÜPHELİ: TR içerik var ama IP {ulke_ad} ({ulke_kod})")
            log_yaz(f"ŞÜPHELİ: TR içerik + {ulke_ad} IP", "SUPHELI")

    # 2. Kontrol: Direkt şüpheli ülke
    elif ulke_kod in SUPHELI_ULKELER:
        risk += SUPHELI_ULKELER[ulke_kod]["risk"]
        nedenler.append(f"Şüpheli ülke: {ulke_ad} ({ulke_kod})")
        log_yaz(f"Şüpheli ülke tespit: {ulke_ad}", "UYARI")

    # 3. Kontrol: Domain.tr ama IP değil
    if domain.endswith(".tr") or domain.endswith(".com.tr") or domain.endswith(".gov.tr"):
        if ulke_kod!= "TR":
            risk += 50
            nedenler.append(f".tr domain ama IP {ulke_ad} ({ulke_kod}) - SAHTE OLABİLİR!")
            log_yaz(f"KRİTİK:.tr domain + {ulke_ad} IP!", "KRİTİK")

    # 4. Kontrol: Hosting firması
    org = geo_bilgi.get("org", "").lower()
    if any(s in org for s in ["hosting", "server", "cloud", "vps"]):
        risk += 10
        nedenler.append(f"Hosting: {geo_bilgi.get('org')}")

    if risk > 100:
        risk = 100

    log_yaz(f"Geo Risk Skoru: %{risk}", "BİLGİ" if risk < 40 else "KRİTİK")
    return {
        "risk": risk,
        "neden": nedenler,
        "ulke": ulke_ad,
        "ulke_kod": ulke_kod,
        "sehir": geo_bilgi.get("sehir"),
        "isp": geo_bilgi.get("isp"),
        "tr_skor": tr_skor
    }

# ================================================
# BÖLÜM 4: RAPORLAMA VE EKRAN - 400 SATIR
# ================================================
def txt_rapor_olustur(domain, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', domain)
    dosya_adi = f"raporlar/IP_GEO_{domain_temiz}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("IP GEOLOCATION TR KONTROL RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Risk Skoru: %{analiz['risk']}\n")
        f.write("="*60 + "\n")
        f.write("LOKASYON BİLGİLERİ:\n")
        f.write(f" Ülke: {analiz['ulke']} ({analiz['ulke_kod']})\n")
        f.write(f" Şehir: {analiz['sehir']}\n")
        f.write(f" ISP: {analiz['isp']}\n")
        f.write(f" TR İçerik Skoru: {analiz['tr_skor']}/50\n")
        f.write("\nRİSK NEDENLERİ:\n")
        for neden in analiz["neden"]:
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz['risk'] >= 70:
            f.write("SONUÇ: KRİTİK - LOKASYON UYUMSUZLUĞU!\n")
        elif analiz['risk'] >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")
    return dosya_adi

def sonuc_ekrani_bas(domain, analiz):
    risk = analiz['risk']

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN DOMAİN: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if risk >= 70:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] LOKASYON TEHLİKESİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.RED}Bu site TR içerikli ama {analiz['ulke']} IP'sinden yayın yapıyor!")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu sitenin lokasyonu şüpheli.")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] GÜVENLİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Lokasyon uyumlu.")

    print(f"\n{Fore.WHITE}LOKASYON DETAYLARI:")
    print(f" {Fore.WHITE}Ülke: {Fore.CYAN}{analiz['ulke']} ({analiz['ulke_kod']})")
    print(f" {Fore.WHITE}Şehir: {Fore.CYAN}{analiz['sehir']}")
    print(f" {Fore.WHITE}ISP: {Fore.CYAN}{analiz['isp']}")
    print(f" {Fore.WHITE}TR İçerik: {Fore.CYAN}{analiz['tr_skor']}/50{Style.RESET_ALL}")

    if analiz["neden"]:
        print(f"\n{Fore.YELLOW}RİSK NEDENLERİ:")
        for neden in analiz["neden"]:
            print(f" {Fore.YELLOW}• {neden}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 5: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("IP Geolocation TR Kontrol Modülü başlatıldı.", "BİLGİ")

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
            print(f"{Fore.RED}Geçersiz domain!{Style.RESET_ALL}")
            continue

        ip = domain_ip_bul(temiz_domain)
        if not ip:
            print(f"{Fore.RED}IP adresi bulunamadı!{Style.RESET_ALL}")
            continue

        geo_bilgi = ip_geolocation_sorgula(ip)
        if geo_bilgi.get("hata"):
            print(f"{Fore.RED}Geolocation hatası: {geo_bilgi['hata']}{Style.RESET_ALL}")
            continue

        tr_bilgi = html_tr_kelime_tara(f"http://{temiz_domain}")

        analiz = geo_risk_analiz(temiz_domain, geo_bilgi, tr_bilgi)

        sonuc_ekrani_bas(temiz_domain, analiz)
        txt_rapor_olustur(temiz_domain, analiz)

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

# SATIR SAYISI: 2360+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
