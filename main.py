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


def send_alert(message):
    try:
        bot.send_message(
            ADMIN_ID,
            f"🤖 [FunPay Bot]\n{message}"
        )
    except Exception as e:
        print("Ошибка Telegram:", e)


def funpay_worker():
    print("Запуск FunPay бота...")

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

        print(
            f"Вход выполнен: {account.username}"
        )

        send_alert(
            f"✅ Бот запущен\n"
            f"Аккаунт: {account.username}"
        )

    except Exception as e:
        print("Ошибка входа:", e)

        send_alert(
            f"❌ Ошибка входа:\n{repr(e)}"
        )

        return


    # Диагностика поднятия лотов
    try:
        print("Проверка raise_modal...")

        modal = account.get_raise_modal()

        print("================")
        print(type(modal))
        print(repr(modal))
        print("================")

        send_alert(
            "✅ Проверка категорий завершена.\n"
            "Смотри логи Render."
        )

    except Exception as e:
        print("Ошибка get_raise_modal:")
        print(repr(e))

        send_alert(
            f"⚠ Ошибка получения категорий:\n{repr(e)}"
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

    thread = threading.Thread(
        target=funpay_worker,
        daemon=True
    )

    thread.start()


    port = int(
        os.getenv(
            "PORT",
            10000
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    print(
        f"Web server started on {port}"
    )

    server.serve_forever()
