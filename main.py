import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Flask ilovasini yaratish
app = Flask(__name__)

# Telegram botini yaratish
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

@app.route("/webhook", methods=["POST"])
async def webhook():
    # Telegram app ni initialize qilish (faqat birinchi marta chaqiriladi)
    if not telegram_app._initialized:
        await telegram_app.initialize()

    # Telegram update obyektini olish va yuborish
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok", 200

# Webhook URL ni o‘rnatish (faqat bir marta ishlaydi)
async def set_webhook():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print("✅ Webhook o‘rnatildi:", f"{WEBHOOK_URL}/webhook")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=10000)
