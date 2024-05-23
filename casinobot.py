import telebot
import random
import json
import time
import os
from telebot import TeleBot, types

# Bot token'ınızı buraya ekleyin
API_TOKEN = '7168613359:AAGlb3Sfk_toTBDYYp2eIAkCdphiEx1qBc0'

bot = telebot.TeleBot(API_TOKEN)
# Kullanıcıların oyun başlangıcını saklamak için sözlük
game_sessions = {}

# Bakiyeleri saklamak için kullanılacak dosyanın adı
BALANCE_FILE = 'balances.json'

# Sudo kullanıcıların kimliklerini içeren liste
SUDO_USERS = ['SUDO_USER_ID1', '6958129929']  # Buraya sudo kullanıcılarının ID'lerini ekleyin

# Kullanıcı bakiyelerini saklamak için sözlük
user_balances = {}

# Bakiyeleri dosyadan yükleme
def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Bakiyeleri dosyaya kaydetme
def save_balances():
    with open(BALANCE_FILE, 'w') as f:
        json.dump(user_balances, f)

# Bot başlatıldığında bakiyeleri yükle
user_balances = load_balances()

# /start komutu işleyicisi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in user_balances:
        user_balances[user_id] = 5000  # Yeni kullanıcıya başlangıç bakiyesi
        save_balances()  # Bakiyeleri kaydet
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Sahibim ❤️‍🩹", url="https://t.me/ramowlfbio")
    button2 = types.InlineKeyboardButton("Kanal 😍", url="https://t.me/TelethonUserbotKanali")
    button3 = types.InlineKeyboardButton("Beni Gruba Ekle💫", url="https://t.me/EglenceRobot?startgroup=new")
    markup.add(button1, button2, button3)
    bot.reply_to(message, "👋 Merhaba botumuza hoşgeldin ilk defa başlattıyorsan 5000 TL bakiye başlangıç hediyesi olarak verilir İyi oyunlar.", reply_markup=markup)
    
# /skor zenginler listesini gösterir
@bot.message_handler(commands=['zenginler'])
def show_leaderboard(message):
    sorted_balances = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)
    
    leaderboard_message = "🏆 En İyi 10 Zengin:\n\n"
    for i, (user_id, balance) in enumerate(sorted_balances[:10], start=1):
        user_name = bot.get_chat(user_id).first_name if user_id != 'None' else "Bilinmiyor"
        leaderboard_message += f"🎖️ {i}. {user_name} ⇒ {balance} TL\n"

    bot.reply_to(message, leaderboard_message)
    
