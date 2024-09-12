from telegram import Update
from telegram.ext import ContextTypes
from config import CHOOSING
from db.MySqlConn import Mysql
from buttons.templates import say_help


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    if context.user_data['lang']:
        lang = context.user_data['lang']
    else:
        mysql = Mysql()
        user = mysql.getOne("select lang from users where user_id=%s", update.effective_user.id)
        mysql.end()
        lang = user.get('lang')
    await update.message.reply_text(say_help[lang])
    return CHOOSING