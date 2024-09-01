from telegram import ReplyKeyboardMarkup
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

fh = logging.FileHandler('main.log')

formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(fh)



config = {
    'AI':
        {
            'TYPE': os.getenv('AI_TYPE'),
            'TOKEN': os.getenv('AI_TOKEN')
        },
    'BOT':
        {
            'TOKEN': os.getenv("BOT_TOKEN")
        },
    'MYSQL':
        {
            'DBHOST': os.getenv("DBHOST"),
            'DBUSER': os.getenv("DBUSER"),
            'DBPORT': int(os.getenv("DBPORT")),
            'DBPWD': os.getenv("DBPWD"),
            'DBNAME': os.getenv("DBNAME"),
            'DBCHAR': "utf8mb4"
        },
    'TRX': os.getenv('TRX'),
    'PIC_API_KEY': os.getenv("PIC_API_KEY"),
    'ASS_API_KEY': os.getenv("ASS_API_KEY"),
    'PRICES':
        {
            '1': 15,
            '2': 20,
            '3': 35,
            '4': 5,
            '5': 8,
            '6': 15,
            '7': 5,
            '8': 10,
            '9': 20,
            '10': 5,
            '11': 10,
            '12': 20,
            '13': 25,
            '14': 40,
            '15': 60
        },
    'DEVELOPER_CHAT_ID': 1211842223,
    'TIME_SPAN': 1440
}
DEVELOPER_CHAT_ID= 1211842223
time_span = 1440
notification_channel = config.get("NOTIFICATION_CHANNEL")

CHOOSING, TYPING_REPLY, TYPING_SYS_CONTENT, TYPING_TEXT_FOR_IMAGE, VOICE = range(5)

en_labels = {
    "contact_admin": "🆘Help",
    "start_button": "🚀Start",
    "set_sys_content_button": "🆔Set Role",
    "reset_context_button": "🔃Restart Session",
    "statistics_button": "📈Statistics",
    "switch_role_button": "🙋Switch Roles",
    "language_button": "🔤Language",
    "done_button": "Done",
    "cancel_button": "🚫Cancel",
    "voice_button": "Voice Assistant 🎤",
    "pic_button": "Image Generation🖼",
    "subscription_button": "Subscription 💳",
    "ref_button": "Referral 👤"
}

fa_labels = {
    "contact_admin": "🆘کمک",
    "start_button": "🚀شروع",
    "set_sys_content_button": "🆔تنظیم نقش",
    "reset_context_button": "🔃شروع مجدد مکالمه",
    "statistics_button": "📈آمار",
    "switch_role_button": "🙋تغییر نقش",
    "language_button": "🔤زبان",
    "done_button": "انجام شد",
    "cancel_button": "🚫لغو",
    "voice_button": "دستیار صوتی 🎤",
    "pic_button": "ساخت تصویر 🖼",
    "subscription_button": "اشتراک 💳",
    "ref_button": "دعوت 👤"
}

language_labels = {
    "en": en_labels,
    "fa": fa_labels
}

def create_reply_keyboard(lang: str):
    labels = language_labels[lang]
    reply_keyboard = [
        [labels["language_button"], labels["statistics_button"], labels["switch_role_button"]],
        [labels['voice_button'], labels['pic_button']],
        [labels['subscription_button'], labels['ref_button'], labels["contact_admin"]],
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

create_reply_keyboard('en')

cancel_button = "🚫Cancel"
cancel_keyboard = [[cancel_button]]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)
