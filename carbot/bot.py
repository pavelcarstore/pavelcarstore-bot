import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8671103733:AAGW_ithKrQEnPRrfFEwjuejrb4lKuzY4cw"
MY_CHAT_ID = 204558057

logging.basicConfig(level=logging.INFO)
NAME, PHONE, CAR_BRAND, CAR_YEAR, BUDGET, COMMENT = range(6)

BRANDS = [["KIA", "BMW"], ["Porsche", "Audi"], ["Другая марка"]]
BUDGETS = [["до 1 000 000 руб", "1 000 000 - 2 000 000 руб"], ["2 000 000 - 4 000 000 руб", "Свыше 4 000 000 руб"], ["Введу сумму сам"]]

FAQ = {
    "доставка": "Доставка из Кореи занимает 25-35 дней. Машина едет морем до Владивостока, затем автовозом до вашего города. Стоимость доставки включена в итоговую цену.",
    "растаможка": "Растаможка рассчитывается индивидуально в зависимости от объема двигателя, года выпуска и стоимости авто. В среднем 500-1500$ для легковых автомобилей.",
    "гарантия": "Мы лично осматриваем каждый автомобиль в Корее, проверяем по базам данных на ДТП и пробег. Все документы чистые, история прозрачная.",
    "оплата": "Оплата происходит в два этапа: предоплата 30% при заказе, остаток при получении автомобиля.",
    "срок": "Весь процесс от заказа до получения занимает 35-50 дней.",
    "цена": "Цены зависят от марки, года и комплектации. Напишите /start и оставьте заявку — рассчитаем стоимость под ваш запрос.",
    "kia": "KIA очень популярны из Кореи — Sportage, Sorento, K5. Отличное соотношение цена/качество. Напишите /start для заявки!",
    "bmw": "BMW из Кореи — редкость но возможно. Чаще везем корейские марки. Напишите /start и уточним наличие.",
    "porsche": "Porsche из Кореи привозим под заказ. Cayenne и Macan наиболее популярны. Напишите /start для заявки!",
    "audi": "Audi из Кореи привозим под заказ. Напишите /start и обсудим детали.",
}

def get_faq_answer(text):
    text = text.lower()
    for key, answer in FAQ.items():
        if key in text:
            return answer
    return None

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в pavelcarstore!\n\nАвто из Кореи под заказ. С нами легко!\n\nМожете задать любой вопрос или нажмите /start чтобы оформить заявку.\n\nКак вас зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["name"] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["phone"] = update.message.text
    await update.message.reply_text(
        "Какую марку автомобиля хотите?",
        reply_markup=ReplyKeyboardMarkup(BRANDS, resize_keyboard=True, one_time_keyboard=True)
    )
    return CAR_BRAND

async def get_brand(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["brand"] = update.message.text
    await update.message.reply_text("Какой год выпуска вас интересует?\n(например: 2021-2023)", reply_markup=ReplyKeyboardRemove())
    return CAR_YEAR

async def get_year(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["year"] = update.message.text
    await update.message.reply_text(
        "Какой у вас бюджет?",
        reply_markup=ReplyKeyboardMarkup(BUDGETS, resize_keyboard=True, one_time_keyboard=True)
    )
    return BUDGET

async def get_budget(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["budget"] = update.message.text
    await update.message.reply_text("Есть пожелания по цвету или комплектации?\n(или напишите нет)", reply_markup=ReplyKeyboardRemove())
    return COMMENT

async def get_comment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["comment"] = update.message.text
    d = ctx.user_data
    user = update.effective_user
    await update.message.reply_text(
        "Ваша заявка принята! Менеджер свяжется с вами в течение 1 часа.\n\nС нами легко!"
    )
    tg = "@" + user.username if user.username else "id" + str(user.id)
    text = "Новая заявка на авто из Кореи\n"
    text += "Имя: " + d["name"] + "\n"
    text += "Телефон: " + d["phone"] + "\n"
    text += "Telegram: " + tg + "\n"
    text += "Марка: " + d["brand"] + "\n"
    text += "Год: " + d["year"] + "\n"
    text += "Бюджет: " + d["budget"] + "\n"
    text += "Комментарий: " + d["comment"]
    await ctx.bot.send_message(chat_id=MY_CHAT_ID, text=text)
    return ConversationHandler.END

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено. Напишите /start снова.\n\nС нами легко!")
    return ConversationHandler.END

async def faq_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    answer = get_faq_answer(update.message.text)
    if answer:
        await update.message.reply_text(answer + "\n\nЕсть ещё вопросы? Напишите /start чтобы оформить заявку!")
    else:
        await update.message.reply_text(
            "Спасибо за вопрос! Наш менеджер ответит вам в ближайшее время.\n\nИли напишите /start чтобы сразу оформить заявку!\n\nС нами легко!"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            CAR_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_brand)],
            CAR_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_year)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_budget)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, faq_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
