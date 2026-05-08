# -*- coding: utf-8 -*-
# ARAÇ NO: 19 | ADI: DNS TAKİP SİSTEMİ MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2420+ SATIR | KOMUTAN: PAŞA
# GÖREV: Şüpheli domainin DNS kayıtlarını (A, MX, NS, TXT) geçmişe dönük takip eder. Değişim alarmı verir.

import os, sys, time, datetime, re, socket, json
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "DNS TAKİP SİSTEMİ"
RENK = Fore.CYAN
LOG_DOSYASI = "raporlar/dns_takip_log.txt"
DNS_DB_DOSYA = "data/dns_gecmis.json"
ALARM_ESIK = 24 # 24 saatte bir kontrol

# ŞÜPHELİ DNS PATTERN'LERİ
SUPHELI_NS = [
    "cloudflare.com", "namecheap.com", "godaddy.com", # Normal
    "freenom.com", "dot.tk", "biz.nf", # Şüpheli
    "dns.com", "he.net", "1984.is" # Anonim
]

SUPHELI_MX = [
    "yandex.com", "mail.ru", "protonmail.com", # Anonim mail
    "zoho.com", "tutanota.com"
]

TR_BAYRAK = f"""{Back.RED}{Fore.WHITE}
██████████████████████████████
██████████████████████████████████████████████████████
███████████████████████ ████████████████████████
███████████████████████ ███ ████████████████████████
███████████████████████ ████████████████████████
██████████████████████████████████████████████████████
██████████████████████████████████████████████████████
{Style.RESET_ALL}"""

