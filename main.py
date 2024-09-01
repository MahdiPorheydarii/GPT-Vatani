from db.MySqlConn import config
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PicklePersistence,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)
from config import (
    language_labels,
    CHOOSING, TYPING_REPLY, TYPING_SYS_CONTENT, TYPING_TEXT_FOR_IMAGE, VOICE
)
from buttons.inline import (
    show_chat_modes_handle,
    show_chat_modes_callback_handle,
    set_chat_mode_handle,
    cancel_chat_mode_handle,
)
from buttons.subscription import (
    show_payment_options,
    show_subscription_options,
    show_subscription_plans,
    generate_payment_link,
    gpt,
    confirm_subscription
)
from buttons.language import show_languages, show_languages_callback_handle
from buttons.help import helper
from buttons.start import start, start_group
from buttons.role import set_system_content, reset_context, set_system_content_handler
from buttons.statistics import statistics
from buttons.voice import transcribe_audio, voice_options, tts, handle_voice, choose
from buttons.pic import handle_text_to_pic, generate_pic
from chat.handler import answer_handler, group_handler
from buttons.others import done, error_handler
from buttons.ref import show_referral_info, exchange, exchange_handler


from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

def main() -> None:
    persistence = PicklePersistence(filepath='conversationbot')
    application = Application.builder().token(config["BOT"]["TOKEN"]).persistence(persistence).build()

    en_labels = language_labels["en"]
    fa_labels = language_labels["fa"]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, filters.ChatType.PRIVATE), 
                      CommandHandler('start', start_group, filters.ChatType.GROUP | filters.ChatType.SUPERGROUP)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex(f'^({en_labels["contact_admin"]}|{fa_labels["contact_admin"]})$') & filters.ChatType.PRIVATE, helper),
                MessageHandler(filters.Regex(f'^({en_labels["start_button"]}|{fa_labels["start_button"]}|/start|Start|شروع)$') & filters.ChatType.PRIVATE & ~filters.ChatType.GROUP, start),
                MessageHandler(filters.Regex(f'^(/start)$') & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP), start_group),
                MessageHandler(filters.Regex(f'^({en_labels["language_button"]}|{fa_labels["language_button"]})$') & filters.ChatType.PRIVATE, show_languages),
                MessageHandler(filters.Regex(f'^({en_labels["reset_context_button"]}|{fa_labels["reset_context_button"]})$') & filters.ChatType.PRIVATE, reset_context),
                MessageHandler(filters.Regex(f'^({en_labels["set_sys_content_button"]}|{fa_labels["set_sys_content_button"]})$') & filters.ChatType.PRIVATE, set_system_content),
                MessageHandler(filters.Regex(f'^({en_labels["statistics_button"]}|{fa_labels["statistics_button"]})$') & filters.ChatType.PRIVATE, statistics),
                MessageHandler(filters.Regex(f'^({en_labels["switch_role_button"]}|{fa_labels["switch_role_button"]})$') & filters.ChatType.PRIVATE, show_chat_modes_handle),
                MessageHandler(filters.Regex(f'^({en_labels["voice_button"]}|{fa_labels["voice_button"]})$') & filters.ChatType.PRIVATE, voice_options),
                MessageHandler(filters.Regex(f'^({en_labels["pic_button"]}|{fa_labels["pic_button"]})$') & filters.ChatType.PRIVATE, handle_text_to_pic),
                MessageHandler(filters.Regex(f'^({en_labels["subscription_button"]}|{fa_labels["subscription_button"]})$') & filters.ChatType.PRIVATE, show_subscription_options),
                MessageHandler(filters.Regex(f'^({en_labels["ref_button"]}|{fa_labels["ref_button"]})$') & filters.ChatType.PRIVATE, show_referral_info),
                MessageHandler(filters.ChatType.PRIVATE & (filters.TEXT | filters.VOICE | filters.PHOTO), answer_handler),
                CommandHandler('prompt', group_handler, filters = filters.ChatType.GROUP | filters.ChatType.SUPERGROUP),
                MessageHandler(filters.Regex(f'^(/prompt)$') & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP), group_handler),
            ],
            TYPING_REPLY: [
                MessageHandler(filters.Regex(f'^({en_labels["contact_admin"]}|{fa_labels["contact_admin"]})$'), helper),
                MessageHandler(filters.Regex(f'^({en_labels["start_button"]}|{fa_labels["start_button"]}|/start|Start|شروع)$'), start),
                MessageHandler(filters.Regex(f'^({en_labels["language_button"]}|{fa_labels["language_button"]})$'), show_languages),
                MessageHandler(filters.Regex(f'^({en_labels["reset_context_button"]}|{fa_labels["reset_context_button"]})$'), reset_context),
                MessageHandler(filters.Regex(f'^({en_labels["set_sys_content_button"]}|{fa_labels["set_sys_content_button"]})$'), set_system_content),
                MessageHandler(filters.Regex(f'^({en_labels["statistics_button"]}|{fa_labels["statistics_button"]})$'), statistics),
                MessageHandler(filters.Regex(f'^({en_labels["switch_role_button"]}|{fa_labels["switch_role_button"]})$'), show_chat_modes_handle),
                MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handler),
            ],
            TYPING_SYS_CONTENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_system_content_handler),
            ],
            TYPING_TEXT_FOR_IMAGE: [
                MessageHandler(filters.TEXT, generate_pic),
            ],
            VOICE: [
                MessageHandler(filters.TEXT, tts),
                MessageHandler(filters.VOICE | filters.AUDIO, transcribe_audio),
                CallbackQueryHandler(choose, pattern='^vice_back')
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(f'^({en_labels["done_button"]}|{fa_labels["done_button"]})$'), done)],
        name="my_conversation",
        persistent=True,
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_voice, pattern="^voice_"))
    application.add_handler(CallbackQueryHandler(show_chat_modes_callback_handle, pattern="^show_chat_modes"))
    application.add_handler(CallbackQueryHandler(set_chat_mode_handle, pattern="^set_chat_mode"))
    application.add_handler(CallbackQueryHandler(cancel_chat_mode_handle, pattern="^cancel"))
    application.add_handler(CallbackQueryHandler(show_languages_callback_handle, pattern="^lang"))
    application.add_handler(CallbackQueryHandler(show_subscription_plans, pattern="^subscription_"))
    application.add_handler(CallbackQueryHandler(gpt, pattern="^gpt_"))
    application.add_handler(CallbackQueryHandler(generate_payment_link, pattern="^pay_"))
    application.add_handler(CallbackQueryHandler(exchange_handler, pattern="^exc_"))
    application.add_handler(CallbackQueryHandler(exchange, pattern="^ex"))
    application.add_handler(CallbackQueryHandler(show_payment_options, pattern="^plan_"))
    application.add_handler(CallbackQueryHandler(confirm_subscription, pattern="^conf"))

    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
