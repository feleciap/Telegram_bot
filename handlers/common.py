from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.helpers import is_admin

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"Привет, {user.first_name}! Что делаем?"

    keyboard = [
        [InlineKeyboardButton("Добавить отзыв", callback_data="add_review")],
        [InlineKeyboardButton("Посмотреть отзывы", callback_data="view_reviews")],
        [InlineKeyboardButton("Поиск имени", callback_data="search_name")]
    ]

    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("Показать все имена (админ)", callback_data="list_names")])
        keyboard.append([InlineKeyboardButton("Добавить/обновить информацию (админ)", callback_data="add_info")])
        keyboard.append([InlineKeyboardButton("Просмотр отзывов (админ)", callback_data="admin_view_reviews")])

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "add_review":
        from handlers.reviews import start_add_review
        return await start_add_review(update, context)
    elif data == "view_reviews":
        from handlers.reviews import view_reviews
        return await view_reviews(update, context)
    elif data == "search_name":
        from handlers.names import ask_name_search
        return await ask_name_search(update, context)
    elif data in ("list_names", "add_info", "admin_view_reviews"):
        from handlers.admin import admin_router
        return await admin_router(update, context)
