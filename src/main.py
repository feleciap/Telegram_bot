import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import TelegramError

from config import TOKEN, ADMIN_IDS
from buttons import admin_menu, guest_menu
from handlers import button_handler


# 🧹 Отключаем прокси (если окружение подкидывает)
for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(var, None)
os.environ["NO_PROXY"] = "*"


# 🪵 Настройка логирования
LOG_FORMAT = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("telegram_bot")


# 🚨 Обработчик ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("❌ Произошла ошибка при обработке апдейта", exc_info=context.error)
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text("⚠️ Произошла ошибка. Администратор уведомлен.")


# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Без имени"

    # Определяем роль
    context.user_data["role"] = "admin" if user_id in ADMIN_IDS else "guest"
    role = context.user_data["role"]

    logger.info(f"👤 Пользователь {username} (ID: {user_id}) вошёл как {role}")

    if role == "admin":
        text = "👑 Режим администратора активен."
        markup = admin_menu()
    else:
        text = "💬 Режим гостя активен."
        markup = guest_menu()

    await update.message.reply_text(text, reply_markup=markup)


# 🧠 Основная функция
def main():
    logger.info("🚀 Запуск Telegram-бота...")

    app = Application.builder().token(TOKEN).build()

    # 📦 Регистрируем хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    logger.info("✅ Бот успешно запущен и ожидает команды...")
    app.run_polling(stop_signals=None)  # Не прерывать при Ctrl+C в некоторых окружениях


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.warning("🛑 Бот остановлен пользователем.")
    except Exception as e:
        logger.exception("🔥 Критическая ошибка при запуске бота:")




# import os

# for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
#     os.environ.pop(var, None)

# os.environ["NO_PROXY"] = "*"

# from telegram import Update
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# from config import TOKEN, ADMIN_IDS
# from buttons import admin_menu, guest_menu
# from handlers import button_handler
# import logging
# from telegram.error import TelegramError


# logging.basicConfig(
#     format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler("bot.log", encoding="utf-8"),  # Лог в файл
#         logging.StreamHandler()  # Лог в консоль
#     ]
# )

# logger = logging.getLogger(__name__)


# async def error_handler(update, context):
#     logger.error(msg="Произошла ошибка при обработке апдейта:", exc_info=context.error)



# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     context.user_data['role'] = 'admin' if user_id in ADMIN_IDS else 'guest'

#     if context.user_data['role'] == 'admin':
#         text = "👑 Режим администратора активен."
#         markup = admin_menu()
#     else:
#         text = "💬 Режим гостя активен."
#         markup = guest_menu()

#     await update.message.reply_text(text, reply_markup=markup)


# def main():
#     app = Application.builder().token(TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(button_handler))

#     print("✅ Бот запущен")
#     app.run_polling()


# if __name__ == "__main__":
#     main()

# application.add_error_handler(error_handler)
