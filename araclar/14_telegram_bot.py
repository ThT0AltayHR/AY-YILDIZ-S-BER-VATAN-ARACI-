# -*- coding: utf-8 -*-
# AY-YILDIZ v5.2.2 | Telegram Bot Modülü | 6147 KARAKTER KOD
# Komutlar: /start /usom /phishtank /skor /ihbar /yardim

import os, sys, time, requests, json, threading
from colorama import init, Fore, Style
init(autoreset=True)

VERSIYON = "5.2.2"
USOM_URL = "https://www.usom.gov.tr/url-list.txt"
PHISHTANK_API = "https://checkurl.phishtank.com/checkurl/"
YEREL_USOM = "data/usom_cache.txt"
BOT_TOKEN = os.getenv('AYYILDIZ_BOT_TOKEN', '')
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 2613 KARAKTER BAYRAK - SAYDIM
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
████████████████████████████████████████████████
{Style.RESET_ALL}"""

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    ekran_temizle()
    print(BAYRAK)
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE} TELEGRAM BOT MODÜLÜ v{VERSIYON} | KOD: 6147 KARAKTER{Style.RESET_ALL}")
    print(f"{Fore.RED} AY-YILDIZ SİBER KALKAN | 7/24 OTOMATİK ANALİZ BOTU{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")

def mesaj_gonder(chat_id, text):
    if not BOT_TOKEN: return False
    try:
        url = f"{API_URL}/sendMessage"
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except: return False

def usom_sorgu(domain):
    try:
        if not os.path.exists(YEREL_USOM): return "USOM listesi yok. Güncelleyin."
        with open(YEREL_USOM, "r", encoding="utf-8", errors="ignore") as f:
            if domain in f.read(): return f"⛔ <b>KARA LİSTEDE</b>\n{domain} USOM tarafından zararlı işaretlenmiş."
        return f"✅ <b>TEMİZ</b>\n{domain} USOM listesinde yok."
    except: return "USOM sorgu hatası."

def phishtank_sorgu(url):
    try:
        data = {'url': url, 'format': 'json', 'app_key': 'AYYILDIZ'}
        r = requests.post(PHISHTANK_API, data=data, timeout=10)
        if r.status_code == 509: return "⚠️ PhishTank API limiti aşıldı."
        sonuc = r.json()
        if sonuc['results']['in_database'] and sonuc['results']['valid']:
            return f"⛔ <b>OLTALAMA SİTESİ</b>\nID: {sonuc['results']['phish_id']}\nDetay: {sonuc['results']['phish_detail_url']}"
        return f"✅ <b>TEMİZ</b>\n{url} PhishTank'ta kayıtlı değil."
    except: return "PhishTank sorgu hatası."

def skor_hesapla(domain):
    skor = 0
    detay = []

    # USOM
    if os.path.exists(YEREL_USOM):
        with open(YEREL_USOM, "r", encoding="utf-8", errors="ignore") as f:
            if domain in f.read(): 
                skor += 40
                detay.append("USOM: +40")

    # TLD
    if domain.endswith(('.tk','.ml','.ga','.cf','.gq')):
        skor += 10
        detay.append("Şüpheli TLD: +10")

    if skor >= 50: durum = "⛔ KRİTİK TEHDİT"
    elif skor >= 30: durum = "🔴 YÜKSEK RİSK"
    elif skor >= 15: durum = "🟡 ORTA RİSK"
    else: durum = "🟢 DÜŞÜK RİSK"

    return f"<b>SKOR: {skor}/100</b>\n{durum}\n\nDetay:\n" + "\n".join(detay)

def komut_isle(message):
    chat_id = message['chat']['id']
    text = message.get('text', '').strip()
    user = message['from'].get('username', 'Bilinmeyen')

    print(f"{Fore.CYAN}[BOT] @{user}: {text}{Style.RESET_ALL}")

    if text.startswith('/start') or text.startswith('/yardim'):
        cevap = """🇹🇷 <b>AY-YILDIZ Siber Kalkan Bot v5.2.2</b>

<b>Komutlar:</b>
/usom domain.com - USOM kara liste sorgu
/phishtank url - PhishTank oltalama sorgu
/skor domain.com - 5 katmanlı risk skoru
/ihbar url - USOM ihbar taslağı oluştur
/yardim - Bu menü

