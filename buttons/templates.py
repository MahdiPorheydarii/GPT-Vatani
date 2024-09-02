from string import Template

say_help = {
    "en": """
🤖 Bot Features:
1)Chat with ChatGPT: Engage in conversations with the AI, ask questions, and receive informative responses.
You can:
   - use voice messages
   - attach pictures 
2)Text to Speech: Convert written text into natural-sounding speech.
3)Speech to Text: Send audio messages, and the bot will transcribe them into text.
4)Generate Images: Describe any scene or idea, and the bot will create a corresponding image for you.

🎁 Free GPT-4o Mini in Groups:
If you add this bot to a group with more than 20 members, you can use the GPT-4o Mini model for free in that group! Here’s how:
1)Add the bot to the group.
2)Type /start to activate the bot in the group.
3)Use /prompt followed by your query to interact with GPT-4o Mini.

👥 Referral Program:
Invite friends to use this bot and earn rewards!
For every successful referral, you get closer to unlocking exclusive features.

🧠 Memory Functionality:
Free Users: The bot remembers only your last message during a conversation.
Subscribers: Enjoy an enhanced experience where the bot remembers your last 3 messages, allowing for more contextual and meaningful conversations.

📢 Channel for Updates:
Stay updated with the latest features and improvements by joining our official channel: [@MyGPT_Channel]
📞 Support:
Need help? Contact our support team at: [@MyGPT_PR]
""",
    "fa": """
🤖 ویژگی‌های ربات:

۱)گفتگو با ChatGPT: با این هوش مصنوعی گفتگو کنید، سوالات خود را بپرسید و پاسخ‌های اطلاعاتی دریافت کنید. شما می‌توانید:
- از پیام‌های صوتی استفاده کنید
- تصاویر ضمیمه کنید
۲)تبدیل متن به گفتار: متن نوشته‌شده را به گفتاری طبیعی تبدیل کنید.
۳)تبدیل گفتار به متن: پیام‌های صوتی ارسال کنید و ربات آن‌ها را به متن تبدیل می‌کند.
۴)تولید تصاویر: هر صحنه یا ایده‌ای را توصیف کنید و ربات تصویری مطابق با آن برای شما ایجاد خواهد کرد.

🎁 استفاده رایگان از GPT-4o Mini در گروه‌ها: اگر این ربات را به گروهی با بیش از ۲۰ عضو اضافه کنید، می‌توانید به صورت رایگان از مدل GPT-4o Mini در آن گروه استفاده کنید! مراحل:

۱)ربات را به گروه اضافه کنید.
۲)دستور /start را برای فعال‌سازی ربات در گروه تایپ کنید.
۳)از دستور /prompt همراه با درخواست خود برای تعامل با GPT-4o Mini استفاده کنید.

👥 برنامه ارجاع: دوستان خود را به استفاده از این ربات دعوت کنید و پاداش بگیرید! با هر ارجاع موفق، به باز کردن ویژگی‌های انحصاری نزدیک‌تر می‌شوید.

🧠 قابلیت حافظه:

کاربران رایگان: ربات فقط آخرین پیام شما را در حین مکالمه به خاطر می‌آورد.
مشترکین: از تجربه بهبود یافته‌ای لذت ببرید که در آن ربات آخرین ۳ پیام شما را به خاطر می‌آورد، که منجر به مکالمات بیشتر و معنادارتر می‌شود.

📢 کانال برای به‌روزرسانی‌ها: با پیوستن به کانال رسمی ما از آخرین ویژگی‌ها و بهبودها مطلع شوید: [@MyGPT_Channel]

📞 پشتیبانی: نیاز به کمک دارید؟ با تیم پشتیبانی ما تماس بگیرید: [@MyGPT_PR]
"""}

role = {
    "en": Template("""
As an AI assistant, my role is now set as🤖：:

**$system_content**

Now you can send my new role directly!

In case you want to stop this setting, just reply: `cancel`‍🤝‍
"""),
    "fa": Template("""
نقش فعلی دستیار هوش مصنوعی من به عنوان 🤖 تنظیم شده است:

**$system_content**

اکنون می‌توانید نقش جدید من را مستقیماً ارسال کنید!

در صورت تمایل به لغو این تنظیمات، فقط پاسخ دهید: `cancel` ‍🤝‍
""")}

