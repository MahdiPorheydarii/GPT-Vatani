from telegram import Update
from telegram.ext import ContextTypes
from config import CHOOSING
from db.MySqlConn import Mysql
from buttons.templates import say_help


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data['lang']
    if lang:
        await update.message.reply_text(say_help[lang])
    else:
        await update.message.reply_text("Please use /start again, we had updates!")
    return CHOOSING