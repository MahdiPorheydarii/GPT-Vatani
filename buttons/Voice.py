import assemblyai as aai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
import time
from telegram.constants import ParseMode
from openai import OpenAI
from config import config, CHOOSING, create_reply_keyboard
import ast
from db.MySqlConn import Mysql

def percent(s):
    alphabet = 'abcdefghijklmnopqrstuvwxyz !@#$%?>.1234567890-=`'
    c = 0
    for i in s:
        if i not in alphabet:
            c+=1
    return 1-c/len(s)

aai.settings.api_key = config['ASS_API_KEY']

async def voice_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Speech to Text", callback_data='speech_to_text'),
            InlineKeyboardButton("Text to Speech", callback_data='text_to_speech')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose one option:', reply_markup=reply_markup)
    return CHOOSING

# Handler for receiving audio files and transcribing them
async def handle_speech_to_text(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Ask the user to send an audio file
    await query.edit_message_text(text="Please send an audio file to transcribe.")

    # Update state to wait for an audio file
    context.user_data['awaiting_audio'] = True

async def transcribe_audio(update: Update, context: CallbackContext):
    mysql = Mysql()
    user_id = update.effective_user.id
    user = mysql.getOne(f"select * from users where user_id={user_id}")

    chat_count = mysql.getOne(
        f"select count(*) as count from records where role='user_voice' and user_id = {user_id};")

    if chat_count.get('count') > 2 and user.get('level') < 2:
        reply = f" محدودیت استفاده رایگان😶‍🌫" \
            f"شما به حد مجاز ۳ بار استفاده رایگان از ربات رسیده‌اید. برای ادامه استفاده از خدمات، لطفاً یکی از اشتراک‌های ما را تهیه کنید. \n"\
            f"[خرید اشتراک](https://Zarinp.al/MyGPT)"\
            f" اگر سوالی دارید، می‌توانید با پشتیبانی تماس بگیرید.\n"
        await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=create_reply_keyboard(user['lang']))
    elif 'awaiting_audio' in context.user_data and context.user_data['awaiting_audio']:
        context.user_data['awaiting_audio'] = False
        
        file = update.message.voice or update.message.audio
        if file.duration > 60:
                reply = f"حداکثر مدت زمان فایل صوتی برای کاربر معمولی 60 ثانیه است.\n" \
                        f"برای استفاده از این بخش، مدت زمان فایل خود را کاهش دهید یا اشتراک تهیه کنید.\n" \
                        f"[خرید اشتراک](https://Zarinp.al/MyGPT)"\
                        f" اگر سوالی دارید، می‌توانید با پشتیبانی تماس بگیرید.\n"                
                await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=create_reply_keyboard(user['lang']))           

        elif file:
            file_path = await file.get_file()
            path = ast.literal_eval(file_path.to_json())
            print(path)
            conf = aai.TranscriptionConfig(language_detection=True, speech_model=aai.SpeechModel.nano)
            transcriber = aai.Transcriber(config=conf)
            transcript = transcriber.transcribe(path['file_path'])

            if transcript.status == aai.TranscriptStatus.error:
                await update.message.reply_text(f"Error transcribing audio: {transcript.error}", reply_markup=create_reply_keyboard(user['lang']))
            else:
                print(percent(transcript.text), transcript.text)
                if percent(transcript.text) > 0.8:
                    res = transcript.text
                else:
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
                mysql.end()
                await update.message.reply_text(f"{res}", reply_markup=create_reply_keyboard(user['lang']))

        else:
            update.message.reply_text("Please send a valid audio file.", reply_markup=create_reply_keyboard(user['lang']))

async def handle_text_to_speech(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    query.edit_message_text(text="Please send the text to convert to speech.")
