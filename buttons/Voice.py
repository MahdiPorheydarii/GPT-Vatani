import assemblyai as aai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
import emoji
from telegram.constants import ParseMode
from config import config, CHOOSING
import ast
from db.MySqlConn import Mysql

# Set your AssemblyAI API key
aai.settings.api_key = config['ASS_API_KEY']

async def voice_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Speech to Text", callback_data='speech_to_text'),
            InlineKeyboardButton("Text to Speech", callback_data='text_to_speech')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose your language:', reply_markup=reply_markup)
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
    if user.get('level') < 2:
        reply = f" محدودیت استفاده رایگان😶‍🌫" \
            f"شما به حد مجاز ۳ بار استفاده رایگان از ربات رسیده‌اید. برای ادامه استفاده از خدمات، لطفاً یکی از اشتراک‌های ما را تهیه کنید. \n"\
            f"[خرید اشتراک](https://Zarinp.al/MyGPT)"\
            f" اگر سوالی دارید، می‌توانید با پشتیبانی تماس بگیرید.\n"
        await update.message.reply_text(reply, parse_mode="Markdown")
    elif 'awaiting_audio' in context.user_data and context.user_data['awaiting_audio']:
        context.user_data['awaiting_audio'] = False
        
        file = update.message.voice or update.message.audio

        if file:
            # Download the audio file
            file_path = await file.get_file()
            path = ast.literal_eval(file_path.to_json())
            # Transcribe the file using AssemblyAI
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(path['file_path'])

            # Send the transcribed text back to the user
            if transcript.status == aai.TranscriptStatus.error:
                await update.message.reply_text(f"Error transcribing audio: {transcript.error}")
            else:
                await update.message.reply_text(f"{transcript.text}")

        else:
            update.message.reply_text("Please send a valid audio file.")

async def handle_text_to_speech(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    # Add logic here to process text to speech
    query.edit_message_text(text="Please send the text to convert to speech.")
