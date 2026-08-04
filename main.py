import os
import time
import requests
import telebot
from FunPayAPI import Account

# Подтягиваем скрытые настройки из Render
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GOLDEN_KEY = os.getenv("GOLDEN_KEY")
PROXY_URL = os.getenv("PROXY")

bot = telebot.TeleBot(TOKEN)

# Функция для отправки уведомлений в Telegram хозяину
def send_alert(message):
    try:
        bot.send_message(ADMIN_ID, f"🤖 [FunPay Bot]: {message}")
    except Exception as e:
        print(f"Ошибка отправки в TG: {e}")

def main():
    print("Бот запускается...")
    
    # Настройка прокси, если он указан в Render
    proxies = None
    if PROXY_URL:
        proxies = {"http": PROXY_URL, "https": PROXY_URL}
        print("Используется прокси.")

    try:
        # Авторизуемся на FunPay
        # Передаем прокси в сессию, если они есть
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies)
            
        account = Account(GOLDEN_KEY, session=session).get()
        print(f"Успешный вход! Аккаунт: {account.username}")
        send_alert(f"Бот успешно запущен для аккаунта {account.username}!")
    except Exception as e:
        print(f"Ошибка авторизации FunPay: {e}")
        send_alert(f"Ошибка входа на FunPay! Проверь GOLDEN_KEY. Ошибка: {e}")
        return

    # Цикл автоподнятия лотов (каждые 4 часа)
    while True:
        try:
            account.raise_lots()
            print("Лоты успешно подняты!")
            send_alert("Лоты на FunPay успешно подняты!")
            time.sleep(14400) # Ждем 4 часа
        except Exception as e:
            print(f"Ошибка при поднятии лотов: {e}")
            send_alert(f"Внимание! Ошибка при поднятии лотов: {e}")
            time.sleep(60) # Если интернет моргнул, пробуем через минуту

if __name__ == "__main__":
    # Запускаем логику в фоновом режиме, чтобы Render не ругался на отсутствие веб-порта
    import threading
    t = threading.Thread(target=main)
    t.daemon = True
    t.start()
    
    # Заглушка для Render, чтобы бесплатный Web Service думал, что это сайт
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running!")
    
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()
