import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater
import asyncio
import time
import schedule
from datetime import datetime
from threading import Thread
import os
from autotest.check_web import Check_Web
import pytz
from dotenv import load_dotenv
import os
load_dotenv()


class TeleBot:
    def __init__(self):
        self.TOKEN = os.getenv("TOKEN")
        self.CHAT_ID = os.getenv("CHAT_ID")
        self.BOT_USERNAME = os.getenv("BOT_USERNAME")
        self.job = None
        self.time_schedule = '13:15'
        self.minute_schedule = ':48'

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("I'm a bot, please talk to me!")

    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        random_number = datetime.now()
        message = f"`Now is {random_number}`"
        await update.message.reply_text(message)

    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.scheduled_job()

    #async def settime_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
    def handle_response(self, text: str) -> str:
        print('Handling response')
        if 'hello' in text.lower() or 'hi' in text.lower() or 'hey' in text.lower():
            return "Hi"
        else:
            return "I don't understand"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        schedule.cancel_job(self.job)
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(
            f"Received message: {update.message.chat.id} in {message_type} with text: {text}")
        if message_type == "private":
            response = self.handle_response(text)
        elif message_type == "group":
            if self.BOT_USERNAME in text:
                new_text = text.replace(self.BOT_USERNAME, "").strip()
                response = self.handle_response(new_text)
            else:
                return
        else:
            response = self.handle_response(text)
        print(f"Sending response: {response}")
        await update.message.reply_text(response)

    async def send_message(self, message):
        telegram_notify = telegram.Bot(self.TOKEN)
        await telegram_notify.send_message(chat_id=self.CHAT_ID, text=message, parse_mode='Markdown')

    async def scheduled_job(self):
        random_number = datetime.now()
        message = f"`Now is {random_number}`"
        await self.send_message(message)
        Check_Web_In = Check_Web()
        if (Check_Web_In.check_url()):
            noti = 'the website is still access normally'
        else:
            noti = 'the website is down'
        await self.send_message(noti)

        if (Check_Web_In.check_login()):
            noti = 'the login is still access normally'
        else:
            noti = 'the login is down'
        await self.send_message(noti)

        avg_time_upload, avg_average_time_visual, avg_hit_rate = Check_Web_In.check_visualize()
        if avg_average_time_visual:
            noti = f'Average time upload: {avg_time_upload}\nAverage time visualize: {avg_average_time_visual}\nHit rate: {avg_hit_rate}'
        else:
            noti = 'The website is down'
        await self.send_message(noti)

    def schedule_checker(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_async_function_sync(self, func):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func())

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused error {context.error}")

    def run(self):
        print('Starting bot')
        app = ApplicationBuilder().token(
            self.TOKEN).read_timeout(30).write_timeout(30).build()
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("random", self.random_command))
        app.add_handler(CommandHandler("check", self.check_command))
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        # schedule.every().hour.at(self.minute_schedule,'Asia/Ho_Chi_Minh').do(
        #     lambda: self.run_async_function_sync(self.scheduled_job))
        # schedule.every().day.at(self.time_schedule).do(
        #     lambda: self.run_async_function_sync(self.scheduled_job))
        schedule.every(10).minutes.do(lambda: self.run_async_function_sync(self.scheduled_job))
        Thread(target=self.schedule_checker).start()
        app.add_error_handler(self.error)
        app.run_polling()