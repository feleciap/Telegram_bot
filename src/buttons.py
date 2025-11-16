from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='back')]])

def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Добавить", callback_data='add')],
        [InlineKeyboardButton("Обновить", callback_data='prepare_update')],
        [InlineKeyboardButton("Удалить", callback_data='delete')],
        [InlineKeyboardButton("Показать все имена", callback_data='show_all')],
        [InlineKeyboardButton("Показать комментарии", callback_data='show_comments')],
        [InlineKeyboardButton("Удалить отзыв", callback_data='delete_review')],
    ])

def guest_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Добавить отзыв", callback_data='add_review')],
        [InlineKeyboardButton("Показать отзывы", callback_data='show_reviews')],
        [InlineKeyboardButton("Оставить комментарий", callback_data='comment')],
    ])
