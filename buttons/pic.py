import httpx
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from config import config, create_reply_keyboard, TYPING_TEXT_FOR_IMAGE
import asyncio
import os

API_KEY = config['PIC_API_KEY']

async def handle_text_to_pic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # query = update.callback_query
    # await query.answer()

    # Ask the user to send the text prompt for image generation
    await update.message.reply_text('Please send the text to make a image of it.')
    
    # Move to the state where we expect the user to send a text prompt for the image
    return TYPING_TEXT_FOR_IMAGE

async def generate_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if context.user_data['awaiting_pic_text']:
        # print("there")
        # context.user_data['awaiting_pic_text'] = False

    prompt = update.message.text
    if prompt:
        url = "https://api.monsterapi.ai/v1/generate/sdxl-base"
        payload = {
            "enhance": False,
            "optimize": False,
            "safe_filter": False,
            "aspect_ratio": "square",
            "guidance_scale": 15,
            "prompt": prompt,
            "style": "photographic",
            "samples": 1
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
                response = await client.get(status_url, headers=headers)
                
                while response.json()['status'] != "COMPLETED":
                    await asyncio.sleep(0.5)
                    response = await client.get(status_url, headers=headers)

                image_url = response.json()['result']['output'][0]
                image_response = await client.get(image_url)

                image_path = image_url[image_url.index('com')+4:]
                with open(image_path, "wb") as f:
                    f.write(image_response.content)

                await update.message.reply_photo(photo=open(image_path, "rb"))
            else:
                await update.message.reply_text("Failed to generate the image. Please try again.")
    else:
        await update.message.reply_text("Please send a valid text prompt.")