context_info = {"en": """
Each time you ask a question, the AI will provide an answer considering your recent conversations, untill it restarts!

Your conversation history has now been cleared, and you can start asking questions again!
""", "fa": """
هر بار که سوالی بپرسید، هوش مصنوعی با در نظر گرفتن آخرین مکالمات شما به شما پاسخ خواهد داد، تا زمانی که آن‌را ریست کنید!

تاریخچه مکالمات شما اکنون پاک شده است و می‌توانید دوباره شروع به پرسش کنید!
"""}

identity_confirmed = {"en": """
The new AI assistant identity has been confirmed.
I will answer your questions based on this new identity.
You can start asking questions now!
""", "fa": """
شناسه جدید دستیار هوش مصنوعی تایید شد.
من به سوالات شما بر اساس این هویت جدید پاسخ خواهم داد.
شما اکنون می‌توانید شروع به پرسش کنید!
"""}

statistics_response = {"en": Template("""
Hi $user!

Your current Credit is as follows:

GPT model: $gpt Tokens
    model: $model
Image Model: $image Tokens
Voice Model: $voice Minutes

Have a nice day!🎉
"""), "fa": Template("""
سلام $user!

وضعیت فعلی اعتبار شما شما به شرح زیر است:

مدل متنی: $gpt توکن                     
    نوع مدل: $model
مدل تصویری: $image توکن
مدل صوتی: $voice دقیقه

روز خوبی داشته باشید!🎉
""")}

token_limit = {
    "en": Template("""
$answer

--------------------------------------

The length of the answer has exceeded your current maximum limit of $max_token tokens per answer.

Please contact @MyGPT_PR for more Tokens!✅
"""),
    "fa": Template("""
$answer

--------------------------------------

طول پاسخ از حداکثر مجاز فعلی شما به تعداد $max_token توکن در هر پاسخ فراتر رفته است.

لطفاً با @MyGPT_PRبرای دریافت توکن‌های بیشتر تماس بگیرید! ✅
""")}

give_referral_link = {
    "en": Template("""
Here's your unique referral link: $referral_link. Share it with friends to earn rewards!
Every successful referral brings you closer to unlocking special features\n
Referrals count: $referral_count
"""),
    "fa": Template("""این لینک ارجاع منحصربه‌فرد شماست: $referral_link. آن را با دوستان خود به اشتراک بگذارید تا جوایز دریافت کنید!
هر ارجاع موفقیت‌آمیز شما را به باز کردن ویژگی‌های ویژه نزدیک‌تر می‌کند\n
تعداد ارجاع : $referral_count
""")
}




referral_limit = {
    "en": """
It looks like you don't have enough referrals to complete this exchange.
You need more referrals to get the GPT Mini feature. Keep sharing your referral link to unlock more rewards!
""",
    "fa": """
به نظر می‌رسد که شما تعداد کافی ارجاع برای این مبادله را ندارید.
شما به ارجاع بیشتر نیاز دارید تا ویژگی GPT Mini را فعال کنید. لینک ارجاع خود را بیشتر به اشتراک بگذارید تا جوایز بیشتری دریافت کنید!
"""}

referral_update = {
    "en": """

Success! Your credits have been applied.
Enjoy your new features and keep sharing your referral link to unlock even more rewards!
""",
    "fa": """
پیام: "موفقیت! امتیازهای شما اعمال شدند.
از ویژگی‌های جدید خود لذت ببرید و لینک ارجاع خود را به اشتراک بگذارید تا جوایز بیشتری کسب کنید!
"""}

exchange_referrals_4o_mini = {
    "en": """

You've successfully exchanged 5 referrals for GPT 4o Mini credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
""",
    "fa": """
شما با موفقیت ۵ ارجاع را برای دریافت اعتبار GPT 4o Mini مبادله کرده‌اید!
از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.
"""}

exchange_referrals_voice_model = {
    "en": """

You've successfully exchanged 5 referrals with 10 voice model credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
""",
    "fa": """شما با موفقیت ۵ ارجاع را با ۱۰ اعتبار مدل صوتی مبادله کرده‌اید!
    از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.

"""}

exchange_referrals_image_model = {
    "en": """

You've successfully exchanged 5 referrals with 10 image model credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
""",
    "fa": """شما با موفقیت ۵ ارجاع را با ۱۰ اعتبار مدل تصویری مبادله کرده‌اید!
    از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.

"""}

reply_text_after_canceling = {
    "en": """

You can continue to ask me questions now.
""",
    "fa": """
    اکنون می‌توانید به پرسیدن سوالات خود ادامه دهید.

"""}

text_to_image = {
    "en": """
Please provide the text you'd like to use for creating an image.
Please only describe in English.
""",
    "fa": """
    لطفاً متنی که می‌خواهید برای ساخت تصویر استفاده کنید را ارسال کنید.
    لطفا توضیحات رو انگلیسی بگید.
"""}

