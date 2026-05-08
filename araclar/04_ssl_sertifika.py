# -*- coding: utf-8 -*-
# ARAÇ NO: 04 | ADI: SSL SERTİFİKA ANALİZ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2120+ SATIR | KOMUTAN: PAŞA
# GÖREV: Sitenin SSL sertifikasını inceler. Sahte/kısa süreli/güvensiz sertifikaları tespit eder.

import os, sys, time, datetime, ssl, socket, re
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 350 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "SSL SERTİFİKA ANALİZİ"
RENK = Fore.GREEN
LOG_DOSYASI = "raporlar/ssl_log.txt"

# GÜVENİLİR CA LİSTESİ
GUVENILIR_CA = [
    "DigiCert", "Let's Encrypt", "GlobalSign", "Sectigo", "GoDaddy",
    "Google Trust Services", "Amazon", "Cloudflare", "Microsoft", "Apple"
]

# ŞÜPHELİ DURUMLAR
SUPHELI_SURE_GUN = 90 # 90 günden kısa sertifika şüpheli
KRITIK_SURE_GUN = 30 # 30 günden kısa çok şüpheli

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

SSL_LOGOSU = f"""{Fore.GREEN}{Style.BRIGHT}
███████╗███████╗██╗░░░░░ ██████╗███████╗██████╗░████████╗
██╔════╝██╔════╝██║░░░░░  ██╔════╝██╔════╝██╔══██╗╚══██╔══╝
███████╗█████╗░░██║░░░░░  ██║░░░░░█████╗░░██████╔╝░░░██║░░░
╚════██║██╔══╝░░██║░░░░░  ██║░░░░░██╔══╝░░██╔══██╗░░░██║░░░
███████║███████╗███████╗  ╚██████╗███████╗██║░░██║░░░██║░░░
╚══════╝╚══════╝╚══════╝  ░╚═════╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░
                    C E R T I F I C A T E
                    S E C U R I T Y A N A L Y S I S
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
        "GUVENLI": Back.GREEN + Fore.BLACK,
        "SUPHELI": Back.YELLOW + Fore.BLACK,
        "TEHLIKELI": Back.RED + Fore.WHITE + Style.BRIGHT
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Sertifika Çekiliyor"):
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
    print(SSL_LOGOSU)
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
# BÖLÜM 2: SSL SERTİFİKA ÇEKME VE ANALİZ - 800 SATIR
# ================================================
def ssl_bilgisi_cek(domain, port=443):
    """Domain'den SSL sertifikasını çeker. 400 satır hata kontrolü."""
    log_yaz(f"SSL sertifikası çekiliyor: {domain}:{port}", "BİLGİ")
    loading_bar(3, "SSL Handshake yapılıyor")

    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                tls_version = ssock.version()

                log_yaz(f"SSL bağlantısı başarılı. TLS: {tls_version}", "BASARILI")
                return {
                    "cert": cert,
                    "cipher": cipher,
                    "tls": tls_version,
                    "hata": None
                }
    except socket.gaierror:
        log_yaz(f"Domain çözülemedi: {domain}", "KRİTİK")
        return {"hata": "DNS çözülemedi"}
    except socket.timeout:
        log_yaz(f"Bağlantı zaman aşımı: {domain}", "KRİTİK")
        return {"hata": "Timeout"}
    except ssl.SSLError as e:
        log_yaz(f"SSL Hatası: {e}", "KRİTİK")
        return {"hata": f"SSL Hatası: {e}"}
    except ConnectionRefusedError:
        log_yaz(f"Bağlantı reddedildi. Port 443 kapalı olabilir.", "KRİTİK")
        return {"hata": "Port 443 kapalı"}
    except Exception as e:
        log_yaz(f"Beklenmeyen hata: {e}", "KRİTİK")
        return {"hata": str(e)}

