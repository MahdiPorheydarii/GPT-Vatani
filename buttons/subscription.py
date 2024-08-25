from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

async def show_subscription_options(update: Update, context: CallbackContext):

    subscription_keyboard = [
        [InlineKeyboardButton(text="Text Model", callback_data="subscription_text")],
        [InlineKeyboardButton(text="Voice Model", callback_data="subscription_voice")],
        [InlineKeyboardButton(text="Image Model", callback_data="subscription_image")],
        [InlineKeyboardButton(text="All in One", callback_data="subscription_all")]
    ]

    reply_markup = InlineKeyboardMarkup(subscription_keyboard)
    await update.message.reply_text('Please choose your desired plan:', reply_markup=reply_markup)


async def show_subscription_plans(update: Update, context: CallbackContext):
    """Show available plans for the selected subscription model."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "subscription_text":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_text_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_text_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_text_1y")]
        ]
    if query.data == "subscription_voice":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_voice_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_voice_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_voice_1y")]
        ]
    if query.data == "subscription_image":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_image_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_image_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_image_1y")]
        ]
    if query.data == "subscription_all":
        plans_keyboard = [
            [InlineKeyboardButton(text="1 Month - 100,000 IR Rial", callback_data="plan_all_1m")],
            [InlineKeyboardButton(text="3 Months - 250,000 IR Rial", callback_data="plan_all_3m")],
            [InlineKeyboardButton(text="1 Year - 900,000 IR Rial", callback_data="plan_all_1y")]
        ]
    
    reply_markup = InlineKeyboardMarkup(plans_keyboard)
    await query.edit_message_text(text="Choose your subscription plan:", reply_markup=reply_markup)


async def show_payment_options(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    payment_keyboard = [
        [InlineKeyboardButton(text="Pay in IR Rial", callback_data="pay_irr")],
        [InlineKeyboardButton(text="Pay with TRON (TRX)", callback_data="pay_trx")]
    ]
    
    reply_markup = InlineKeyboardMarkup(payment_keyboard)
    await query.edit_message_text(text="Choose your payment method:", reply_markup=reply_markup)


async def generate_payment_link(update: Update, context: CallbackContext):
    """Generate and send a payment link."""
    query = update.callback_query
    await query.answer()

    if query.data == "pay_irr":
        # Generate payment link for IR Rial
        payment_link = "https://yourpaymentgateway.com/ir-rial-payment"
    elif query.data == "pay_trx":
        # Generate payment link for TRON (TRX)
        payment_link = "https://yourpaymentgateway.com/trx-payment"
    
    await query.edit_message_text(text=f"Please complete your payment: {payment_link}")


async def confirm_subscription(update: Update, context: CallbackContext):
    """Activate the user's subscription after payment confirmation."""
    # This would be called after payment confirmation
    await update.message.reply_text("Thank you! Your subscription is now active.")
