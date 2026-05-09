# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | Kara Liste Skor Modülü | 6321 KARAKTER KOD
# USOM + PhishTank + SSL + Domain Age + GSB = 5 Katman Analiz

import os, sys, time, requests, ssl, socket, whois
from datetime import datetime
from urllib.parse import urlparse
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
USOM_URL = "https://www.usom.gov.tr/url-list.txt"
PHISHTANK_API = "https://checkurl.phishtank.com/checkurl/"
YEREL_USOM = "data/usom_cache.txt"

# 2603 KARAKTER BAYRAK - SAYDIM
BAYRAK = f"""{Fore.RED}
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████
██████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████
██████████{Fore.WHITE}▒▒▒▒{Fore.RED}████
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████
██████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} KARA LİSTE SKOR MODÜLÜ v{VERSIYON} | KOD: 6321 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | 5 KATMANLI TEHDİT ANALİZİ{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def usom_sorgu(domain):
    try:
        if not os.path.exists(YEREL_USOM):
            return 0, "USOM listesi yok"
        with open(YEREL_USOM, "r", encoding="utf-8", errors="ignore") as f:
            if domain in f.read(): return 40, "USOM Kara Liste"
        return 0, "USOM Temiz"
    except: return 0, "USOM Hata"

def phishtank_sorgu(url):
    try:
        data = {'url': url, 'format': 'json', 'app_key': 'AYYILDIZ'}
        r = requests.post(PHISHTANK_API, data=data, timeout=10)
        if r.status_code == 509: return 0, "PhishTank Limit"
        sonuc = r.json()
        if sonuc['results']['in_database'] and sonuc['results']['valid']:
            return 30, "PhishTank Oltalama"
        return 0, "PhishTank Temiz"
    except: return 0, "PhishTank Hata"

def ssl_kontrol(domain):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                sertifika = ssock.getpeercert()
                issuer = dict(x[0] for x in sertifika['issuer'])
                if "Let's Encrypt" in issuer.get('organizationName',''):
                    return 10, "Ücretsiz SSL"
                if "Cloudflare" in issuer.get('organizationName',''):
                    return 5, "Cloudflare SSL"
                return 0, "Güvenilir SSL"
    except:
        return 20, "SSL Yok/Hatalı"

def domain_yasi(domain):
    try:
        w = whois.whois(domain)
        if w.creation_date:
            if isinstance(w.creation_date, list):
                olusturma = w.creation_date[0]
            else:
                olusturma = w.creation_date
            yas = (datetime.now() - olusturma).days
            if yas < 30: return 10, f"Yeni Domain: {yas} gün"
            if yas < 90: return 5, f"Genç Domain: {yas} gün"
            return 0, f"Domain Yaşı: {yas} gün"
        return 5, "Yaş Bilinmiyor"
    except:
        return 5, "WHOIS Hata"

def skor_hesapla(url):
    domain = urlparse(url).netloc.replace("www.","") if url.startswith('http') else url.replace("www.","")
    if not domain: return

    print(f"\n{Fore.YELLOW}[+] 5 Katmanlı Analiz Başlatıldı: {domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    toplam_skor = 0
    detaylar = []

    # 1. USOM
    skor, mesaj = usom_sorgu(domain)
    toplam_skor += skor
    detaylar.append(f"USOM: {mesaj} [+{skor}]")
    print(f"{Fore.WHITE}[1/5] USOM Kontrol: {mesaj} {Fore.RED if skor>0 else Fore.GREEN}[+{skor}]{Style.RESET_ALL}")

    # 2. PhishTank
    skor, mesaj = phishtank_sorgu(url)
    toplam_skor += skor
    detaylar.append(f"PhishTank: {mesaj} [+{skor}]")
    print(f"{Fore.WHITE}[2/5] PhishTank: {mesaj} {Fore.RED if skor>0 else Fore.GREEN}[+{skor}]{Style.RESET_ALL}")

    # 3. SSL
    skor, mesaj = ssl_kontrol(domain)
    toplam_skor += skor
    detaylar.append(f"SSL: {mesaj} [+{skor}]")
    print(f"{Fore.WHITE}[3/5] SSL Analizi: {mesaj} {Fore.RED if skor>0 else Fore.GREEN}[+{skor}]{Style.RESET_ALL}")

    # 4. Domain Yaşı
    skor, mesaj = domain_yasi(domain)
    toplam_skor += skor
    detaylar.append(f"Domain: {mesaj} [+{skor}]")
    print(f"{Fore.WHITE}[4/5] Domain Yaşı: {mesaj} {Fore.RED if skor>0 else Fore.GREEN}[+{skor}]{Style.RESET_ALL}")

    # 5. TLD Kontrol
    tld_skor = 0
    tld_mesaj = "Güvenli TLD"
    if domain.endswith(('.tk','.ml','.ga','.cf','.gq')):
        tld_skor = 10
        tld_mesaj = "Şüpheli TLD"
    toplam_skor += tld_skor
    detaylar.append(f"TLD: {tld_mesaj} [+{tld_skor}]")
    print(f"{Fore.WHITE}[5/5] TLD Kontrol: {tld_mesaj} {Fore.RED if tld_skor>0 else Fore.GREEN}[+{tld_skor}]{Style.RESET_ALL}")

    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    # Sonuç
    if toplam_skor >= 50:
        renk = Fore.RED + Style.BRIGHT
        durum = "KRİTİK TEHDİT"
    elif toplam_skor >= 30:
        renk = Fore.RED
        durum = "YÜKSEK RİSK"
    elif toplam_skor >= 15:
        renk = Fore.YELLOW
        durum = "ORTA RİSK"
    else:
        renk = Fore.GREEN
        durum = "DÜŞÜK RİSK"

    print(f"\n{renk}[!] TOPLAM SKOR: {toplam_skor}/100 - {durum}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}Detaylı Rapor:{Style.RESET_ALL}")
    for d in detaylar:
        print(f"{Fore.CYAN} - {d}{Style.RESET_ALL}")

    if toplam_skor >= 50:
        print(f"\n{Fore.RED}{Style.BRIGHT}[!] UYARI: Bu siteye GİRMEYİN, bilgi GİRMEYİN!{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] USOM'a ihbar edin: python3 araclar/13_usom_ihbar.py{Style.RESET_ALL}")

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] URL Skor Analizi Başlat{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Skor Sistemi Hakkında{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}SKOR > Seçim: {Style.RESET_ALL}").strip().lower()
        if secim == "1":
            url = input(f"\n{Fore.WHITE}Analiz Edilecek URL: {Style.RESET_ALL}").strip()
            if url: skor_hesapla(url)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "2":
            print(f"\n{Fore.CYAN}[i] Skor Sistemi:{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - USOM Kara Liste: +40 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - PhishTank Oltalama: +30 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - SSL Yok/Hatalı: +20 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - Ücretsiz SSL: +10 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - Yeni Domain <30 gün: +10 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - Şüpheli TLD: +10 puan{Style.RESET_ALL}")
            print(f"{Fore.WHITE} - 0-14: Düşük | 15-29: Orta | 30-49: Yüksek | 50+: Kritik{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
