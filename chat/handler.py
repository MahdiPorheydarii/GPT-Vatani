from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
import asyncio
import re

from chat.ai import ChatCompletionsAI
import time
import emoji

from db.MySqlConn import Mysql
from buttons.templates import token_limit
from config import (
    create_reply_keyboard,
    CHOOSING,
    time_span,
    notification_channel)


async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    prompt = update.message.text
    user_id = user.id
    nick_name = user.full_name
    mysql = Mysql()

    user_checkin = mysql.getOne(f"select * from users where user_id={user_id}")
    if not user_checkin:
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into users (user_id, name, nick_name, system_content, created_at, lang, gpt, voice, pic) values (%s, %s, %s, %s, %s, %s, %s)"
        value = [user_id, user.username, nick_name, 0, None,
                 date_time, 'en', 0, 3, 3]
        mysql.insertOne(sql, value)

    if user_checkin and not user_checkin.get("nick_name"):
        mysql.update("update users set nick_name=%s where user_id=%s", (nick_name, user_id))

    logged_in_user = mysql.getOne(f"select * from users where user_id={user_id}")
    parse_mode = logged_in_user.get("parse_mode")

    # Rate limit controller
    chat_count = mysql.getOne(
        f"select count(*) as count from records where role='user' and user_id = {user_id} and created_at >=NOW() - INTERVAL {time_span} MINUTE;")

    if chat_count.get("count") > 2 and logged_in_user.get('gtp') < 1:
        reply = f" محدودیت استفاده رایگان😶‍🌫" \
            f"شما به حد مجاز ۳ بار استفاده رایگان از ربات رسیده‌اید. برای ادامه استفاده از خدمات، لطفاً یکی از اشتراک‌های ما را تهیه کنید. \n"\
            f"[خرید اشتراک](https://Zarinp.al/MyGPT)"\
            f" اگر سوالی دارید، می‌توانید با پشتیبانی تماس بگیرید.\n"
        await update.message.reply_text(reply, reply_markup=create_reply_keyboard(logged_in_user["lang"]))
        return CHOOSING

    placeholder_message = await update.message.reply_text("...")
    records = mysql.getMany(f"select * from records where user_id={user_id} and role='user' and reset_at is null order by id desc",
                            3)
    if update.message:
        messages = []
        prompt_tokens = 0
        if records:
            for record in records:
                messages.append({"role": record["role"], "content": record["content"]})
                prompt_tokens += count_tokens(record["content"])
            messages.reverse()
        if logged_in_user["system_content"]:
            messages.insert(0, {"role": "system", "content": logged_in_user["system_content"]})
            prompt_tokens += count_tokens(logged_in_user["system_content"])
        messages.append({"role": "user", "content": prompt})
        prompt_tokens += count_tokens(prompt)

        replies = ChatCompletionsAI(logged_in_user, messages)
        prev_answer = ""
        index = 0
        answer = ""
        cnt = logged_in_user.get('gpt')
        mysql.update("Update users set gpt = %s where user_id = %s", [cnt-1, logged_in_user.get('user_id')])
        async for reply in replies:
            index += 1
            answer, status = reply
            if abs(count_tokens(answer) - count_tokens(prev_answer)) < 30 and status is None:
                continue
            prev_answer = answer
            try:
                if status == "length":
                    answer = token_limit[user_checkin["lang"]].safe_substitute(answer=answer, max_token=1500)
                    parse_mode = "Markdown"
                elif status == "content_filter":
                    answer = f"{answer}\n\nAs an AI assistant, please ask me appropriate questions!！\nPlease contact @AiMessagerBot for more help!" \
                             f"{emoji.emojize(':check_mark_button:')}"
                await context.bot.edit_message_text(answer, chat_id=placeholder_message.chat_id,
                                                    message_id=placeholder_message.message_id,
                                                    parse_mode=parse_mode, disable_web_page_preview=True)
            except BadRequest as e:
                if str(e).startswith("Message is not modified"):
                    continue
                else:
                    await context.bot.edit_message_text(answer, chat_id=placeholder_message.chat_id,
                                                        message_id=placeholder_message.message_id)
            await asyncio.sleep(0.01)  # wait a bit to avoid flooding

        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into records (user_id, role, content, created_at, tokens) " \
              "values (%s, %s, %s, %s, %s)"
        value = [user_id, "user", prompt, date_time, prompt_tokens]
        mysql.insertOne(sql, value)

        value = [user_id, 'assistant', answer, date_time, count_tokens(answer)]
        mysql.insertOne(sql, value)
        mysql.end()
        if notification_channel:
            msg = f"#U{user_id}: {prompt} \n#Jarvis : {answer}"
            await context.bot.send_message(chat_id=notification_channel, text=msg, disable_web_page_preview=True,
                                           parse_mode=parse_mode)
    return CHOOSING


def count_tokens(text):
    token_count = 0
    if text:
        pattern = r"[\u4e00-\u9fa5]|[a-zA-Z]+|[^\s\w]"
        tokens = re.findall(pattern, text)

        token_count = len(tokens)

    return token_count