# /bagis arkadaşına bakiye göndermek için
@bot.message_handler(commands=['borc'])
def send_balance_to_friend(message):
    user_id = str(message.from_user.id)

    try:
        parts = message.text.split()
        friend_id = parts[1]
        amount = int(parts[2])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Geçerli bir miktar girin Kullanım: /borc <kullanıcı_id> <miktar>')
        return

    if amount <= 0:
        bot.reply_to(message, 'Sayı girin')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    if user_balances[user_id] < amount:
        bot.reply_to(message, 'Yeterli bakiyeniz yok.')
        return

    if friend_id not in user_balances:
        user_balances[friend_id] = 0

    user_balances[user_id] -= amount
    user_balances[friend_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {friend_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi.')

# /slot komutu işleyicisi
@bot.message_handler(commands=['slot'])
def slot_command(message):
    user_id = str(message.from_user.id)

    # Kullanıcıya slot oyununu tanıtıcı mesaj gönderme
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Slot Oyununu Oynayarak Bakiyen kasın Çıkarın\nKullanım: /slot <miktar>')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    try:
        # Mesajdan bahis miktarını alma
        bet_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir bahis miktarı girin. Kullanım: /slot <miktar>')
        return

    if bet_amount <= 0:
        bot.reply_to(message, 'Bahis miktarı sayı olmalı.')
        return

    if user_balances[user_id] < bet_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    # Slot sonucu
    slot_result = random.choices(["🍒", "🍋", "🍉", "⭐", "💎", "🍊", "🍏", "🔔"], k=3)
    unique_symbols = len(set(slot_result))

    # Kazanma durumu
    if unique_symbols == 1:  # 3 sembol de aynı
        winnings = bet_amount * 4
        user_balances[user_id] += winnings - bet_amount  # Bahis miktarı geri verildiği için çıkarılır
        bot.reply_to(message, f'3 sembol eşleşti! Kazandınız!\nKazanılan Bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    elif unique_symbols == 2:  # 2 sembol aynı
        winnings = bet_amount * 3
        user_balances[user_id] += winnings - bet_amount  # Bahis miktarı geri verildiği için çıkarılır
        bot.reply_to(message, f'2 sembol eşleşti Kazandınız!\nKazanılan bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    else:
        user_balances[user_id] -= bet_amount
        bot.reply_to(message, f'Kazanamadınız. Bir dahakine daha şanslı olabilirsiniz.\nSlot sonucu: {" ".join(slot_result)}\nKalan bakiye: {user_balances[user_id]} TL')

    # Bakiyeleri güncelle
    save_balances()

# /gonder komutu işleyicisi
@bot.message_handler(commands=['gonder'])
def send_balance(message):
    user_id = str(message.from_user.id)

    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Bu komutu kullanma yetkin yok yarram.')
        return

    try:
        # Mesajdan alıcı kullanıcı ID'si ve gönderilecek miktarı alma
        parts = message.text.split()
        target_id = parts[1]
        amount = int(parts[2])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir format kullanın. Kullanım: /gonder <kullanıcı_id> <miktar>')
        return

    if amount <= 0:
        bot.reply_to(message, 'Gönderilecek miktar pozitif bir sayı olmalıdır.')
        return

    if target_id not in user_balances:
        user_balances[target_id] = 100  # Hedef kullanıcı yoksa, başlangıç bakiyesi verilir

    user_balances[target_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {target_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi. Yeni bakiye: {user_balances[target_id]} TL')
    
# /risk komutu işleyicisi
@bot.message_handler(commands=['risk'])
def risk_command(message):
    user_id = str(message.from_user.id)

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Risk Alıp Bakiye kazan\nKullanım: /risk <miktar>')
        return

    try:
        # Mesajdan risk miktarını alma
        risk_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'geçerli bir risk miktarı gir Kullanım: /risk <miktar>')
        return

    if risk_amount <= 0:
        bot.reply_to(message, 'Risk miktarı sayı olmalı.')
        return

    if user_balances[user_id] < risk_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    # Risk oyunu
    if random.random() < 0.5:  # %50 kazanma olasılığı
        winnings = risk_amount * 2
        user_balances[user_id] += winnings - risk_amount  # Bahis miktarı geri verildiği için çıkarılır
        bot.reply_to(message, f'Tebrikler  {winnings} TL kazandınız.\nYeni bakiyeniz: {user_balances[user_id]} TL')
    else:
        user_balances[user_id] -= risk_amount
        bot.reply_to(message, f'Üzgünüm {risk_amount} TL kaybettiniz.\nbakiyeniz: {user_balances[user_id]} TL')

    # Bakiyeleri güncelle
    save_balances()
    
# /help yardım menüsü
@bot.message_handler(commands=['yardim'])
def send_help_message(message):
    help_message = """
    ⭐ Hey dostum aşağıdaki komutları kullanabilirsin

/slot [miktar]: 🎰 Slot oyununu oynamak için bahis yapın.

/tahmin: 🔢 Sayı Tahmin Oyununu Başlatır.

/bakiye: 💰 Mevcut bakiyenizi kontrol edin.

/risk: Risk oyunu oynayıp bakiye kazanabilirsiniz.

/borc [kullanıcı adı veya Kullanıcı İd] [miktar]: 💸 Başka bir kullanıcıya bakiye göndermesi yapın.

/zenginler: 🏆 Genel Sıralamayı gösterir.

/yardim: ℹ️ Bu yardım mesajını görüntüleyin.
    """
    bot.reply_to(message, help_message)
    
# /bakiye güncel bakiye gösterme
@bot.message_handler(commands=['bakiye'])
def check_balance(message):
    user_id = str(message.from_user.id)

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    bot.reply_to(message, f"Güncel bakiyeniz: {user_balances[user_id]} TL")


# /tahmin komutu işleyicisi
@bot.message_handler(commands=['tahmin'])
def start_guessing_game(message):
    user_id = str(message.from_user.id)

    # Oyun zaten başlatılmışsa
    if user_id in game_sessions:
        bot.reply_to(message, 'Oyun zaten başlatılmış Bu Durumda Size Sayıyı.Tahmin Etmek Düşüyor')
        return

    # Yeni bir oyun başlatılması
    bot.reply_to(message, '🔢 Sayı Tahmin Oyunu Başlatıldı!\n\n1 İle 100 Arasındaki Sayıyı Tahmin Et\nİlk Doğru Tahmini Yapan 30 TL Kazanır. Herkes Tahminde Bulunabilir. Elini Çabuk Tut 😎')
    game_sessions[user_id] = {'target_number': random.randint(1, 100)}

# Doğrudan tahmin işleyicisi
@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    user_id = str(message.from_user.id)

    # Oyun başlatılmamışsa
    if user_id not in game_sessions:
        bot.reply_to(message, '')
        return

    # Hesap kontrolü
    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    # Tahmin edilecek rasgele sayıyı almak
    target_number = game_sessions[user_id]['target_number']

    # Tahmin edilen sayıyı almak
    try:
        guess = int(message.text)
    except ValueError:
        bot.reply_to(message, '')
        return

    # Doğru tahminde bulunma durumu
    if guess < target_number:
        bot.reply_to(message, '⬆️ Daha Büyük Bir Sayı Gir.')
    elif guess > target_number:
        bot.reply_to(message, '⬇️ Daha Küçük Bir Sayı Gir.')
    else:
        user_balances[user_id] += 30
        user_name = message.from_user.first_name
        bot.reply_to(message, f'🎉 Tebrikler {user_name}! Doğru Cevabı İlk Buldu Ve 30 TL Kazandı. Oyun Sona Erdi. Yeni Başlat /tahmin')
        del game_sessions[user_id]  # Oyun sona erdi, oyun oturumunu kaldır

    # Bakiyeleri güncelle
    save_balances()
    
# Tahmin edilecek rasgele sayıyı oluşturma
target_number = random.randint(1, 100)

# Botu çalıştır
bot.polling()
