import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
import random
import asyncio
import time
import schedule
from datetime import datetime, timedelta
from threading import Thread
# from dotenv import load_dotenv
# import os
# load_dotenv()



# TOKEN = os.getenv("TOKEN")
# CHAT_ID = os.getenv("CHAT_ID")
from typing import Final
TOKEN: Final = '6504368492:AAFi0KQ1AR4FmzWrpijgvItUlWoZ1YzNMLU'
CHAT_ID: Final = "1954699583"
BOT_USERNAME: Final = "datalace_bot"

# async def call():
#     try:
#         random_number = datetime.now()
#         telegram_notify = telegram.Bot(TOKEN)
#         message = f"`Now is {random_number}`"
#         await telegram_notify.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
#     except asyncio.TimeoutError as e:
#         print(f"Asyncio Timeout: {e}")
#     except telegram.error.TimedOut as e:
#         print(f"Telegram Timed out: {e}")
#     except Exception as e:
#         print(f"Error: {e}")


# async def send_message():
#     retries = 3
#     delay_between_retries = 10  # seconds

#     for attempt in range(retries):
#         try:
#             await call()
#             break
#         except telegram.error.TimedOut as e:
#             print(f"Timed out: {e}. Retrying (attempt {attempt + 1}/{retries})...")
#             # Exponential backoff: increase delay between retries
#             time.sleep(delay_between_retries * 2**attempt)
#         except Exception as e:
#             print(f"Error: {e}. Retrying (attempt {attempt + 1}/{retries})...")
#             time.sleep(delay_between_retries * 2**attempt)


# async def scheduled_task():
#     start_time = datetime(year=2024, month=3, day=4, hour=15, minute=44)
#     while True:
#         now = datetime.now()
#         if now >= start_time:
#             await send_message()
#             start_time += timedelta(minutes=1)
#         else:
#             time_until_start = start_time - now
#             await asyncio.sleep(time_until_start.total_seconds())


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot, please talk to me!")

async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_number = datetime.now()
    message = f"`Now is {random_number}`"
    await update.message.reply_text(message)

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global job
    job = schedule.every(1).seconds.do(lambda: run_async_function_sync(scheduled_job))
    
    Thread(target=schedule_checker).start() 

def handle_response(text: str) -> str:
    print('Handling response')
    if 'hello' in text.lower() or 'hi' in text.lower() or 'hey' in text.lower():
        return "Hi"
    else:
        return "I don't understand"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule.cancel_job(job)
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(
        f"Received message: {update.message.chat.id} in {message_type} with text: {text}")
    if message_type == "private":
        response = handle_response(text)
    elif message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
    print(f"Sending response: {response}")
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")



async def scheduled_job():
    random_number = datetime.now()
    telegram_notify = telegram.Bot(TOKEN)
    message = f"`Now is {random_number}`"
    await telegram_notify.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_async_function_sync(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func())
job = None
def main():
    print('Starting bot')
    app = ApplicationBuilder().token(TOKEN).read_timeout(30).write_timeout(30).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("check", check_command))
    # Update the filter here
    # app.add_handler(MessageHandler(filters.Dice.ALL, handle_message))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)
    app.run_polling()

if __name__ == "__main__":
    main()

