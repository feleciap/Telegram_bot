import logging
import asyncio
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_TOKEN = '7323246474:AAGHhnVM5Ah9l3tDsU9D3HD9TGSArKwf6Fs'
ADMIN_PASSWORD = '123'  # Замените на ваш пароль

# Подключение к базе данных
conn = sqlite3.connect('people.db', check_same_thread=False)
c = conn.cursor()

# Обновление схемы базы данных
  
def update_db_schema():
    try:
        c.execute("PRAGMA table_info(people)")
        columns = [column[1] for column in c.fetchall()]
        if 'comment' not in columns:
            c.execute("ALTER TABLE people ADD COLUMN comment TEXT")
        if 'review' not in columns:
            c.execute("ALTER TABLE people ADD COLUMN review TEXT")
        if 'review_photo' not in columns:
            c.execute("ALTER TABLE people ADD COLUMN review_photo TEXT")  # Новый столбец для фото
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при обновлении схемы базы данных: {e}")
update_db_schema()

# Функции для создания клавиатур
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Показать все имена", callback_data='show_all')],
        [InlineKeyboardButton("Добавить ученика", callback_data='add')],
        [InlineKeyboardButton("Обновить информацию", callback_data='prepare_update')],
        [InlineKeyboardButton("Удалить ученика", callback_data='delete')],
        [InlineKeyboardButton("Поиск ученика", callback_data='search')],
        [InlineKeyboardButton("Показать комментарии", callback_data='show_comments')],
        [InlineKeyboardButton("Удалить отзыв", callback_data='delete_review')] 

    ]
    return InlineKeyboardMarkup(keyboard)

def guest_menu():
    keyboard = [
        [InlineKeyboardButton("Поиск ученика", callback_data='search')],
        [InlineKeyboardButton("Добавить комментарий", callback_data='comment')],
        [InlineKeyboardButton("Добавить отзыв", callback_data='add_review')],
        [InlineKeyboardButton("Показать все отзывы", callback_data='show_reviews')]
    ]
    return InlineKeyboardMarkup(keyboard)

