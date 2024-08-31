import random
import string
from buttons.templates import referral_limit,referral_update,give_referral_link
from buttons.templates import exchange_referrals_4o_mini, exchange_referrals_voice_model,exchange_referrals_image_model
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db.MySqlConn import Mysql

async def generate_referral_link(user_id):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    referral_link = f"https://t.me/MyGPT_Assist_Bot?start={code}"
    mysql = Mysql()
    mysql.update("UPDATE users SET ref_link = %s WHERE user_id = %s", [code, user_id])
    mysql.end()
    return referral_link


async def show_referral_info(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    mysql = Mysql()
    user = mysql.getOne("SELECT ref_link, ref_count FROM users WHERE user_id = %s", [user_id])
    
    if user['ref_link'] is None:
        referral_link = await generate_referral_link(user_id)
    else:
        referral_link = "https://t.me/MyGPT_Assist_Bot?start=" + user['ref_link']

    referral_count = user['ref_count']
    
    keyboard = [
        [InlineKeyboardButton("Exchange", callback_data='ex')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_text = give_referral_link[context.user_data['lang']].safe_substitute(referral_link=referral_link, referral_count=referral_count)
    await update.message.reply_text(reply_text, disable_web_page_preview=True, reply_markup=reply_markup)
    mysql.end()

async def exchange(update : Update, context : CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    mysql = Mysql()
    user = mysql.getOne("select * from users where user_id=%s", [user_id])
    mysql.end()

    keyboard = [
        [InlineKeyboardButton(exchange_referrals_4o_mini[user['lang']], callback_data='exc_gpt')],
        [InlineKeyboardButton(exchange_referrals_voice_model[user['lang']], callback_data='exc_voice')],
        [InlineKeyboardButton(exchange_referrals_image_model[user['lang']], callback_data='exc_im')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Choose your plan.", reply_markup=reply_markup)

async def exchange_handler(update : Update, context : CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    mysql = Mysql()
    user = mysql.getOne("select * from users where user_id=%s", [user_id])
    refs = user.get('ref_count')

    if refs < 5:
        reply = referral_limit[user["lang"]]
        await query.edit_message_text(reply)
        mysql.end()
        return
    else:
        mysql.update("Update users set ref_count = ref_count - 5 where user_id=%s", [user_id])
        if query.data == "exc_gpt":
            mysql.update("Update users set gpt = gpt+50 where user_id=%s", [user_id])
        elif query.data == "exc_voice":
            mysql.update("Update users set voice = voice+10 where user_id=%s", [user_id])
        elif query.data == "exc_im":
            mysql.update("Update users set pic = pic+10 where user_id=%s", [user_id])
        await query.edit_message_text(referral_update[user['lang']])
        mysql.end()