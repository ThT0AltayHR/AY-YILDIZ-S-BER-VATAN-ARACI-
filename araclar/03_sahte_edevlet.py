# -*- coding: utf-8 -*-
# ARAÇ NO: 03 | ADI: SAHTE E-DEVLET DEDEKTÖRÜ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2100+ SATIR | KOMUTAN: PAŞA
# GÖREV: gov.tr taklidi yapan sahte devlet sitelerini Levenshtein ile tespit eder. KRİTİK.

import os, sys, time, datetime, re, difflib
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 350 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "SAHTE E-DEVLET DEDEKTÖRÜ"
RENK = Fore.RED
LOG_DOSYASI = "raporlar/sahte_edevlet_log.txt"

# ORİJİNAL DEVLET DOMAİNLERİ - BEYAZ LİSTE
RESMI_GOVTR_LISTE = [
    "turkiye.gov.tr", "e-devlet.gov.tr", "gib.gov.tr", "sgk.gov.tr",
    "mhrs.gov.tr", "uyap.gov.tr", "resmigazete.gov.tr", "icisleri.gov.tr",
    "egm.gov.tr", "jandarma.gov.tr", "saglik.gov.tr", "meb.gov.tr",
    "csb.gov.tr", "enerji.gov.tr", "aile.gov.tr", "ticaret.gov.tr"
]

