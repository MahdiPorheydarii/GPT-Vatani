import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db.MySqlConn import Mysql
from config import create_reply_keyboard

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
    reply_text = (f"Your referral link: {referral_link}\n"
                  f"Referrals: {referral_count}\n")
    await update.message.reply_text(reply_text, disable_web_page_preview=True, reply_markup=reply_markup)
    mysql.end()

async def exchange(update : Update, context : CallbackContext):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Exchange 5 refs with 50 GPT 4o mini credits", callback_data='exc_gpt')],
        [InlineKeyboardButton("Exchange 5 refs with 10 voice model credits", callback_data='exc_voice')],
        [InlineKeyboardButton("Exchange 5 refs with 10 image model credits", callback_data='exc_im')],
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
        reply = """
                    you do not have enough referrals to exchange.
                """
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
        await query.edit_message_text("Your credits have been applied! check Statistics.")
        mysql.end()