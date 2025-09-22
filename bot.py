import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

# توکن‌های بات و OpenAI
TELEGRAM_TOKEN = '8251776630:AAEimkTlsAHuhnCDS-dOXV6rjUcVVY_0Ct8'
OPENAI_API_KEY = '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'

# تنظیم کلاینت OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# فعال کردن لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('سلام! من بات هوش مصنوعی‌ام. هر سوالی داری بپرس!')

async def handle_message(update: Update, context):
    user_message = update.message.text
    try:
        # فراخوانی مدل OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logger.error(f"خطا در ارتباط با OpenAI: {str(e)}")
        await update.message.reply_text(f'خطا: {str(e)}')

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
