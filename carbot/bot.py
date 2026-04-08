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
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/2019_BMW_X5_xDrive30d_M_Sport_Automatic_3.0.jpg/1280px-2019_BMW_X5_xDrive30d_M_Sport_Automatic_3.0.jpg", "name": "BMW X5 M Sport", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/2019_BMW_X7_xDrive30d_Automatic_3.0_Front.jpg/1280px-2019_BMW_X7_xDrive30d_Automatic_3.0_Front.jpg", "name": "BMW X7 xDrive", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/2022_BMW_X3_xDrive20i_Automatic_2.0_Front.jpg/1280px-2022_BMW_X3_xDrive20i_Automatic_2.0_Front.jpg", "name": "BMW X3 M Sport", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/2021_BMW_5_Series_%28G30%2C_facelift%2C_2020%29_530i%2C_front_8.18.19.jpg/1280px-2021_BMW_5_Series_%28G30%2C_facelift%2C_2020%29_530i%2C_front_8.18.19.jpg", "name": "BMW 5 Series", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/2022_BMW_X1_xDrive25e_Automatic_1.5_Front.jpg/1280px-2022_BMW_X1_xDrive25e_Automatic_1.5_Front.jpg", "name": "BMW X1", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/2019_Porsche_Cayenne_S_V6_2.9_Front.jpg/1280px-2019_Porsche_Cayenne_S_V6_2.9_Front.jpg", "name": "Porsche Cayenne", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/2022_Porsche_Macan_S_2.9_Front.jpg/1280px-2022_Porsche_Macan_S_2.9_Front.jpg", "name": "Porsche Macan", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/2021_Porsche_Panamera_4_V6_2.9_Front.jpg/1280px-2021_Porsche_Panamera_4_V6_2.9_Front.jpg", "name": "Porsche Panamera", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/2022_Porsche_Taycan_4S_AT_79.2_Front.jpg/1280px-2022_Porsche_Taycan_4S_AT_79.2_Front.jpg", "name": "Porsche Taycan", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/2020_Mercedes-Benz_GLE_300d_4MATIC_Automatic_2.0_Front.jpg/1280px-2020_Mercedes-Benz_GLE_300d_4MATIC_Automatic_2.0_Front.jpg", "name": "Mercedes-Benz GLE", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/2020_Mercedes-Benz_GLS_400d_4MATIC_Automatic_3.0_Front.jpg/1280px-2020_Mercedes-Benz_GLS_400d_4MATIC_Automatic_3.0_Front.jpg", "name": "Mercedes-Benz GLS", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/2022_Mercedes-Benz_GLC_220d_4MATIC_Automatic_2.0_Front.jpg/1280px-2022_Mercedes-Benz_GLC_220d_4MATIC_Automatic_2.0_Front.jpg", "name": "Mercedes-Benz GLC", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/2021_Mercedes-Benz_E_220d_AMG_Line_Automatic_2.0_Front.jpg/1280px-2021_Mercedes-Benz_E_220d_AMG_Line_Automatic_2.0_Front.jpg", "name": "Mercedes-Benz E-Class", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/2022_Mercedes-Benz_S_350d_L_AMG_Line_Automatic_3.0_Front.jpg/1280px-2022_Mercedes-Benz_S_350d_L_AMG_Line_Automatic_3.0_Front.jpg", "name": "Mercedes-Benz S-Class", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/2020_Audi_Q7_TDI_Quattro_S_Line_3.0_Front.jpg/1280px-2020_Audi_Q7_TDI_Quattro_S_Line_3.0_Front.jpg", "name": "Audi Q7", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/2021_Audi_Q5_S_Line_TDI_Quattro_Automatic_2.0_Front.jpg/1280px-2021_Audi_Q5_S_Line_TDI_Quattro_Automatic_2.0_Front.jpg", "name": "Audi Q5", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/2020_Audi_Q8_TDI_Quattro_S_Line_3.0_Front.jpg/1280px-2020_Audi_Q8_TDI_Quattro_S_Line_3.0_Front.jpg", "name": "Audi Q8", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/2020_Audi_A6_S_Line_TDI_Automatic_2.0_Front.jpg/1280px-2020_Audi_A6_S_Line_TDI_Automatic_2.0_Front.jpg", "name": "Audi A6", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/2020_Audi_A4_S_Line_TDI_Automatic_2.0_Front.jpg/1280px-2020_Audi_A4_S_Line_TDI_Automatic_2.0_Front.jpg", "name": "Audi A4", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/2022_Genesis_GV80_2.5T_Automatic_2.5_Front.jpg/1280px-2022_Genesis_GV80_2.5T_Automatic_2.5_Front.jpg", "name": "Genesis GV80", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/2022_Genesis_GV70_2.5T_Automatic_2.5_Front.jpg/1280px-2022_Genesis_GV70_2.5T_Automatic_2.5_Front.jpg", "name": "Genesis GV70", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/2021_Hyundai_Palisade_2.2_CRDi_AWD_Automatic_Front.jpg/1280px-2021_Hyundai_Palisade_2.2_CRDi_AWD_Automatic_Front.jpg", "name": "Hyundai Palisade", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/2022_Hyundai_Santa_Fe_2.2_CRDi_AWD_Automatic_Front.jpg/1280px-2022_Hyundai_Santa_Fe_2.2_CRDi_AWD_Automatic_Front.jpg", "name": "Hyundai Santa Fe", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/2022_Hyundai_Tucson_1.6_T-GDI_PHEV_AWD_Automatic_Front.jpg/1280px-2022_Hyundai_Tucson_1.6_T-GDI_PHEV_AWD_Automatic_Front.jpg", "name": "Hyundai Tucson", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/2022_Kia_Sportage_HEV_1.6_T-GDI_Automatic_Front.jpg/1280px-2022_Kia_Sportage_HEV_1.6_T-GDI_Automatic_Front.jpg", "name": "Kia Sportage", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/2021_Kia_Sorento_2.2_CRDi_AWD_Automatic_Front.jpg/1280px-2021_Kia_Sorento_2.2_CRDi_AWD_Automatic_Front.jpg", "name": "Kia Sorento", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/2022_Kia_EV6_GT-Line_AWD_Automatic_Front.jpg/1280px-2022_Kia_EV6_GT-Line_AWD_Automatic_Front.jpg", "name": "Kia EV6", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/2022_Hyundai_IONIQ_5_AWD_Automatic_Front.jpg/1280px-2022_Hyundai_IONIQ_5_AWD_Automatic_Front.jpg", "name": "Hyundai IONIQ 5", "year": "2022-2024", "km": "от 5 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/2022_Kia_Carnival_3.5_MPi_AWD_Automatic_Front.jpg/1280px-2022_Kia_Carnival_3.5_MPi_AWD_Automatic_Front.jpg", "name": "Kia Carnival", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
    {"photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/2021_Hyundai_Staria_Premium_3.5_MPi_Automatic_Front.jpg/1280px-2021_Hyundai_Staria_Premium_3.5_MPi_Automatic_Front.jpg", "name": "Hyundai Staria", "year": "2022-2024", "km": "от 10 000 км", "price": "Цена по запросу"},
]

