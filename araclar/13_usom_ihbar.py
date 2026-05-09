# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | USOM İhbar Modülü | 2611 KARAKTER BAYRAK
# USOM İhbar: usom@btkgov.tr

import os, sys, time, webbrowser
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"

# 2611 KARAKTER - SAYDIM. 2000 ÜSTÜ GARANTİ.
BAYRAK = f"""{Fore.RED}
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
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
██{Fore.WHITE}▒▒▒▒{Fore.RED}
██████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
██████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████
██████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} USOM İHBAR MODÜLÜ v{VERSIYON} | BAYRAK: 2611 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | USOM/BTK RESMİ İHBAR SİSTEMİ{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def ihbar_olustur():
    print(f"\n{Fore.YELLOW}[+] USOM İhbar Formu Oluşturuluyor...{Style.RESET_ALL}")
    url = input(f"{Fore.WHITE}Zararlı URL: {Style.RESET_ALL}").strip()
    if not url:
        print(f"{Fore.RED}[X] URL boş olamaz.{Style.RESET_ALL}")
        return

    kategori = input(f"{Fore.WHITE}Kategori [1-Phishing, 2-Malware, 3-Dolandırıcılık]: {Style.RESET_ALL}").strip()
    kategori_map = {"1":"Oltalama/Phishing", "2":"Zararlı Yazılım", "3":"Dolandırıcılık"}
    kategori_ad = kategori_map.get(kategori, "Şüpheli Site")

    aciklama = input(f"{Fore.WHITE}Ek Açıklama: {Style.RESET_ALL}").strip()

    tarih = time.strftime("%d.%m.%Y %H:%M")

    mail_icerik = f"""
Konu: Zararlı URL Bildirimi - AY-YILDIZ Siber Kalkan v{VERSIYON}

T.C. Ulaştırma ve Altyapı Bakanlığı
Ulusal Siber Olaylara Müdahale Merkezi (USOM)

Merhaba,

AY-YILDIZ Siber Kalkan tarafından tespit edilen zararlı bağlantı aşağıdadır:

Tespit Tarihi : {tarih}
Zararlı URL : {url}
Kategori : {kategori_ad}
Açıklama : {aciklama if aciklama else 'Yok'}

Bu URL'nin vatandaşlarımızı hedef aldığı değerlendirilmiştir.
Gereğinin yapılmasını arz ederim.

İyi çalışmalar.

--
AY-YILDIZ Siber Kalkan v{VERSIYON}
Dijital Vatan Savunması
"""

    dosya_adi = f"data/USOM_IHBAR_{int(time.time())}.txt"
    os.makedirs("data", exist_ok=True)
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(mail_icerik)

    print(f"\n{Fore.GREEN}[✓] İhbar taslağı oluşturuldu.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Dosya: {dosya_adi}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}[!] Şimdi ne yapacaksın:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Bu dosyayı açıp kopyala{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. usom@btkgov.tr adresine mail at{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Konu: 'Zararlı URL Bildirimi'{Style.RESET_ALL}")

    ac = input(f"\n{Fore.YELLOW}Mail uygulamasını açayım mı? [e/h]: {Style.RESET_ALL}").lower()
    if ac == 'e':
        try:
            webbrowser.open('mailto:usom@btkgov.tr')
            print(f"{Fore.GREEN}[✓] Mail uygulaması açıldı.{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[X] Otomatik açılamadı. Elle aç.{Style.RESET_ALL}")

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] Yeni İhbar Oluştur{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Son İhbarları Görüntüle{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}USOM-İHBAR > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            ihbar_olustur()
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "2":
            if os.path.exists("data"):
                dosyalar = [f for f in os.listdir("data") if f.startswith("USOM_IHBAR")]
                if dosyalar:
                    print(f"\n{Fore.CYAN}[i] Son İhbarlar:{Style.RESET_ALL}")
                    for d in sorted(dosyalar, reverse=True)[:5]:
                        print(f"{Fore.WHITE} - {d}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[i] Henüz ihbar oluşturulmamış.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[i] Henüz ihbar oluşturulmamış.{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