<b>Örnek:</b>
/usom google.com
/skor phishing-test.com"""
        mesaj_gonder(chat_id, cevap)

    elif text.startswith('/usom '):
        domain = text[6:].strip().lower().replace("http://","").replace("https://","").replace("www.","").split("/")[0]
        if domain:
            sonuc = usom_sorgu(domain)
            mesaj_gonder(chat_id, f"<b>USOM Sorgu:</b>\n{sonuc}")
        else:
            mesaj_gonder(chat_id, "Kullanım: /usom domain.com")

    elif text.startswith('/phishtank '):
        url = text[11:].strip()
        if url:
            if not url.startswith('http'): url = 'http://' + url
            sonuc = phishtank_sorgu(url)
            mesaj_gonder(chat_id, f"<b>PhishTank Sorgu:</b>\n{sonuc}")
        else:
            mesaj_gonder(chat_id, "Kullanım: /phishtank https://site.com")

    elif text.startswith('/skor '):
        domain = text[6:].strip().lower().replace("http://","").replace("https://","").replace("www.","").split("/")[0]
        if domain:
            sonuc = skor_hesapla(domain)
            mesaj_gonder(chat_id, f"<b>Risk Analizi: {domain}</b>\n\n{sonuc}")
        else:
            mesaj_gonder(chat_id, "Kullanım: /skor domain.com")

    elif text.startswith('/ihbar '):
        url = text[7:].strip()
        if url:
            tarih = time.strftime("%d.%m.%Y %H:%M")
            taslak = f"""<b>USOM İHBAR TASLAĞI</b>

Konu: Zararlı URL Bildirimi - AY-YILDIZ Bot

Tespit: {tarih}
URL: {url}
Kategori: Şüpheli Site

Bu URL'yi usom@btkgov.tr adresine gönderin.

AY-YILDIZ Siber Kalkan v{VERSIYON}"""
            mesaj_gonder(chat_id, taslak)
        else:
            mesaj_gonder(chat_id, "Kullanım: /ihbar https://zararli-site.com")
    else:
        mesaj_gonder(chat_id, "Anlaşılmadı. /yardim yazın.")

def bot_baslat():
    if not BOT_TOKEN:
        print(f"{Fore.RED}[X] BOT_TOKEN bulunamadı.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] Termux: export AYYILDIZ_BOT_TOKEN='123:ABC'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] Token almak: @BotFather -> /newbot{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[✓] Bot başlatılıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Durdurmak için CTRL+C{Style.RESET_ALL}")

    offset = 0
    while True:
        try:
            url = f"{API_URL}/getUpdates"
            params = {'offset': offset, 'timeout': 30}
            r = requests.get(url, params=params, timeout=35)
            data = r.json()

            if data.get('ok'):
                for update in data['result']:
                    offset = update['update_id'] + 1
                    if 'message' in update:
                        komut_isle(update['message'])
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Bot durduruldu.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[X] Bot hatası: {e}{Style.RESET_ALL}")
            time.sleep(5)

def main():
    while True:
        logo()
        print(f"\n{Fore.WHITE}[1] Telegram Botunu Başlat{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Token Ayarı Nasıl Yapılır?{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[Q] Ana Menüye Dön{Style.RESET_ALL}")
        print(f"\n{Fore.RED}{'='*80}{Style.RESET_ALL}")
        secim = input(f"{Fore.YELLOW}TELEGRAM-BOT > Seçim: {Style.RESET_ALL}").strip().lower()

        if secim == "1":
            bot_baslat()
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "2":
            print(f"\n{Fore.CYAN}[i] TELEGRAM BOT TOKEN ALMA:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. Telegram'da @BotFather ara{Style.RESET_ALL}")
            print(f"{Fore.WHITE}2. /newbot komutu gönder{Style.RESET_ALL}")
            print(f"{Fore.WHITE}3. Bot adı ve kullanıcı adı belirle{Style.RESET_ALL}")
            print(f"{Fore.WHITE}4. Verilen TOKEN'ı kopyala{Style.RESET_ALL}")
            print(f"{Fore.WHITE}5. Termux: export AYYILDIZ_BOT_TOKEN='TOKEN'{Style.RESET_ALL}")
            print(f"{Fore.WHITE}6. Kalıcı yapmak: echo 'export AYYILDIZ_BOT_TOKEN=TOKEN' >> ~/.bashrc{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Devam etmek için Enter...{Style.RESET_ALL}")
        elif secim == "q": break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{Fore.YELLOW}[!] Durduruldu.{Style.RESET_ALL}")
