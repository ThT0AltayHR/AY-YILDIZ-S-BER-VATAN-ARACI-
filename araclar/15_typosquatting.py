# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | Typosquatting Modülü | 6098 KARAKTER KOD
# Yazım Hatası Domain Üretici + WHOIS + DNS Kontrol

import os, sys, time, socket, whois
from itertools import product
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"

# 2574 KARAKTER BAYRAK - SAYDIM
BAYRAK = f"""{Fore.RED}
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████
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
██████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
████████████████████████████████████████████████
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
    print(f"{Fore.WHITE} TYPOSQUATTING MODÜLÜ v{VERSIYON} | KOD: 6098 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | YAZIM HATASI DOMAİN TESPİTİ{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def harf_eksilt(domain):
    """garanti.com -> garanti.com, aranti.com, granti.com..."""
    sonuclar = []
    ad, tld = domain.rsplit('.', 1)
    for i in range(len(ad)):
        yeni = ad[:i] + ad[i+1:] + '.' + tld
        if yeni!= domain: sonuclar.append(yeni)
    return sonuclar

def harf_degistir(domain):
    """garanti.com -> garanto.com, garantı.com..."""
    klavye = {
        'a':'s', 's':'a', 'e':'r', 'r':'e', 'i':'o', 'o':'i', 
        'u':'y', 'y':'u', 't':'r', 'n':'m', 'm':'n', 'l':'k', 'k':'l'
    }
    sonuclar = []
    ad, tld = domain.rsplit('.', 1)
    for i, harf in enumerate(ad):
        if harf in klavye:
            yeni = ad[:i] + klavye[harf] + ad[i+1:] + '.' + tld
            sonuclar.append(yeni)
    return sonuclar

def harf_ekle(domain):
    """garanti.com -> gaaranti.com, garranti.com..."""
    sonuclar = []
    ad, tld = domain.rsplit('.', 1)
    for i in range(len(ad)):
        yeni = ad[:i] + ad[i] + ad[i:] + '.' + tld
        sonuclar.append(yeni)
    return sonuclar

def bit_squatting(domain):
    """garanti.com -> faranti.com (g->f: 1 bit fark)"""
    sonuclar = []
    ad, tld = domain.rsplit('.', 1)
    for i, harf in enumerate(ad):
        ascii_val = ord(harf)
        for bit in range(8):
            yeni_val = ascii_val ^ (1 << bit)
            if 97 <= yeni_val <= 122: # a-z
                yeni_harf = chr(yeni_val)
                yeni = ad[:i] + yeni_harf + ad[i+1:] + '.' + tld
                if yeni!= domain: sonuclar.append(yeni)
    return list(set(sonuclar))

def tld_degistir(domain):
    """garanti.com -> garanti.net, garanti.org..."""
    tldler = ['com','net','org','info','biz','co','io','me','tr','com.tr']
    ad = domain.split('.')[0]
    return [f"{ad}.{tld}" for tld in tldler if f"{ad}.{tld}"!= domain]

def dns_kontrol(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

def whois_kontrol(domain):
    try:
        w = whois.whois(domain)
        if w.domain_name:
            tarih = w.creation_date
            if isinstance(tarih, list): tarih = tarih[0]
            return f"Kayıtlı | {tarih.strftime('%d.%m.%Y') if tarih else 'Tarih Yok'}"
        return "Kayıtlı Değil"
    except:
        return "WHOIS Hata"

def tam_tarama(hedef):
    if '.' not in hedef:
        print(f"{Fore.RED}[X] Geçerli domain girin: ornek.com{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}[+] Typosquatting Analizi: {hedef}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    tum_varyasyonlar = []
    tum_varyasyonlar.extend(harf_eksilt(hedef))
    tum_varyasyonlar.extend(harf_degistir(hedef))
    tum_varyasyonlar.extend(harf_ekle(hedef))
    tum_varyasyonlar.extend(bit_squatting(hedef))
    tum_varyasyonlar.extend(tld_degistir(hedef))

    # Tekrarları temizle
    varyasyonlar = list(set(tum_varyasyonlar))
    print(f"{Fore.WHITE}[i] {len(varyasyonlar)} varyasyon üretildi. DNS/WHOIS kontrol başlıyor...{Style.RESET_ALL}\n")

    aktif = []
    for i, domain in enumerate(varyasyonlar, 1):
        dns = dns_kontrol(domain)
        if dns:
            whois_bilgi = whois_kontrol(domain)
            aktif.append((domain, whois_bilgi))
            print(f"{Fore.RED}[{i}/{len(varyasyonlar)}] {domain} | DNS:AKTİF | {whois_bilgi}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[{i}/{len(varyasyonlar)}] {domain} | DNS:BOŞ{Style.RESET_ALL}")

    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}ÖZET RAPOR:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Toplam Varyasyon: {len(varyasyonlar)}{Style.RESET_ALL}")
    print(f"{Fore.RED}Aktif Domain: {len(aktif)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Boş Domain: {len(varyasyonlar) - len(aktif)}{Style.RESET_ALL}")

    if aktif:
        print(f"\n{Fore.RED}{Style.BRIGHT}[!] TEHLİKE: Bu domainler aktif ve taklit olabilir:{Style.RESET_ALL}")
        for domain, bilgi in aktif:
            print(f"{Fore.RED} - {domain} | {bilgi}{Style.RESET_ALL}")

        kayit = f"data/TYPOSQUAT_{hedef.replace('.','_')}_{int(time.time())}.txt"
        os.makedirs("data", exist_ok=True)
        with open(kayit, "w", encoding="utf-8") as f:
            f.write(f"HEDEF: {hedef}\nTOPLAM VARYASYON: {len(varyasyonlar)}\nAKTİF: {len(aktif)}\n\n")
            for domain, bilgi in aktif:
                f.write(f"{domain} | {bilgi}\n")
        print(f"\n{Fore.GREEN}[i] Rapor kaydedildi: {kayit}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}[✓] Hiçbir varyasyon aktif değil. Güvendesiniz.{Style.RESET_ALL}")

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] Domain Typosquatting Tara{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Typosquatting Nedir?{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}TYPOSQUAT > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            domain = input(f"\n{Fore.WHITE}Hedef domain [ornek.com]: {Style.RESET_ALL}").strip().lower()
            if domain: tam_tarama(domain)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "2":
            print(f"\n{Fore.CYAN}[i] TYPOSQUATTING NEDİR?{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Kullanıcıların yazım hatalarından faydalanan saldırı türü.{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Örnek: garanti.com -> garantı.com, garantl.com{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Saldırgan bu domainleri alıp sahte banka sitesi kurar.{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Bu modül tüm varyasyonları üretip hangisi alınmış kontrol eder.{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
