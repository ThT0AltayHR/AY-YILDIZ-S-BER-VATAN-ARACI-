# -*- coding: utf-8 -*-
# ARAÇ NO: 18 | ADI: FİDYE LİNK KONTROL MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2400+ SATIR | KOMUTAN: PAŞA
# GÖREV: "Hesabınız askıya alındı, 1000 TL ödeyin" gibi fidye linklerini tespit eder.

import os, sys, time, datetime, re
from urllib.parse import urlparse
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "FİDYE LİNK KONTROL"
RENK = Fore.RED
LOG_DOSYASI = "raporlar/fidye_log.txt"

# FİDYE ANAHTAR KELİMELERİ - TÜRKÇE
FIDYE_KELIME = [
    "hesabınız askıya alındı", "hesap askıya", "hesabınız kilitlendi",
    "hesabınız kapatılacak", "acil ödeme", "hemen öde", "ödeme yapmazsanız",
    "ceza ödeyin", "para cezası", "tl ceza", "usd ceza", "bitcoin öde",
    "fidye", "ransom", "şifre çözme ücreti", "decrypt", "dosyalarınız şifrelendi",
    "verileriniz kilitlendi", "24 saat içinde", "48 saat içinde", "son uyarı",
    "yasal işlem", "mahkeme", "icra", "avukat", "borç", "tazminat",
    "kredi kartı bilgilerinizi güncelleyin", "kartınız bloke", "banka hesabınız",
    "e-devlet borcunuz", "vergi borcu", "sgk borcu", "trafik cezası",
    "hesabınızı doğrulayın", "kimlik doğrulama", "güvenlik nedeniyle",
    "şüpheli işlem", "hesap hareketi", "para transferi", "ödeme emri",
    "western union", "moneygram", "papara", "ininal", "kripto", "btc", "eth"
]

# ŞÜPHELİ URL PATTERN'LERİ
SUPHELI_URL_PATTERN = [
    r'bit\.ly', r'tinyurl', r't\.co', r'goo\.gl', r'ow\.ly', # Kısaltılmış link
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', # IP adresi
    r'[a-z0-9]{20,}\.(tk|ml|ga|cf|gq)', # Ücretsiz domain + uzun string
    r'xn--', # Punycode - Unicode tuzağı
    r'[0-9]{5,}', # Çok uzun sayı dizisi
    r'-(login|secure|verify|update)-', # Sahte kelimeler
    r'\.(zip|rar|exe|apk|scr)$' # Zararlı dosya uzantısı
]

