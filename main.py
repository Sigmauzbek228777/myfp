import os
import time
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
        print("Ошибка Telegram:", e)


def funpay_worker():

    print("Запуск FunPay...", flush=True)

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
            f"Вход: {account.username}",
            flush=True
        )

        send_alert(
            f"✅ Бот запущен\n"
            f"Аккаунт: {account.username}"
        )

    except Exception as e:
        send_alert(
            f"❌ Ошибка входа:\n{repr(e)}"
        )
        return


    while True:

        try:
            print("Получаем категории...", flush=True)

            categories = account.get_sorted_categories()

            category_ids = list(categories.keys())

            print(
                f"Найдено категорий: {len(category_ids)}",
                flush=True
            )


            success = 0


            for category_id in category_ids:

                try:
                    account.raise_lots(category_id)

                    print(
                        f"Поднята категория {category_id}",
                        flush=True
                    )

                    success += 1

                except Exception as e:
                    print(
                        f"Ошибка категории {category_id}: {e}",
                        flush=True
                    )


            send_alert(
                f"✅ Поднятие завершено\n"
                f"Успешно: {success}/{len(category_ids)}"
            )


            print(
                "Ждем 4 часа...",
                flush=True
            )

            time.sleep(14400)


        except Exception as e:

            print(
                "Ошибка цикла:",
                repr(e),
                flush=True
            )

            send_alert(
                f"⚠ Ошибка цикла:\n{repr(e)}"
            )

            time.sleep(60)



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

    threading.Thread(
        target=funpay_worker,
        daemon=True
    ).start()


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
        "Web server started",
        flush=True
    )


    server.serve_forever()
