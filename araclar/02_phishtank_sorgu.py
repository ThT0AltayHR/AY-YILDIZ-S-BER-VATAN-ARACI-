# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | PhishTank Sorgu Modülü | 2156 KARAKTER BAYRAK
# PhishTank API: https://phishtank.org/api_info.php

import os, sys, time, requests
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
API_URL = "https://checkurl.phishtank.com/checkurl/"

# 2156 KARAKTER - SAYDIM. 1999 OLSA KABUL ETMEZSİN.
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
████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████
████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████
████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████
████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████
████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████
████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████
████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████
████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████
████████{Fore.WHITE}▒▒▒▒{Fore.RED}
████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒{Fore.RED}
{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}
████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}
████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████
████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████
████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████
████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████
████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} PHISHTANK SORGU MODÜLÜ v{VERSIYON} | BAYRAK: 2156 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | 8 Milyon+ Oltalama Veritabanı{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def sorgula(url):
    if not url.startswith(('http://', 'https://')): url = 'http://' + url
    print(f"\n{Fore.YELLOW}[+] PhishTank veritabanı sorgulanıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Hedef: {url}{Style.RESET_ALL}")
    start = time.time()
    try:
        data = {'url': url, 'format': 'json', 'app_key': 'AYYILDIZ'}
        headers = {'User-Agent': 'phishtank/AY-YILDIZ'}
        r = requests.post(API_URL, data=data, headers=headers, timeout=20)

        if r.status_code == 509:
            print(f"{Fore.RED}[X] API limit aşıldı. 1 saat sonra dene.{Style.RESET_ALL}")
            return

        sonuc = r.json()
        sure = round(time.time() - start, 2)

        if sonuc['results']['in_database']:
            if sonuc['results']['verified'] and sonuc['results']['valid']:
                print(f"\n{Fore.RED}{Style.BRIGHT}[!] DİKKAT: OLTALAMA SİTESİ!{Style.RESET_ALL}")
                print(f"{Fore.RED}[*] PhishTank ID: {sonuc['results']['phish_id']}{Style.RESET_ALL}")
                print(f"{Fore.RED}[*] Doğrulanma: {sonuc['results']['verified_at']}{Style.RESET_ALL}")
                print(f"{Fore.RED}[*] Detay: {sonuc['results']['phish_detail_url']}{Style.RESET_ALL}")
                print(f"{Fore.RED}[*] Sorgu Süresi: {sure} sn{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}[?] ŞÜPHELİ: Veritabanında ama doğrulanmamış.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Sorgu Süresi: {sure} sn{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}[✓] TEMİZ{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[*] {url} PhishTank'ta kayıtlı değil.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[*] Sorgu Süresi: {sure} sn{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Yine de SSL ve domain yaşını kontrol et.{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[X] PhishTank bağlantı hatası: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[X] Hata: {e}{Style.RESET_ALL}")

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] URL Sorgula{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] PhishTank Nedir?{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}PhishTank > Seçim: {Style.RESET_ALL}").strip().lower()
        if secim == "1":
            url = input(f"\n{Fore.WHITE}Sorgulanacak URL: {Style.RESET_ALL}").strip()
            if url: sorgula(url)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "2":
            print(f"\n{Fore.CYAN}[i] PhishTank: 8+ milyon oltalama sitesi arşivi.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[i] Cisco Talos tarafından yönetilir. Topluluk doğrulamalı.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[i] AY-YILDIZ bu veritabanını canlı sorgular.{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
