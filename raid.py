import os
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread

# API tokens for bots
API_TOKENS = [
    '7274292874:AAE95eVX0BE3LyECLELa7VE5_oA9JXJMDzM',
    '7513832134:AAH-J3ZxQojb_VdZNW-Xgw0PKBSB2wPX6tM',
    '7202346355:AAGBgVYB2svyQgboCWO6TmwxLV4k_9yq4wI',
    '6745752993:AAHdggLwLO_gBpY8-YkzupdXYQRxjqPTDWo',
    '7513768736:AAE9Z4IVoDwT9RwNXBbmXEYFOoX3GXy_RiU',
    '7424700585:AAFvFK56XF77Lj78c-tzJUpnMN4aVhyiTes',
    '7045462494:AAH2umwnaF12UFBxwh8sBByt1RMOSRBbYIw',
    '6942028585:AAEoK0JpC187XRYEiwJX4dx688jcBcoT5y4',
    '7430127221:AAG3qOqe3j9SbYFvhbWGS7Y_ACprqopOEU8',
    '7352686451:AAEmwKY9dbEBr5tf5b_NyJhN8oskFqzylYM',
    

    
]


# Initialize bots
bots = [telebot.TeleBot(token) for token in API_TOKENS]

# Telegram chat ID
CHAT_ID = '-1002217780167'

# Your Telegram username and group link
USERNAME = "raoxc"
GROUP_LINK = "https://t.me/raoxc_gc"

# RAID messages
RAID_MESSAGES = [
    "😭",
    "🤣",
    "😡",
    "😅",
]

# Control variable for stopping messages
stop_flags = [False] * len(bots)

# Function to send starting message
def send_starting_message(bot):
    photo_url = 'https://telegra.ph/file/9fdec96f8f340b8946845.jpg'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Contact Us", url=f"https://t.me/{USERNAME}")
    button2 = InlineKeyboardButton("Join Our Group", url=GROUP_LINK)
    markup.add(button1, button2)
    
    try:
        bot.send_photo(CHAT_ID, photo=photo_url, caption="Click one of the buttons below for more info:", reply_markup=markup)
        print("Starting message sent successfully.")
    except Exception as e:
        print(f"Error sending starting message: {e}")

# Function to send RAID messages
def send_raid_messages(bot, index):
    while not stop_flags[index]:
        try:
            for message in RAID_MESSAGES:
                if stop_flags[index]:
                    break
                bot.send_message(CHAT_ID, message)
                time.sleep(0.1)  # Adjust sleep time as needed
            time.sleep(1)  # Adjust sleep time as needed
        except Exception as e:
            print(f"Error with bot {index}: {e}")
            time.sleep(5)

# Start RAID
def start_raid():
    for index, bot in enumerate(bots):
        stop_flags[index] = False
        Thread(target=send_raid_messages, args=(bot, index)).start()

# Stop RAID
def stop_raid():
    for index in range(len(bots)):
        stop_flags[index] = True

# Function to send messages
def send_messages(bot, index, count, message_id=None, text_message=None):
    for _ in range(count):
        if stop_flags[index]:
            break
        try:
            if message_id:
                bot.send_sticker(CHAT_ID, message_id)
            elif text_message:
                bot.send_message(CHAT_ID, text_message)
            else:
                bot.send_message(CHAT_ID, "No message or sticker ID provided.")
            time.sleep(0.1)  # Adjust as needed
        except telebot.apihelper.ApiException as e:
            if e.error_code == 429:
                print(f"Rate limit reached for bot {index}. Retrying...")
                time.sleep(5)
            else:
                print(f"Error with bot {index}: {e}")
                time.sleep(5)

# Function to handle spam command
def start_sending_messages(message, bot, index):
    stop_flags[index] = False
    try:
        parts = message.text.split(' ', 2)
        count = int(parts[1])
        message_id = None
        text_message = None

        if message.reply_to_message:
            if message.reply_to_message.sticker:
                message_id = message.reply_to_message.sticker.file_id
            else:
                text_message = message.reply_to_message.text
        elif len(parts) > 2:
            if parts[2].startswith('sticker_'):
                message_id = parts[2]
            else:
                text_message = parts[2]

        thread = Thread(target=send_messages, args=(bot, index, count, message_id, text_message))
        thread.start()
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Usage: /spam <count> <message or reply to a sticker>")

# Command handlers
def handle_commands(bot, index):
    @bot.message_handler(commands=['alive'])
    def alive_command_handler(message):
        send_starting_message(bot)

    @bot.message_handler(commands=['start_raid'])
    def start_raid_handler(message):
        start_raid()
        bot.send_message(message.chat.id, "✅ RAID Activated")

    @bot.message_handler(commands=['stop_raid'])
    def stop_raid_handler(message):
        stop_raid()
        bot.send_message(message.chat.id, "✅ RAID De-Activated")

    @bot.message_handler(commands=['spam'])
    def start_message_handler(message):
        start_sending_messages(message, bot, index)

    @bot.message_handler(commands=['stop'])
    def stop_message_handler(message):
        stop_flags[index] = True

# Start the bot threads
def setup_bot(bot, index):
    handle_commands(bot)  # Set command handlers
    send_starting_message(bot)  # Send starting message
    bot.polling(none_stop=True)

# Start all bot threads
threads = []
for index, bot in enumerate(bots):
    thread = Thread(target=setup_bot, args=(bot, index))
    thread.start()
    threads.append(thread)

# Wait for all bot threads to finish
for thread in threads:
    thread.join()
