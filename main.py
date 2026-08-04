import os
import time
import telebot
from FunPayAPI import Account
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GOLDEN_KEY = os.getenv("GOLDEN_KEY")
PROXY_URL = os.getenv("PROXY")

bot = telebot.TeleBot(TOKEN)


def send_alert(text):
    try:
        bot.send_message(ADMIN_ID, f"🤖 [FunPay Bot]\n{text}")
    except Exception as e:
        print(f"Ошибка Telegram: {e}")


def main():
    print("Запуск бота...")

    proxy = None
    if PROXY_URL:
        proxy = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        print("Используется прокси.")

    try:
        account = Account(
            GOLDEN_KEY,
            proxy=proxy
        ).get()

        print(f"Вход выполнен: {account.username}")
        send_alert(f"✅ Бот запущен.\nАккаунт: {account.username}")

    except Exception as e:
        print(e)
        send_alert(f"❌ Ошибка входа:\n{e}")
        return

   while True:
    try:
        print(account.categories)

        send_alert("Категории выведены в лог.")

        break

    except Exception as e:
        print(e)
        send_alert(f"⚠ Ошибка:\n{e}")

        break


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()

    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()
