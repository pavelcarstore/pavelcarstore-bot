import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8671103733:AAGW_ithKrQEnPRrfFEwjuejrb4lKuzY4cw"
MY_CHAT_ID = 204558057

logging.basicConfig(level=logging.INFO)
NAME, PHONE, CAR_BRAND, CAR_YEAR, BUDGET, COMMENT = range(6)

BRANDS = [["KIA", "BMW"], ["Porsche", "Audi"], ["Mercedes", "Другая марка"]]
BUDGETS = [["до 1 000 000 руб", "1 000 000 - 2 000 000 руб"], ["2 000 000 - 4 000 000 руб", "Свыше 4 000 000 руб"], ["Введу сумму сам"]]

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["🚗 Каталог авто"],
        ["📋 Оставить заявку"],
        ["💬 Задать вопрос", "📞 Связаться с менеджером"],
    ],
    resize_keyboard=True
)

CATALOG = [
    {
        "photo": "https://image.heydealer.com/unsafe/900x0/https://heydealer-api.s3.amazonaws.com/media/cars/image/2026/04/04/121193027_a8cc8fb5-51ef-486f-a17e-3b6b4e123c54.JPEG",
        "name": "BMW X6 xDrive 30d M Sport",
        "year": "2025",
        "km": "20 900 км",
        "price": "10 900 000 руб.",
    },
    {
        "photo": "https://image.heydealer.com/unsafe/900x0/https://heydealer-api.s3.amazonaws.com/media/cars/image/2026/04/07/121468349_ebe303b2-844f-443d-a26c-0a1e6db07a34.JPEG",
        "name": "Porsche Cayenne Coupe",
        "year": "2025",
        "km": "6 100 км",
        "price": "14 000 000 руб.",
    },
]