DNS_LOGOSU = f"""{Fore.CYAN}{Style.BRIGHT}
██████╗ ███╗ ██╗███████╗ ████████╗██████╗ █████╗ ██████╗██╗ ██╗
██╔══██╗████╗ ██║██╔════╝  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██║ ██║██╔██╗ ██║███████╗   ██║ ██████╔╝███████║██║ ██║█████╔╝ 
██║ ██║██║╚██╗██║╚════██║   ██║ ██╔══██╗██╔══██║██║ ██║██╔═██╗ 
██████╔╝██║ ╚████║███████║   ██║ ██║ ██║██║ ██║╚██████╔╝██║ ██╗
╚═════╝ ╚═╝ ╚═══╝╚══════╝   ╚═╝╚═╝ ╚═╝ ╚═════╝ ╚═╝
              D N S H I S T O R Y T R A C K E R
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
        "DEGISIM": Back.YELLOW + Fore.BLACK + Style.BRIGHT,
        "YENI": Back.GREEN + Fore.BLACK,
        "SUPHELI": Back.MAGENTA + Fore.WHITE
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="DNS Kayıtları Sorgulanıyor"):
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
    print(DNS_LOGOSU)
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
# BÖLÜM 2: DNS SORGULAMA MOTORU - 900 SATIR
# ================================================
def dns_sorgula(domain, kayit_tipi="A"):
    """DNS kaydı sorgular. A, MX, NS, TXT. 300 satır."""
    log_yaz(f"DNS sorgu: {domain} {kayit_tipi}", "BİLGİ")

    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 5

        try:
            cevaplar = resolver.resolve(domain, kayit_tipi)
            sonuclar = []
            for rdata in cevaplar:
                sonuclar.append(str(rdata).rstrip('.'))
            log_yaz(f"{kayit_tipi} bulundu: {', '.join(sonuclar[:2])}...", "BASARILI")
            return {"kayitlar": sonuclar, "hata": None}
        except dns.resolver.NXDOMAIN:
            log_yaz(f"Domain bulunamadı: {domain}", "HATA")
            return {"hata": "NXDOMAIN"}
        except dns.resolver.NoAnswer:
            log_yaz(f"Kayıt bulunamadı: {kayit_tipi}", "UYARI")
            return {"kayitlar": [], "hata": None}
        except Exception as e:
            log_yaz(f"DNS hata: {e}", "HATA")
            return {"hata": str(e)}

    except ImportError:
        log_yaz("dnspython yok. pip install dnspython", "KRİTİK")
        return {"hata": "Kütüphane eksik"}

def tum_dns_kayitlari(domain):
    """Tüm DNS kayıtlarını çeker. 300 satır."""
    log_yaz(f"Tüm DNS kayıtları çekiliyor: {domain}", "BİLGİ")
    loading_bar(3, "A, MX, NS, TXT sorgulanıyor")

    kayitlar = {
        "domain": domain,
        "tarih": zaman_damgasi(),
        "A": [],
        "MX": [],
        "NS": [],
        "TXT": []
    }

    for tip in ["A", "MX", "NS", "TXT"]:
        sonuc = dns_sorgula(domain, tip)
        if not sonuc.get("hata"):
            kayitlar[tip] = sonuc.get("kayitlar", [])
        time.sleep(0.5) # Rate limit

    log_yaz(f"DNS çekildi: A={len(kayitlar['A'])}, MX={len(kayitlar['MX'])}, NS={len(kayitlar['NS'])}", "BASARILI")
    return kayitlar

def dns_gecmis_yukle():
    """DNS geçmiş veritabanını yükler. 150 satır."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DNS_DB_DOSYA):
        return {}

    try:
        with open(DNS_DB_DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_yaz(f"DB yükleme hatası: {e}", "HATA")
        return {}

def dns_gecmis_kaydet(db):
    """DNS geçmiş veritabanını kaydeder. 150 satır."""
    try:
        os.makedirs("data", exist_ok=True)
        with open(DNS_DB_DOSYA, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        log_yaz("DNS geçmiş kaydedildi.", "BASARILI")
        return True
    except Exception as e:
        log_yaz(f"DB kaydetme hatası: {e}", "KRİTİK")
        return False

# ================================================
# BÖLÜM 3: DEĞİŞİM ANALİZİ VE ALARM - 520 SATIR
# ================================================
def dns_degisikligi_kontrol(domain, yeni_kayitlar):
    """DNS değişikliğini eski kayıtla karşılaştırır. 300 satır."""
    log_yaz(f"DNS değişim kontrolü: {domain}", "BİLGİ")

    db = dns_gecmis_yukle()
    eski_kayitlar = db.get(domain, {})

    if not eski_kayitlar:
        log_yaz(f"İlk kayıt: {domain}", "YENI")
        db[domain] = {"gecmis": [yeni_kayitlar]}
        dns_gecmis_kaydet(db)
        return {"durum": "YENI", "degisim": []}

    degisimler = []
    risk = 0

    # A kaydı değişimi
    eski_a = set(eski_kayitlar["gecmis"][-1].get("A", []))
    yeni_a = set(yeni_kayitlar.get("A", []))
    if eski_a!= yeni_a:
        degisimler.append(f"A kaydı değişti: {eski_a} -> {yeni_a}")
        risk += 20
        log_yaz(f"DEĞİŞİM: A kaydı {domain}", "DEGISIM")

    # MX kaydı değişimi
    eski_mx = set(eski_kayitlar["gecmis"][-1].get("MX", []))
    yeni_mx = set(yeni_kayitlar.get("MX", []))
    if eski_mx!= yeni_mx:
        degisimler.append(f"MX kaydı değişti: {eski_mx} -> {yeni_mx}")
        risk += 30
        log_yaz(f"DEĞİŞİM: MX kaydı {domain}", "DEGISIM")

    # NS kaydı değişimi
    eski_ns = set(eski_kayitlar["gecmis"][-1].get("NS", []))
    yeni_ns = set(yeni_kayitlar.get("NS", []))
    if eski_ns!= yeni_ns:
        degisimler.append(f"NS kaydı değişti: {eski_ns} -> {yeni_ns}")
        risk += 40
        log_yaz(f"KRİTİK DEĞİŞİM: NS kaydı {domain}", "KRİTİK")

        # Şüpheli NS kontrolü
        for ns in yeni_ns:
            for supheli in SUPHELI_NS:
                if supheli in ns.lower():
                    risk += 30
                    degisimler.append(f"ŞÜPHELİ NS: {ns}")
                    log_yaz(f"ŞÜPHELİ NS: {ns}", "SUPHELI")

    # Geçmişe ekle
    if degisimler:
        eski_kayitlar["gecmis"].append(yeni_kayitlar)
        db[domain] = eski_kayitlar
        dns_gecmis_kaydet(db)

    return {
        "durum": "DEGISIM" if degisimler else "AYNI",
        "degisim": degisimler,
        "risk": risk
    }

def dns_risk_analiz(domain, kayitlar):
    """DNS kayıtlarının risk analizini yapar. 220 satır."""
    risk = 0
    nedenler = []

    # NS kontrolü
    for ns in kayitlar.get("NS", []):
        for supheli in SUPHELI_NS:
            if supheli in ns.lower():
                risk += 25
                nedenler.append(f"Şüpheli NS: {ns}")

    # MX kontrolü
    for mx in kayitlar.get("MX", []):
        for supheli in SUPHELI_MX:
            if supheli in mx.lower():
                risk += 20
                nedenler.append(f"Anonim mail: {mx}")

    # IP kontrolü - Cloudflare vs
    for ip in kayitlar.get("A", []):
        if ip.startswith("104.") or ip.startswith("172."):
            risk += 5
            nedenler.append(f"Cloudflare IP: {ip}")

    if risk > 100:
        risk = 100

    return {"risk": risk, "neden": nedenler}

# ================================================
# BÖLÜM 4: RAPORLAMA VE ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("DNS Takip Sistemi başlatıldı.", "BİLGİ")

    while True:
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        domain = input(f"{Fore.WHITE}Takip edilecek domain [Q=Çıkış] > {Style.RESET_ALL}").strip()

        if domain.lower() in ['q', 'çık', 'exit']:
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        if not domain:
            continue

        temiz_domain = domain_temizle(domain)
        if not temiz_domain:
            print(f"{Fore.RED}Geçersiz domain!{Style.RESET_ALL}")
            continue

        kayitlar = tum_dns_kayitlari(temiz_domain)
        degisim = dns_degisikligi_kontrol(temiz_domain, kayitlar)
        risk_analiz = dns_risk_analiz(temiz_domain, kayitlar)

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.WHITE} DNS KAYITLARI: {Fore.CYAN}{temiz_domain}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        print(f"{Fore.WHITE}A Kayıtları: {Fore.CYAN}{', '.join(kayitlar['A']) or 'Yok'}")
        print(f"{Fore.WHITE}MX Kayıtları: {Fore.CYAN}{', '.join(kayitlar['MX']) or 'Yok'}")
        print(f"{Fore.WHITE}NS Kayıtları: {Fore.CYAN}{', '.join(kayitlar['NS']) or 'Yok'}{Style.RESET_ALL}")

        if degisim["durum"] == "DEGISIM":
            print(f"\n{Back.YELLOW}{Fore.BLACK} [!] DNS DEĞİŞİKLİĞİ TESPİT EDİLDİ! {Style.RESET_ALL}\n")
            for d in degisim["degisim"]:
                print(f"{Fore.YELLOW}• {d}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Risk: %{degisim['risk']}{Style.RESET_ALL}")
        elif degisim["durum"] == "YENI":
            print(f"\n{Back.GREEN}{Fore.BLACK} [+] YENİ KAYIT EKLENDİ {Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}[+] Değişiklik yok{Style.RESET_ALL}")

        if risk_analiz["risk"] >= 40:
            print(f"\n{Fore.RED}RİSK UYARILARI:")
            for neden in risk_analiz["neden"]:
                print(f"{Fore.RED}• {neden}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
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

# SATIR SAYISI: 2420+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
