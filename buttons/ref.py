import random
import string
from telegram import Update
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
    
    reply_text = (f"Your referral link: {referral_link}\n"
                  f"Referrals: {referral_count}\n")
    await update.message.reply_text(reply_text, disable_web_page_preview=True)
    mysql.end()