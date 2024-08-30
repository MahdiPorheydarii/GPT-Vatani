from telegram import ReplyKeyboardMarkup
import logging
import yaml

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

fh = logging.FileHandler('main.log')

formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(fh)

# Load data from config.yaml file
with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
time_span = config["TIME_SPAN"]
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
    "voice_button": "Voice 🎤",
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
    "voice_button": "صدا 🎤",
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
        [labels["language_button"], labels["reset_context_button"], labels["switch_role_button"]],
        [labels["statistics_button"], labels['voice_button'], labels['pic_button']],
        [labels['subscription_button'], labels['ref_button'], labels["contact_admin"]],
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

create_reply_keyboard('en')

cancel_button = "🚫Cancel"
cancel_keyboard = [[cancel_button]]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)
