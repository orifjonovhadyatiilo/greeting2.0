import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-bot-name.onrender.com

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# 👋 Yangi a'zoga javob
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"👋 Salom, {user.full_name}! Guruhimizga xush kelibsiz!")

telegram_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))


@flask_app.route("/")
def home():
    return "Bot ishlayapti!"

@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

if __name__ == "__main__":
    import asyncio
    from telegram import Bot

    # Flask portni ochamiz
    port = int(os.environ.get("PORT", 10000))
    
    # Webhookni sozlash
    bot = Bot(token="7395563447:AAEN5xQTNdO1h736ExIhKualN2bwgebXDKA")
    asyncio.run(bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))

    flask_app.run(host="0.0.0.0", port=port)
