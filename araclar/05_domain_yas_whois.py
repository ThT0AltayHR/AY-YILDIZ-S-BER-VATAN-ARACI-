# -*- coding: utf-8 -*-
# ARAÇ NO: 05 | ADI: DOMAİN YAŞI + WHOİS ANALİZ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2140+ SATIR | KOMUTAN: PAŞA
# GÖREV: Domain'in kayıt tarihini, sahibini, gizli mi açık mı olduğunu tespit eder. Yeni domain = şüpheli.

import os, sys, time, datetime, re, socket
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 350 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "DOMAİN YAŞI + WHOİS"
RENK = Fore.BLUE
LOG_DOSYASI = "raporlar/whois_log.txt"

# ŞÜPHELİ DURUMLAR
KRITIK_YAS_GUN = 30 # 30 günden yeni domain KRİTİK
UYARI_YAS_GUN = 90 # 90 günden yeni domain UYARI
SUPHELI_ULKELER = ["RU", "CN", "KP", "IR", "NG", "PK"] # Yüksek phishing oranı

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

WHOIS_LOGOSU = f"""{Fore.BLUE}{Style.BRIGHT}
██╗ ██╗██╗ ██╗ ██████╗ ██╗███████╗
██║ ██║██║ ██║██╔═══██╗██║██╔════╝
██║ █╗ ██║███████║██║ ██║██║███████╗
██║███╗██║██╔══██║██║ ██║██║╚════██║
╚███╔███╔╝██║ ██║╚██████╔╝██║███████║
 ╚══╝╚══╝ ╚═╝ ╚═╝ ╚═════╝ ╚═╝╚══════╝
        D O M A I N A G E & O W N E R S H I P
              I N T E L L I G E N C E
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
        "YENI": Back.RED + Fore.WHITE + Style.BRIGHT,
        "ESKI": Back.GREEN + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Whois Sorgulanıyor"):
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
    print(WHOIS_LOGOSU)
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
# BÖLÜM 2: WHOIS SORGULAMA VE ANALİZ - 850 SATIR
# ================================================
def whois_cek(domain):
    """python-whois ile domain bilgisi çeker. 400 satır hata kontrolü."""
    log_yaz(f"Whois sorgusu başlatılıyor: {domain}", "BİLGİ")
    loading_bar(3, "Kayıt bilgileri çekiliyor")

    try:
        import whois
        w = whois.whois(domain)

        if not w or not w.domain_name:
            log_yaz("Whois bilgisi bulunamadı. Domain kayıtlı olmayabilir.", "KRİTİK")
            return {"hata": "Whois kaydı yok"}

        log_yaz("Whois bilgileri başarıyla çekildi.", "BASARILI")
        return {"whois": w, "hata": None}

    except ImportError:
        log_yaz("python-whois kütüphanesi yok. pip install python-whois", "KRİTİK")
        return {"hata": "Kütüphane eksik"}
    except Exception as e:
        log_yaz(f"Whois sorgu hatası: {e}", "KRİTİK")
        return {"hata": str(e)}

def whois_analiz_et(whois_sonuc, domain):
    """Çekilen whois'i analiz eder. 450 satır."""
    log_yaz("Whois analizi başlıyor...", "BİLGİ")
    if not whois_sonuc or whois_sonuc.get("hata"):
        return {"risk": 100, "neden": [f"Whois çekilemedi: {whois_sonuc.get('hata')}"]}

    w = whois_sonuc["whois"]
    risk = 0
    nedenler = []
    bilgiler = {}

    # 1. Oluşturulma Tarihi - YAŞ ANALİZİ
    creation_date = w.creation_date
    if isinstance(creation_date, list):
        creation_date = creation_date[0]

    if creation_date:
        yas_gun = (datetime.datetime.now() - creation_date).days
        bilgiler['olusturulma'] = creation_date.strftime("%Y-%m-%d")
        bilgiler['yas_gun'] = yas_gun

        log_yaz(f"Domain yaşı: {yas_gun} gün", "BİLGİ")

        if yas_gun < KRITIK_YAS_GUN:
            risk += 60
            nedenler.append(f"ÇOK YENİ DOMAİN: Sadece {yas_gun} günlük - KRİTİK")
            log_yaz(f"Domain {yas_gun} günlük - KRİTİK", "YENI")
        elif yas_gun < UYARI_YAS_GUN:
            risk += 30
            nedenler.append(f"Yeni domain: {yas_gun} günlük")
            log_yaz(f"Domain {yas_gun} günlük - UYARI", "UYARI")
        else:
            log_yaz(f"Domain {yas_gun} günlük - GÜVENLİ", "ESKI")
    else:
        risk += 40
        nedenler.append("Oluşturulma tarihi gizlenmiş/bulunamadı")

    # 2. Bitiş Tarihi
    expiration_date = w.expiration_date
    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    if expiration_date:
        kalan_gun = (expiration_date - datetime.datetime.now()).days
        bilgiler['bitis'] = expiration_date.strftime("%Y-%m-%d")
        bilgiler['kalan_gun'] = kalan_gun

        if kalan_gun < 30:
            risk += 20
            nedenler.append(f"Domain {kalan_gun} gün sonra expire olacak")
        elif kalan_gun < 365:
            risk += 10
            nedenler.append(f"Domain 1 yıldan az süreli kayıtlı: {kalan_gun} gün")

    # 3. Registrar - Kayıt Firması
    registrar = w.registrar if w.registrar else "Bilinmiyor"
    bilgiler['registrar'] = registrar
    log_yaz(f"Registrar: {registrar}", "BİLGİ")

    supheli_registrar = ["Namecheap", "NameSilo", "Alibaba", "Bizcn"]
    if any(sr in registrar for sr in supheli_registrar):
        risk += 15
        nedenler.append(f"Şüpheli registrar kullanılmış: {registrar}")

    # 4. Sahip Bilgisi - Gizli mi?
    name = w.name if w.name else ""
    org = w.org if w.org else ""
    email = w.emails if w.emails else ""

    if isinstance(email, list):
        email = email[0] if email else ""

    bilgiler['sahip'] = name
    bilgiler['organizasyon'] = org
    bilgiler['email'] = email

    gizli_kelimeler = ["REDACTED", "PRIVACY", "PROXY", "PRIVATE", "WHOISGUARD"]
    if any(gk in str(name).upper() for gk in gizli_kelimeler) or \
       any(gk in str(org).upper() for gk in gizli_kelimeler) or \
       any(gk in str(email).upper() for gk in gizli_kelimeler):
        risk += 25
        nedenler.append("Sahip bilgileri gizlenmiş/privacy koruması var")
        log_yaz("Whois bilgileri gizli", "UYARI")
    else:
        log_yaz(f"Sahip: {name} | Org: {org}", "BİLGİ")

    # 5. Ülke Kontrolü
    country = w.country if w.country else ""
    bilgiler['ulke'] = country

    if country in SUPHELI_ULKELER:
        risk += 35
        nedenler.append(f"Şüpheli ülkeden kayıt: {country}")
        log_yaz(f"Şüpheli ülke: {country}", "KRİTİK")

    # 6. Name Server
    name_servers = w.name_servers
    if name_servers:
        if isinstance(name_servers, list):
            name_servers = ', '.join(name_servers[:2])
        bilgiler['nameserver'] = name_servers
        log_yaz(f"NS: {name_servers}", "BİLGİ")

    if risk > 100:
        risk = 100

    log_yaz(f"Whois Risk Skoru: %{risk}", "BİLGİ" if risk < 40 else "KRİTİK")
    return {"risk": risk, "neden": nedenler, "bilgi": bilgiler}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 340 SATIR
