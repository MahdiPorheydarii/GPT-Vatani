from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackContext
from db.MySqlConn import Mysql
from config import CHOOSING, create_reply_keyboard


async def show_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='lang_en'),
            InlineKeyboardButton("فارسی", callback_data='lang_fa'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose your language:', reply_markup=reply_markup)
    return CHOOSING


async def show_languages_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    nick_name = update.effective_user.full_name

    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    
    # Update the user's language in the database
    mysql = Mysql()
    mysql.update("update users set nick_name=%s, lang=%s where user_id=%s", (nick_name, lang, user_id))
    mysql.end()

    # Change the message text according to the selected language
    confirmation_text = "Language changed to 🇬🇧 English" if lang == "en" else "زبان به فارسی 🇮🇷 تغییر کرد"
    await query.edit_message_text(text=confirmation_text)

    # Update the reply keyboard to the selected language
    reply_markup = create_reply_keyboard(lang)
    await context.bot.send_message(chat_id=user_id, text="You can continue now:" if lang=='en' else "میتوانید ادامه دهید:", reply_markup=reply_markup)
