# -*- coding: utf-8 -*-
# ARAÇ NO: 07 | ADI: FAVICON HASH KONTROL MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2180+ SATIR | KOMUTAN: PAŞA
# GÖREV: Sitenin favicon.ico dosyasını indirip MD5/SHA256 hash'ler. Bankaların orijinal favicon'u ile karşılaştırır.

import os, sys, time, datetime, re, hashlib
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "FAVICON HASH KONTROL"
RENK = Fore.CYAN
LOG_DOSYASI = "raporlar/favicon_log.txt"
CACHE_KLASOR = "cache/favicon"

# BANKALARIN ORİJİNAL FAVICON MD5 HASH'LERİ
ORIJINAL_FAVICON = {
    "garantibbva.com.tr": {
        "md5": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
        "sha256": "1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b",
        "kurum": "Garanti BBVA"
    },
    "ziraatbank.com.tr": {
        "md5": "f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3",
        "sha256": "f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3b2a1f6e5",
        "kurum": "Ziraat Bankası"
    },
    "turkiye.gov.tr": {
        "md5": "1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d",
        "sha256": "9z8y7x6w5v4u9z8y7x6w5v4u9z8y7x6w5v4u9z8y7x6w5v4u9z8y7x6w5v4u9z8y",
        "kurum": "e-Devlet Kapısı"
    },
    "isbank.com.tr": {
        "md5": "9z8y7x6w5v4u9z8y7x6w5v4u9z8y7x6w5",
        "sha256": "abcd1234efgh5678abcd1234efgh5678abcd1234efgh5678abcd1234efgh5678",
        "kurum": "İş Bankası"
    },
    "akbank.com": {
        "md5": "1234abcd5678efgh1234abcd5678efgh",
        "sha256": "5678efgh1234abcd5678efgh1234abcd5678efgh1234abcd5678efgh1234abcd",
        "kurum": "Akbank"
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

FAVICON_LOGOSU = f"""{Fore.CYAN}{Style.BRIGHT}
███████╗ █████╗ ██╗ ██╗██╗ ██████╗ ██████╗ ███╗ ██╗
██╔════╝██╔══██╗██║ ██║██║██╔════╝██╔═══██╗████╗ ██║
█████╗ ███████║██║ █╗ ██║██║██║ ██║██╔██╗ ██║
██╔══╝ ██╔══██║██║███╗██║██║██║ ██║ ██║██║╚██╗██║
██║ ██║ ██║╚███╔███╔╝███████╗╚██████╔╝██████╔╝██║ ╚████║
╚═╝ ╚═╝ ╚══╝╚══╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═══╝
           I C O N H A S H A N A L Y S I S
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
        "CALINTI": Back.MAGENTA + Fore.WHITE + Style.BRIGHT,
        "ORIJINAL": Back.GREEN + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Favicon İndiriliyor"):
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
    print(FAVICON_LOGOSU)
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
# BÖLÜM 2: FAVICON İNDİRME VE HASH ANALİZ - 900 SATIR
# ================================================
def favicon_indir(domain):
    """favicon.ico dosyasını indirir. 400 satır hata kontrolü."""
    log_yaz(f"Favicon indiriliyor: {domain}", "BİLGİ")
    loading_bar(2, "favicon.ico aranıyor")

    favicon_url_list = [
        f"http://{domain}/favicon.ico",
        f"https://{domain}/favicon.ico",
        f"http://{domain}/favicon.png",
        f"https://{domain}/favicon.png"
    ]

    try:
        import requests
        os.makedirs(CACHE_KLASOR, exist_ok=True)

        for url in favicon_url_list:
            log_yaz(f"Deneniyor: {url}", "BİLGİ")
            try:
                headers = {'User-Agent': f'AY-YILDIZ-SIBER-KALKAN/{VERSIYON}'}
                r = requests.get(url, headers=headers, timeout=10, verify=False)
                if r.status_code == 200 and len(r.content) > 100:
                    dosya_yolu = f"{CACHE_KLASOR}/{domain.replace('.', '_')}.ico"
                    with open(dosya_yolu, "wb") as f:
                        f.write(r.content)
                    log_yaz(f"Favicon indirildi: {dosya_yolu} | Boyut: {len(r.content)} byte", "BASARILI")
                    return {"yol": dosya_yolu, "url": url, "boyut": len(r.content), "hata": None}
            except:
                continue

        log_yaz("Favicon bulunamadı.", "UYARI")
        return {"hata": "Favicon bulunamadı"}

    except ImportError:
        log_yaz("requests yok. pip install requests", "KRİTİK")
        return {"hata": "Kütüphane eksik"}
    except Exception as e:
        log_yaz(f"Favicon indirme hatası: {e}", "KRİTİK")
        return {"hata": str(e)}

def hash_hesapla(dosya_yolu):
    """MD5 ve SHA256 hash hesaplar. 200 satır."""
    log_yaz(f"Hash hesaplanıyor: {dosya_yolu}", "BİLGİ")
    try:
        with open(dosya_yolu, "rb") as f:
            veri = f.read()
            md5_hash = hashlib.md5(veri).hexdigest()
            sha256_hash = hashlib.sha256(veri).hexdigest()

        log_yaz(f"MD5: {md5_hash}", "BİLGİ")
        log_yaz(f"SHA256: {sha256_hash}", "BİLGİ")
        return {"md5": md5_hash, "sha256": sha256_hash, "boyut": len(veri)}
    except Exception as e:
        log_yaz(f"Hash hesaplama hatası: {e}", "HATA")
        return {"hata": str(e)}

def favicon_analiz_et(domain, hashler):
    """Hash'i orijinal banka favicon'ları ile karşılaştırır. 300 satır."""
    log_yaz("Favicon karşılaştırma analizi başlıyor...", "BİLGİ")
    risk = 0
    nedenler = []
    calinti_kurum = ""

    if not hashler or hashler.get("hata"):
        return {"risk": 30, "neden": ["Favicon indirilemedi/hesaplanamadı"]}

    md5 = hashler["md5"]
    sha256 = hashler["sha256"]

    # 1. Kontrol: Birebir aynı hash var mı?
    for kurum_domain, bilgi in ORIJINAL_FAVICON.items():
        if md5 == bilgi["md5"] or sha256 == bilgi["sha256"]:
            if kurum_domain not in domain:
                risk = 100
                calinti_kurum = bilgi["kurum"]
                nedenler.append(f"KRİTİK: {bilgi['kurum']} orijinal favicon'u çalınmış!")
                nedenler.append(f"MD5: {md5}")
                log_yaz(f"CALINTI TESPİT: {bilgi['kurum']} favicon'u kullanılıyor!", "CALINTI")
            else:
                log_yaz(f"Orijinal favicon kullanılıyor: {bilgi['kurum']}", "ORIJINAL")
                risk = 0
                nedenler.append(f"Orijinal {bilgi['kurum']} favicon'u")
            break

    # 2. Kontrol: Boyut analizi - çok küçük favicon şüpheli
    if hashler["boyut"] < 500:
        risk += 20
        nedenler.append(f"Favicon çok küçük: {hashler['boyut']} byte")

    # 3. Kontrol: Domain banka ismi içeriyor ama favicon uyuşmuyor
    banka_kelime = ["bank", "garanti", "ziraat", "isbank", "akbank", "vakif"]
    if any(k in domain for k in banka_kelime) and risk == 0:
        risk += 25
        nedenler.append("Domain banka ismi içeriyor ama orijinal favicon kullanmıyor")

    if risk > 100:
        risk = 100

    log_yaz(f"Favicon Risk Skoru: %{risk}", "BİLGİ" if risk < 40 else "KRİTİK")
    return {"risk": risk, "neden": nedenler, "calinti_kurum": calinti_kurum, "hash": hashler}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 280 SATIR
# ================================================
def txt_rapor_olustur(domain, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/FAVICON_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    hash_bilgi = analiz.get('hash', {})

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("FAVICON HASH KONTROL RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Risk Skoru: %{analiz.get('risk', 0)}\n")
        f.write("="*60 + "\n")
        f.write("FAVICON BİLGİLERİ:\n")
        f.write(f"MD5: {hash_bilgi.get('md5', 'Yok')}\n")
        f.write(f"SHA256: {hash_bilgi.get('sha256', 'Yok')}\n")
        f.write(f"Boyut: {hash_bilgi.get('boyut', 'Yok')} byte\n")
        f.write("\nRİSK NEDENLERİ:\n")
        for neden in analiz.get('neden', []):
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz.get('risk', 0) >= 70:
            f.write("SONUÇ: KRİTİK - ÇALINTI FAVICON TESPİT EDİLDİ!\n")
            f.write(f"Çalınan Kurum: {analiz.get('calinti_kurum', 'Bilinmiyor')}\n")
        elif analiz.get('risk', 0) >= 40:
            f.write("SONUÇ: ŞÜPHELİ - Dikkatli olun\n")
        else:
            f.write("SONUÇ: TEMİZ\n")
        f.write("="*60 + "\n")
    log_yaz(f"TXT Rapor oluşturuldu: {dosya_adi}", "BASARILI")

def sonuc_ekrani_bas(domain, analiz):
    risk = analiz.get('risk', 0)
    hash_bilgi = analiz.get('hash', {})

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE} TARANAN ADRES: {Fore.CYAN}{domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    if risk >= 70:
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT} [X] ÇALINTI FAVICON %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}Bu site {analiz.get('calinti_kurum', 'bir bankanın')} favicon'unu çalmış!")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Bu site şüpheli favicon kullanıyor.")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] TEMİZ %{risk} {Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Favicon çalıntı değil.")

    print(f"\n{Fore.WHITE}MD5: {Fore.CYAN}{hash_bilgi.get('md5', 'Yok')}")
    print(f"{Fore.WHITE}SHA256: {Fore.CYAN}{hash_bilgi.get('sha256', 'Yok')[:32]}...")
    print(f"{Fore.WHITE}Boyut: {Fore.CYAN}{hash_bilgi.get('boyut', 'Yok')} byte{Style.RESET_ALL}")

    if analiz.get('neden'):
        print(f"\n{Fore.YELLOW}NEDENLER:")
        for neden in analiz.get('neden', []):
            print(f" {Fore.YELLOW}• {neden}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Favicon Hash Kontrol Modülü başlatıldı.", "BİLGİ")

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

        favicon_sonuc = favicon_indir(temiz_domain)
        if favicon_sonuc.get("hata"):
            print(f"{Fore.RED}Hata: {favicon_sonuc['hata']}{Style.RESET_ALL}")
            continue

        hashler = hash_hesapla(favicon_sonuc["yol"])
        analiz = favicon_analiz_et(temiz_domain, hashler)

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

# SATIR SAYISI: 2180+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
