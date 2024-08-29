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

    if user_checkin:
            await update.message.reply_html(
        rf"""Hey  {user.mention_html()}!
I'm an AI chatbot created to interact with you and make your day a little brighter. If you have any questions or just want to have a friendly chat, I'm here to help! 🤗
Do you know what's great about me? I can help you with anything from giving advice to telling you a joke, and I'm available 24/7! 🕰️
        """ if user_checkin.get('lang') == 'en' else 
        rf"""سلام {user.mention_html()}!
من یک ربات چت هوش مصنوعی هستم که برای تعامل با شما و روشن کردن روزتان ایجاد شده است. اگر سوالی دارید یا فقط می خواهید یک چت دوستانه داشته باشید، من اینجا هستم تا کمک کنم! 🤗
آیا می دانید چه چیزی در مورد من عالی است؟ من می توانم در هر کاری به شما کمک کنم، از نصیحت کردن تا گفتن یک جوک، و 24 ساعته در خدمت هستم! 🕰️
        """,
        reply_markup=create_reply_keyboard(user_checkin.get('lang')), disable_web_page_preview=True
    )
    else:
        await show_languages(update, context)
    return CHOOSING

async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mysql = Mysql()
    chat = update.effective_chat
    chat_info = await context.bot.get_chat(chat.id)
    member_count = await chat_info.get_member_count()
    

    group_checkin = mysql.getOne(f"select * from group_chats where group_id={chat_info.id}")
    if not group_checkin:
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into group_chats (group_id, members, created_at) values (%s, %s, %s)"
        value = [chat_info.id, member_count, date_time]
        mysql.insertOne(sql, value)
    if group_checkin and group_checkin.get("members") != member_count:
        mysql.update("update group_chats set members=%s where group_id=%s", (member_count, chat_info.id))
    mysql.end()

    await update.message.reply_text(
        rf"""Hey! to use this bot, use the command /prompt following by your prompt.
        سلام!
        برای استفاده از این ربات، از دستور /prompt و سپس سوال خود استفاده کنید.
        """,
    )