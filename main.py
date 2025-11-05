import os

for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(var, None)

os.environ["NO_PROXY"] = "*"

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import TOKEN
from handlers import common, reviews, names, admin


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Старт
    app.add_handler(CommandHandler("start", common.start))

    # Главное меню
    app.add_handler(CallbackQueryHandler(common.menu_router))

    # Отзывы
    reviews.register_handlers(app)

    # Имена
    names.register_handlers(app)

    # Админ
    admin.register_handlers(app)

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