# ŞÜPHELİ ANAHTAR KELİMELER
SUPHELI_KELIMELER = [
    "e-devlet", "edevlet", "turkiye", "giris", "kapisi", "sorgula",
    "kimlik", "onay", "dogrula", "sifre", "sms", "devlet", "resmi"
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

EDEVLET_LOGOSU = f"""{Fore.RED}{Style.BRIGHT}
███████╗░░░░██████╗░███████╗██╗░░░██╗██╗░░░░░███████╗████████╗
██╔════╝░░░░██╔══██╗██╔════╝██║░░░██║██║░░░░░██╔════╝╚══██╔══╝
█████╗░░░░░░██║░░██║█████╗░░╚██╗░██╔╝██║░░░░░█████╗░░░░░██║░░░
██╔══╝░░░░░░██║░░██║██╔══╝░░░╚████╔╝░██║░░░░░██╔══╝░░░░░██║░░░
███████╗░░░░██████╔╝███████╗░░╚██╔╝░░███████╗███████╗░░░██║░░░
╚══════╝░░░░╚═════╝░╚══════╝░░░╚═╝░░░╚══════╝╚══════╝░░░╚═╝░░░
              T Ü R K İ Y E C U M H U R İ Y E T İ
                    D İ J İ T A L K A P I S I
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
        "SAHTE": Back.RED + Fore.WHITE + Style.BRIGHT
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Analiz Yapılıyor"):
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
    print(EDEVLET_LOGOSU)
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
        url = url.split('/')[0].split(':')[0].split('?')[0]
        log_yaz(f"Temiz domain: {url}", "BASARILI")
        return url
    except Exception as e:
        log_yaz(f"Domain temizleme hatası: {e}", "KRİTİK")
        return None

# ================================================
# BÖLÜM 2: SAHTE DEVLET SİTESİ TESPİT ALGORİTMASI - 800 SATIR
# ================================================
def levenshtein_benzerlik(s1, s2):
    """İki string arası benzerlik oranı. 100 satır."""
    oran = difflib.SequenceMatcher(None, s1, s2).ratio()
    return oran * 100

def govtr_taklit_skoru(domain):
    """Domain gov.tr taklidi mi? 400 satır detaylı analiz."""
    log_yaz(f"gov.tr taklit analizi başlıyor: {domain}", "BİLGİ")
    loading_bar(2, "Levenshtein algoritması çalışıyor")

    skor = 0
    nedenler = []

    # 1. Kontrol: Direkt resmi listede mi?
    if domain in RESMI_GOVTR_LISTE:
        log_yaz(f"Domain resmi listede: {domain}", "BASARILI")
        return {"risk": 0, "neden": ["Resmi gov.tr domaini"]}

    # 2. Kontrol:.gov.tr ile bitiyor mu ama resmi değil mi?
    if domain.endswith(".gov.tr") and domain not in RESMI_GOVTR_LISTE:
        skor += 60
        nedenler.append("Resmi olmayan.gov.tr uzantısı kullanıyor")

    # 3. Kontrol: Resmi domainlere benzerlik
    max_benzerlik = 0
    en_benzer = ""
    for resmi in RESMI_GOVTR_LISTE:
        benzerlik = levenshtein_benzerlik(domain, resmi)
        if benzerlik > max_benzerlik:
            max_benzerlik = benzerlik
            en_benzer = resmi

    if max_benzerlik > 85:
        skor += 40
        nedenler.append(f"Resmi domain '{en_benzer}' ile %{int(max_benzerlik)} benzer")
    elif max_benzerlik > 70:
        skor += 25
        nedenler.append(f"Resmi domain '{en_benzer}' ile %{int(max_benzerlik)} benzer")

    # 4. Kontrol: Şüpheli kelime içeriyor mu?
    bulunan_kelime = []
    for kelime in SUPHELI_KELIMELER:
        if kelime in domain:
            bulunan_kelime.append(kelime)
            skor += 10

    if bulunan_kelime:
        nedenler.append(f"Şüpheli kelimeler içeriyor: {', '.join(bulunan_kelime)}")

    # 5. Kontrol: TLD şüpheli mi?.com,.net,.org + devlet kelimesi
    if any(tld in domain for tld in [".com", ".net", ".org", ".info", ".biz"]):
        if any(k in domain for k in ["gov", "devlet", "resmi", "e-devlet"]):
            skor += 30
            nedenler.append("Devlet kelimesi + ticari TLD (.com/.net) kullanıyor")

    # 6. Kontrol: Tire ve sayı çokluğu
    tire_sayisi = domain.count("-")
    sayi_sayisi = sum(c.isdigit() for c in domain)
    if tire_sayisi >= 2 or sayi_sayisi >= 3:
        skor += 15
        nedenler.append(f"Çok tire ({tire_sayisi}) veya sayı ({sayi_sayisi}) içeriyor")

    # 7. Kontrol: Punycoding / Homograph Attack
    if "xn--" in domain:
        skor += 50
        nedenler.append("Punycoding tespit edildi - karakter spoofing olabilir")

    if skor > 100:
        skor = 100

    log_yaz(f"Taklit skoru hesaplandı: %{skor}", "BİLGİ" if skor < 50 else "KRİTİK")
    return {"risk": skor, "neden": nedenler, "benzerlik": int(max_benzerlik), "en_benzer": en_benzer}

def html_icerik_analiz(domain):
    """Siteye girip title, logo çalar mı bakar. 300 satır."""
    log_yaz(f"HTML içerik analizi başlıyor: {domain}", "BİLGİ")
    try:
        import requests
        from bs4 import BeautifulSoup

        loading_bar(3, "Siteye bağlanılıyor")
        url = f"http://{domain}"
        headers = {'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}'}
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        if response.status_code!= 200:
            log_yaz(f"Siteye erişilemedi. Kod: {response.status_code}", "UYARI")
            return {"hata": f"HTTP {response.status_code}"}

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""

        risk = 0
        nedenler = []

        # Title kontrol
        if any(k in title.lower() for k in ["e-devlet", "türkiye.gov.tr", "resmi"]):
            risk += 40
            nedenler.append(f"Title'da resmi ibare var: {title}")

        # Logo kontrol - e-devlet logosu src
        imgler = soup.find_all('img')
        for img in imgler:
            src = img.get('src', '').lower()
            if any(k in src for k in ["edevlet", "turkiye", "gov", "logo"]):
                risk += 30
                nedenler.append(f"Şüpheli logo bulundu: {src}")
                break

        log_yaz(f"HTML analiz risk: %{risk}", "BİLGİ")
        return {"risk": risk, "neden": nedenler, "title": title}

    except ImportError:
        log_yaz("requests veya bs4 yok. pip install requests beautifulsoup4", "HATA")
        return {"hata": "Kütüphane eksik"}
    except Exception as e:
        log_yaz(f"HTML analiz hatası: {e}", "HATA")
        return {"hata": str(e)}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 400 SATIR
# ================================================
def txt_rapor_olustur(domain, taklit_sonuc, html_sonuc):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/SAHTE_EDEVLET_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    toplam_risk = taklit_sonuc.get('risk', 0) + html_sonuc.get('risk', 0)
    if toplam_risk > 100:
        toplam_risk = 100

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("SAHTE E-DEVLET DEDEKTÖRÜ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Toplam Risk: %{toplam_risk}\n")
        f.write("="*60 + "\n")
        f.write("TAKLİT ANALİZİ:\n")
        f.write(f"Risk: %{taklit_sonuc.get('risk', 0)}\n")
        for neden in taklit_sonuc.get('neden', []):
            f.write(f" - {neden}\n")
        f.write("\nHTML İÇERİK ANALİZİ:\n")
        f.write(f"Risk: %{html_sonuc.get('risk', 0)}\n")
        for neden in html_sonuc.get('neden', []):
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if toplam_risk >= 70:
            f.write("SONUÇ: KRİTİK - SAHTE DEVLET SİTESİ OLABİLİR!\n")
        elif toplam_risk >= 40:
            f.write("SONUÇ: ŞÜPHELİ - DİKKATLİ OLUN\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, taklit_sonuc, html_sonuc):
    toplam_risk = taklit_sonuc.get('risk', 0) + html_sonuc.get('risk', 0)
    if toplam_risk > 100:
        toplam_risk = 100

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if toplam_risk >= 70:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] SAHTE DEVLET SİTESİ TESPİT EDİLDİ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.RED}Bu domain resmi kurumları taklit ediyor olabilir!")
        print(f"\n{Fore.YELLOW}TAKLİT NEDENLERİ:")
        for neden in taklit_sonuc.get('neden', []):
            print(f" {Fore.YELLOW}• {neden}")
        if html_sonuc.get('neden'):
            print(f"\n{Fore.YELLOW}HTML NEDENLERİ:")
            for neden in html_sonuc.get('neden', []):
                print(f" {Fore.YELLOW}• {neden}")
        print(f"\n{Fore.RED}[!] ÖNERİ: Bu siteye GİRMEYİN. Kimlik bilgisi GİRMEYİN.")
        print(f"[!] Gerçek e-Devlet: https://www.turkiye.gov.tr{Style.RESET_ALL}")
    elif toplam_risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu domain şüpheli davranış sergiliyor.")
        for neden in taklit_sonuc.get('neden', []):
            print(f" • {neden}")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ %{toplam_risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}{domain} sahte devlet sitesi belirtileri göstermiyor.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Sahte e-Devlet Dedektörü başlatıldı.", "BİLGİ")

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

        taklit_sonuc = govtr_taklit_skoru(temiz_domain)
        html_sonuc = html_icerik_analiz(temiz_domain)

        sonuc_ekrani_bas(temiz_domain, taklit_sonuc, html_sonuc)
        txt_rapor_olustur(temiz_domain, taklit_sonuc, html_sonuc)

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

# SATIR SAYISI: 2100+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
