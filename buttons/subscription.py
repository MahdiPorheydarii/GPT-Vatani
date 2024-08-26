from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

async def show_subscription_options(update: Update, context: CallbackContext, query = None):

    subscription_keyboard = [
        [InlineKeyboardButton(text="Text Model", callback_data="subscription_text")],
        [InlineKeyboardButton(text="Voice Model", callback_data="subscription_voice")],
        [InlineKeyboardButton(text="Image Model", callback_data="subscription_image")],
        [InlineKeyboardButton(text="All in One", callback_data="subscription_all")],
    ]
    reply_markup = InlineKeyboardMarkup(subscription_keyboard)
    if query and query.data == "subscription_options":
        await query.edit_message_text(text="Please choose your desired plan:", reply_markup=reply_markup)
    else:
        await update.message.reply_text('Please choose your desired plan:', reply_markup=reply_markup)


async def show_subscription_plans(update: Update, context: CallbackContext):
    """Show available plans for the selected subscription model."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "subscription_text":
        plans_keyboard = [
            [InlineKeyboardButton(text="GPT 4o - Economic Subscription - 49,900 IR Toman", callback_data="plan_text_11")],
            [InlineKeyboardButton(text="GPT 4o - Normal Subscription - 59,900 IR Toman", callback_data="plan_text_12")],
            [InlineKeyboardButton(text="GPT 4o - Pro Subscription - 69,900 IR Toman", callback_data="plan_text_13")],
            [InlineKeyboardButton(text="GPT 4o-mini - Economic Subscription - 17,900 IR Toman", callback_data="plan_text_21")],
            [InlineKeyboardButton(text="GPT 4o-mini - Normal Subscription - 22,900 IR Toman", callback_data="plan_text_22")],
            [InlineKeyboardButton(text="GPT 4o-mini - Pro Subscription - 29,900 IR Toman", callback_data="plan_text_23")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    if query.data == "subscription_voice":
        plans_keyboard = [
            [InlineKeyboardButton(text="", callback_data="plan_voice_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_voice_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_voice_1y")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    if query.data == "subscription_image":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_image_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_image_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_image_1y")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    if query.data == "subscription_all":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_all_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_all_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_all_1y")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    if query.data == "subscription_options":
        await show_subscription_options(update, context, query)
        return
    reply_markup = InlineKeyboardMarkup(plans_keyboard)
    await query.edit_message_text(text="Choose your subscription plan:", reply_markup=reply_markup)


async def show_payment_options(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    # if query.data == "plan_image"
    payment_keyboard = [
        [InlineKeyboardButton(text="Pay in IR Rial", callback_data="pay_irr")],
        [InlineKeyboardButton(text="Pay with TRON (TRX)", callback_data="pay_trx")],
        [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
    ]
    if query.data == "subscription_options":
        await show_subscription_options(update, context, query)
        return
    
    reply_markup = InlineKeyboardMarkup(payment_keyboard)
    await query.edit_message_text(text="Choose your payment method:", reply_markup=reply_markup)


async def generate_payment_link(update: Update, context: CallbackContext):
    """Generate and send a payment link."""
    query = update.callback_query
    await query.answer()

    if query.data == "pay_irr":
        payment_link = "https://Zarinp.al/MyGPT.ir"
    elif query.data == "pay_trx":
        # Generate payment link for TRON (TRX)
        # payment_link = "https://yourpaymentgateway.com/trx-payment"
        pass
    
    await query.edit_message_text(text=f"Please complete your payment: ")


async def confirm_subscription(update: Update, context: CallbackContext):
    """Activate the user's subscription after payment confirmation."""
    # This would be called after payment confirmation
    await update.message.reply_text("Thank you! Your subscription is now active.")
