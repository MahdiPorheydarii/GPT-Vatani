from telegram import Update
from telegram.ext import ContextTypes

from buttons.templates import statistics_response
from db.MySqlConn import Mysql
from config import (
    create_reply_keyboard,
    CHOOSING)


async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    mysql = Mysql()
    user_id = user.id
    chat_count = mysql.getOne(
    f"select count(*) as count from records where role='user' and user_id = {user_id} and created_at >=NOW() - INTERVAL 1440 MINUTE;")['count']
    chat_count = max(0, 3 - chat_count)
    gpt = mysql.getOne(
        f"select gpt from users where user_id={user_id}")['gpt']
    image = mysql.getOne(
        f"select pic from users where user_id={user_id}")['pic']
    voice = mysql.getOne(
        f"select voice from users where user_id={user_id}")['voice']

    user_info = mysql.getOne("select * from users where user_id=%s", user_id)
    mysql.end()

    if not gpt:
        gpt = 0
    if not image:
        image = 0

    await update.message.reply_html(
        statistics_response[user_info["lang"]]
        .safe_substitute(user=user.mention_html(),
                         gpt=max(chat_count, gpt),
                         image=image,
                         voice=voice),
        reply_markup=create_reply_keyboard(user_info["lang"]), disable_web_page_preview=True
    )
    return CHOOSING
