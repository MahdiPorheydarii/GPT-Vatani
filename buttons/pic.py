import httpx
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import config, create_reply_keyboard, TYPING_TEXT_FOR_IMAGE, CHOOSING
import asyncio
import time
from db.MySqlConn import Mysql
from buttons.templates import text_to_image, failed_to_generate_image, valid_text_to_img

API_KEY = config['PIC_API_KEY']
BACK_BUTTON = "🔙 Back"

def create_back_button_keyboard():
    return ReplyKeyboardMarkup([[BACK_BUTTON]], resize_keyboard=True, one_time_keyboard=True)

async def handle_text_to_pic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    back_keyboard = create_back_button_keyboard()
    lang = context.user_data['lang']
    if lang:
        await update.message.reply_text(
            text_to_image[lang], 
            reply_markup=back_keyboard
        )
    else:
        mysql = Mysql()
        user = mysql.getOne("select lang from users where user_id=%s", update.effective_user.id)
        mysql.end()
        lang = user.get('lang')
        await update.message.reply_text(
            text_to_image[lang], 
            reply_markup=back_keyboard
        )
        return TYPING_TEXT_FOR_IMAGE
    
async def generate_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mysql = Mysql()
    user = mysql.getOne("select * from users where user_id=%s", update.effective_user.id)
    prompt = update.message.text
    if update.message.text == BACK_BUTTON:
        await update.message.reply_text(
            "Returning to the main menu.", 
            reply_markup=create_reply_keyboard(user.get('lang'))
        )
        return CHOOSING 
    if prompt:
        url = "https://api.monsterapi.ai/v1/generate/sdxl-base"
        payload = {
            "enhance": True,
            "optimize": False,
            "safe_filter": False,
            "aspect_ratio": "square",
            "guidance_scale": 15,
            "prompt": prompt,
            "style": "photographic",
            "samples": 1,
            "steps": 60
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {API_KEY}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                pi = response.json()['process_id']
                status_url = f"https://api.monsterapi.ai/v1/status/{pi}"

                while True:
                    status_response = await client.get(status_url, headers=headers)
                    status_data = status_response.json()
                    
                    if status_data['status'] == "COMPLETED":
                        image_url = status_data['result']['output'][0]
                        image_response = await client.get(image_url)
                        image_path = image_url[image_url.index('com') + 4:]
                        with open(image_path, "wb") as f:
                            f.write(image_response.content)
                        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        await update.message.reply_photo(
                            photo=open(image_path, "rb"), 
                            reply_markup=create_reply_keyboard(user.get('lang'))
                        )
                        mysql.insertOne(
                            "insert into records (user_id, role, content, created_at) values (%s, %s, %s, %s)", 
                            [update.effective_user.id, "user_pic", prompt, date_time]
                        )
                        mysql.update("update users set pic=pic-1 where user_id=%s", [update.effective_user.id])
                        mysql.end()
                        return CHOOSING
                    else:
                        await asyncio.sleep(0.5)
            else:
                await update.message.reply_text(
                    failed_to_generate_image[user['lang']], 
                    reply_markup=create_reply_keyboard(user.get('lang'))
                )
                return CHOOSING
    else:
        await update.message.reply_text(
            valid_text_to_img[user['lang']], 
            reply_markup=create_reply_keyboard(user.get('lang'))
        )
    mysql.end()
    return CHOOSING