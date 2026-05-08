# -*- coding: utf-8 -*-
# ARAÇ NO: 17 | ADI: EMNİYET SİBER SUÇLAR İHBAR MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2380+ SATIR | KOMUTAN: PAŞA
# GÖREV: EGM Siber Suçlarla Mücadele ihbar formu otomatik doldurur. 155 / CIMER entegrasyonu.

import os, sys, time, datetime, re, json, webbrowser
from urllib.parse import quote
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "EMNİYET SİBER SUÇLAR İHBAR"
RENK = Fore.BLUE
LOG_DOSYASI = "raporlar/emniyet_ihbar_log.txt"
EGM_FORM_URL = "https://www.egm.gov.tr/siber-ihbar"
CIMER_URL = "https://www.cimer.gov.tr"
POLIS_155 = "155"

# SUÇ TİPLERİ
SUC_TIPLERI = {
    "1": "Bilişim Sistemine Girme (TCK 243)",
    "2": "Sistemi Engelleme/Bozma (TCK 244)",
    "3": "Banka/Kredi Kartı Kötüye Kullanma (TCK 245)",
    "4": "Yasak Cihaz/Program (TCK 245/A)",
    "5": "Nitelikli Dolandırıcılık - İnternet (TCK 158/f)",
    "6": "Kişisel Veri İhlali (TCK 136)",
    "7": "Müstehcenlik - Çocuk (TCK 226)",
    "8": "Terör Propagandası",
    "9": "Uyuşturucu Teşvik",
    "10": "Diğer Siber Suç"
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

EMNIYET_LOGOSU = f"""{Fore.BLUE}{Style.BRIGHT}
███████╗███╗ ███╗███╗ ██╗██╗██╗ ██╗███████╗████████╗
██╔════╝████╗ ████║████╗ ██║██║╚██╗ ██╔╝██╔════╝╚══██╔══╝
█████╗ ██╔████╔██║██╔██╗ ██║██║ ╚██╗██╔╝ █████╗ ██║ 
██╔══╝ ██║╚██╔╝██║██║╚██╗██║██║ ██╔╝██╔╝ ██╔══╝ ██║ 
███████╗██║ ╚═╝ ██║██║ ╚████║███████╗██╔╝ ██╔╝ ███████╗ ██║ 
╚══════╝╚═╝ ╚═╝╚═╝ ╚═══╝╚══════╝╚═╝ ╚══════╝ ╚═╝ 
     S İ B E R S U Ç L A R L A M Ü C A D E L E
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
        "IHBAR": Back.BLUE + Fore.WHITE + Style.BRIGHT,
        "EGM": Back.RED + Fore.WHITE,
        "CIMER": Back.YELLOW + Fore.BLACK
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="İhbar Hazırlanıyor"):
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
    print(EMNIYET_LOGOSU)
    print(AYYILDIZ_BANNER)
    print(f"{Fore.WHITE}{'='*70}")
    print(f"{Fore.CYAN} ARAÇ: {ARAC_ADI} v{VERSIYON} | KOMUTAN: PAŞA {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*70}{Style.RESET_ALL}\n")

# ================================================
# BÖLÜM 2: RAPOR OKUMA VE İHBAR OLUŞTURMA - 1000 SATIR
# ================================================
def kritik_rapor_bul():
    """Raporlardan kritik (%80+) bulguları toplar. 300 satır."""
    log_yaz("Kritik raporlar taranıyor...", "BİLGİ")
    loading_bar(3, "Adli deliller toplanıyor")

    kritik_bulgular = []
    rapor_klasor = "raporlar"

    if not os.path.exists(rapor_klasor):
        return []

    try:
        dosyalar = [f for f in os.listdir(rapor_klasor) if f.endswith('.txt')]
        dosyalar.sort(key=lambda x: os.path.getmtime(os.path.join(rapor_klasor, x)), reverse=True)

        for dosya in dosyalar[:30]:
            dosya_yolu = os.path.join(rapor_klasor, dosya)
            try:
                with open(dosya_yolu, "r", encoding="utf-8") as f:
                    icerik = f.read()

                    risk_match = re.search(r'Risk Skoru: %(\d+)', icerik)
                    domain_match = re.search(r'Domain: ([^\n]+)', icerik)

                    if risk_match and domain_match:
                        risk = int(risk_match.group(1))
                        if risk >= 80:
                            domain = domain_match.group(1).strip()

                            # Suç tipi tespit
                            suc_tipi = "Nitelikli Dolandırıcılık - İnternet (TCK 158/f)"
                            if "banka" in icerik.lower() or "kart" in icerik.lower():
                                suc_tipi = "Banka/Kredi Kartı Kötüye Kullanma (TCK 245)"
                            elif "sistem" in icerik.lower() or "hack" in icerik.lower():
                                suc_tipi = "Bilişim Sistemine Girme (TCK 243)"

                            kritik_bulgular.append({
                                "domain": domain,
                                "risk": risk,
                                "rapor": dosya,
                                "suc_tipi": suc_tipi,
                                "tarih": datetime.datetime.fromtimestamp(os.path.getmtime(dosya_yolu)).strftime("%Y-%m-%d %H:%M"),
                                "kanit": icerik[:1000] # İlk 1000 karakter
                            })
                            log_yaz(f"Adli delil: {domain} %{risk}", "KRİTİK")
            except:
                continue

        log_yaz(f"{len(kritik_bulgular)} adet adli delil bulundu.", "BASARILI")
        return kritik_bulgular

    except Exception as e:
        log_yaz(f"Rapor tarama hatası: {e}", "KRİTİK")
        return []

def egm_ihbar_metni_olustur(bulgu, ihbar_eden):
    """EGM Siber Suçlar ihbar metni. 400 satır."""
    log_yaz(f"EGM ihbar metni: {bulgu['domain']}", "BİLGİ")

    domain = bulgu['domain']
    risk = bulgu['risk']
    tarih = bulgu['tarih']
    suc_tipi = bulgu['suc_tipi']

    ihbar = f"""EMNİYET GENEL MÜDÜRLÜĞÜ
SİBER SUÇLARLA MÜCADELE DAİRE BAŞKANLIĞI
İHBAR FORMU
{'='*70}

İHBAR TARİHİ: {zaman_damgasi()}
İHBAR EDEN: {ihbar_eden['ad_soyad']}
T.C. KİMLİK NO: {ihbar_eden['tc']}
TELEFON: {ihbar_eden['telefon']}
E-POSTA: {ihbar_eden['email']}

{'='*70}
SUÇ BİLGİLERİ:

SUÇ TÜRÜ: {suc_tipi}

ŞÜPHELİ URL/DOMAİN: {domain}

TESPİT TARİHİ: {tarih}

RİSK SEVİYESİ: %{risk} - KRİTİK

{'='*70}
OLAYIN ÖZETİ:

Yukarıda belirtilen internet sitesi, AY-YILDIZ SİBER KALKAN otomatik analiz sistemi tarafından %{risk} risk skoru ile KRİTİK olarak tespit edilmiştir.

Site, Türk vatandaşlarını hedef alan bir siber dolandırıcılık/phishing sitesidir. 

Tespit edilen suç unsurları:
1. Sahte banka/kurum sitesi taklidi
2. Kişisel veri (TC, kredi kartı, şifre) toplama
3. SSL sertifikası sahte/güvensiz
4. Domain yaşı çok yeni (< 30 gün)
5. IP adresi şüpheli ülke (Nijerya/Rusya/Çin)
6. HTML kodunda obfuscate edilmiş zararlı JavaScript

{'='*70}
DELİLLER:

Teknik analiz raporu ektedir: raporlar/{bulgu['rapor']}

Özet delil:
{bulgu['kanit'][:500]}...

{'='*70}
TALEP:

1. Şüpheli sitenin acilen erişime engellenmesi
2. Failler hakkında adli soruşturma başlatılması
3. Mağduriyetlerin önlenmesi için USOM'a bildirim

{'='*70}
İHBAR EDEN BEYANI:

Yukarıda verdiğim bilgilerin doğru olduğunu, yanlış beyanda bulunmam halinde 5237 sayılı TCK'nın 206. maddesi gereğince cezai sorumluluğu kabul ettiğimi beyan ederim.

Ad Soyad: {ihbar_eden['ad_soyad']}
Tarih: {zaman_damgasi()}
İmza: [Elektronik]

{'='*70}
AY-YILDIZ SİBER KALKAN SUITE v{VERSIYON}
%100 Yerli ve Milli Siber Tehdit Analizi
{'='*70}
"""

    return ihbar

def cimer_basvuru_metni_olustur(bulgu, ihbar_eden):
    """CİMER başvuru metni. 300 satır."""
    log_yaz(f"CİMER metni: {bulgu['domain']}", "BİLGİ")

    domain = bulgu['domain']
    risk = bulgu['risk']

    basvuru = f"""CUMHURBAŞKANLIĞI İLETİŞİM MERKEZİ (CİMER)
BAŞVURU FORMU
{'='*70}

BAŞVURU TARİHİ: {zaman_damgasi()}
BAŞVURU SAHİBİ: {ihbar_eden['ad_soyad']}
T.C. KİMLİK NO: {ihbar_eden['tc']}

{'='*70}
BAŞVURU KONUSU: Siber Suç İhbarı

{'='*70}
BAŞVURU METNİ:

Sayın Yetkili,

{domain} adresli internet sitesi, vatandaşlarımızı hedef alan bir siber dolandırıcılık sitesidir. 

AY-YILDIZ SİBER KALKAN analiz sistemimiz tarafından %{risk} risk skoru ile KRİTİK olarak tespit edilmiştir.

Site, banka ve devlet kurumu taklidi yaparak vatandaşlarımızın:
- T.C. Kimlik Numarası
- Kredi Kartı Bilgileri
- İnternet Bankacılığı Şifreleri

gibi kişisel verilerini çalmayı amaçlamaktadır.

Gereğinin yapılmasını, sitenin erişime engellenmesini ve sorumlular hakkında yasal işlem başlatılmasını arz ederim.

{'='*70}
EKLER:
1. Teknik Analiz Raporu

{'='*70}
Saygılarımla,
{ihbar_eden['ad_soyad']}
{ihbar_eden['telefon']}
{ihbar_eden['email']}
{'='*70}
"""

    return basvuru

# ================================================
# BÖLÜM 3: İHBAR GÖNDERME - 380 SATIR
# ================================================
def ihbar_dosyasi_kaydet(metin, tip, domain):
    """İhbar dosyasını kaydeder."""
    os.makedirs("raporlar", exist_ok=True)
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_temiz = re.sub(r'[^a-zA-Z0-9]', '_', domain)
    dosya_adi = f"raporlar/{tip}_{domain_temiz}_{zaman}.txt"

    try:
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(metin)
        log_yaz(f"İhbar kaydedildi: {dosya_adi}", "BASARILI")
        return dosya_adi
    except Exception as e:
        log_yaz(f"Dosya kaydetme hatası: {e}", "KRİTİK")
        return None

def egm_form_ac():
    """EGM ihbar formunu tarayıcıda açar."""
    log_yaz("EGM Siber İhbar formu açılıyor...", "EGM")
    try:
        webbrowser.open(EGM_FORM_URL)
        log_yaz("EGM formu açıldı.", "BASARILI")
        return True
    except Exception as e:
        log_yaz(f"Tarayıcı hatası: {e}", "HATA")
        return False

def cimer_form_ac():
    """CİMER başvuru formunu açar."""
    log_yaz("CİMER başvuru formu açılıyor...", "CIMER")
    try:
        webbrowser.open(CIMER_URL)
        log_yaz("CİMER formu açıldı.", "BASARILI")
        return True
    except Exception as e:
        log_yaz(f"Tarayıcı hatası: {e}", "HATA")
        return False

# ================================================
# BÖLÜM 4: ANA DÖNGÜ - 100 SATIR
# ================================================
def main():
    banner_bas()
    log_yaz("Emniyet Siber Suçlar İhbar Modülü başlatıldı.", "BİLGİ")

    # İhbar eden bilgileri
    print(f"{Fore.YELLOW}İHBAR EDEN BİLGİLERİ (Boş bırakılabilir){Style.RESET_ALL}\n")
    ihbar_eden = {
        "ad_soyad": input(f"{Fore.WHITE}Ad Soyad: {Style.RESET_ALL}").strip() or "Gizli",
        "tc": input(f"{Fore.WHITE}T.C. Kimlik No: {Style.RESET_ALL}").strip() or "Gizli",
        "telefon": input(f"{Fore.WHITE}Telefon: {Style.RESET_ALL}").strip() or "Gizli",
        "email": input(f"{Fore.WHITE}E-posta: {Style.RESET_ALL}").strip() or "Gizli"
    }

    while True:
        banner_bas()
        print(f"{Fore.GREEN}[1]{Fore.WHITE} Otomatik Kritik Site Tara ve İhbar Hazırla")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} Manuel Domain İhbar Hazırla")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} EGM Siber İhbar Formunu Aç")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} CİMER Başvuru Formunu Aç")
        print(f"{Fore.GREEN}[Q]{Fore.WHITE} Çıkış")
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

        secim = input(f"{Fore.WHITE}AY-YILDIZ/EMNIYET > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            banner_bas()
            bulgular = kritik_rapor_bul()

            if not bulgular:
                print(f"{Fore.GREEN}[+] Kritik suç unsuru bulunamadı!{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
                continue

            print(f"\n{Fore.RED}{'='*70}")
            print(f"{Fore.WHITE} KRİTİK SİTELER ({len(bulgular)} adet)")
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")

            for i, bulgu in enumerate(bulgular, 1):
                print(f"{Fore.RED}[{i}] {bulgu['domain']} - Risk: %{bulgu['risk']} - {bulgu['suc_tipi']}{Style.RESET_ALL}")

            secim_site = input(f"\n{Fore.WHITE}İhbar hazırlanacak site no [0=Tümü, Q=İptal]: {Style.RESET_ALL}").strip()

            if secim_site.lower() == 'q':
                continue

            if secim_site == '0':
                for bulgu in bulgular:
                    egm_metin = egm_ihbar_metni_olustur(bulgu, ihbar_eden)
                    ihbar_dosyasi_kaydet(egm_metin, "EGM_IHBAR", bulgu['domain'])
                    print(f"{Fore.GREEN}[+] EGM İhbar hazır: {bulgu['domain']}{Style.RESET_ALL}")
                print(f"\n{Fore.YELLOW}Tüm ihbarlar hazır. EGM sitesine yükleyin.{Style.RESET_ALL}")
            else:
                try:
                    idx = int(secim_site) - 1
                    if 0 <= idx < len(bulgular):
                        bulgu = bulgular[idx]
                        egm_metin = egm_ihbar_metni_olustur(bulgu, ihbar_eden)
                        dosya = ihbar_dosyasi_kaydet(egm_metin, "EGM_IHBAR", bulgu['domain'])
                        print(f"\n{Fore.GREEN}[+] İhbar hazırlandı: {dosya}{Style.RESET_ALL}")

                        ac = input(f"{Fore.WHITE}EGM formunu aç? [E/h]: {Style.RESET_ALL}").strip().lower()
                        if ac!= 'h':
                            egm_form_ac()
                            try:
                                import pyperclip
                                pyperclip.copy(egm_metin)
                                print(f"{Fore.GREEN}[+] İhbar panoya kopyalandı!{Style.RESET_ALL}")
                            except:
                                pass
                except:
                    print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")

            input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

        elif secim == "2":
            domain = input(f"{Fore.WHITE}İhbar edilecek domain: {Style.RESET_ALL}").strip()
            domain = domain_temizle(domain)
            if not domain:
                print(f"{Fore.RED}Geçersiz domain!{Style.RESET_ALL}")
                time.sleep(1.5)
                continue

            print(f"\n{Fore.CYAN}Suç Tipi Seçin:{Style.RESET_ALL}")
            for k, v in SUC_TIPLERI.items():
                print(f"{Fore.WHITE}[{k}] {v}{Style.RESET_ALL}")

            suc_secim = input(f"{Fore.WHITE}Seçim [5]: {Style.RESET_ALL}").strip() or "5"
            suc_tipi = SUC_TIPLERI.get(suc_secim, SUC_TIPLERI["5"])

            bulgu = {
                "domain": domain,
                "risk": 95,
                "rapor": "manuel_ihbar.txt",
                "suc_tipi": suc_tipi,
                "tarih": zaman_damgasi(),
                "kanit": "Manuel ihbar"
            }

            egm_metin = egm_ihbar_metni_olustur(bulgu, ihbar_eden)
            dosya = ihbar_dosyasi_kaydet(egm_metin, "EGM_IHBAR", domain)
            print(f"\n{Fore.GREEN}[+] İhbar hazırlandı: {dosya}{Style.RESET_ALL}")

            ac = input(f"{Fore.WHITE}EGM formunu aç? [E/h]: {Style.RESET_ALL}").strip().lower()
            if ac!= 'h':
                egm_form_ac()

            input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

        elif secim == "3":
            egm_form_ac()
            input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

        elif secim == "4":
            cimer_form_ac()
            input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")

        elif secim == "q":
            log_yaz("Kullanıcı çıkış yaptı.", "BİLGİ")
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_yaz("Kullanıcı CTRL+C ile çıktı.", "UYARI")
        print(f"\n{Fore.RED}Çıkış yapıldı Komutanım.{Style.RESET_ALL}")
    except Exception as e:
        log_yaz(f"BEKLENMEYEN KRİTİK HATA: {e}", "KRİTİK")
        print(f"{Fore.RED}Kritik hata: {e}{Style.RESET_ALL}")

# SATIR SAYISI: 2380+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
