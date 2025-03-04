from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton)
import yaml
import time

from db.MySqlConn import Mysql
from config import create_reply_keyboard


async def show_chat_modes_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    if lang:
        text, inline_reply_markup = get_chat_mode_menu(0, lang)
        await update.message.reply_text(text, reply_markup=inline_reply_markup, parse_mode=ParseMode.HTML)
    else:
        mysql = Mysql()
        user = mysql.getOne("select lang from users where user_id=%s", update.effective_user.id)
        mysql.end()
        lang = user.get('lang')
        await update.message.reply_text(text, reply_markup=inline_reply_markup, parse_mode=ParseMode.HTML)


with open("chat_modes.yml", encoding='utf-8') as f:
    chat_modes = yaml.load(f, Loader=yaml.FullLoader)


def get_chat_mode_menu(page_index: int, lang: str):
    n_chat_modes_per_page = 5
    text = f"Select <b>chat mode</b> ({len(chat_modes)} modes available):" if lang == "en" else f"انتخاب <b>حالت چت</b> ({len(chat_modes)} حالت موجود است):"

    # buttons
    chat_mode_keys = list(chat_modes.keys())
    page_chat_mode_keys = chat_mode_keys[page_index * n_chat_modes_per_page:(page_index + 1) * n_chat_modes_per_page]

    keyboard = []
    for chat_mode_key in page_chat_mode_keys:
        name = chat_modes[chat_mode_key]["name"][lang]  # Use the appropriate language for the name
        keyboard.append([InlineKeyboardButton(name, callback_data=f"set_chat_mode|{chat_mode_key}")])

    # pagination
    if len(chat_mode_keys) > n_chat_modes_per_page:
        is_first_page = (page_index == 0)
        is_last_page = ((page_index + 1) * n_chat_modes_per_page >= len(chat_mode_keys))

        if is_first_page:
            keyboard.append([
                InlineKeyboardButton("»", callback_data=f"show_chat_modes|{page_index + 1}")
            ])
        elif is_last_page:
            keyboard.append([
                InlineKeyboardButton("«", callback_data=f"show_chat_modes|{page_index - 1}"),
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("«", callback_data=f"show_chat_modes|{page_index - 1}"),
                InlineKeyboardButton("»", callback_data=f"show_chat_modes|{page_index + 1}")
            ])
    keyboard.append([InlineKeyboardButton("🚫Cancel", callback_data="cancel")])

    inline_reply_markup = InlineKeyboardMarkup(keyboard)

    return text, inline_reply_markup


async def show_chat_modes_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    page_index = int(query.data.split("|")[1])
    if page_index < 0:
        return
    lang = context.user_data['lang']
    if lang:
        text, markup = get_chat_mode_menu(page_index, lang)
        try:
            await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
        except BadRequest as e:
            if str(e).startswith("Message is not modified"):
                pass
    else:
        mysql = Mysql()
        user = mysql.getOne("select lang from users where user_id=%s", update.effective_user.id)
        mysql.end()
        lang = user.get('lang')
        text, markup = get_chat_mode_menu(page_index, lang)
        try:
            await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
        except BadRequest as e:
            if str(e).startswith("Message is not modified"):
                pass


async def set_chat_mode_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    nick_name = update.effective_user.full_name

    query = update.callback_query
    await query.answer()

    system_content = query.data.split("|")[1]

    mysql = Mysql()
    user = mysql.getOne("select lang from users where user_id=%s", user_id)

    mysql.update("update users set system_content=%s, nick_name=%s where user_id=%s",
                 (chat_modes[system_content]['prompt_start'], nick_name,
                  user_id))
    reset_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mysql.update("update records set reset_at=%s where user_id=%s and reset_at is null", (reset_at, user_id))
    mysql.end()

    await context.bot.send_message(
        update.callback_query.message.chat.id,
        f"{chat_modes[system_content]['welcome_message'][user.get('lang')]}",
        parse_mode=ParseMode.HTML, reply_markup=create_reply_keyboard(user["lang"])
    )


async def cancel_chat_mode_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data['lang']
    if lang:
        await context.bot.send_message(
            update.callback_query.message.chat.id,
            text="Cancelled. \nYou can continue to ask me questions now.",
            parse_mode=ParseMode.HTML, reply_markup=create_reply_keyboard(lang)
        )
    else:
        mysql = Mysql()
        user = mysql.getOne("select lang from users where user_id=%s", update.effective_user.id)
        mysql.end()
        lang = user.get('lang')
        await context.bot.send_message(
            update.callback_query.message.chat.id,
            text="Cancelled. \nYou can continue to ask me questions now.",
            parse_mode=ParseMode.HTML, reply_markup=create_reply_keyboard(lang)
        )