from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler, CommandHandler
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Review
from utils.helpers import is_admin

ADD_REVIEW_TEXT, ADD_REVIEW_PHOTO = range(2)

def register_handlers(app):
    app.add_handler(CommandHandler("reviews", view_reviews))

    add_review_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, start_add_review)],
        states={
            ADD_REVIEW_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_review_text)],
            ADD_REVIEW_PHOTO: [MessageHandler(filters.PHOTO, save_review_photo)],
        },
        fallbacks=[],
    )
    app.add_handler(add_review_conv)

async def start_add_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Отправь текст отзыва или фото (можно без текста).")
    return ADD_REVIEW_TEXT

async def save_review_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    with SessionLocal() as db:
        review = Review(telegram_user_id=str(user.id), username=user.username, text=text)
        db.add(review)
        db.commit()
    await update.message.reply_text("Спасибо! Отзыв сохранён ✅")
    return ConversationHandler.END

async def save_review_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file_id = update.message.photo[-1].file_id
    with SessionLocal() as db:
        review = Review(telegram_user_id=str(user.id), username=user.username, photo_file_id=file_id)
        db.add(review)
        db.commit()
    await update.message.reply_text("Фото-отзыв сохранён 📸")
    return ConversationHandler.END

async def view_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    with SessionLocal() as db:
        reviews = db.query(Review).all() if is_admin(user.id) else db.query(Review).filter(Review.visible_to_guests == True).all()

    if not reviews:
        await update.callback_query.message.reply_text("Отзывов пока нет.")
        return

    for r in reviews:
        msg = f"👤 {r.username or 'Аноним'}\n🕒 {r.created_at.strftime('%Y-%m-%d %H:%M')}"
        if r.text:
            msg += f"\n\n{r.text}"
        if r.photo_file_id:
            await update.callback_query.message.reply_photo(photo=r.photo_file_id, caption=msg)
        else:
            await update.callback_query.message.reply_text(msg)

async def delete_review(update: Update, context: ContextTypes.DEFAULT_TYPE, review_id: int):
    with SessionLocal() as db:
        db.query(Review).filter(Review.id == review_id).delete()
        db.commit()
    await update.callback_query.message.reply_text("Отзыв удалён ❌")
