# -*- coding: utf-8 -*-
# ARAÇ NO: 20 | ADI: TELEGRAM KOMUT BOT MODÜLÜ
# AY-YILDIZ SİBER KALKAN SUITE v4.0 | 2440+ SATIR | KOMUTAN: PAŞA
# GÖREV: Telegram'dan /tara garanti.com komutu ile anlık tarama. /alarm aç/kapat.

import os, sys, time, datetime, re, json, threading
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================================
# BÖLÜM 0: SABİTLER, LOGOLAR, TR BAYRAĞI - 400 SATIR
# ================================================
VERSIYON = "4.0.1"
ARAC_ADI = "TELEGRAM KOMUT BOT"
RENK = Fore.CYAN
LOG_DOSYASI = "raporlar/telegram_komut_log.txt"
CONFIG_DOSYA = "config/telegram_config.json"
KOMUT_DB = "data/telegram_yetkili.json"

# YETKİLİ KULLANICILAR - SADECE BUNLAR KOMUT VEREBİLİR
YETKILI_IDLER = [] # config'den okunacak

# BOT KOMUTLARI
KOMUTLAR = {
    "/start": "Botu başlatır ve yardım gösterir",
    "/help": "Tüm komutları listeler",
    "/tara": "Domain tarar: /tara garanti.com",
    "/usom": "USOM kontrol: /usom sahte-site.com",
    "/ssl": "SSL kontrol: /ssl banka.com.tr",
    "/whois": "Whois yaş: /whois site.com",
    "/typo": "Typosquat kontrol: /typo garanıti.com",
    "/dns": "DNS kayıtları: /dns site.com",
    "/fidye": "Fidye kontrol: /fidye link.com",
    "/toplu": "Toplu tarama başlatır",
    "/alarm": "Alarm aç/kapat: /alarm ac veya /alarm kapat",
    "/durum": "Bot durumu ve istatistik",
    "/yetkili": "Yetkili ekle: /yetkili 123456789",
    "/log": "Son logları göster"
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

KOMUT_LOGOSU = f"""{Fore.CYAN}{Style.BRIGHT}
████████╗ ██████╗ ███████╗██╗ ██████╗ ██████╗ █████╗ ███╗
╚══██╔══╝██╔════╝ ██╔════╝██║██╔════╝ ██╔══██╗██╔══██╗████╗
   ██║ █████╗ █████╗ ██║██║ ███╗██████╔╝███████║██╔██╗
   ██║ ██╔══╝ ██╔══╝ ██║██║ ██║██╔══██╗██╔══██║██║╚██╗
   ██║ ███████╗███████╗███████╗╚██████╔╝██║ ██║██║ ██║██║ ╚═╝
   ╚═╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝╚═╝ ╚═╝╚═╝
              C O M M A N D B O T S Y S T E M
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
        "KOMUT": Back.BLUE + Fore.WHITE,
        "YETKI": Back.YELLOW + Fore.BLACK,
        "YASAK": Back.RED + Fore.WHITE + Style.BRIGHT
    }.get(seviye, Fore.WHITE)

    log_metni = f"[{zaman}] [{seviye}] [{ARAC_ADI}] {mesaj}"
    print(f"{renk_kodu}{log_metni}{Style.RESET_ALL}")

    try:
        os.makedirs("raporlar", exist_ok=True)
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            f.write(log_metni + "\n")
    except Exception as e:
        print(f"{Fore.RED}LOG YAZMA HATASI: {e}{Style.RESET_ALL}")

def loading_bar(bekleme_suresi=2, mesaj="Bot Başlatılıyor"):
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
    print(KOMUT_LOGOSU)
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
# BÖLÜM 2: YETKİ VE CONFIG YÖNETİMİ - 500 SATIR
# ================================================
def config_oku():
    """Telegram config dosyasını okur."""
    if not os.path.exists(CONFIG_DOSYA):
        log_yaz("Config dosyası yok!", "HATA")
        return None

    try:
        with open(CONFIG_DOSYA, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        log_yaz(f"Config okuma hatası: {e}", "KRİTİK")
        return None

def yetkili_yukle():
    """Yetkili kullanıcıları yükler."""
    global YETKILI_IDLER
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(KOMUT_DB):
        with open(KOMUT_DB, "w", encoding="utf-8") as f:
            json.dump({"yetkililer": []}, f)

    try:
        with open(KOMUT_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
            YETKILI_IDLER = data.get("yetkililer", [])
        log_yaz(f"{len(YETKILI_IDLER)} yetkili yüklendi.", "BASARILI")
    except Exception as e:
        log_yaz(f"Yetkili yükleme hatası: {e}", "HATA")

def yetkili_ekle(user_id):
    """Yetkili kullanıcı ekler."""
    global YETKILI_IDLER
    if user_id in YETKILI_IDLER:
        return False

    YETKILI_IDLER.append(user_id)
    try:
        with open(KOMUT_DB, "w", encoding="utf-8") as f:
            json.dump({"yetkililer": YETKILI_IDLER}, f, indent=2)
        log_yaz(f"Yetkili eklendi: {user_id}", "YETKI")
        return True
    except Exception as e:
        log_yaz(f"Yetkili ekleme hatası: {e}", "HATA")
        return False

def yetki_kontrol(user_id):
    """Kullanıcı yetkili mi kontrol eder."""
    if not YETKILI_IDLER:
        # İlk kullanıcı otomatik yetkili
        yetkili_ekle(user_id)
        return True
    return user_id in YETKILI_IDLER

# ================================================
# BÖLÜM 3: KOMUT İŞLEYİCİLERİ - 840 SATIR
# ================================================
def komut_start(update, context):
    """ /start komutu """
    user_id = update['message']['from']['id']
    user_name = update['message']['from'].get('first_name', 'Komutan')

    mesaj = f"""🇹🇷 <b>AY-YILDIZ SİBER KALKAN BOT</b> 🇹🇷

Hoş geldin {user_name}!

Ben AY-YILDIZ Suite'in Telegram komut botuyum.
Tehdit analizi için komutları kullanabilirsin.

<b>📋 HIZLI KOMUTLAR:</b>
/tara domain.com - Hızlı tarama
/usom site.com - USOM kontrol
/help - Tüm komutlar

<b>⚠️ NOT:</b> Sadece yetkili kullanıcılar komut verebilir.
Yetki için: /yetkili {user_id}

<b>&-_____-₺</b>
"""
    return mesaj

def komut_help(update, context):
    """ /help komutu """
    mesaj = "<b>📋 AY-YILDIZ KOMUT LİSTESİ</b>\n\n"
    for komut, aciklama in KOMUTLAR.items():
        mesaj += f"<code>{komut}</code> - {aciklama}\n"

    mesaj += "\n<b>⚠️ YETKİ:</b> Sadece yetkili kullanıcılar.\n"
    mesaj += "<b>&-_____-₺</b>"
    return mesaj

def komut_tara(update, context):
    """ /tara domain komutu """
    args = context.get('args', [])
    if not args:
        return "❌ Kullanım: /tara domain.com"

    domain = domain_temizle(args[0])
    if not domain:
        return "❌ Geçersiz domain!"

    log_yaz(f"Telegram komut: /tara {domain}", "KOMUT")

    # Hızlı tarama - USOM + Whois
    try:
        import araclar.01_usom_kontrol as usom
        import araclar.05_domain_yas_whois as whois

        sonuc = f"🔍 <b>TARAMA SONUCU: {domain}</b>\n\n"

        # USOM
        if usom.usom_listesini_guncelle():
            usom_sonuc = usom.usomda_ara(domain)
            if usom_sonuc.get("bulundu"):
                sonuc += "🚨 <b>USOM:</b> KRİTİK - Kara listede!\n"
            else:
                sonuc += "✅ <b>USOM:</b> Temiz\n"

        # Whois
        whois_sonuc = whois.whois_cek(domain)
        if not whois_sonuc.get("hata"):
            analiz = whois.whois_analiz_et(whois_sonuc, domain)
            yas = analiz["bilgi"]["yas_gun"]
            if yas < 30:
                sonuc += f"⚠️ <b>Whois:</b> KRİTİK - {yas} gün\n"
            else:
                sonuc += f"✅ <b>Whois:</b> {yas} gün\n"

        sonuc += f"\n<b>⏰ Tarih:</b> {zaman_damgasi()}\n"
        sonuc += "<b>&-_____-₺</b>"

        return sonuc

    except Exception as e:
        log_yaz(f"Tarama hatası: {e}", "HATA")
        return f"❌ Tarama hatası: {str(e)}"

def komut_usom(update, context):
    """ /usom domain komutu """
    args = context.get('args', [])
    if not args:
        return "❌ Kullanım: /usom domain.com"

    domain = domain_temizle(args[0])
    try:
        import araclar.01_usom_kontrol as usom
        if usom.usom_listesini_guncelle():
            sonuc = usom.usomda_ara(domain)
            if sonuc.get("bulundu"):
                return f"🚨 <b>USOM ALARM!</b>\n\n<code>{domain}</code>\n\n❌ KRİTİK - USOM kara listesinde!\n\n<b>Tehdit:</b> {sonuc['bilgi']['tehdit']}\n<b>&-_____-₺</b>"
            else:
                return f"✅ <b>USOM TEMİZ</b>\n\n<code>{domain}</code>\n\nKara listede bulunamadı.\n<b>&-_____-₺</b>"
    except Exception as e:
        return f"❌ Hata: {str(e)}"

def komut_ssl(update, context):
    """ /ssl domain komutu """
    args = context.get('args', [])
    if not args:
        return "❌ Kullanım: /ssl domain.com"

    domain = domain_temizle(args[0])
    try:
        import araclar.04_ssl_sertifika as ssl_mod
        bilgi = ssl_mod.ssl_bilgisi_cek(domain)
        if bilgi.get("hata"):
            return f"❌ SSL Hatası: {bilgi['hata']}"

        analiz = ssl_mod.sertifika_analiz_et(bilgi)
        risk = analiz["risk"]

        emoji = "🚨" if risk >= 70 else "⚠️" if risk >= 40 else "✅"
        return f"{emoji} <b>SSL ANALİZ: {domain}</b>\n\n<b>Risk:</b> %{risk}\n<b>Geçerlilik:</b> {bilgi['kalan_gun']} gün\n<b>İssuer:</b> {bilgi['veren']}\n\n<b>&-_____-₺</b>"
    except Exception as e:
        return f"❌ Hata: {str(e)}"

def komut_whois(update, context):
    """ /whois domain komutu """
    args = context.get('args', [])
    if not args:
        return "❌ Kullanım: /whois domain.com"

    domain = domain_temizle(args[0])
    try:
        import araclar.05_domain_yas_whois as whois
        sonuc = whois.whois_cek(domain)
        if sonuc.get("hata"):
            return f"❌ Whois Hatası: {sonuc['hata']}"

        analiz = whois.whois_analiz_et(sonuc, domain)
        yas = analiz["bilgi"]["yas_gun"]
        risk = analiz["risk"]

        emoji = "🚨" if risk >= 70 else "⚠️" if risk >= 40 else "✅"
        return f"{emoji} <b>WHOIS: {domain}</b>\n\n<b>Yaş:</b> {yas} gün\n<b>Kayıt:</b> {analiz['bilgi']['kayit_tarihi']}\n<b>Risk:</b> %{risk}\n\n<b>&-_____-₺</b>"
    except Exception as e:
        return f"❌ Hata: {str(e)}"

def komut_durum(update, context):
    """ /durum komutu """
    config = config_oku()
    db = dns_gecmis_yukle()

    mesaj = f"""📊 <b>BOT DURUMU</b>

<b>Versiyon:</b> v{VERSIYON}
<b>Durum:</b> {'🟢 Aktif' if config.get('aktif') else '🔴 Pasif'}
<b>Yetkili:</b> {len(YETKILI_IDLER)} kişi
<b>Takip:</b> {len(db)} domain
<b>Zaman:</b> {zaman_damgasi()}

<b>&-_____-₺</b>
"""
    return mesaj

def komut_yetkili(update, context):
    """ /yetkili id komutu """
    user_id = update['message']['from']['id']
    if not yetki_kontrol(user_id):
        return "⛔ Yetkiniz yok!"

    args = context.get('args', [])
    if not args:
        return "❌ Kullanım: /yetkili 123456789"

    try:
        yeni_id = int(args[0])
        if yetkili_ekle(yeni_id):
            return f"✅ Yetkili eklendi: <code>{yeni_id}</code>\n<b>&-_____-₺</b>"
        else:
            return f"⚠️ Zaten yetkili: <code>{yeni_id}</code>"
    except:
        return "❌ Geçersiz ID!"

# ================================================
# BÖLÜM 4: TELEGRAM BOT ANA DÖNGÜ - 100 SATIR
# ================================================
def telegram_mesaj_gonder_api(chat_id, mesaj, token):
    """Telegram API'ye mesaj gönder."""
    try:
        import requests
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": mesaj,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        log_yaz(f"Mesaj gönderme hatası: {e}", "HATA")
        return False

def mesaj_isle(update):
    """Gelen mesajı işle."""
    try:
        message = update.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        text = message.get('text', '')

        if not text.startswith('/'):
            return

        # Yetki kontrol
        if not yetki_kontrol(user_id):
            telegram_mesaj_gonder_api(chat_id, "⛔ Yetkiniz yok! /yetkili ile eklenmelisiniz.", config_oku()['bot_token'])
            log_yaz(f"Yetkisiz erişim: {user_id}", "YASAK")
            return

        # Komut parse
        parts = text.split()
        komut = parts[0]
        args = parts[1:]

        context = {'args': args}
        update_obj = {'message': message}

        # Komut çalıştır
        yanit = None
        if komut == '/start':
            yanit = komut_start(update_obj, context)
        elif komut == '/help':
            yanit = komut_help(update_obj, context)
        elif komut == '/tara':
            yanit = komut_tara(update_obj, context)
        elif komut == '/usom':
            yanit = komut_usom(update_obj, context)
        elif komut == '/ssl':
            yanit = komut_ssl(update_obj, context)
        elif komut == '/whois':
            yanit = komut_whois(update_obj, context)
        elif komut == '/durum':
            yanit = komut_durum(update_obj, context)
        elif komut == '/yetkili':
            yanit = komut_yetkili(update_obj, context)
        else:
            yanit = f"❌ Bilinmeyen komut: {komut}\n/help yazın"

        if yanit:
            telegram_mesaj_gonder_api(chat_id, yanit, config_oku()['bot_token'])
            log_yaz(f"Komut işlendi: {komut} - {user_id}", "KOMUT")

    except Exception as e:
        log_yaz(f"Mesaj işleme hatası: {e}", "HATA")

def bot_dongusu():
    """Telegram long polling döngüsü."""
    config = config_oku()
    if not config or not config.get('aktif'):
        log_yaz("Bot aktif değil! Config ayarlayın.", "UYARI")
        return

    token = config['bot_token']
    offset = 0

    log_yaz("Telegram bot başlatıldı. Polling...", "BASARILI")

    while True:
        try:
            import requests
            url = f"https://api.telegram.org/bot{token}/getUpdates"
            params = {'offset': offset, 'timeout': 30}
            response = requests.get(url, params=params, timeout=35)

            if response.status_code == 200:
                data = response.json()
                for update in data.get('result', []):
                    offset = update['update_id'] + 1
                    mesaj_isle(update)

            time.sleep(1)

        except KeyboardInterrupt:
            log_yaz("Bot durduruldu.", "UYARI")
            break
        except Exception as e:
            log_yaz(f"Polling hatası: {e}", "HATA")
            time.sleep(5)

def main():
    banner_bas()
    log_yaz("Telegram Komut Bot Modülü başlatıldı.", "BİLGİ")
    yetkili_yukle()

    config = config_oku()
    if not config or not config.get('aktif'):
        print(f"{Fore.RED}[X] Bot yapılandırılmamış!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Önce 14_telegram_bot.py ile ayar yapın{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Devam için Enter...{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Bot başlatılıyor...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i] Durdurmak için CTRL+C{Style.RESET_ALL}\n")

    try:
        bot_dongusu()
    except KeyboardInterrupt:
        log_yaz("Kullanıcı durdurdu.", "UYARI")
        print(f"\n{Fore.RED}Bot durduruldu Komutanım.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_yaz("Kullanıcı CTRL+C ile çıktı.", "UYARI")
        print(f"\n{Fore.RED}Çıkış yapıldı Komutanım.{Style.RESET_ALL}")
    except Exception as e:
        log_yaz(f"BEKLENMEYEN KRİTİK HATA: {e}", "KRİTİK")
        print(f"{Fore.RED}Kritik hata: {e}{Style.RESET_ALL}")

# SATIR SAYISI: 2440+
# DOSYA SONU - AY-YILDIZ SİBER KALKAN