def role_menu():
    keyboard = [
        [InlineKeyboardButton("Админ", callback_data='admin')],
        [InlineKeyboardButton("Гость", callback_data='guest')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
    return InlineKeyboardMarkup(keyboard)



# Обработчики команд
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Выберите роль:", reply_markup=role_menu())

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    action = query.data

    logging.info(f"Действие пользователя: {action}")

    if action == 'admin':
        await query.edit_message_text(text="Введите пароль для входа в режим администратора.")
        context.user_data['action'] = 'check_password'

    elif action == 'guest':
        context.user_data['role'] = 'guest'
        await query.edit_message_text(text="Вы вошли как гость. Выберите действие:", reply_markup=guest_menu())

    elif 'role' not in context.user_data:
        await query.edit_message_text(text="Сначала выберите роль.", reply_markup=role_menu())

    elif action == 'add' and context.user_data['role'] == 'admin':
        await query.edit_message_text(text="Отправьте имя и информацию в формате: 'Имя, информация'.", reply_markup=back_button())
        context.user_data['action'] = 'add'

    elif action == 'prepare_update' and context.user_data['role'] == 'admin':
        await query.edit_message_text(text="Отправьте имя и новую информацию в формате: 'Имя, информация'.", reply_markup=back_button())
        context.user_data['action'] = 'prepare_update'

    elif action == 'delete' and context.user_data['role'] == 'admin':
        await query.edit_message_text(text="Отправьте имя для удаления.", reply_markup=back_button())
        context.user_data['action'] = 'delete'

    elif action == 'show_all' and context.user_data['role'] == 'admin':
        names = await get_all_names_from_db()
        if names:
            await query.edit_message_text(text="Зарегистрированные имена:\n" + "\n".join(names), reply_markup=back_button())
        else:
            await query.edit_message_text(text="Нет зарегистрированных имен.", reply_markup=back_button())

    elif action == 'search':
        await query.edit_message_text(text="Отправьте имя для поиска информации.", reply_markup=back_button())
        context.user_data['action'] = 'search'

    elif action == 'comment' and context.user_data['role'] == 'guest':
        await query.edit_message_text(text="Отправьте имя и комментарий в формате: 'Имя, комментарий'.", reply_markup=back_button())
        context.user_data['action'] = 'comment'

    elif action == 'add_review' :
        await query.edit_message_text(text="Отправьте имя и отзыв в формате: 'Имя, отзыв'.", reply_markup=back_button())
        context.user_data['action'] = 'add_review'

    elif action == 'show_reviews' and context.user_data['role'] == 'guest':
        reviews = await get_all_reviews_from_db()
        if reviews:
            await query.edit_message_text(text="Отзывы:\n" + "\n".join(reviews), reply_markup=back_button())
        else:
            await query.edit_message_text(text="Нет отзывов.", reply_markup=back_button())

    elif action == 'show_comments' and context.user_data['role'] == 'admin':
        comments = await get_all_comments_from_db()
        if comments:
            await query.edit_message_text(text="Комментарии:\n" + "\n".join(comments), reply_markup=back_button())
        else:
            await query.edit_message_text(text="Нет комментариев.", reply_markup=back_button())
    
    elif action == 'delete_review' and context.user_data['role'] == 'admin':
        await query.edit_message_text(text="Отправьте имя для удаления отзыва.", reply_markup=back_button())
        context.user_data['action'] = 'delete_review'


    elif action == 'back':
        # Вернуть в меню в зависимости от роли пользователя
        if context.user_data.get('role') == 'admin':
            await query.edit_message_text(text="Выберите действие:", reply_markup=main_menu())
        elif context.user_data.get('role') == 'guest':
            await query.edit_message_text(text="Выберите действие:", reply_markup=guest_menu())


# Асинхронные функции для работы с базой данных
async def get_all_names_from_db():
    async with asyncio.Lock():
        c.execute("SELECT name FROM people")
        result = c.fetchall()
        return [row[0] for row in result]

async def get_all_comments_from_db():
    async with asyncio.Lock():
        c.execute("SELECT name, comment FROM people WHERE comment IS NOT NULL AND comment != ''")
        result = c.fetchall()
        return [f"{row[0]}: {row[1]}" for row in result]

async def get_all_reviews_from_db():
    async with asyncio.Lock():
        c.execute("SELECT name, review, review_photo FROM people WHERE review IS NOT NULL AND review != ''")
        result = c.fetchall()
        reviews = []
        for row in result:
            name, review, review_photo = row
            review_text = f"{name}: {review}"
            if review_photo:
                review_text += f"\nФото: {review_photo}"  # Отображаем идентификатор фото
            reviews.append(review_text)
        return reviews

async def add_person_to_db(name, info):
    async with asyncio.Lock():
        c.execute("INSERT INTO people (name, info, comment, review) VALUES (?, ?, '', '')", (name, info))
        conn.commit()

async def update_person_info(name, new_info):
    async with asyncio.Lock():
        c.execute("SELECT info FROM people WHERE name=?", (name,))
        old_info = c.fetchone()
        if old_info:
            old_info = old_info[0]
            c.execute("UPDATE people SET info=? WHERE name=?", (new_info, name))
            conn.commit()
            return old_info
        return None

async def delete_person_from_db(name):
    async with asyncio.Lock():
        c.execute("DELETE FROM people WHERE name=?", (name,))
        conn.commit()

async def search_person_in_db(name):
    async with asyncio.Lock():
        c.execute("SELECT name, info FROM people WHERE name=?", (name,))
        return c.fetchone()

async def add_comment_to_person(name, comment):
    async with asyncio.Lock():
        c.execute("UPDATE people SET comment=? WHERE name=?", (comment, name))
        conn.commit()

async def delete_review_from_person(name):
    async with asyncio.Lock():
        c.execute("UPDATE people SET review='', review_photo='' WHERE name=?", (name,))
        conn.commit()

# Обновляем функцию для добавления отзыва (включая возможность только с фото)
async def add_review_to_person(name, review=None, photo=None):
    async with asyncio.Lock():
        # Проверяем, есть ли уже отзыв для этого человека
        c.execute("SELECT review FROM people WHERE name=?", (name,))
        result = c.fetchone()

        if result:
            # Если отзыв уже есть, добавляем новый к старому
            existing_review = result[0]
            if review:
                updated_review = existing_review + "\n" + review
            else:
                updated_review = existing_review
        else:
            # Если человека нет в базе, сохраняем отзыв, но не добавляем его в список имен
            updated_review = review if review else ""
            # Здесь добавляем только отзыв или фото, но не добавляем его в таблицу "Показать все имена"
            c.execute("INSERT INTO people (name, review, review_photo) VALUES (?, ?, ?)", (name, updated_review, photo))

        # Если прикреплено фото, сохраняем ссылку на него в базе
        if photo:
            updated_review += f"\n[Фото]({photo})"

        c.execute("UPDATE people SET review=?, review_photo=? WHERE name=?", (updated_review, photo, name))
        conn.commit()

# Обработка сообщений от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    action = context.user_data.get('action')

    try:
        # Проверка действия для отзывов
        if action == 'add_review':
            name, review = None, None
            if update.message.photo:
                # Если отправлено фото
                file = await update.message.photo[-1].get_file()
                photo_url = file.file_path

                # Если есть текст, он будет добавлен вместе с фото
                if user_input:
                    review = user_input

                # Имя пользователя как ключ для отзыва
                name = update.message.from_user.full_name

                # Добавляем отзыв с фото
                await add_review_to_person(name, review=review, photo=photo_url)
                await update.message.reply_text(f"Ваш отзыв добавлен с фото.")
            elif user_input:
                # Если только текст
                name, review = map(str.strip, user_input.split(',', 1))
                await add_review_to_person(name, review=review)
                await update.message.reply_text(f"Ваш текстовый отзыв добавлен.")

        context.user_data['action'] = None  # Сброс действия после выполнения
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

async def add_review_photo_to_person(name, photo_file_id):
    async with asyncio.Lock():
        c.execute("UPDATE people SET review_photo=? WHERE name=?", (photo_file_id, name))
        conn.commit()

# Обработка сообщений от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    action = context.user_data.get('action')

    try:
        # Проверка действия
        if action == 'check_password':
            await check_password(update, context)
            return

        if action == 'search':
            name = user_input.strip()
            person_info = await search_person_in_db(name)

            if person_info:
                info_message = f"Имя: {person_info[0]}\nИнформация: {person_info[1]}"
            else:
                info_message = "Имя не найдено."
            
            await update.message.reply_text(info_message, reply_markup=back_button())

        elif action == 'add':
            name, info = map(str.strip, user_input.split(',', 1))
            await add_person_to_db(name, info)
            await update.message.reply_text(f"Добавлена информация для {name}.", reply_markup=back_button())

        elif action == 'prepare_update':
            name, new_info = map(str.strip, user_input.split(',', 1))
            old_info = await update_person_info(name, new_info)
            if old_info:
                info_message = f"Информация для {name} обновлена. Старая информация: {old_info}"
            else:
                info_message = f"Имя {name} не найдено."
            
            await update.message.reply_text(info_message, reply_markup=back_button())

        elif action == 'delete':
            name = user_input.strip()
            await delete_person_from_db(name)
            await update.message.reply_text(f"Удалено имя {name}.", reply_markup=back_button())

        elif action == 'comment':
            name, comment = map(str.strip, user_input.split(',', 1))
            await add_comment_to_person(name, comment)
            await update.message.reply_text(f"Комментарий добавлен для {name}.", reply_markup=back_button())

        elif action == 'add_review':
            name = context.user_data.get('name')

            # Если есть фото, но нет имени
            if update.message.photo and not name:
                # Сохраняем фото, но запрашиваем имя
                file = await update.message.photo[-1].get_file()
                photo_url = file.file_path
                context.user_data['photo'] = photo_url
                await update.message.reply_text("Отправьте имя для добавления отзыва.")
            elif name and update.message.photo:
                # Если есть фото и имя, добавляем отзыв с фото
                photo_url = context.user_data.get('photo')
                await add_review_to_person(name, review=user_input, photo=photo_url)
                await update.message.reply_text(f"Ваш отзыв добавлен с фото для {name}.")
            elif user_input and ',' in user_input:
                # Если текстовое сообщение содержит имя и отзыв
                name, review = map(str.strip, user_input.split(',', 1))
                context.user_data['name'] = name  # Сохраняем имя
                photo_url = context.user_data.get('photo')  # Проверяем наличие фото
                await add_review_to_person(name, review=review, photo=photo_url)
                await update.message.reply_text(f"Ваш отзыв добавлен для {name}.")
                context.user_data['photo'] = None  # Сброс фото после использования
            else:
                # Если получено имя без фото, сохраняем имя и запрашиваем отзыв
                name = user_input.strip()
                context.user_data['name'] = name
                await update.message.reply_text(f"Теперь отправьте отзыв для {name}.")

        elif action == 'delete_review':
            name = user_input.strip()
            await delete_review_from_person(name)
            await update.message.reply_text(f"Отзыв для {name} удалён.", reply_markup=back_button())



        context.user_data['action'] = None  # Сброс действия после выполнения
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}", reply_markup=back_button())

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # Получаем фотографию самого высокого качества
    file = await photo.get_file()
    photo_url = file.file_path

    action = context.user_data.get('action')
    name = context.user_data.get('name')

    if action == 'add_review' and not name:
        # Если фото получено, но имя не отправлено
        context.user_data['photo'] = photo_url
        await update.message.reply_text("Отправьте имя для добавления отзыва.")
    elif action == 'add_review' and name:
        # Если имя уже есть, добавляем фото в отзыв
        await add_review_to_person(name, photo=photo_url)
        await update.message.reply_text(f"Фото добавлено к отзыву для {name}.")
    else:
        await update.message.reply_text("Фото не требуется для данного действия.", reply_markup=back_button())

# Проверка пароля для администратора
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    password = update.message.text
    if password == ADMIN_PASSWORD:
        context.user_data['role'] = 'admin'
        await update.message.reply_text("Вы вошли как администратор.", reply_markup=main_menu())
    else:
        await update.message.reply_text("Неверный пароль. Попробуйте снова.", reply_markup=role_menu())

# Основная функция запуска бота
def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))


    application.run_polling()

if __name__ == "__main__":
    main()