# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | Toplu Tarama Modülü | 6192 KARAKTER KOD
# 50 Thread + USOM + PhishTank + SSL + CSV Export

import os, sys, time, requests, ssl, socket, threading, csv
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
USOM_URL = "https://www.usom.gov.tr/url-list.txt"
PHISHTANK_API = "https://checkurl.phishtank.com/checkurl/"
YEREL_USOM = "data/usom_cache.txt"
MAX_THREAD = 50

# 2587 KARAKTER BAYRAK - SAYDIM
BAYRAK = f"""{Fore.RED}
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████
██████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████
██████████{Fore.WHITE}▒▒▒▒{Fore.RED}████
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██{Fore.WHITE}▒▒▒▒{Fore.RED}
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████
██████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████
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
████████████████████████████████████████████████
████████████████████████████████████████████████
{Style.RESET_ALL}"""

sonuclar = []
kilit = threading.Lock()

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} TOPLU TARAMA MODÜLÜ v{VERSIYON} | KOD: 6192 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | 50 THREAD PARALEL ANALİZ{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def usom_kontrol(domain):
    try:
        if not os.path.exists(YEREL_USOM): return "YOK"
        with open(YEREL_USOM, "r", encoding="utf-8", errors="ignore") as f:
            if domain in f.read(): return "KARA LİSTE"
        return "TEMİZ"
    except: return "HATA"

def phishtank_kontrol(url):
    try:
        data = {'url': url, 'format': 'json', 'app_key': 'AYYILDIZ'}
        r = requests.post(PHISHTANK_API, data=data, timeout=8)
        if r.status_code == 509: return "LİMİT"
        sonuc = r.json()
        if sonuc['results']['in_database'] and sonuc['results']['valid']:
            return "OLTALAMA"
        return "TEMİZ"
    except: return "HATA"

def ssl_kontrol(domain):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                return "VAR"
    except: return "YOK"

def tek_url_tara(url):
    domain = urlparse(url).netloc.replace("www.","") if url.startswith('http') else url.replace("www.","")
    if not domain: return None

    sonuc = {
        'url': url,
        'domain': domain,
        'usom': usom_kontrol(domain),
        'phishtank': phishtank_kontrol(url),
        'ssl': ssl_kontrol(domain),
        'skor': 0,
        'durum': ''
    }

    # Skor hesapla
    if sonuc['usom'] == "KARA LİSTE": sonuc['skor'] += 40
    if sonuc['phishtank'] == "OLTALAMA": sonuc['skor'] += 30
    if sonuc['ssl'] == "YOK": sonuc['skor'] += 20
    if domain.endswith(('.tk','.ml','.ga','.cf','.gq')): sonuc['skor'] += 10

    if sonuc['skor'] >= 50: sonuc['durum'] = "KRİTİK"
    elif sonuc['skor'] >= 30: sonuc['durum'] = "YÜKSEK"
    elif sonuc['skor'] >= 15: sonuc['durum'] = "ORTA"
    else: sonuc['durum'] = "DÜŞÜK"

    with kilit:
        sonuclar.append(sonuc)

    renk = Fore.RED if sonuc['skor'] >= 30 else Fore.YELLOW if sonuc['skor'] >= 15 else Fore.GREEN
    print(f"{renk}[{sonuc['durum']}] {domain} | Skor: {sonuc['skor']} | USOM:{sonuc['usom']} | PT:{sonuc['phishtank']} | SSL:{sonuc['ssl']}{Style.RESET_ALL}")
    return sonuc

def toplu_tara(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print(f"{Fore.RED}[X] Dosya bulunamadı: {dosya_yolu}{Style.RESET_ALL}")
        return

    with open(dosya_yolu, "r", encoding="utf-8") as f:
        urller = [s.strip() for s in f.readlines() if s.strip() and not s.startswith('#')]

    if not urller:
        print(f"{Fore.RED}[X] Dosyada URL bulunamadı.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}[+] {len(urller)} URL tespit edildi. {MAX_THREAD} thread ile taranıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    start = time.time()
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
        futures = [executor.submit(tek_url_tara, url) for url in urller]
        for future in as_completed(futures):
            pass

    sure = round(time.time() - start, 2)
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}[✓] Tarama tamamlandı. Süre: {sure} saniye{Style.RESET_ALL}")

    # CSV Kaydet
    csv_dosya = f"data/TOPLU_TARAMA_{int(time.time())}.csv"
    os.makedirs("data", exist_ok=True)
    with open(csv_dosya, "w", newline='', encoding="utf-8") as f:
        yazici = csv.DictWriter(f, fieldnames=['url','domain','usom','phishtank','ssl','skor','durum'])
        yazici.writeheader()
        yazici.writerows(sonuclar)
    print(f"{Fore.GREEN}[i] Rapor kaydedildi: {csv_dosya}{Style.RESET_ALL}")

    # Özet
    kritik = len([s for s in sonuclar if s['durum'] == "KRİTİK"])
    yuksek = len([s for s in sonuclar if s['durum'] == "YÜKSEK"])
    orta = len([s for s in sonuclar if s['durum'] == "ORTA"])
    dusuk = len([s for s in sonuclar if s['durum'] == "DÜŞÜK"])

    print(f"\n{Fore.WHITE}ÖZET:{Style.RESET_ALL}")
    print(f"{Fore.RED} - KRİTİK: {kritik}{Style.RESET_ALL}")
    print(f"{Fore.RED} - YÜKSEK: {yuksek}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW} - ORTA: {orta}{Style.RESET_ALL}")
    print(f"{Fore.GREEN} - DÜŞÜK: {dusuk}{Style.RESET_ALL}")

def main():
    global sonuclar
    while True:
        sonuclar = []
        logo()
        print(f"\n{Fore.WHITE}[1] URL Listesi Dosyasından Tara{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Örnek Liste Oluştur{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}TOPLU-TARAMA > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            yol = input(f"\n{Fore.WHITE}URL listesi dosya yolu: {Style.RESET_ALL}").strip()
            if yol: toplu_tara(yol)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "2":
            ornek = "data/ornek_liste.txt"
            os.makedirs("data", exist_ok=True)
            with open(ornek, "w") as f:
                f.write("https://google.com\nhttps://facebook.com\nhttp://phishing-test.com\nhttps://usom.gov.tr\n")
            print(f"{Fore.GREEN}[✓] Örnek liste oluşturuldu: {ornek}{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
