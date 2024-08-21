import httpx
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from config import config, create_reply_keyboard, TYPING_TEXT_FOR_IMAGE, CHOOSING
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
            print(response.json())
            if response.status_code == 200:
                pi = response.json()['process_id']
                print(pi)
                status_url = f"https://api.monsterapi.ai/v1/status/{pi}"

                while True:
                    status_response = await client.get(status_url, headers=headers)
                    status_data = status_response.json()
                    
                    if status_data['status'] == "COMPLETED":
                        image_url = status_data['result']['output'][0]
                        image_response = await client.get(image_url)
                        
                        # Save and send the image
                        print(status_data)
                        image_path = image_url[image_url.index('com') + 4:]
                        with open(image_path, "wb") as f:
                            f.write(image_response.content)
                        
                        await update.message.reply_photo(photo=open(image_path, "rb"))
                        break
                    else:
                        await asyncio.sleep(0.5)
            else:
                await update.message.reply_text("Failed to generate the image. Please try again.")
    else:
        await update.message.reply_text("Please send a valid text prompt.")

    return CHOOSING