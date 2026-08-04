import os
import time
import telebot
from FunPayAPI import Account

# Подтягиваем скрытые настройки из Render
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GOLDEN_KEY = os.getenv("GOLDEN_KEY")
PROXY_URL = os.getenv("PROXY")

bot = telebot.TeleBot(TOKEN)

# Настройка прокси для FunPay, если он указан
# (Для работы библиотеки FunPayAPI)
# Если прокси пустой, запросы пойдут напрямую через сервер