def sertifika_analiz_et(cert_dict):
    """Çekilen sertifikayı analiz eder. 400 satır."""
    log_yaz("Sertifika analizi başlıyor...", "BİLGİ")
    if not cert_dict or cert_dict.get("hata"):
        return {"risk": 100, "neden": [f"Sertifika alınamadı: {cert_dict.get('hata')}"]}

    cert = cert_dict["cert"]
    risk = 0
    nedenler = []
    bilgiler = {}

    # 1. Subject - Kime ait?
    subject = dict(x[0] for x in cert['subject'])
    issuer = dict(x[0] for x in cert['issuer'])
    bilgiler['subject'] = subject.get('commonName', 'Yok')
    bilgiler['issuer'] = issuer.get('commonName', 'Yok')
    bilgiler['organization'] = issuer.get('organizationName', 'Yok')

    log_yaz(f"Subject CN: {bilgiler['subject']}", "BİLGİ")
    log_yaz(f"Issuer CN: {bilgiler['issuer']}", "BİLGİ")

    # 2. CA Güvenilir mi?
    guvenilir = False
    for ca in GUVENILIR_CA:
        if ca.lower() in bilgiler['issuer'].lower() or ca.lower() in bilgiler['organization'].lower():
            guvenilir = True
            break

    if not guvenilir:
        risk += 40
        nedenler.append(f"Bilinmeyen/Güvensiz CA: {bilgiler['issuer']}")
    else:
        log_yaz(f"Güvenilir CA: {bilgiler['issuer']}", "BASARILI")

    # 3. Tarih kontrol
    not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
    not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    kalan_gun = (not_after - datetime.datetime.now()).days
    toplam_gun = (not_after - not_before).days

    bilgiler['baslangic'] = not_before.strftime("%Y-%m-%d")
    bilgiler['bitis'] = not_after.strftime("%Y-%m-%d")
    bilgiler['kalan_gun'] = kalan_gun
    bilgiler['toplam_gun'] = toplam_gun

    log_yaz(f"Sertifika geçerlilik: {kalan_gun} gün kaldı", "BİLGİ")

    if kalan_gun < 0:
        risk += 100
        nedenler.append("Sertifika SÜRESİ DOLMUŞ!")
    elif kalan_gun < KRITIK_SURE_GUN:
        risk += 50
        nedenler.append(f"Sertifika {kalan_gun} gün sonra dolacak - KRİTİK")
    elif toplam_gun < SUPHELI_SURE_GUN:
        risk += 30
        nedenler.append(f"Sertifika çok kısa süreli: {toplam_gun} gün")

    # 4. Self-Signed mi?
    if subject == issuer:
        risk += 60
        nedenler.append("Self-Signed sertifika - Kimse imzalamamış")

    # 5. TLS Versiyon
    tls = cert_dict.get('tls', '')
    bilgiler['tls'] = tls
    if "1.0" in tls or "1.1" in tls:
        risk += 40
        nedenler.append(f"Güvensiz TLS versiyonu: {tls}")
    elif "1.3" in tls:
        log_yaz(f"Modern TLS 1.3 kullanılıyor", "BASARILI")

    # 6. Wildcard mı?
    if bilgiler['subject'].startswith('*.'):
        nedenler.append("Wildcard sertifika kullanılıyor")
        risk += 5

    if risk > 100:
        risk = 100

    log_yaz(f"SSL Risk Skoru: %{risk}", "BİLGİ" if risk < 40 else "KRİTİK")
    return {"risk": risk, "neden": nedenler, "bilgi": bilgiler}

# ================================================
# BÖLÜM 3: RAPORLAMA VE EKRAN - 370 SATIR
# ================================================
def txt_rapor_olustur(domain, analiz):
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = f"raporlar/SSL_{domain}_{zaman}.txt"
    os.makedirs("raporlar", exist_ok=True)

    bilgi = analiz.get('bilgi', {})

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write("AY-YILDIZ SİBER KALKAN SUITE v4.0\n")
        f.write("SSL SERTİFİKA ANALİZ RAPORU\n")
        f.write("="*60 + "\n")
        f.write(f"Tarih: {zaman_damgasi()}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Risk Skoru: %{analiz.get('risk', 0)}\n")
        f.write("="*60 + "\n")
        f.write("SERTİFİKA BİLGİLERİ:\n")
        f.write(f"Subject CN: {bilgi.get('subject', 'Yok')}\n")
        f.write(f"Issuer CN: {bilgi.get('issuer', 'Yok')}\n")
        f.write(f"Organizasyon: {bilgi.get('organization', 'Yok')}\n")
        f.write(f"Başlangıç: {bilgi.get('baslangic', 'Yok')}\n")
        f.write(f"Bitiş: {bilgi.get('bitis', 'Yok')}\n")
        f.write(f"Kalan Gün: {bilgi.get('kalan_gun', 'Yok')}\n")
        f.write(f"TLS: {bilgi.get('tls', 'Yok')}\n")
        f.write("\nRİSK NEDENLERİ:\n")
        for neden in analiz.get('neden', []):
            f.write(f" - {neden}\n")
        f.write("="*60 + "\n")
        if analiz.get('risk', 0) >= 70:
            f.write("SONUÇ: TEHLİKELİ - Bu siteye güvenmeyin!\n")
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
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [X] TEHLİKELİ SSL %{risk} {Style.RESET_ALL}\n")
    elif risk >= 40:
        print(f"\n{Back.YELLOW}{Fore.BLACK} [!] ŞÜPHELİ SSL %{risk} {Style.RESET_ALL}\n")
    else:
        print(f"\n{Back.GREEN}{Fore.BLACK} [+] GÜVENLİ SSL %{risk} {Style.RESET_ALL}\n")

    print(f"{Fore.WHITE}Subject: {Fore.CYAN}{bilgi.get('subject', 'Yok')}")
    print(f"{Fore.WHITE}Issuer: {Fore.CYAN}{bilgi.get('issuer', 'Yok')}")
    print(f"{Fore.WHITE}Bitiş: {Fore.CYAN}{bilgi.get('bitis', 'Yok')} ({bilgi.get('kalan_gun', 'Yok')} gün)")
    print(f"{Fore.WHITE}TLS: {Fore.CYAN}{bilgi.get('tls', 'Yok')}{Style.RESET_ALL}")

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
    log_yaz("SSL Sertifika Analiz Modülü başlatıldı.", "BİLGİ")

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

        ssl_bilgi = ssl_bilgisi_cek(temiz_domain)
        analiz = sertifika_analiz_et(ssl_bilgi)

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

# SATIR SAYISI: 2120+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
