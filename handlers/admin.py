from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db import SessionLocal
from models import Name, Review
from utils.helpers import is_admin

def register_handlers(app):
    pass  # админские кнопки вызываются через common.menu_router

async def admin_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if not is_admin(user_id):
        await query.message.reply_text("⛔ Доступ только для администратора.")
        return

    if query.data == "list_names":
        await list_all_names(update, context)
    elif query.data == "add_info":
        from handlers.names import add_or_update_name
        await add_or_update_name(update, context)
    elif query.data == "admin_view_reviews":
        await admin_view_reviews(update, context)

async def list_all_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        names = db.query(Name).all()
    if not names:
        await update.callback_query.message.reply_text("Нет сохранённых имён.")
        return

    msg = "📜 Список имён:\n\n" + "\n".join([n.name for n in names])
    await update.callback_query.message.reply_text(msg)

async def admin_view_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        reviews = db.query(Review).all()
    if not reviews:
        await update.callback_query.message.reply_text("Отзывов нет.")
        return

    for r in reviews:
        caption = f"ID: {r.id}\n👤 {r.username or 'Аноним'}\n🕒 {r.created_at.strftime('%Y-%m-%d %H:%M')}"
        if r.text:
            caption += f"\n\n{r.text}"

        buttons = [[InlineKeyboardButton("❌ Удалить", callback_data=f"del_review_{r.id}")]]
        markup = InlineKeyboardMarkup(buttons)

        if r.photo_file_id:
            await update.callback_query.message.reply_photo(photo=r.photo_file_id, caption=caption, reply_markup=markup)
        else:
            await update.callback_query.message.reply_text(caption, reply_markup=markup)
