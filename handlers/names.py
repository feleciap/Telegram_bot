from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler
from db import SessionLocal
from models import Name
from datetime import datetime
from utils.helpers import is_admin

ASK_NAME, ASK_NEW_INFO = range(2)

def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_name))

async def ask_name_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Введите имя для поиска:")
    return ASK_NAME

async def search_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_query = update.message.text.strip()
    with SessionLocal() as db:
        person = db.query(Name).filter(Name.name.ilike(f"%{name_query}%")).first()
    if person:
        msg = f"📋 Имя: {person.name}\n\nИнформация: {person.info}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Имя не найдено 😕")

async def add_or_update_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Только админ может обновлять информацию.")
        return

    await update.message.reply_text("Введите имя:")
    return ASK_NAME

async def ask_new_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["name_to_update"] = name
    await update.message.reply_text("Введите новую информацию:")
    return ASK_NEW_INFO

async def save_new_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_info = update.message.text.strip()
    name_value = context.user_data.get("name_to_update")

    with SessionLocal() as db:
        person = db.query(Name).filter(Name.name == name_value).first()
        if person:
            old_info = person.info or ""
            person.info = f"{old_info}\n\n🕒 {datetime.utcnow()}: {new_info}"
            person.updated_at = datetime.utcnow()
        else:
            person = Name(name=name_value, info=new_info)
            db.add(person)
        db.commit()

    await update.message.reply_text("Информация обновлена ✅")
    return ConversationHandler.END
