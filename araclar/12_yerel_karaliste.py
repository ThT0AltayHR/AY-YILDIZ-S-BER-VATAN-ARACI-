# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | Yerel Karaliste Modülü | 6051 KARAKTER KOD
# SQLite DB | Ekle/Sil/Ara/Listele | USOM Dışı Özel Liste

import os, sys, sqlite3, time
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
DB_DOSYA = "data/yerel_karaliste.db"

# 2599 KARAKTER BAYRAK - SAYDIM
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
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████████████
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
██████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████████
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
    print(f"{Fore.WHITE} YEREL KARALİSTE MODÜLÜ v{VERSIYON} | KOD: 6051 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | ÖZEL TEHDİT VERİTABANI{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def db_baglan():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_DOSYA)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS karaliste
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      domain TEXT UNIQUE NOT NULL,
                      sebep TEXT,
                      ekleyen TEXT,
                      tarih TEXT,
                      skor INTEGER DEFAULT 50)''')
    conn.commit()
    return conn, cursor

def ekle():
    domain = input(f"\n{Fore.WHITE}Eklenecek domain: {Style.RESET_ALL}").strip().lower()
    if not domain:
        print(f"{Fore.RED}[X] Domain boş olamaz.{Style.RESET_ALL}")
        return

    sebep = input(f"{Fore.WHITE}Sebep [Phishing/Malware/Dolandırıcılık]: {Style.RESET_ALL}").strip()
    ekleyen = input(f"{Fore.WHITE}Ekleyen [Varsayılan: OPERATOR]: {Style.RESET_ALL}").strip() or "OPERATOR"
    skor = input(f"{Fore.WHITE}Risk Skoru [0-100] Varsayılan:50: {Style.RESET_ALL}").strip()

    try:
        skor = int(skor) if skor else 50
        if skor < 0 or skor > 100: skor = 50
    except: skor = 50

    conn, cursor = db_baglan()
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    try:
        cursor.execute("INSERT INTO karaliste (domain, sebep, ekleyen, tarih, skor) VALUES (?,?,?,?,?)",
                      (domain, sebep, ekleyen, tarih, skor))
        conn.commit()
        print(f"\n{Fore.GREEN}[✓] {domain} karalisteye eklendi.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[i] Sebep: {sebep} | Skor: {skor} | Ekleyen: {ekleyen}{Style.RESET_ALL}")
    except sqlite3.IntegrityError:
        print(f"{Fore.YELLOW}[!] {domain} zaten listede mevcut.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[X] Hata: {e}{Style.RESET_ALL}")
    finally:
        conn.close()

def sil():
    domain = input(f"\n{Fore.WHITE}Silinecek domain: {Style.RESET_ALL}").strip().lower()
    if not domain:
        print(f"{Fore.RED}[X] Domain boş olamaz.{Style.RESET_ALL}")
        return

    conn, cursor = db_baglan()
    cursor.execute("DELETE FROM karaliste WHERE domain=?", (domain,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"\n{Fore.GREEN}[✓] {domain} karalisteden silindi.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] {domain} listede bulunamadı.{Style.RESET_ALL}")
    conn.close()

def ara():
    domain = input(f"\n{Fore.WHITE}Aranacak domain: {Style.RESET_ALL}").strip().lower()
    if not domain:
        print(f"{Fore.RED}[X] Domain boş olamaz.{Style.RESET_ALL}")
        return

    conn, cursor = db_baglan()
    cursor.execute("SELECT * FROM karaliste WHERE domain LIKE?", (f'%{domain}%',))
    sonuclar = cursor.fetchall()
    conn.close()

    if sonuclar:
        print(f"\n{Fore.GREEN}[✓] {len(sonuclar)} sonuç bulundu:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        for s in sonuclar:
            renk = Fore.RED if s[5] >= 50 else Fore.YELLOW if s[5] >= 30 else Fore.GREEN
            print(f"{renk}ID:{s[0]} | Domain:{s[1]} | Skor:{s[5]} | Sebep:{s[2]}{Style.RESET_ALL}")
            print(f"{Fore.WHITE} Ekleyen:{s[3]} | Tarih:{s[4]}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-'*80}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[!] Sonuç bulunamadı.{Style.RESET_ALL}")

def listele():
    conn, cursor = db_baglan()
    cursor.execute("SELECT * FROM karaliste ORDER BY skor DESC, id DESC LIMIT 50")
    sonuclar = cursor.fetchall()
    conn.close()

    if sonuclar:
        print(f"\n{Fore.GREEN}[✓] Son 50 Kayıt (Yüksek risk önce):{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        for s in sonuclar:
            renk = Fore.RED if s[5] >= 50 else Fore.YELLOW if s[5] >= 30 else Fore.GREEN
            print(f"{renk}[{s[5]}] {s[1]} - {s[2]}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Toplam: {len(sonuclar)} kayıt gösterildi{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[!] Karaliste boş.{Style.RESET_ALL}")

def istatistik():
    conn, cursor = db_baglan()
    cursor.execute("SELECT COUNT(*) FROM karaliste")
    toplam = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM karaliste WHERE skor >= 50")
    kritik = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM karaliste WHERE skor >= 30 AND skor < 50")
    yuksek = cursor.fetchone()[0]
    cursor.execute("SELECT sebep, COUNT(*) FROM karaliste GROUP BY sebep ORDER BY COUNT(*) DESC LIMIT 5")
    sebepler = cursor.fetchall()
    conn.close()

    print(f"\n{Fore.CYAN}[i] VERİTABANI İSTATİSTİKLERİ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Toplam Kayıt: {toplam}{Style.RESET_ALL}")
    print(f"{Fore.RED}Kritik Risk >=50: {kritik}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Yüksek Risk 30-49: {yuksek}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Düşük/Orta <30: {toplam-kritik-yuksek}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}En Çok Kullanılan Sebepler:{Style.RESET_ALL}")
    for s in sebepler:
        print(f"{Fore.CYAN} - {s[0]}: {s[1]} adet{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] Karalisteye Domain Ekle{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Karalisteden Domain Sil{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[3] Domain Ara{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[4] Tüm Listeyi Görüntüle{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[5] İstatistik Göster{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}YEREL-DB > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1": ekle()
        elif secim == "2": sil()
        elif secim == "3": ara()
        elif secim == "4": listele()
        elif secim == "5": istatistik()
        elif secim == "q": break

        if secim in ["1","2","3","4","5"]:
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
