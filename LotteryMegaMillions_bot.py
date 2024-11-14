import random
import telebot
from telebot import types
from datetime import datetime, timedelta
from froll_price import froll_price  # Import giá FROLL từ file froll_price.py

# API token cho bot
API_TOKEN = '7667905013:AAHJSt6qk9KYZ9J7qpzXZwqOulnqf_hK9zo'
bot = telebot.TeleBot(API_TOKEN)

# Địa chỉ ví TON để nhận thanh toán và trả thưởng jackpot
MAIN_WALLET_ADDRESS = 'UQCe6Tlk4uLjrBm29EjMm7NLShFns1KvXtuRWIgWPDuM7kSs'

# Giả lập thời gian quay và kết quả kỳ trước
next_draw_time = datetime.now() + timedelta(hours=24)
last_draw_result = "12, 34, 56, 23, 45; 9"
ticket_price_usd = 2

user_data = {}
current_froll_price = froll_price  # Khởi tạo với giá từ file froll_price.py

# ID của bạn để xác nhận quyền chủ sở hữu
OWNER_ID = 901534751  # Thay số này bằng User ID của bạn

@bot.message_handler(commands=['start'])
def send_welcome(message):
    time_remaining = next_draw_time - datetime.now()
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    welcome_message = (
        "🎉 *Welcome to the Mega Millions Lottery Bot!* 🎉\n\n"
        "Experience the thrill of winning big with the *Mega Millions Lottery*! "
        "Buy a ticket and join the community-driven, decentralized lottery platform—completely powered by smart contracts for transparency and fairness. 🏆💰\n\n"
        f"⏰ *Next Draw Time:* {next_draw_time.strftime('%Y-%m-%d %H:%M:%S')} (GMT)\n"
        f"🕒 *Time Remaining:* {hours}h {minutes}m {seconds}s\n\n"
        f"🏆 *Last Draw Result:* {last_draw_result}\n"
        f"💵 *Ticket Price:* $2 (payable in FROLL) 🎟\n"
        f"💰 *Jackpot Prize:* 10,000 FROLL\n\n"
        "📌 *How It Works:*\n"
        "- Choose 5 numbers from 1 to 69 and a Mega Ball from 1 to 26.\n"
        "- Buy more tickets to boost your chances!\n\n"
        "Press *Play* to start selecting your numbers or *Connect* to join our community channels. Good luck! 🍀"
    )

    markup = types.InlineKeyboardMarkup()
    btn_play = types.InlineKeyboardButton("🎟 Play", callback_data="play_start")
    btn_connect = types.InlineKeyboardButton("📱 Connect", callback_data="connect")
    markup.add(btn_play, btn_connect)
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown", reply_markup=markup)

# Xử lý khi người dùng nhấn nút "Connect"
@bot.callback_query_handler(func=lambda call: call.data == "connect")
def send_social_links(call):
    social_links = (
        "📱 Connect with Us for Updates and Support:\n\n"
        "📱 Telegram Channel: [FortuneRolls Channel](https://t.me/FortuneRollschannel)\n"
        "📱 Telegram Group: [FortuneRolls Group](https://t.me/FortuneRolls)\n"
        "📱 X (Twitter): [FortuneRolls on X](https://x.com/FortuneRolls)\n"
        "📱 YouTube: [FortuneRolls on YouTube](https://www.youtube.com/@FortuneRolls)\n"
        "📱 Facebook: [FortuneRolls on Facebook](https://www.facebook.com/FortuneRolls)\n"
        "🌐 Web: [LottoreyFroll.com](https://lottoreyfroll.com/)"
    )
    bot.send_message(call.message.chat.id, social_links, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "play_start")