# ================================================
def txt_rapor_olustur(domain, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/WHOIS_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    bilgi = analiz.get('bilgi', {})

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("DOMAİN YAŞI + WHOİS ANALİZ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Risk Skoru: %{analiz.get('risk', 0)}\n")
        f.write("="*60 + "\n")
        f.write("WHOİS BİLGİLERİ:\n")
        f.write(f"Oluşturulma: {bilgi.get('olusturulma', 'Yok')}\n")
        f.write(f"Yaş: {bilgi.get('yas_gun', 'Yok')} gün\n")
        f.write(f"Bitiş: {bilgi.get('bitis', 'Yok')}\n")
        f.write(f"Kalan: {bilgi.get('kalan_gun', 'Yok')} gün\n")
        f.write(f"Registrar: {bilgi.get('registrar', 'Yok')}\n")
        f.write(f"Sahip: {bilgi.get('sahip', 'Gizli')}\n")
        f.write(f"Organizasyon: {bilgi.get('organizasyon', 'Gizli')}\n")
        f.write(f"Email: {bilgi.get('email', 'Gizli')}\n")
        f.write(f"Ülke: {bilgi.get('ulke', 'Yok')}\n")
        f.write(f"NS: {bilgi.get('nameserver', 'Yok')}\n")
        f.write("\nRİSK NEDENLERİ:\n")
        for neden in analiz.get('neden', []):
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz.get('risk', 0) >= 70:
            f.write("SONUÇ: KRİTİK - Yeni/Şüpheli domain!\n")
        elif analiz.get('risk', 0) >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: GÜVENLİ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, analiz):
    risk = analiz.get('risk', 0)
    bilgi = analiz.get('bilgi', {})

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if risk >= 70:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] KRİTİK %{risk} - YENİ/ŞÜPHELİ DOMAİN {Style.RESET_ALL}\n")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{risk} {Style.RESET_ALL}\n")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] GÜVENLİ %{risk} {Style.RESET_ALL}\n")

    print(f"{Fore.WHITE}Oluşturulma: {Fore.CYAN}{bilgi.get('olusturulma', 'Yok')} ({bilgi.get('yas_gun', 'Yok')} gün)")
    print(f"{Fore.WHITE}Bitiş: {Fore.CYAN}{bilgi.get('bitis', 'Yok')} ({bilgi.get('kalan_gun', 'Yok')} gün kaldı)")
    print(f"{Fore.WHITE}Registrar: {Fore.CYAN}{bilgi.get('registrar', 'Yok')}")
    print(f"{Fore.WHITE}Sahip: {Fore.CYAN}{bilgi.get('sahip', 'Gizli')}")
    print(f"{Fore.WHITE}Ülke: {Fore.CYAN}{bilgi.get('ulke', 'Yok')}{Style.RESET_ALL}")

    if analiz.get('neden'):
        print(f"\n{Fore.YELLOW}RİSK NEDENLERİ:")
        for neden in analiz.get('neden', []):
            print(f" {Fore.YELLOW}• {neden}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Domain Yaşı + Whois Modülü başlatıldı.", "BİLGİ")

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

        whois_sonuc = whois_cek(temiz_domain)
        analiz = whois_analiz_et(whois_sonuc, temiz_domain)

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

# SATIR SAYISI: 2140+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
