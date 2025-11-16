from telegram import Update
from telegram.ext import ContextTypes
from buttons import admin_menu, guest_menu, back_button
from database.db import SessionLocal
from database.crud import (
    get_all_comments,
    get_all_reviews,
    get_all_people,
)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_role = context.user_data.get("role", "guest")
    db = SessionLocal()

    try:
        if data == "add_info":
            await query.edit_message_text(
                "✏️ Отправьте имя и информацию в формате:\n<b>Имя, информация</b>",
                parse_mode="HTML",
                reply_markup=back_button()
            )

        elif data == "update_info":
            await query.edit_message_text(
                "🔄 Отправьте имя и новую информацию в формате:\n<b>Имя, информация</b>",
                parse_mode="HTML",
                reply_markup=back_button()
            )

        elif data == "delete_info":
            await query.edit_message_text(
                "❌ Отправьте имя, которое хотите удалить:",
                reply_markup=back_button()
            )

        elif data == "show_all":
            people = get_all_people(db)
            if not people:
                await query.edit_message_text("Нет зарегистрированных имён.", reply_markup=back_button())
            else:
                text = "\n".join([f"👤 <b>{p.name}</b>: {p.info or '—'}" for p in people])
                await query.edit_message_text(text, parse_mode="HTML", reply_markup=back_button())

        elif data == "show_comments":
            comments = get_all_comments()
            if not comments:
                await query.edit_message_text("Нет комментариев.", reply_markup=back_button())
            else:
                text = "\n".join([f"💬 {c}" for c in comments])
                await query.edit_message_text(text, reply_markup=back_button())

        elif data == "delete_comment":
            await query.edit_message_text("Отправьте имя для удаления отзыва.", reply_markup=back_button())

        elif data == "back":
            if user_role == "admin":
                await query.edit_message_text("👑 Главное меню администратора", reply_markup=admin_menu())
            else:
                await query.edit_message_text("💬 Главное меню гостя", reply_markup=guest_menu())

    except Exception as e:
        from main import logger
        logger.exception("❌ Ошибка при обработке кнопки:")
        await query.edit_message_text("⚠️ Произошла ошибка. Проверьте логи.")
    finally:
        db.close()




# from telegram import Update
# from telegram.ext import ContextTypes
# from buttons import admin_menu, guest_menu, back_button
# from database.db import SessionLocal
# from database.crud import (
#     add_person,
#     delete_person,
#     get_all_comments,
#     get_all_reviews,
#     get_all_people,
# )

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     data = query.data
#     user_role = context.user_data.get("role", "guest")

#     db = SessionLocal()

#     try:
#         if data == "add_info":
#             comments = add_person()
#             await query.edit_message_text(
#                 "Отправьте имя и информацию в формате: 'Имя, информация'.",
#                 reply_markup=back_button()
#             )

#         elif data == "update_info":
#             await query.edit_message_text(
#                 "Отправьте имя и новую информацию в формате: 'Имя, информация'.",
#                 reply_markup=back_button()
#             )

#         elif data == "delete_info":
#             comments = delete_person()
#             await query.edit_message_text(
#                 "Отправьте имя для удаления.",
#                 reply_markup=back_button()
#             )

#         elif data == "show_all":
#             people = get_all_people(db) 
#             if not people:
#                 await query.edit_message_text("Нет зарегистрированных имён.", reply_markup=back_button())
#             else:
#                 text = "\n".join([f"👤 {p.name}: {p.info or '—'}" for p in people])
#                 await query.edit_message_text(text, reply_markup=back_button())

#         elif data == "show_comments":
#             comments = get_all_comments()
#             if not comments:
#                 await query.edit_message_text("Нет комментариев.", reply_markup=back_button())
#             else:
#                 text = "\n".join([f"💬 {c}" for c in comments])
#                 await query.edit_message_text(text, reply_markup=back_button())

#         elif data == "delete_comment":
#             await query.edit_message_text("Отправьте имя для удаления отзыва.", reply_markup=back_button())

#         elif data == "back":
#             if user_role == "admin":
#                 await query.edit_message_text("👑 Главное меню администратора", reply_markup=admin_menu())
#             else:
#                 await query.edit_message_text("💬 Главное меню гостя", reply_markup=guest_menu())

#     except Exception as e:
#         from main import logger
#         logger.exception("❌ Ошибка при обработке кнопки:")
#         await query.edit_message_text("⚠️ Произошла ошибка. Проверьте логи.")
#     finally:
#         db.close()
