from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
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
    user = update.effective_user
    lang = query.data.split("_")[1]
    context.user_data['lang'] = lang
    mysql = Mysql()
    mysql.update("update users set nick_name=%s, lang=%s where user_id=%s", (nick_name, lang, user_id))
    mysql.end()

    confirmation_text = "Language changed to 🇬🇧 English\n" if lang == "en" else "زبان به فارسی 🇮🇷 تغییر کرد"
    await query.edit_message_text(text=confirmation_text)
    await query.message.reply_html(
        rf"""Hey  {user.mention_html()}!
I'm an AI chatbot created to interact with you and make your day a little brighter. If you have any questions or just want to have a friendly chat, I'm here to help! 🤗
Do you know what's great about me? I can help you with anything from giving advice to telling you a joke, and I'm available 24/7! 🕰️
        """ if lang == 'en' else 
        rf"""سلام {user.mention_html()}!
من یک ربات چت هوش مصنوعی هستم که برای تعامل با شما و روشن کردن روزتان ایجاد شده است. اگر سوالی دارید یا فقط می خواهید یک چت دوستانه داشته باشید، من اینجا هستم تا کمک کنم! 🤗
آیا می دانید چه چیزی در مورد من عالی است؟ من می توانم در هر کاری به شما کمک کنم، از نصیحت کردن تا گفتن یک جوک، و 24 ساعته در خدمت هستم! 🕰️
        """,
        reply_markup=create_reply_keyboard(lang), disable_web_page_preview=True
    )
