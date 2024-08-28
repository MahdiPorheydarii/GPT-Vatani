from string import Template

say_help = {
    "en": """
If anything went wrong, just type: /start or restart the Bot to reset it.

or 

contact 👉 @MyGPT_PR 👈 for more help!
""",
    "fa": """
اگر مشکلی پیش آمد، فقط تایپ کنید: /start یا ربات را ریستارت کنید تا تنظیمات به حالت اولیه بازگردد.

یا

با 👉 @MyGPT_PR 👈 برای کمک بیشتر تماس بگیرید!
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

GPT-4o mini: $gpt Tokens
Image Model: $image Tokens
Voice Model: $voice Tokens

Have a nice day!🎉
"""), "fa": Template("""
سلام $user!

وضعیت فعلی اعتبار شما شما به شرح زیر است:

GPT-4o mini: $gpt توکن
مدل تصویری: $image توکن
مدل صوتی: $voice توکن

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

# generating = {
#     "en": Template("""

# """),
#     "fa": Template("""
# درحال دریافت پاسخ.
# """)}


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
    "en": Template("""

It looks like you don't have enough referrals to complete this exchange.
You need more referrals to get the GPT Mini feature. Keep sharing your referral link to unlock more rewards!
"""),
    "fa": Template("""
به نظر می‌رسد که شما تعداد کافی ارجاع برای این مبادله را ندارید.
شما به ارجاع بیشتر نیاز دارید تا ویژگی GPT Mini را فعال کنید. لینک ارجاع خود را بیشتر به اشتراک بگذارید تا جوایز بیشتری دریافت کنید!
""")}

referral_update = {
    "en": Template("""

Success! Your credits have been applied.
Enjoy your new features and keep sharing your referral link to unlock even more rewards!
"""),
    "fa": Template("""
پیام: "موفقیت! امتیازهای شما اعمال شدند.
از ویژگی‌های جدید خود لذت ببرید و لینک ارجاع خود را به اشتراک بگذارید تا جوایز بیشتری کسب کنید!
""")}

exchange_referrals_4o_mini = {
    "en": Template("""

You've successfully exchanged 5 referrals for GPT 4.0 Mini credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
"""),
    "fa": Template("""
شما با موفقیت ۵ ارجاع را برای دریافت اعتبار GPT 4.0 Mini مبادله کرده‌اید!
از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.
""")}

exchange_referrals_voice_model = {
    "en": Template("""

You've successfully exchanged 5 referrals with 10 voice model credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
"""),
    "fa": Template("""شما با موفقیت ۵ ارجاع را با ۱۰ اعتبار مدل صوتی مبادله کرده‌اید!
    از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.

""")}

exchange_referrals_image_model = {
    "en": Template("""

You've successfully exchanged 5 referrals with 10 image model credits!
Enjoy your new features and continue sharing your referral link to unlock even more rewards.
"""),
    "fa": Template("""شما با موفقیت ۵ ارجاع را با ۱۰ اعتبار مدل تصویری مبادله کرده‌اید!
    از ویژگی‌های جدید خود لذت ببرید و با اشتراک‌گذاری لینک ارجاع خود، جوایز بیشتری کسب کنید.

""")}

reply_text_after_canceling = {
    "en": Template("""

You can continue to ask me questions now.
"""),
    "fa": Template("""
    اکنون می‌توانید به پرسیدن سوالات خود ادامه دهید.

""")}

text_to_image = {
    "en": Template("""
Please provide the text you'd like to use for creating an image.
"""),
    "fa": Template("""
    لطفاً متنی که می‌خواهید برای ساخت تصویر استفاده کنید را ارسال کنید.
""")}

failed_to_generate_image = {
    
    "en": Template("""
Failed to generate the image. Please try again.
"""),
    "fa": Template("""
ایجاد تصویر با شکست مواجه شد. لطفاً دوباره تلاش کنید.
""")}

valid_text_to_img = {
    
    "en": """
Please send a valid text prompt.
    """,
    "fa": """
لطفاً یک متن معتبر برای درخواست ارسال کنید.
    """
}

