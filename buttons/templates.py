from string import Template

say_help = {
    "en": """
If anything went wrong, just type: /start or restart the Bot to reset it.

or 

contact 👉 @MahdiPorheydari 👈 for more help!
""",
    "fa": """
اگر مشکلی پیش آمد، فقط تایپ کنید: /start یا ربات را ریستارت کنید تا تنظیمات به حالت اولیه بازگردد.

یا

با 👉 @MahdiPorheydari 👈 برای کمک بیشتر تماس بگیرید!
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

context_info = {"en": Template("""
Each time you ask a question, the AI will provide an answer considering your most recent $context_count conversations!

Your conversation history has now been cleared, and you can start asking questions again!
"""), "fa": Template("""
هر بار که سوالی بپرسید، هوش مصنوعی با در نظر گرفتن آخرین $context_count مکالمات شما به شما پاسخ خواهد داد!

تاریخچه مکالمات شما اکنون پاک شده است و می‌توانید دوباره شروع به پرسش کنید!
""")}

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

Your current Token usage is as follows:

Query: $prompt_tokens Tokens
Answer: $completion_tokens Tokens
Total: $total_tokens Tokens

Have a nice day!🎉
"""), "fa": Template("""
سلام $user!

وضعیت فعلی استفاده از توکن شما به شرح زیر است:

پرسش: $prompt_tokens توکن
پاسخ: $completion_tokens توکن
مجموع: $total_tokens توکن

روز خوبی داشته باشید!🎉
""")}

token_limit = {
    "en": Template("""
$answer

--------------------------------------

The length of the answer has exceeded your current maximum limit of $max_token tokens per answer.

Please contact @MahdiPorheydari for more Tokens!✅
"""),
    "fa": Template("""
$answer

--------------------------------------

طول پاسخ از حداکثر مجاز فعلی شما به تعداد $max_token توکن در هر پاسخ فراتر رفته است.

لطفاً با @MahdiPorheydari برای دریافت توکن‌های بیشتر تماس بگیرید! ✅
""")}