failed_to_generate_image = {
    
    "en": """
Failed to generate the image. Please try again.
""",
    "fa": """
ایجاد تصویر با شکست مواجه شد. لطفاً دوباره تلاش کنید.
"""}

valid_text_to_img = {
    
    "en": """
Please send a valid text prompt.
    """,
    "fa": """
لطفاً یک متن معتبر برای درخواست ارسال کنید.
    """
}
voice_back_respond = {
    
    "en": """
Back to the main menu
""",
    "fa": """
بازگشت به منوی اصلی
"""
}

voice_tts_respond = {

    "en": """
Please enter the text you want to convert to speech.
""",
    "fa": """
"لطفاً متنی که می‌خواهید به گفتار تبدیل شود را وارد کنید"""

}
voice_reply_text = {

    "en": """
Please choose one option:
""",
    "fa": """
لطفاً یکی از گزینه ها را انتخاب کنید"""

}

handle_stt = {

    "en": """
Please send an audio file to transcribe.
""",
    "fa": """
    لطفاً یک فایل صوتی برای تبدیل به متن ارسال کنید"""

}
voice_text_count_limit = {
    "en": """
Free usage limit reached😶‍🌫
You have reached the limit of 3 free uses of the bot. To continue using the services, please purchase one of our subscriptions.
[Purchase Subscription](https://Zarinp.al/MyGPT)
If you have any questions, you can contact support at @MyGPT_PR.
""",
    "fa": """
محدودیت استفاده رایگان😶‍🌫
شما به حد مجاز ۳ بار استفاده رایگان از ربات رسیده‌اید. برای ادامه استفاده از خدمات، لطفاً یکی از اشتراک‌های ما را تهیه کنید.
[خرید اشتراک](https://Zarinp.al/MyGPT)
اگر سوالی دارید، می‌توانید با پشتیبانی @MyGPT_PR تماس بگیرید.
"""
}

voice_min_limit = {
    "en": """
The maximum audio file duration for a regular user is 60 seconds.
To use this feature, please reduce the duration of your file or purchase a subscription.
[Purchase Subscription](https://Zarinp.al/MyGPT)
If you have any questions, you can contact support at @MyGPT_PR.
""",

    "fa": """
حداکثر مدت زمان فایل صوتی برای کاربر معمولی ۶۰ ثانیه است.
برای استفاده از این بخش، مدت زمان فایل خود را کاهش دهید یا اشتراک تهیه کنید.
[خرید اشتراک](https://Zarinp.al/MyGPT)
اگر سوالی دارید، می‌توانید با پشتیبانی @MyGPT_PR تماس بگیرید.
"""
}
error_transcribing_audio = {
    

    "en": Template("""
Error transcribing audio: $transcript.error
"""),
    "fa": Template("""
    خطا در تبدیل صدا به متن: $transcript_error""")

}

invalid_audio_file = {
    

    "en": """
Please send a valid audio file.
""",
    "fa": """
    .لطفاً یک فایل صوتی معتبر ارسال کنید"""

}
handle_text_to_speech = {
    

    "en": """
Please enter the text you want to convert to speech.
""",
    "fa": """
لطفا یک متن برای تبدیل به فایل صوتی ارسال کنید."""

}
text_min_limit = {
    "en": Template("""
The maximum number of characters for a regular user is 200.
To use this feature, please reduce the number of characters in your message or purchase a subscription.
[Purchase Subscription](https://Zarinp.al/MyGPT)
If you have any questions, you can contact support at @MyGPT_PR.
"""),
    
    "fa": Template("""
حداکثر تعداد کاراکتر برای کاربر معمولی ۲۰۰ عدد است.
برای استفاده از این بخش، تعداد کاراکتر پیام خود را کاهش دهید یا اشتراک تهیه کنید.
[خرید اشتراک](https://Zarinp.al/MyGPT)
اگر سوالی دارید، می‌توانید با پشتیبانی @MyGPT_PR تماس بگیرید.
""")
}
appropriate_question = {
    "en": Template("""
$answer

As an AI assistant, please ask me appropriate questions!
For more help, please contact @MyGPT_PR ✔️)
"""),

    "fa": Template("""
$answer

به عنوان یک دستیار هوش مصنوعی، لطفاً سوالات مناسب بپرسید!
برای کمک بیشتر، لطفاً با @MyGPT_PR تماس بگیرید.✔️)
""")
}