FAQ = {
    "доставка": "🚢 Доставка до порта Владивосток — 100 000 руб. Далее по России рассчитывается индивидуально до вашего города. Срок — около 30 дней с момента оплаты.",
    "растаможка": "📋 Растаможка от 200 000 руб. Рассчитывается индивидуально в зависимости от объёма двигателя, года и стоимости авто. Всё делаем дистанционно — вам никуда ехать не нужно!",
    "предоплата": "💰 Предоплата 20% при заказе. Остаток 80% оплачиваете по прибытии автомобиля в ваш город!",
    "оплата": "💳 Оплата банковским переводом или в USD. Никаких скрытых платежей — всё прописано в договоре.",
    "кредит": "🏦 В кредит под заказ не продаём, но вы можете взять потребительский кредит в банке и заказать у нас.",
    "скрытые": "✅ Никаких скрытых платежей! Всё обсуждается заранее и прописывается в договоре.",
    "срок": "⏱ Около 30 дней с момента оплаты автомобиля.",
    "отслеживать": "📍 Да! В каждом автовозе GPS-трекер. Получите номер трека и отслеживайте путь онлайн.",
    "проверка": "🔍 Проверяем лакокрасочное покрытие, делаем диагностику, снимаем подробное видео и фото. Всё отправляем до покупки.",
    "битый": "🛡 Битые и восстановленные авто сразу видим и не работаем с ними. Только чистые автомобили!",
    "история": "📊 Историю можно посмотреть по корейским базам данных — все страховые случаи как на ладони.",
    "дефект": "⚠️ Если придёт дефект который не был показан — оплачиваем устранение за свой счёт.",
    "пробег": "🛣 Любой пробег — от 10 000 до 100 000 км. Всё зависит от вашего бюджета и пожеланий.",
    "процесс": "📝 Пишете нам → ищем в Корее → осмотр → видеоотчёт → договор → доставка.",
    "цвет": "🎨 Да, выбираете цвет и комплектацию — подбираем именно под ваш запрос.",
    "передумал": "↩️ Если передумали до выкупа — возвращаем предоплату без проблем.",
    "документы": "📄 Получите: таможенную декларацию и техпаспорт из Кореи.",
    "таможня": "✅ Таможню оформляем дистанционно во Владивостоке. Авто приедет уже растаможенным — только ГИБДД для постановки на учёт.",
    "гарантия": "🔧 Гарантия дилера снимается при пересечении границы, но при перевозке все авто застрахованы.",
    "марки": "🚗 BMW, Mercedes, Audi, Porsche, Hyundai, Kia, Genesis и японские бренды с корейского рынка.",
    "электромобиль": "⚡️ Электромобили в огромном количестве! Kia EV6, Hyundai IONIQ 5, Porsche Taycan и другие.",
    "электро": "⚡️ Электромобили в огромном количестве! Kia EV6, Hyundai IONIQ 5, Porsche Taycan и другие.",
    "популярные": "🏆 BMW X5/X7, Porsche Cayenne, Mercedes GLE/GLS, Audi Q7, Genesis GV80, Hyundai Palisade.",
    "корейский рынок": "🌍 Корейский рынок — оригинальные авто европейской и американской сборки. BMW из Германии, Mercedes из Германии и США. Настоящий оригинал!",
    "цена": "💰 Самые лояльные цены в РФ! Каждый автомобиль рассчитывается индивидуально. Оставьте заявку!",
    "сколько": "💰 Самые лояльные цены в РФ! Каждый автомобиль рассчитывается индивидуально. Оставьте заявку!",
    "porsche": "🏎 Cayenne, Macan, Panamera, Taycan — все модели под заказ. Самые лояльные цены в РФ!",
    "bmw": "🚗 X1, X3, X5, X7, 5-серия и другие. Европейской и американской сборки. Самые лояльные цены в РФ!",
    "mercedes": "⭐️ GLC, GLE, GLS, E-класс, S-класс. Немецкая и американская сборка. Самые лояльные цены в РФ!",
    "audi": "🔷 Q5, Q7, Q8, A4, A6. Европейской сборки. Самые лояльные цены в РФ!",
    "kia": "🇰🇷 Sportage, Sorento, EV6, Carnival — популярные модели с отличным качеством.",
    "hyundai": "🇰🇷 Tucson, Santa Fe, Palisade, IONIQ 5, Staria — широкий выбор.",
    "genesis": "💎 Genesis GV80, GV70, G80 — корейский премиум мирового уровня.",
    "японские": "🇯🇵 Японские бренды с корейского рынка тоже привозим. Напишите — найдём!",
}