FAQ = {
    "доставка": "🚢 Доставка автомобиля до порта Владивосток стоит 100 000 руб. Далее доставка по России рассчитывается индивидуально в зависимости от вашего города. Автомобиль едет паромом до Владивостока, затем в закрытой фуре до вашего города. Среднее время — 30 дней с момента оплаты.",
    "растаможка": "📋 Растаможка автомобиля начинается от 200 000 руб. Точная сумма рассчитывается индивидуально в зависимости от объёма двигателя, года и стоимости авто. Мы делаем всё дистанционно во Владивостоке — вам никуда ехать не нужно!",
    "предоплата": "💰 Мы работаем по предоплате 20% от стоимости автомобиля. Также можно оплатить полную стоимость при заключении договора. Остаток 80% оплачиваете по прибытии автомобиля в ваш город!",
    "оплата": "💳 Способы оплаты: банковский перевод (для несанкционных авто) или оплата в USD. Никаких скрытых платежей — всё прописано в договоре заранее.",
    "кредит": "🏦 К сожалению, в кредит автомобиль под заказ мы не продаём. Но вы можете взять потребительский кредит в банке и заказать у нас автомобиль.",
    "скрытые": "✅ Никаких скрытых платежей и дополнительных расходов нет. Всё обсуждается заранее и прописывается в договоре.",
    "срок": "⏱ Доставка занимает около 30 дней с момента оплаты автомобиля.",
    "отслеживать": "📍 Да! В каждом автовозе есть GPS-трекер. Вы получаете номер трека и можете отслеживать путь вашего автомобиля в режиме реального времени.",
    "трекер": "📍 Да! В каждом автовозе есть GPS-трекер. Вы получаете номер трека и можете отслеживать путь вашего автомобиля в режиме реального времени.",
    "проверка": "🔍 Перед покупкой мы проверяем каждый автомобиль: замеряем лакокрасочное покрытие специальными приборами, делаем полную диагностику, снимаем подробное видео и фото. Всё отправляем клиенту до покупки.",
    "битый": "🛡 Битые и восстановленные автомобили мы сразу видим при осмотре и не работаем с такими. Только чистые автомобили.",
    "история": "📊 Да, историю автомобиля можно посмотреть по корейским базам данных — там отображаются все страховые случаи, как в нашей автомойке в России.",
    "дефект": "⚠️ Если автомобиль придёт с дефектом который не был показан на видео или фото — мы оплачиваем устранение этого дефекта в сервисе за свой счёт.",
    "пробег": "🛣 Пробег — индивидуально. Кто-то хочет до 10 000 км, кого-то устраивает и 100 000 км. Всё зависит от цены и ваших пожеланий. У нас гибкий подход!",
    "процесс": "📝 Процесс заказа: пишете нам какой автомобиль хотите → мы ищем варианты в Корее → выезжаем на осмотр → присылаем видеоотчёт → вы выбираете → заключаем договор → закупаем и доставляем.",
    "заказ": "📝 Процесс заказа: пишете нам какой автомобиль хотите → мы ищем варианты в Корее → выезжаем на осмотр → присылаем видеоотчёт → вы выбираете → заключаем договор → закупаем и доставляем.",
    "цвет": "🎨 Да! Вы можете выбрать конкретный цвет и комплектацию. Мы подбираем автомобиль под ваши пожелания.",
    "комплектация": "🎨 Да! Вы можете выбрать конкретный цвет и комплектацию. Мы подбираем автомобиль под ваши пожелания.",
    "нет в каталоге": "🔎 Конечно! Если нужной модели нет в каталоге — просто напишите нам и мы найдём именно то что вы хотите.",
    "передумал": "↩️ Если вы передумали до выкупа автомобиля — предоплату 10-20% вернём без проблем. Небольшая предоплата только на осмотр автомобиля не возвращается.",
    "возврат": "↩️ Если вы передумали до выкупа автомобиля — предоплату вернём без проблем. Небольшая предоплата только на осмотр не возвращается.",
    "документы": "📄 Вы получите: государственную таможенную декларацию и технический паспорт автомобиля из Кореи.",
    "номера": "🔢 Автомобиль приедет без российских номеров. Таможню мы оформляем дистанционно во Владивостоке. Автомобиль приезжает к вам уже растаможенным — вам остаётся только поехать в ГИБДД и поставить на учёт.",
    "таможня": "✅ Вам не нужно ехать на таможню! Мы всё оформляем дистанционно во Владивостоке. Автомобиль приезжает уже растаможенным прямо к вашему дому.",
    "гарантия": "🔧 В Корее автомобиль находится на гарантии дилера. После пересечения границы гарантия снимается. Но при перевозке мы страхуем все автомобили — переживать не стоит!",
    "страховка": "🔧 При перевозке мы страхуем все автомобили. Если в пути что-то случится — всё покрывается страховкой.",
    "марки": "🚗 Мы привозим премиальные бренды: BMW, Mercedes, Audi, Porsche. А также все корейские и японские марки которые есть на корейском рынке. Напишите — найдём любой вариант!",
    "японские": "🇯🇵 Да, японские марки тоже привозим! Те которые присутствуют на корейском рынке. Напишите нам какой автомобиль вас интересует.",
    "электромобиль": "⚡️ Электромобили есть в огромном количестве на корейском рынке! Без проблем привезём электричку под ваш заказ.",
    "электро": "⚡️ Электромобили есть в огромном количестве на корейском рынке! Без проблем привезём электричку под ваш заказ.",
    "популярные": "🏆 Самые популярные модели: Audi Q7, Audi A4, BMW X1, BMW X3, BMW 5-серии, BMW X5, BMW X7, Porsche Cayenne, Porsche Macan, Porsche Taycan.",
    "корейский рынок": "🌍 Корейский рынок — это как российский рынок 5 лет назад когда были все дилеры. Здесь можно купить оригинальные автомобили немецкого и европейского производства. BMW, Mercedes, Audi, Porsche — все собраны в Германии, Испании, США. Настоящий оригинал!",
    "отличие": "🌍 Корейский рынок похож на российский каким он был 5 лет назад — с официальными дилерами всех брендов. Все авто оригинальные, собраны в Европе и США. Никаких параллельных схем!",
    "цена": "💰 Привозим автомобили от 2 500 000 руб. Цена зависит от марки, года и комплектации. Оставьте заявку — рассчитаем точную стоимость под ваш запрос!",
    "сколько": "💰 Привозим автомобили от 2 500 000 руб. Стоимость зависит от марки, года и комплектации. Оставьте заявку — рассчитаем под ваш запрос!",
    "porsche": "🏎 Porsche привозим из Кореи — Cayenne, Macan, Panamera, Taycan. Европейской сборки. Предоплата 20%, остаток при получении.",
    "bmw": "🚗 BMW привозим из Кореи — X1, X3, X5, X7, 5-серия и другие. Европейской и американской сборки. Предоплата 20%, остаток при получении.",
    "mercedes": "⭐️ Mercedes-Benz привозим из Кореи — GLE, GLC, E-класс и другие. Сборка Германия, США. Предоплата 20%, остаток при получении.",
    "audi": "🔷 Audi привозим из Кореи — Q7, Q5, A4, A6 и другие. Европейской сборки. Предоплата 20%, остаток при получении.",
    "kia": "🇰🇷 KIA — одна из самых популярных марок. Sportage, Sorento, K5, EV6. Отличное качество по хорошей цене.",
    "hyundai": "🇰🇷 Hyundai привозим из Кореи — Tucson, Santa Fe, Sonata, IONIQ. Напишите /start для заявки!",
}

