from telegram import Update
from telegram.ext import ContextTypes
import time
from buttons.language import show_languages
from config import (
    create_reply_keyboard,
    CHOOSING)
from db.MySqlConn import Mysql


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    mysql = Mysql()
    user = update.effective_user
    user_id = user.id
    nick_name = user.full_name

    user_checkin = mysql.getOne(f"select * from users where user_id={user_id}")
    if not user_checkin:
        if context.args:
            referral_code = context.args[0]
            referrer = mysql.getOne("SELECT user_id FROM users WHERE ref_link LIKE %s", [f"%{referral_code}"])

            if referrer:
                referrer_id = referrer['user_id']
                mysql.update("UPDATE users SET ref_count = ref_count + 1 WHERE user_id = %s", [referrer_id])

        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into users (user_id, name, nick_name, system_content, created_at, voice, pic) values (%s, %s, %s, %s, %s, %s, %s)"
        value = [user_id, user.username, nick_name, None, date_time, 3, 3]
        mysql.insertOne(sql, value)
    if user_checkin and not user_checkin.get("nick_name"):
        mysql.update("update users set nick_name=%s where user_id=%s", (nick_name, user_id))
    mysql.end()

    user = update.effective_user
    await show_languages(update, context)
    return CHOOSING
