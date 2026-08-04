import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import telebot
from FunPayAPI import Account


TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GOLDEN_KEY = os.getenv("GOLDEN_KEY")
PROXY_URL = os.getenv("PROXY")

bot = telebot.TeleBot(TOKEN)


def send_alert(text):
    try:
        bot.send_message(
            ADMIN_ID,
            f"🤖 [FunPay Bot]\n{text}"
        )
    except Exception as e:
        print("Telegram error:", e)


def funpay_worker():
    print("=== THREAD START ===")

    try:
        proxy = None

        if PROXY_URL:
            proxy = {
                "http": PROXY_URL,
                "https": PROXY_URL
            }

        print("Создаем Account")

        account = Account(
            GOLDEN_KEY,
            proxy=proxy
        )

        print("Получаем аккаунт")

        account = account.get()

        print("АККАУНТ:", account.username)

        send_alert(
            f"✅ Вход успешен\n{account.username}"
        )


        print("Получаем категории")

        categories = account.get_sorted_categories()

        print("ТИП:", type(categories))
        print("КАТЕГОРИИ:", repr(categories))


        send_alert(
            "Категории получены. Смотри Render."
        )


    except Exception as e:
        print("=== ERROR ===")
        print(repr(e))
        send_alert(
            f"❌ Ошибка:\n{repr(e)}"
        )


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            b"Bot is running"
        )

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":

    print("MAIN START", flush=True)

    funpay_worker()

    port = int(os.getenv("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    print("WEB START", port, flush=True)

    server.serve_forever()