def get_faq_answer(text):
    text = text.lower()
    for key, answer in FAQ.items():
        if key in text:
            return answer
    return None

async def show_catalog(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 Актуальные авто из Кореи:")
    for car in CATALOG:
        caption = (
            f"🚗 {car['name']}\n"
            f"📅 Год: {car['year']}\n"
            f"🛣 Пробег: {car['km']}\n"
            f"💰 Цена под ключ: {car['price']}\n\n"
            f"Хотите эту машину? Нажмите 📋 Оставить заявку!"
        )
        try:
            await update.message.reply_photo(photo=car["photo"], caption=caption)
        except Exception:
            await update.message.reply_text(caption)
    await update.message.reply_text(
        "Понравился автомобиль? Нажмите 📋 Оставить заявку!",
        reply_markup=MAIN_MENU
    )

async def contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Связаться с менеджером:\n\n"
        "📱 Телефон: 89173550909\n"
        "💬 Telegram: @MIKHALEV_CAPITAL\n\n"
        "Напишите нам — ответим быстро!\n\n"
        "С нами легко! 🚗",
        reply_markup=MAIN_MENU
    )

async def ask_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 Задайте ваш вопрос!\n\n"
        "Например:\n"
        "• Сколько стоит доставка?\n"
        "• Как проходит растаможка?\n"
        "• Есть ли BMW X5 2023 года?\n"
        "• Какая предоплата?\n\n"
        "Просто напишите ваш вопрос 👇",
        reply_markup=MAIN_MENU
    )

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать в pavelcarstore!\n\n"
        "🇰🇷 Авто из Кореи под заказ.\n\n"
        "✅ Предоплата 20%\n"
        "✅ Доставка 30 дней\n"
        "✅ Растаможка под ключ\n"
        "✅ Видеоотчёт перед покупкой\n\n"
        "С нами легко! Выберите что вас интересует 👇",
        reply_markup=MAIN_MENU
    )
    return ConversationHandler.END

async def begin_order(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Давайте оформим заявку.\n\nКак вас зовут?",
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
    await update.message.reply_text(
        "Какой год выпуска вас интересует?\n(например: 2022-2024)",
        reply_markup=ReplyKeyboardRemove()
    )
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
    await update.message.reply_text(
        "Есть пожелания по цвету или комплектации?\n(или напишите нет)",
        reply_markup=ReplyKeyboardRemove()
    )
    return COMMENT

async def get_comment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["comment"] = update.message.text
    d = ctx.user_data
    user = update.effective_user
    await update.message.reply_text(
        "✅ Ваша заявка принята!\n\n"
        "Менеджер свяжется с вами в течение 1 часа.\n\n"
        "С нами легко! 🚗",
        reply_markup=MAIN_MENU
    )
    tg = "@" + user.username if user.username else "id" + str(user.id)
    text = "🚗 Новая заявка на авто из Кореи\n"
    text += "━━━━━━━━━━━━━━━━\n"
    text += "👤 Имя: " + d["name"] + "\n"
    text += "📞 Телефон: " + d["phone"] + "\n"
    text += "💬 Telegram: " + tg + "\n"
    text += "🚘 Марка: " + d["brand"] + "\n"
    text += "📅 Год: " + d["year"] + "\n"
    text += "💰 Бюджет: " + d["budget"] + "\n"
    text += "💬 Комментарий: " + d["comment"] + "\n"
    text += "━━━━━━━━━━━━━━━━"
    await ctx.bot.send_message(chat_id=MY_CHAT_ID, text=text)
    return ConversationHandler.END

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отменено. Выберите действие 👇\n\nС нами легко! 🚗",
        reply_markup=MAIN_MENU
    )
    return ConversationHandler.END

async def message_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚗 Каталог авто":
        await show_catalog(update, ctx)
    elif text == "📋 Оставить заявку":
        await begin_order(update, ctx)
        return NAME
    elif text == "💬 Задать вопрос":
        await ask_question(update, ctx)
    elif text == "📞 Связаться с менеджером":
        await contact(update, ctx)
    else:
        answer = get_faq_answer(text)
        if answer:
            await update.message.reply_text(
                answer + "\n\nЕсть ещё вопросы? 👇",
                reply_markup=MAIN_MENU
            )
        else:
            await update.message.reply_text(
                "Спасибо за вопрос! Менеджер ответит в ближайшее время.\n\n"
                "📞 Телефон: 89173550909\n"
                "💬 Telegram: @MIKHALEV_CAPITAL\n\n"
                "Или выберите действие 👇",
                reply_markup=MAIN_MENU
            )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^📋 Оставить заявку$"), begin_order),
        ],
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
