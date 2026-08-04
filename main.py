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
        bot.send_message(ADMIN_ID, f"🤖 [FunPay Bot]\n{text}")
    except Exception as e:
        print("Ошибка Telegram:", e)


def funpay_worker():

    proxy = None

    if PROXY_URL:
        proxy = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }

    try:
        account = Account(
            GOLDEN_KEY,
            proxy=proxy
        ).get()

        print("АККАУНТ:", account.username)

        send_alert(
            f"✅ Бот запущен\n{account.username}"
        )

    except Exception as e:
        print("Ошибка входа:", repr(e))
        return


    try:
        print("=== CATEGORY DEBUG ===")

        categories = account.get_sorted_categories()

        print("TYPE:")
        print(type(categories))

        print("DIR:")
        print(dir(categories))

        print("REPR:")
        print(repr(categories))

        print("=== END DEBUG ===")

        send_alert(
            "Категории проверены, смотри Render."
        )

    except Exception as e:
        print("ОШИБКА:")
        print(repr(e))


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":

    threading.Thread(
        target=funpay_worker,
        daemon=True
    ).start()

    port = int(os.getenv("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    server.serve_forever()
