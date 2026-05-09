#!/usr/bin/env python3
import os, requests, time
from colorama import Fore, Style, Back

def banner():
    os.system("clear")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE} AY-YILDIZ SİBER KALKAN - SAVUNMA MERKEZİ {Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Bu araçlar sadece yasal savunma ve analiz içindir.{Style.RESET_ALL}\n")

def usom_sorgu():
    domain = input(f"{Fore.CYAN}[?] Şüpheli domain/IP: {Style.RESET_ALL}").strip()
    print(f"{Fore.YELLOW}[i] USOM zararlı listesi kontrol ediliyor...{Style.RESET_ALL}")
    try:
        r = requests.get("https://www.usom.gov.tr/url-list.txt", timeout=10)
        if domain in r.text:
            print(f"{Fore.RED}[X] TEHLİKELİ: {domain} USOM listesinde!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[✓] Temiz: {domain} USOM listesinde yok.{Style.RESET_ALL}")
    except: print(f"{Fore.RED}[X] USOM erişim hatası.{Style.RESET_ALL}")
    input("\nDevam için Enter...")

def phish_analiz():
    print(f"{Fore.YELLOW}[i] Phishing Mail Header Analizi{Style.RESET_ALL}")
    header = input("Mail header'ını yapıştırıp Enter'a bas:\n")
    if "Return-Path:" in header and "Received:" in header:
        print(f"{Fore.GREEN}[✓] Header alındı. Sahte gönderen kontrolü için 'whois' kullan.{Style.RESET_ALL}")
    else: print(f"{Fore.RED}[X] Geçersiz header.{Style.RESET_ALL}")
    input("\nDevam için Enter...")

def port_tarama():
    hedef = input(f"{Fore.CYAN}[?] KENDİ IP/Domain'in: {Style.RESET_ALL}").strip()
    print(f"{Fore.RED}[!] Sadece kendi sistemini tarayabilirsin. Yasal sorumluluk sende.{Style.RESET_ALL}")
    onay = input("Kendi sistemin mi? e/h: ")
    if onay.lower() == 'e':
        os.system(f"nmap -F {hedef}") # Hızlı tarama
    input("\nDevam için Enter...")

def ip_reputation():
    ip = input(f"{Fore.CYAN}[?] Kontrol edilecek IP: {Style.RESET_ALL}").strip()
    print(f"{Fore.YELLOW}[i] AbuseIPDB kontrolü: https://www.abuseipdb.com/check/{ip}{Style.RESET_ALL}")
    input("\nDevam için Enter...")

while True:
    banner()
    print(f"{Fore.WHITE}[1] USOM Zararlı Domain Sorgu{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[2] Phishing Mail Header Analiz{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[3] Kendi Sistemin Port Tarama{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[4] IP Reputation Kontrol{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[0] Ana Menüye Dön{Style.RESET_ALL}")

    sec = input(f"\n{Fore.RED}SAVUNMA > {Style.RESET_ALL}").strip()
    if sec == "1": usom_sorgu()
    elif sec == "2": phish_analiz()
    elif sec == "3": port_tarama()
    elif sec == "4": ip_reputation()
    elif sec == "0": break
    else: print(f"{Fore.RED}Geçersiz seçim{Style.RESET_ALL}"); time.sleep(1)