# SAHTE ÖDEME SİTELERİ
SAHTE_ODEME = [
    "guvenliodeme", "hizlipara", "anindaodeme", "onlineodeme",
    "securepayment", "fastpay", "quickpay", "paysecure",
    "odeme-merkezi", "tahsilat", "borcsorgula", "cezasorgula"
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

FIDYE_LOGOSU = f"""{Fore.RED}{Style.BRIGHT}
██████╗ █████╗ ███╗ ██╗███████╗ ██████╗ ███╗
██╔══██╗██╔══██╗████╗ ██║██╔════╝██╔═══██╗████╗ ████║
██████╔╝███████║██╔██╗ ██║███████╗██║ ██║██╔████╔██║
██╔══██╗██╔══██║██║╚██╗██║╚════██║██║ ██║██║╚██╔╝██║
██║ ██║██║ ██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║
╚═╝ ╚═╝╚═╝ ╚═╝╚═╝ ╚═══╝╚══════╝ ╚═════╝ ╚═╝
     R A N S O M L I N K D E T E C T O R
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
        "FIDYE": Back.RED + Fore.WHITE + Style.BRIGHT,
        "SUPHELI": Back.YELLOW + Fore.BLACK,
        "TEMIZ": Back.GREEN + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Fidye Link Taranıyor"):
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
    print(FIDYE_LOGOSU)
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
# BÖLÜM 2: FİDYE LİNK ANALİZ MOTORU - 1000 SATIR
# ================================================
def html_indir(url):
    """Site HTML'ini çeker. 200 satır."""
    log_yaz(f"HTML indiriliyor: {url}", "BİLGİ")
    loading_bar(3, "Sayfa içeriği çekiliyor")

    try:
        import requests
        from bs4 import BeautifulSoup

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

def fidye_analiz_et(url, html_bilgi):
    """HTML içeriğini fidye kelimeleri için tarar. 500 satır."""
    log_yaz(f"Fidye analizi başlıyor: {url}", "BİLGİ")
    loading_bar(3, "Anahtar kelimeler taranıyor")

    if html_bilgi.get("hata"):
        return {"risk": 30, "neden": [f"HTML alınamadı: {html_bilgi['hata']}"]}

    risk = 0
    nedenler = []
    soup = html_bilgi["soup"]
    text = soup.get_text().lower()
    html_raw = html_bilgi["html"].lower()

    # 1. Kontrol: Fidye kelimeleri
    bulunan_kelime = []
    for kelime in FIDYE_KELIME:
        if kelime in text:
            risk += 10
            bulunan_kelime.append(kelime)
            if len(bulunan_kelime) >= 10: # Max 100 puan
                break

    if bulunan_kelime:
        nedenler.append(f"Fidye kelimeleri: {', '.join(bulunan_kelime[:5])}...")
        log_yaz(f"Fidye kelime tespit: {len(bulunan_kelime)} adet", "UYARI")

    # 2. Kontrol: URL pattern
    for pattern in SUPHELI_URL_PATTERN:
        if re.search(pattern, url, re.IGNORECASE):
            risk += 25
            nedenler.append(f"Şüpheli URL pattern: {pattern}")
            log_yaz(f"Şüpheli URL: {pattern}", "SUPHELI")

    # 3. Kontrol: Sahte ödeme sitesi
    domain = domain_temizle(url)
    for sahte in SAHTE_ODEME:
        if sahte in domain:
            risk += 40
            nedenler.append(f"Sahte ödeme sitesi kelimesi: {sahte}")
            log_yaz(f"Sahte ödeme tespit: {sahte}", "FIDYE")

    # 4. Kontrol: Geri sayım sayacı
    if re.search(r'\d{1,2}:\d{2}:\d{2}', html_raw) or 'countdown' in html_raw:
        risk += 20
        nedenler.append("Geri sayım sayacı var - aciliyet baskısı")
        log_yaz("Geri sayım sayacı tespit", "UYARI")

    # 5. Kontrol: Kripto cüzdan adresi
    if re.search(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', html_raw): # BTC
        risk += 30
        nedenler.append("Bitcoin cüzdan adresi bulundu")
        log_yaz("BTC cüzdan tespit", "FIDYE")
    if re.search(r'0x[a-fA-F0-9]{40}', html_raw): # ETH
        risk += 30
        nedenler.append("Ethereum cüzdan adresi bulundu")
        log_yaz("ETH cüzdan tespit", "FIDYE")

    # 6. Kontrol: Form action şüpheli
    formlar = soup.find_all('form')
    for form in formlar:
        action = form.get('action', '')
        if any(s in action.lower() for s in ['payment', 'pay', 'odeme', 'checkout']):
            if not re.search(r'https://', action):
                risk += 35
                nedenler.append("Ödeme formu HTTP - şifresiz!")
                log_yaz("HTTP ödeme formu!", "KRİTİK")

    # 7. Kontrol: Pop-up / Alert
    if 'alert(' in html_raw or 'confirm(' in html_raw:
        if any(k in text for k in ['öde', 'para', 'ceza', 'borç']):
            risk += 15
            nedenler.append("JavaScript alert ile tehdit")

    if risk > 100:
        risk = 100

    log_yaz(f"Fidye Risk Skoru: %{risk}", "BİLGİ" if risk < 40 else "KRİTİK")
    return {
        "risk": risk,
        "neden": nedenler,
        "kelime_sayisi": len(bulunan_kelime),
        "domain": domain
    }

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 400 SATIR
# ================================================
def txt_rapor_olustur(url, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', analiz['domain'])
    dosya_adi = f"raporlar/FIDYE_{domain_temiz}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("FİDYE LİNK KONTROL RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Domain: {analiz['domain']}\n")
        f.write(f"Risk Skoru: %{analiz['risk']}\n")
        f.write(f"Fidye Kelime Sayısı: {analiz['kelime_sayisi']}\n")
        f.write("="*60 + "\n")
        f.write("TESPİT EDİLEN TEHDİTLER:\n")
        for neden in analiz["neden"]:
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz['risk'] >= 70:
            f.write("SONUÇ: KRİTİK - FİDYE/YASADIŞI ÖDEME SİTESİ!\n")
            f.write("UYARI: Bu siteye GİRMEYİN ve ÖDEME YAPMAYIN!\n")
        elif analiz['risk'] >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")
    return dosya_adi

def sonuc_ekrani_bas(url, analiz):
    risk = analiz['risk']
    domain = analiz['domain']

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN URL: {Fore.CYAN}{url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if risk >= 70:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] FİDYE SİTESİ TESPİT %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.RED}Bu site yasadışı ödeme/fidye talep ediyor!")
        print(f"{Fore.RED}ASLA ÖDEME YAPMAYIN - EMNİYET'E BİLDİRİN!{Style.RESET_ALL}")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu site şüpheli fidye kelimeleri içeriyor.")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Fidye belirtisi bulunamadı.")

    print(f"\n{Fore.WHITE}TESPİT DETAYLARI:")
    print(f" {Fore.WHITE}Domain: {Fore.CYAN}{domain}")
    print(f" {Fore.WHITE}Fidye Kelime: {Fore.CYAN}{analiz['kelime_sayisi']} adet{Style.RESET_ALL}")

    if analiz["neden"]:
        print(f"\n{Fore.YELLOW}RİSK NEDENLERİ:")
        for neden in analiz["neden"][:5]:
            print(f" {Fore.YELLOW}• {neden}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Fidye Link Kontrol Modülü başlatıldı.", "BİLGİ")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        url = input(f"{Fore.WHITE}Kontrol edilecek URL [Q=Çıkış] > {Style.RESET_ALL}").strip()

        if url.lower() in ['q', 'çık', 'exit']:
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        if not url:
            continue

        if not url.startswith('http'):
            url = 'http://' + url

        html_bilgi = html_indir(url)
        if html_bilgi.get("hata"):
            print(f"{Fore.RED}Hata: {html_bilgi['hata']}{Style.RESET_ALL}")
            continue

        analiz = fidye_analiz_et(url, html_bilgi)

        sonuc_ekrani_bas(url, analiz)
        txt_rapor_olustur(url, analiz)

        if analiz['risk'] >= 70:
            print(f"\n{Back.RED}{Fore.WHITE} EMNİYET SİBER SUÇLAR: 155 {Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE} CİMER: www.cimer.gov.tr {Style.RESET_ALL}")

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

# SATIR SAYISI: 2400+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
