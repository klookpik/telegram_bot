from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = "7715221883:AAGRV-oA9A50Bye2nQz8fGeYKYwOlRw0Zac"
ADMIN_ID = 8122476596

# پیام شروع و دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("خرید از تلگرام", url="https://t.me/QRcode_admin")],
        [InlineKeyboardButton("خرید از واتساپ", url="https://wa.me/989935392997")],
        [InlineKeyboardButton("خرید با ربات", callback_data="buy_with_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به فروشگاه QRcode خوش آمدید!", reply_markup=reply_markup)

# کلیک روی دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy_with_bot":
        await query.message.reply_text(
            "لطفا معادل قیمت محصول مورد نظر به ولت زیر تتر ارسال کنید و اطلاعاتی همچون اسکرین شات یا عکس تراکنش به همراه تاریخ و ساعت دقیق را همینجا برای ربات ارسال کنید تا بررسی شود:\n\n"
            "`UQAlL7DpvKOX4H0pRZULm98VR1hpR3vzL3w4Gt9NJLnB4HV9`",
            parse_mode="Markdown"
        )

# عکس از کاربر
async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = update.message.caption or "(بدون توضیح)"
    photo = update.message.photo[-1]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=f"اسکرین‌شات از کاربر:\n"
                f"نام کاربری: @{user.username or 'ندارد'}\n"
                f"آیدی عددی: {user.id}\n"
                f"پیام همراه: {caption}"
    )

    await update.message.reply_text("سفارش شما برای بررسی به پشتیبانی ارسال شد. لطفاً منتظر تأیید باشید.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))
    print("ربات با موفقیت اجرا شد.")
    app.run_polling()