def show_ticket_selection(call):
    user_id = call.from_user.id
    user_data[user_id] = {'tickets': [], 'quantity': 10}  # Cho phép người dùng chọn tối đa 10 vé
    
    bot.send_message(call.message.chat.id, "Please select your tickets. You can choose up to 10 tickets.")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(1, 11):  # Tạo 10 nút để người chơi có thể chọn tối đa 10 vé
        btn_quick = types.InlineKeyboardButton(f"Quick {i}", callback_data=f"quick_{i}")
        btn_manual = types.InlineKeyboardButton(f"Manual {i}", callback_data=f"manual_{i}")
        markup.add(btn_quick, btn_manual)

    bot.send_message(call.message.chat.id, "Select your ticket type (Quick or Manual):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("quick_"))
def quick_select_ticket(call):
    user_id = call.from_user.id
    ticket_number = int(call.data.split("_")[1])

    # Kiểm tra nếu người chơi đã chọn đủ vé
    if len(user_data[user_id]['tickets']) >= user_data[user_id]['quantity']:
        bot.send_message(call.message.chat.id, "You have already selected the maximum of 10 tickets.")
        return

    # Tạo vé ngẫu nhiên duy nhất
    main_numbers = sorted(random.sample(range(1, 69), 5))  # Chỉnh lại phạm vi 1-69
    mega_ball = random.randint(1, 26)
    formatted_ticket = f"{','.join(map(str, main_numbers))};{mega_ball}"

    # Thêm vé vào danh sách vé của người dùng
    user_data[user_id]['tickets'].append(formatted_ticket)

    bot.send_message(call.message.chat.id, f"Ticket {ticket_number} (Quick): {formatted_ticket}")

    # Thông báo khi đã chọn đủ vé
    if len(user_data[user_id]['tickets']) == user_data[user_id]['quantity']:
        bot.send_message(call.message.chat.id, f"You have selected all {user_data[user_id]['quantity']} tickets.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("manual_"))
def manual_select_ticket(call):
    user_id = call.from_user.id
    ticket_number = int(call.data.split("_")[1])

    # Kiểm tra nếu người chơi đã chọn đủ vé
    if len(user_data[user_id]['tickets']) >= user_data[user_id]['quantity']:
        bot.send_message(call.message.chat.id, "You have already selected the maximum of 10 tickets.")
        return

    # Hỏi người dùng nhập vé thủ công
    bot.send_message(call.message.chat.id, f"Ticket {ticket_number}: Please enter 5 numbers from 1 to 69 separated by commas, followed by a Mega Ball number from 1 to 26 (e.g., 5,12,23,34,45;8).")

@bot.message_handler(func=lambda message: ";" in message.text)
def handle_manual_ticket(message):
    user_id = message.from_user.id
    if user_id not in user_data or 'tickets' not in user_data[user_id]:
        user_data[user_id] = {'tickets': [], 'quantity': 10}

    try:
        parts = message.text.split(";")
        main_numbers = list(map(int, parts[0].split(",")))
        mega_ball = int(parts[1])

        if len(main_numbers) == 5 and all(1 <= n <= 69 for n in main_numbers) and 1 <= mega_ball <= 26:
            formatted_ticket = f"{','.join(map(str, main_numbers))};{mega_ball}"
            user_data[user_id]['tickets'].append(formatted_ticket)
            bot.reply_to(message, f"Ticket (Manual): {formatted_ticket}")
            
            # Kiểm tra nếu đã chọn đủ vé
            if len(user_data[user_id]['tickets']) >= user_data[user_id]['quantity']:
                bot.send_message(message.chat.id, f"You have selected all {user_data[user_id]['quantity']} tickets.")
        else:
            bot.reply_to(message, "Invalid numbers. Please enter 5 numbers from 1 to 69 and a Mega Ball from 1 to 26.")
    except ValueError:
        bot.reply_to(message, "Please enter valid numbers in the format: 5,12,23,34,45;8")

@bot.callback_query_handler(func=lambda call: call.data == "pay")
def handle_payment(call):
    user_id = call.from_user.id
    ticket_count = len(user_data.get(user_id, {}).get('tickets', []))
    
    if ticket_count == 0:
        bot.send_message(call.message.chat.id, "You haven't selected any tickets yet. Please choose your tickets first.")
    else:
        total_froll = (ticket_price_usd * ticket_count) / current_froll_price
        memo = f"Tickets: {', '.join(user_data[user_id]['tickets'])}, Time:
