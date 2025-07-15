import logging
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from telegram.ext import Updater, MessageHandler, Filters

# === НАЛАШТУВАННЯ ===
TELEGRAM_TOKEN = '7838331561:AAGHYpG3aBKw6tG3M3A4CfqCf1pqIYkDCeU'
SPREADSHEET_ID = '1yMR1EyWs-C2D2N-G4caRY5YagMEsWDSopg4HecTVyMw'
SHEET_NAME = 'Лист1'

# Авторизація Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === ФУНКЦІЯ ПАРСИНГУ ===
def parse_hours(text):
    pattern = r'(\d+[.,]?\d*)\s*(год|годин|h)?'
    match = re.search(pattern, text, re.IGNORECASE)
    hours = float(match.group(1).replace(',', '.')) if match else None
    return hours

# === ОБРОБКА ПОВІДОМЛЕНЬ ===
def handle_message(update, context):
    message = update.message
    if message and message.text and message.is_topic_message:
        name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
        text = message.text
        hours = parse_hours(text)
        date = datetime.now().strftime('%d.%m.%Y')

        if hours:
            sheet.append_row([date, name, hours, text])
            logging.info(f"✅ Додано: {name}, {hours} год.")
        else:
            logging.info("⚠️ Не вдалось знайти години у повідомленні.")

# === ЗАПУСК БОТА ===
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & Filters.group, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()