import requests
from fastapi import FastAPI, Request, Response
import os

app = FastAPI()

# --- Configuration ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Get from environment variable
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# --- Hardcoded responses ---
RESPONSES = {
    "/start": "👋 Hello! Welcome! I'm a simple bot with hardcoded responses.",
    "/help": "🤖 I respond to a fixed set of commands:\n/start - Welcome message\n/help - Show this help\n/about - About this bot",
    "/about": "📌 This is a simple Telegram bot built with FastAPI and no telegram libraries.",
}
DEFAULT_RESPONSE = "🤷 I don't understand that. Try /help to see available commands."


def send_message(chat_id: int, text: str):
    """Send a message back to the Telegram user."""
    try:
        response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=30
        )
        if response.status_code == 200:
            print(f"✅ Sent message to {chat_id}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Receive updates from Telegram via webhook."""
    try:
        data = await request.json()
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()

        print(f"📩 Received: '{text}' from {chat_id}")

        if chat_id and text:
            response_text = RESPONSES.get(text, DEFAULT_RESPONSE)
            send_message(chat_id, response_text)

        return Response(status_code=200)
    except Exception as e:
        print(f"❌ Error: {e}")
        return Response(status_code=200)


@app.get("/")
async def root():
    return {"status": "Bot is running"}