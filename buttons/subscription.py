from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from config import config, create_reply_keyboard
import httpx
from db.MySqlConn import Mysql
import random
import time
from buttons.templates import subscription_plan,desired_plan,subscription_costs


Zarinpal = {
    '1': 'https://zarinp.al/626420',
    '2': 'https://zarinp.al/626422',
    '3': 'https://zarinp.al/626424',
    '4': 'https://zarinp.al/619779',
    '5': 'https://zarinp.al/626405',
    '6': 'https://zarinp.al/626406',
    '7': 'https://zarinp.al/626407',
    '8': 'https://zarinp.al/626408',
    '9': 'https://zarinp.al/626410',
    '10': 'https://zarinp.al/626412',
    '11': 'https://zarinp.al/626413',
    '12': 'https://zarinp.al/626414',
}

class TRX:
    invoice_url = "https://api.plisio.net/api/v1/invoices/new"
    check_url = "https://api.plisio.net/api/v1/operations"
    API_KEY = config['TRX']

    def __init__(self):
        pass
    async def create_invoice(self,price):
        id = random.randint(10000, 99999)
        async with httpx.AsyncClient() as client:
            invoice_params = {
                "order_number": id,
                "currency": "TRX",
                "amount": price,
                "order_name": "test",
                "api_key": self.API_KEY
            }
            response = await client.get(self.invoice_url, params=invoice_params)

        if response.status_code == 200:
            invoice_data = response.json()
            print(invoice_data)
            return invoice_data['data']
        else:
            print(f"Error creating invoice: {response.status_code} - {response.text}")

    async def check_invoice(self, id):
        check_params = {
            "api_key": self.API_KEY,
            "search": id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.check_url, params=check_params)

        if response.status_code == 200:
            return response.json()
        else:
            return 'fail'


        
async def show_subscription_options(update: Update, context: CallbackContext, query=None):
    subscription_keyboard = [
        [InlineKeyboardButton(text="Text Model", callback_data="subscription_text")],
        [InlineKeyboardButton(text="Voice Model", callback_data="subscription_voice")],
        [InlineKeyboardButton(text="Image Model", callback_data="subscription_image")],
    ]

    reply_markup = InlineKeyboardMarkup(subscription_keyboard)
    if query and query.data == "subscription_options":
        await query.edit_message_text(text=desired_plan[context.user_data['lang']], reply_markup=reply_markup)
    else:
        await update.message.reply_text(desired_plan[context.user_data['lang']], reply_markup=reply_markup)