def get_faq_answer(text):
    text = text.lower()
    for key, answer in FAQ.items():
        if key in text:
            return answer
    return None

async def show_catalog(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 Актуальные авто из Кореи — самые лояльные цены в РФ!\n\nКаждый автомобиль рассчитывается индивидуально 👇")
    for car in CATALOG:
        caption = (
            f"🚗 {car['name']}\n"
            f"📅 Год: {car['year']}\n"
            f"🛣 Пробег: {car['km']}\n"
            f"💰 {car['price']} — самые лояльные цены в РФ!\n\n"
            f"Хотите эту машину? Нажмите 📋 Оставить заявку!"
        )
        try:
            await update.message.reply_photo(photo=car["photo"], caption=caption)
        except Exception:
            await update.message.reply_text(caption)
    await update.message.reply_text("Понравился автомобиль? Нажмите 📋 Оставить заявку!", reply_markup=MAIN_MENU)

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
        "Просто напишите 👇",
        reply_markup=MAIN_MENU
    )

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать в pavelcarstore!\n\n"
        "🇰🇷 Авто из Кореи под заказ.\n\n"
        "✅ Предоплата 20%\n"
        "✅ Доставка 30 дней\n"
        "✅ Растаможка под ключ\n"
        "✅ Видеоотчёт перед покупкой\n"
        "✅ Самые лояльные цены в РФ\n\n"
        "С нами легко! Выберите действие 👇",
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
    await update.message.reply_text("Какой год выпуска?\n(например: 2022-2024)", reply_markup=ReplyKeyboardRemove())
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
        "Пожелания по цвету или комплектации?\n(или напишите нет)",
        reply_markup=ReplyKeyboardRemove()
    )
    return COMMENT

async def get_comment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["comment"] = update.message.text
    d = ctx.user_data
    user = update.effective_user
    await update.message.reply_text(
        "✅ Ваша заявка принята!\n\nМенеджер свяжется с вами в течение 1 часа.\n\nС нами легко! 🚗",
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
    await update.message.reply_text("Отменено.\n\nС нами легко! 🚗", reply_markup=MAIN_MENU)
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
            await update.message.reply_text(answer + "\n\nС нами легко! 🚗", reply_markup=MAIN_MENU)
        else:
            await update.message.reply_text(
                "Спасибо за вопрос! Менеджер ответит в ближайшее время.\n\n"
                "📱 Телефон: 89173550909\n"
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
