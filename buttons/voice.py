from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import time
from openai import OpenAI
from config import config, CHOOSING, create_reply_keyboard, VOICE
import ast
from db.MySqlConn import Mysql
from buttons.templates import *

BACK_BUTTON = "🔙 Back"

def create_back_button_keyboard():
    return ReplyKeyboardMarkup([[BACK_BUTTON]], resize_keyboard=True, one_time_keyboard=True)

async def handle_voice(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    lang = context.user_data['lang']

    if lang:
        if query.data == "voice_tts":
            await update.message.reply_text(voice_tts_respond[lang], reply_markup=create_back_button_keyboard())
            context.user_data['awaiting_prompt'] = True
            return VOICE
        elif query.data == "voice_stt":
            await handle_speech_to_text(update, context)
            return VOICE
    else:
        await update.message.reply_text("Please use /start again, we had updates!")
        return CHOOSING

async def choose(update: Update, context: CallbackContext):
    if update.message.text == BACK_BUTTON:
        await update.message.reply_text(
            voice_back_respond[context.user_data['lang']],
            reply_markup=create_reply_keyboard(context.user_data['lang'])
        )
        return CHOOSING

async def voice_options(update: Update, context: CallbackContext):
    lang = context.user_data['lang']
    keyboard = [
        [
            InlineKeyboardButton("Speech to Text", callback_data='voice_stt'),
            InlineKeyboardButton("Text to Speech", callback_data='voice_tts')
        ],
        [
            InlineKeyboardButton("Back", callback_data='vice_back')
        ]
    ]
    if lang:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(voice_reply_text[lang], reply_markup=reply_markup)
        return VOICE
    else:
        await update.message.reply_text("Please use /start again, we had updates!")
        return CHOOSING

async def handle_speech_to_text(update: Update, context: CallbackContext):
    lang = context.user_data['lang']
    if lang:
        await update.message.reply_text(handle_stt[lang], reply_markup=create_back_button_keyboard())
        context.user_data['awaiting_audio'] = True
    else:
        await update.message.reply_text("Please use /start again, we had updates!")

async def transcribe_audio(update: Update, context: CallbackContext):
    if 'awaiting_audio' in context.user_data and context.user_data['awaiting_audio']:
        context.user_data['awaiting_audio'] = False
        mysql = Mysql()
        user_id = update.effective_user.id
        user = mysql.getOne(f"select * from users where user_id={user_id}")

        chat_count = mysql.getOne(
            f"select count(*) as count from records where role='user_voice' and user_id = {user_id};")

        if chat_count.get('count') > 2 and user.get('voice') < 1:
            reply = voice_text_count_limit[user['lang']]
            await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=create_reply_keyboard(user['lang']))
            mysql.end()
            return CHOOSING
            
        file = update.message.voice or update.message.audio
        duration = file.duration
        if duration > 60 and user.get('voice') < 1:
                reply = voice_min_limit[user['lang']]              
                await update.message.reply_text(reply, parse_mode="HTML", reply_markup=create_reply_keyboard(user['lang']))   
                return CHOOSING    

        elif file:
            if duration > user.get('voice') * 60 :
                await update.message.reply_text("Not enough credits", parse_mode="HTML", reply_markup=create_reply_keyboard(user['lang'])) 
                mysql.end()
                return CHOOSING
            file_path = await file.get_file()
            path = ast.literal_eval(file_path.to_json())

            client = OpenAI(api_key=config['AI']['TOKEN'])
            await file_path.download_to_drive()
            print(path['file_path'][path['file_path'].index('ice/')+4:],)
            audio_file= open(path['file_path'][path['file_path'].index('ice/')+4:], "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            res = transcription.text
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "insert into records (user_id, role, content, created_at, tokens) " \
                "values (%s, %s, %s, %s, %s);"
            value = [user_id, "user_voice", res, date_time, 0]
            mysql.insertOne(sql, value)
            await update.message.reply_text(f"{res}", reply_markup=create_reply_keyboard(user['lang']))
            mysql.update("Update users set voice = %s where user_id=%s", [user.get('voice')-duration/60, user_id])
            mysql.end()
            return CHOOSING
        else:
            update.message.reply_text(invalid_audio_file[user['lang']], reply_markup=create_reply_keyboard(user['lang']))
            return CHOOSING

async def handle_text_to_speech(update: Update, context: CallbackContext):
    lang = context.user_data['lang']
    if lang:
        await update.message.reply_text(handle_text_to_speech[lang], reply_markup=create_back_button_keyboard())
        context.user_data['awaiting_prompt'] = True
    else:
        await update.message.reply_text("Please use /start again, we had updates!")

async def tts(update: Update, context: CallbackContext):
    if 'awaiting_prompt' in context.user_data and context.user_data['awaiting_prompt']:
        context.user_data['awaiting_prompt'] = False

        mysql = Mysql()
        user_id = update.effective_user.id
        user = mysql.getOne(f"select * from users where user_id={user_id}")

        chat_count = mysql.getOne(
            f"select count(*) as count from records where role='user_voice' and user_id = {user_id};")

        if chat_count.get('count') > 2 and user.get('voice') < 1:
            reply = voice_text_count_limit[user['lang']]
            await update.message.reply_text(reply, parse_mode="HTML", reply_markup=create_reply_keyboard(user['lang']))
            mysql.end()
            return CHOOSING
        
        input_text = update.message.text

        if len(input_text) > 200 and user.get('voice') < 1:
                reply = text_min_limit[user['lang']]              
                await update.message.reply_text(reply, parse_mode="HTML", reply_markup=create_reply_keyboard(user['lang']))
                mysql.end()
        else:        
            API_KEY = config['AI']['TOKEN']
            client = OpenAI(api_key=API_KEY)

            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=input_text,
                speed=0.9
            )
            response.stream_to_file("output.ogg")
            duration = len(input_text.split(' ')) / 2.5
    
            await update.message.reply_voice("output.ogg")
            
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "insert into records (user_id, role, content, created_at, tokens) " \
                    "values (%s, %s, %s, %s, %s);"
            value = [user_id, "user_voice", input_text, date_time, 0]
            mysql.insertOne(sql, value)

            cnt = user.get('voice')
            mysql.update("Update users set voice = %s where user_id = %s", [cnt-duration/60, user_id])
            mysql.end()
            return CHOOSING
    else:
        await voice_options(update, context)