async def show_subscription_plans(update: Update, context: CallbackContext):
    """Show available plans for the selected subscription model."""
    query = update.callback_query
    await query.answer()
    if query.data == "subscription_text":
        plans_keyboard = [
            [InlineKeyboardButton(text="GPT 4o", callback_data="gpt_4")],
            [InlineKeyboardButton(text="GPT 4o mini", callback_data="gpt_4_m")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    elif query.data == "subscription_voice":
        plans_keyboard = [
            [InlineKeyboardButton(text="10 Minutes - 14,900 IR Toman - 5 TRX", callback_data="plan_7")],
            [InlineKeyboardButton(text="20 Minutes - 24,900 IR Toman - 10 TRX", callback_data="plan_8")],
            [InlineKeyboardButton(text="60 Minutes - 59,900 IR Toman 20 TRX", callback_data="plan_9")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    elif query.data == "subscription_image":
        plans_keyboard = [
            [InlineKeyboardButton(text="20 Credits - 14,900 IR Toman - 5 TRX", callback_data="plan_10")],
            [InlineKeyboardButton(text="40 Credits - 24,900 IR Toman - 10 TRX", callback_data="plan_11")],
            [InlineKeyboardButton(text="100 Credits - 49,900 IR Toman - 20 TRX", callback_data="plan_12")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
    elif query.data == "subscription_options":
        await show_subscription_options(update, context, query)
        return
    reply_markup = InlineKeyboardMarkup(plans_keyboard)
    await query.edit_message_text(text=subscription_plan[context.user_data['lang']], reply_markup=reply_markup)

async def gpt(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "gpt_4":
        plans_keyboard = [
            [InlineKeyboardButton(text="Economic Subscription - 49,900 IR Toman - 15 TRX", callback_data="plan_1")],
            [InlineKeyboardButton(text="Normal Subscription - 69,900 IR Toman - 20 TRX", callback_data="plan_2")],
            [InlineKeyboardButton(text="Pro Subscription - 119,900 IR Toman - 35 TRX", callback_data="plan_3")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
        reply = subscription_costs[context.user_data['lang']]
    elif query.data == "gpt_4_m":
        plans_keyboard = [
            [InlineKeyboardButton(text="Economic Subscription - 14,900 IR Toman - 5 TRX", callback_data="plan_4")],
            [InlineKeyboardButton(text="Normal Subscription - 24,900 IR Toman - 8 TRX", callback_data="plan_5")],
            [InlineKeyboardButton(text="Pro Subscription - 49,900 IR Toman - 15 TRX", callback_data="plan_6")],
            [InlineKeyboardButton(text="Back", callback_data="subscription_options")]
        ]
        reply = subscription_costs[context.user_data['lang']]
    
    if query.data == "subscription_options":
        await show_subscription_options(update, context, query)
        return

    reply_markup = InlineKeyboardMarkup(plans_keyboard)
    await query.edit_message_text(text=reply, reply_markup=reply_markup)
    
async def show_payment_options(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    payment_keyboard = [
        [InlineKeyboardButton(text="Pay in IR Rial", callback_data=f"pay_irr_{query.data}")],
        [InlineKeyboardButton(text="Pay with TRON (TRX)", callback_data=f"pay_trx_{query.data}")],
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

    payment_method, plan = query.data.split('_', 2)[1:]
    plan = plan.split('_')[1]

    if payment_method == "irr":
        payment_link = Zarinpal[plan]
    elif payment_method == "trx":
        client = TRX()
        invoice = await client.create_invoice(config['PRICES'][plan])
        payment_link = invoice['invoice_url']
        id = invoice['txn_id']
        context.user_data['trans_id'] = id
    reply_keyboard = [
        [InlineKeyboardButton(text="Done", callback_data=f"conf_{payment_method}_{plan}")]
    ]
    reply_keyboard = InlineKeyboardMarkup(reply_keyboard)
    await query.edit_message_text(text=f"Please complete your payment here:\n {payment_link}\nclick on Done button after you made the payment.", reply_markup=reply_keyboard)

async def confirm_subscription(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    payment_method = query.data.split('_')[1:]
    payment_method, plan = payment_method[0], payment_method[1]

    mysql = Mysql()

    if payment_method == 'trx':
        if 'trans_id' in context.user_data:
            client = TRX()
            response = await client.check_invoice(context.user_data['trans_id'])
            status = response['data']['operations'][0]['status']
            txn_id = response['data']['operations'][0]['txn_id']
            price = int(float(response['data']['operations'][0]['invoice_total_sum']))
            date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            mysql.insertOne("""
                INSERT INTO payments (user_id, plan, price, txn_id, created_at, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, value=[update.effective_user.id, plan, price, txn_id, date_time, status])
            if status == 'completed':
                creds(update.effective_user.id, plan)
                text = "Successful"
            else:
                text = "The payment was unsuccessful"

    elif payment_method == 'irr':
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mysql.insertOne("""
            INSERT INTO payments (user_id, plan, created_at)
            VALUES (%s, %s, %s)
        """, value=[update.effective_user.id, plan, date_time])
        text = "در صورت موفقیت بودن پرداختتون اشتراکتون به زودی فعال میشه!"
    
    mysql.end()

    await query.edit_message_text(text)



def creds(user_id, plan):
    plans ={
        '1': "gpt=gpt+50, set sub=1",
        '2': "gpt=gpt+100, set sub=1",
        '3': "gpt=gpt+200, set sub=1",
        '4': "gpt=gpt+100",
        '5': "gpt=gpt+200",
        '6': "gpt=gpt+500",
        '7': "voice=voice+10",
        '8': "voice=voice+20",
        '9': "voice=voice+60",
        '10': "image=image+20",
        '11': "image=image+40",
        '12': "image=image+100",
        # '13': "gpt=gpt+500",
        # '14': "gpt=gpt+500",
        # '15': "gpt=gpt+500",
    }

    query = f"update users set {plans[plan]} where user_id = {user_id};"

    mysql = Mysql()
    mysql.__query(query)
    mysql.end()