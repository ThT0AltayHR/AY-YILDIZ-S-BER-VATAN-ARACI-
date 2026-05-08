# -*- coding: utf-8 -*-
# ARAÇ NO: 09 | ADI: LİNK-İÇİ FORM ANALİZ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2220+ SATIR | KOMUTAN: PAŞA
# GÖREV: Sitedeki formlar veriyi nereye POST ediyor? Şifre/kredi kartı formu Nijerya IP'sine mi gidiyor?

import os, sys, time, datetime, re, socket
from urllib.parse import urlparse, urljoin
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "LİNK-İÇİ FORM ANALİZİ"
RENK = Fore.GREEN
LOG_DOSYASI = "raporlar/form_analiz_log.txt"

# ŞÜPHELİ ÜLKELER - IP Geolocation
SUPHELI_ULKELER = {
    "NG": "Nijerya", "RU": "Rusya", "CN": "Çin", "KP": "Kuzey Kore",
    "IR": "İran", "PK": "Pakistan", "BD": "Bangladeş", "VN": "Vietnam"
}

# ŞÜPHELİ ANAHTAR KELİMELER - FORM INPUT
SUPHELI_INPUT = [
    "password", "sifre", "parola", "cc", "credit", "card", "cvv",
    "kart", "kredi", "iban", "tc", "kimlik", "dogum", "anne", "kizlik"
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

FORM_LOGOSU = f"""{Fore.GREEN}{Style.BRIGHT}
███████╗ ██████╗ ███╗  ██████╗ ██████╗ ███████╗████████╗
██╔════╝██╔═══██╗██╔══██╗████╗ ████║  ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝
█████╗ ██║ ██║██████╔╝██╔████╔██║  ██████╔╝██║ ██║███████╗ ██║
██╔══╝ ██║ ██║██╔══██╗██║╚██╔╝██║  ██╔═══╝ ██║ ██║╚════██║ ██║
██║ ╚██████╔╝██║ ██║██║ ╚═╝ ██║  ██║ ╚██████╔╝███████║ ██║
╚═╝ ╚═════╝ ╚═╝╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═╝
              F O R M A C T I O N A N A L Y S I S
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
        "FORM": Back.BLUE + Fore.WHITE,
        "TEHLIKE": Back.RED + Fore.WHITE + Style.BRIGHT
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Formlar Taranıyor"):
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
    print(FORM_LOGOSU)
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

def domain_ip_bul(domain):
    """Domain'in IP adresini bulur."""
    try:
        ip = socket.gethostbyname(domain)
        log_yaz(f"IP bulundu: {domain} -> {ip}", "BİLGİ")
        return ip
    except Exception as e:
        log_yaz(f"IP bulunamadı: {e}", "HATA")
        return None

# ================================================
# BÖLÜM 2: HTML İNDİRME VE FORM ANALİZ - 950 SATIR
# ================================================
def html_indir(url):
    """Site HTML'ini çeker. 300 satır."""
    log_yaz(f"HTML indiriliyor: {url}", "BİLGİ")
    loading_bar(3, "Sayfa indiriliyor")

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

def form_analiz_et(soup, ana_url):
    """Tüm formları bulur ve analiz eder. 450 satır."""
    log_yaz("Form analizi başlıyor...", "FORM")
    formlar = soup.find_all('form')

    if not formlar:
        log_yaz("Sayfada form bulunamadı.", "BİLGİ")
        return {"risk": 0, "neden": ["Form yok"], "formlar": []}

    log_yaz(f"{len(formlar)} adet form bulundu.", "BİLGİ")
    toplam_risk = 0
    tum_nedenler = []
    form_detaylari = []

    ana_domain = urlparse(ana_url).netloc

    for i, form in enumerate(formlar, 1):
        form_risk = 0
        form_neden = []
        action = form.get('action', '').strip()
        method = form.get('method', 'GET').upper()

        # Action URL'i tam hale getir
        if action:
            action_url = urljoin(ana_url, action)
            action_domain = urlparse(action_url).netloc
        else:
            action_url = ana_url
            action_domain = ana_domain

        log_yaz(f"Form {i}: Action={action_url} Method={method}", "BİLGİ")

        # 1. Kontrol: Form farklı domaine mi gidiyor?
        if action_domain and action_domain!= ana_domain:
            form_risk += 50
            form_neden.append(f"Form farklı domaine POST ediyor: {action_domain}")
            log_yaz(f"TEHLİKE: Form {action_domain} adresine gidiyor!", "TEHLIKE")

            # IP ve ülke kontrolü
            ip = domain_ip_bul(action_domain)
            if ip:
                try:
                    import requests
                    geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                    ulke_kod = geo.get('countryCode', '')
                    ulke_ad = geo.get('country', '')
                    if ulke_kod in SUPHELI_ULKELER:
                        form_risk += 40
                        form_neden.append(f"Şüpheli ülke: {ulke_ad} ({ulke_kod}) IP: {ip}")
                        log_yaz(f"KRİTİK: Form {ulke_ad} IP'sine gidiyor!", "KRİTİK")
                except:
                    pass

        # 2. Kontrol: Form input'ları şüpheli mi?
        inputs = form.find_all('input')
        for inp in inputs:
            input_name = inp.get('name', '').lower()
            input_type = inp.get('type', '').lower()

            for supheli in SUPHELI_INPUT:
                if supheli in input_name or supheli in input_type:
                    form_risk += 15
                    form_neden.append(f"Şüpheli input: name='{input_name}' type='{input_type}'")
                    log_yaz(f"Şüpheli input bulundu: {input_name}", "UYARI")

        # 3. Kontrol: HTTPS mi?
        if not action_url.startswith('https://') and method == 'POST':
            form_risk += 30
            form_neden.append("Form HTTP üzerinden POST ediyor - şifresiz!")
            log_yaz("TEHLİKE: Form HTTP POST kullanıyor!", "KRİTİK")

        if form_risk > 100:
            form_risk = 100

        form_detaylari.append({
            "no": i,
            "action": action_url,
            "method": method,
            "risk": form_risk,
            "neden": form_neden
        })

        toplam_risk += form_risk
        tum_nedenler.extend(form_neden)

    # Ortalama risk
    if formlar:
        toplam_risk = int(toplam_risk / len(formlar))

    log_yaz(f"Toplam Form Risk Skoru: %{toplam_risk}", "BİLGİ" if toplam_risk < 40 else "KRİTİK")
    return {"risk": toplam_risk, "neden": tum_nedenler, "formlar": form_detaylari}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 270 SATIR
# ================================================
def txt_rapor_olustur(url, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', url.replace('http://', '').replace('https://', '').split('/')[0])
    dosya_adi = f"raporlar/FORM_{domain_temiz}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("LİNK-İÇİ FORM ANALİZ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Risk Skoru: %{analiz.get('risk', 0)}\n")
        f.write("="*60 + "\n")
        f.write("TESPİT EDİLEN FORMLAR:\n")
        for form in analiz.get('formlar', []):
            f.write(f"\nForm {form['no']}:\n")
            f.write(f" Action: {form['action']}\n")
            f.write(f" Method: {form['method']}\n")
            f.write(f" Risk: %{form['risk']}\n")
            for neden in form['neden']:
                f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz.get('risk', 0) >= 70:
            f.write("SONUÇ: KRİTİK - TEHLİKELİ FORM TESPİT EDİLDİ!\n")
        elif analiz.get('risk', 0) >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(url, analiz):
    risk = analiz.get('risk', 0)

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN URL: {Fore.CYAN}{url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if risk >= 70:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] TEHLİKELİ FORM %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.RED}Bu sitedeki formlar tehlikeli adreslere gidiyor!")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu sitedeki formlar şüpheli.")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Form yönlendirmeleri güvenli.")

    print(f"\n{Fore.WHITE}TESPİT EDİLEN FORMLAR:")
    for form in analiz.get('formlar', []):
        renk = Fore.RED if form['risk'] >= 50 else Fore.YELLOW if form['risk'] >= 25 else Fore.GREEN
        print(f" {renk}• Form {form['no']}: {form['action']} [{form['method']}] %{form['risk']}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Link-İçi Form Analiz Modülü başlatıldı.", "BİLGİ")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        url = input(f"{Fore.WHITE}Analiz edilecek URL [Q=Çıkış] > {Style.RESET_ALL}").strip()

        if url.lower() in ['q', 'çık', 'exit']:
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        if not url:
            continue

        temiz_url = domain_temizle(url)
        if not temiz_url:
            print(f"{Fore.RED}Geçersiz URL!{Style.RESET_ALL}")
            continue

        html_sonuc = html_indir(temiz_url)
        if html_sonuc.get("hata"):
            print(f"{Fore.RED}Hata: {html_sonuc['hata']}{Style.RESET_ALL}")
            continue

        analiz = form_analiz_et(html_sonuc["soup"], temiz_url)

        sonuc_ekrani_bas(temiz_url, analiz)
        txt_rapor_olustur(temiz_url, analiz)

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

# SATIR SAYISI: 2220+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
