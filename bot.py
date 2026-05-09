import asyncio
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp
from datetime import datetime

# ==================== КОНФИГУРАЦИЯ SWILL ====================
BOT_TOKEN = "8248718556:AAGyxQyL-q8iCy34ChBJ5CWQ1SYcT7X8gps"
CRYPTO_WALLET = "TXjkf93jFg7GdH8sLp2QaBcDeFgHiJkLmNoPqRsTuV"  # USDT TRC20
SUPPORT_LINK = "@greenman_supp"
CACTUS_API_URL = "https://lk.cactuspay.pro/api/?method=create"
CACTUS_TOKEN = "5c687699511aa6201a12fd2d"
# ==================== БАЗА ОТЗЫВОВ (100+) ====================
FAKE_REVIEWS = [
    "закинул бабки через 15 мин уже дымил красавы",
    "пацаны все чотко по красоте",
    "первый раз брал боялся а зря",
    "где мой бонус за третий заказ а так огонь",
    "вшышке пушка мужской",
    "скинули гео через 5 мин я охуел",
    "заказываю не первый раз стабильно",
    "лучше чем у дилера и по весу больше",
    "кидалово думал но нет рил тема",
    "тверь спасибо бро",
    "два часа назад оплатил щас уже никакой",
    "качество не подвал не бодяга",
    "камрады советую",
    "хз че вы тут гоните норм все",
    "спс за скорость",
    "вчера брал шишку дым норм",
    "еще закажу пишите когда пополнение",
    "по цене норм по качеству тоже",
    "первый опыт удачный",
    "в Питере лучшие",
    "заняли денег до среды отдам",
    "уже третий заказ и все четко парни",
    "я стафф нюхаю в основном все ок",
    "реальные челы не кидалы",
    "мусорам не советую а так топ",
    "рекомендую родственникам и близким друзьям шучу сижу",
    "братан через сколько клад скинут жду 5 мин",
    "я тут новенький но все ровно выдали",
    "старый третий день на связи красава",
    "а говорят не найдешь а я нашел лол",
    "петрович ты где потерялся а магаз норм",
    "скидка бы не помешала ну такое",
    "лучше вы тут чем этот шлак в соседнем тгк",
    "не верьте если пишут что лохотрон",
    "оператор сказал будет через 20 мин пришло через 18",
    "искал не долго ща пойду забью",
    "можно предзаказ делать?",
    "я маме не говорите",
    "артем виноват",
    "третий день подряд в нулину",
    "пять звезд ставлю",
    "без обид но долго отвечали поддержка",
    "слыш с вас магарыч",
    "заебался ждать заказ с утра",
    "все на высоте",
    "магаз проверенный",
    "не пойму почему вы жалуетесь все ок",
    "я спать",
    "изи найти",
    "прям возле подъезда спрятали имба",
    "фотку гео скинули без обмана",
    "не тупите пацаны",
    "разводилово везде а тут четко+",
    "такая шишка что чуть не выпал в окно",
    "заказываю ток тут",
    "на кармане 500р до среды хватит?",
    "чисто пацанам респект",
    "на районе все берут",
    "если бы не вы я бы не справился",
    "вкусный дым",
    "бошки огонь",
    "где моя молодость",
    "не звоните мне",
    "сплю уже",
    "утром в 4 утра оплатил в 5 уже забрал",
    "все по феншую",
]

# ==================== ТОВАРЫ ====================
CATEGORIES = {
    "shishki": "🌿 Шишки и Гашиш",
    "stim": "❄️ Стимуляторы",
    "mef": "💊 Мефедрон и Экстази",
    "apteka": "🧪 Аптека и Картриджи",
}

PRODUCTS = {
    "ice": {
        "name": "🍫 Гашиш ICE-O-LATOR",
        "cat": "shishki",
        "desc": "Импортный гашиш из Европы, настоящий ICE-O-LATOR. Высшее качество, натуральный, без химии. Изготовлен по технологии холодной фильтрации.",
        "prices": {1: 2650, 2: 5050, 3: 7200, 4: 9350},
    },
    "ak47": {
        "name": "☘️ Шишка VHQ АК-47",
        "cat": "shishki",
        "desc": "Настоящий импортный продукт из Европы. Характерен чрезвычайно сильным ароматом и густым дымом. 'Убойное' качество.",
        "prices": {1: 2650, 2: 5050, 3: 7200, 4: 9350, 5: 11000, 10: 18000},
    },
    "amph": {
        "name": "☆ Амфетамин Импорт 3.0",
        "cat": "stim",
        "desc": "Премиальное качество от Европейских производителей. Повышение продуктивности до максимальных значений.",
        "prices": {1: 3000, 2: 5750, 3: 8150},
    },
    "pvp": {
        "name": "⚗️ АЛЬФА ПВП Premium",
        "cat": "stim",
        "desc": "Самый качественный синтез на рынке, очень яркий и мощный эффект.",
        "prices": {0.5: 2350, 1: 4200, 2: 8250, 3: 11000, 10: 27000},
    },
    "coke": {
        "name": "★ VHQ FishScale Кокаин ROLLS ROYCE",
        "cat": "stim",
        "desc": "Активизирует все центры удовольствия. Состояние несравнимой эйфории.",
        "prices": {1: 16300, 2: 31900, 4: 59600, 5: 70800},
    },
    "mef_muka": {
        "name": "💊 Мефедрон МУКА VIP (VHQ)",
        "cat": "mef",
        "desc": "Высокое качество от импортного производителя, без примесей.",
        "prices": {0.5: 2650, 1: 4800, 2: 9100},
    },
    "mef_crystal": {
        "name": "⚡ Мефедрон Кристаллы VIP (VHQ)",
        "cat": "mef",
        "desc": "Наша гордость. Премиальное качество. Абсолютная эйфория.",
        "prices": {0.5: 3000, 1: 5750, 2: 10800, 3: 14400, 4: 18000, 30: 80000},
    },
    "xtc": {
        "name": "🎱 ECSTASY Blue Punisher",
        "cat": "mef",
        "desc": "Производитель Голландия. 300мкг МДМА. Эйфория, длительность 4 часа.",
        "prices": {1: 2500, 2: 4800, 3: 6500},
    },
    "lirika": {
        "name": "💊 ЛИРИКА 300мг",
        "cat": "apteka",
        "desc": "Мощные капсулы. Настоящая сильная лирика.",
        "prices": {7: 2500, 14: 4500, 28: 7000},
    },
    "jeeter": {
        "name": "🖊️ Картридж Jeeter Juice",
        "cat": "apteka",
        "desc": "Жидкие алмазы. Самый чистый концентрат на рынке. 1000мг, 97.05% ТГК.",
        "prices": {1: 9600},
    },
    
}

CITIES = [
    "Москва", "Санкт-Петербург", "Екатеринбург", "Казань",
    "Нижний Новгород", "Новосибирск", "Краснодар", "Ростов-на-Дону",
    "Челябинск", "Уфа", "Самара", "Омск", "Красноярск",
    "Воронеж", "Пермь", "Волгоград",
]

# ==================== СОСТОЯНИЯ FSM ====================
class OrderStates(StatesGroup):
    waiting_for_weight = State()

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==================== КЛАВИАТУРЫ ====================
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 АССОРТИМЕНТ", callback_data="menu_catalog")],
        [InlineKeyboardButton(text="💬 ПОДДЕРЖКА", callback_data="menu_support")],
        [InlineKeyboardButton(text="⭐️ ОТЗЫВЫ", callback_data="menu_reviews")],
    ])
    return kb



def reviews_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👁 ПОСМОТРЕТЬ ОТЗЫВЫ", callback_data="show_reviews")],
        [InlineKeyboardButton(text="📝 НАПИСАТЬ ОТЗЫВ", callback_data="write_review")],
        [InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_main")],
    ])
    return kb

def cities_menu():
    buttons = []
    row = []
    for i, city in enumerate(CITIES):
        row.append(InlineKeyboardButton(text=city, callback_data=f"city_{city}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def categories_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌿 Шишки и Гашиш", callback_data="cat_shishki")],
        [InlineKeyboardButton(text="❄️ Стимуляторы", callback_data="cat_stim")],
        [InlineKeyboardButton(text="💊 Мефедрон и Экстази", callback_data="cat_mef")],
        [InlineKeyboardButton(text="🧪 Аптека и Картриджи", callback_data="cat_apteka")],
        [InlineKeyboardButton(text="◀️ ВЫБРАТЬ ДРУГОЙ ГОРОД", callback_data="menu_catalog")],
        [InlineKeyboardButton(text="◀️ ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])
    return kb

def products_menu(cat_key):
    buttons = []
    for key, prod in PRODUCTS.items():
        if prod["cat"] == cat_key:
            buttons.append([InlineKeyboardButton(text=prod["name"], callback_data=f"prod_{key}")])
    buttons.append([InlineKeyboardButton(text="◀️ НАЗАД К КАТЕГОРИЯМ", callback_data="show_categories")])
    buttons.append([InlineKeyboardButton(text="◀️ ГЛАВНОЕ МЕНЮ", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def weights_menu(product_key):
    prod = PRODUCTS[product_key]
    buttons = []
    row = []
    for weight, price in prod["prices"].items():
        w_str = str(int(weight)) if weight == int(weight) else str(weight)
        usdt_price = rub_to_usdt(price)
        row.append(InlineKeyboardButton(
            text=f"{w_str}г — {usdt_price} USDT (~{price:,} ₽)",
            callback_data=f"weight_{product_key}_{weight}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(
        text="◀️ НАЗАД К ТОВАРАМ",
        callback_data=f"back_to_cat_{PRODUCTS[product_key]['cat']}"
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.callback_query(lambda c: c.data.startswith("prod_"))
async def show_product(call: CallbackQuery):
    prod_key = call.data.replace("prod_", "")
    prod = PRODUCTS[prod_key]
    prices_str = "\n".join([
        f"▪️ {str(int(k)) if k == int(k) else k} г — {rub_to_usdt(v)} USDT (~{v:,} ₽)"
        for k, v in prod["prices"].items()
    ])
    await call.message.edit_text(
        f"{prod['name']}\n\n"
        f"{prod['desc']}\n\n"
        f"💎 <b>СТОИМОСТЬ:</b>\n{prices_str}\n\n"
        f"⬇️ <i>Выберите вес для заказа:</i>",
        reply_markup=weights_menu(prod_key),
        parse_mode="html",
        disable_web_page_preview=True,
    )
    await call.answer()

def back_to_main_btn():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])
    return kb

# ==================== ОБРАБОТЧИКИ ====================
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user = message.from_user
    await message.answer(
        f"💊 <b>TheGreenMan 24/7</b> 💊\n\n"
        f"🏙️ РФ: Москва, СПБ, ЕКБ, Казань, НСК и др.\n"
        f"🕒 Работаем круглосуточно\n"
        f"👤 <i>Ваш ID: {user.id}</i>\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=main_menu(),
        parse_mode="html",
    )

@dp.callback_query(lambda c: c.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text(
            f"💊 <b>TheGreenMan 24/7</b> 💊\n\n"
            f"🕒 Работаем круглосуточно\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=main_menu(),
            parse_mode="html",
        )
    except:
        await call.message.answer(
            f"💊 <b>TheGreenMan 24/7</b> 💊\n\n"
            f"🕒 Работаем круглосуточно\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=main_menu(),
            parse_mode="html",
        )
    await call.answer()

# ==================== КАТАЛОГ И ГОРОДА ====================
@dp.callback_query(lambda c: c.data == "menu_catalog")
async def show_cities(call: CallbackQuery):
    await call.message.edit_text(
        "📍 <b>Выберите ваш город:</b>",
        reply_markup=cities_menu(),
        parse_mode="html",
    )
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("city_"))
async def city_selected(call: CallbackQuery):
    city = call.data.split("_", 1)[1]
    await call.message.edit_text(
        f"✅ <b>Город: {city}</b>\n\n"
        f"<i>Выберите категорию товаров:</i>",
        reply_markup=categories_menu(),
        parse_mode="html",
    )
    await call.answer()

@dp.callback_query(lambda c: c.data == "show_categories")
async def show_categories(call: CallbackQuery):
    await call.message.edit_text(
        "<i>Выберите категорию товаров:</i>",
        reply_markup=categories_menu(),
        parse_mode="html",
    )
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("cat_"))
async def show_products(call: CallbackQuery):
    cat_key = call.data.replace("cat_", "")
    await call.message.edit_text(
        f"📦 <b>{CATEGORIES.get(cat_key, 'Товары')}</b>\n\n"
        f"<i>Выберите товар:</i>",
        reply_markup=products_menu(cat_key),
        parse_mode="html",
    )
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("back_to_cat_"))
async def back_to_category(call: CallbackQuery):
    cat_key = call.data.replace("back_to_cat_", "")
    await call.message.edit_text(
        f"📦 <b>{CATEGORIES.get(cat_key, 'Товары')}</b>\n\n"
        f"<i>Выберите товар:</i>",
        reply_markup=products_menu(cat_key),
        parse_mode="html",
    )
    await call.answer()

USDT_RATE = 90  # примерный курс, можно менять

def rub_to_usdt(rub):
    return round(rub / USDT_RATE, 1)

@dp.callback_query(lambda c: c.data.startswith("prod_"))
async def show_product(call: CallbackQuery):
    prod_key = call.data.replace("prod_", "")
    prod = PRODUCTS[prod_key]
    prices_str = "\n".join([
        f"▪️ {str(int(k)) if k == int(k) else k} г — {rub_to_usdt(v)} USDT"
        for k, v in prod["prices"].items()
    ])
    await call.message.edit_text(
        f"{prod['name']}\n\n"
        f"{prod['desc']}\n\n"
        f"💎 <b>СТОИМОСТЬ:</b>\n{prices_str}\n\n"
        f"⬇️ <i>Выберите вес для заказа:</i>",
        reply_markup=weights_menu(prod_key),
        parse_mode="html",
        disable_web_page_preview=True,
    )
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("weight_"))
async def start_payment(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    if len(parts) < 3:
        return
    prod_key = parts[1]
    try:
        weight = float(parts[2])
    except ValueError:
        return
    prod = PRODUCTS[prod_key]
    price_rub = prod["prices"][weight]
    price_usdt = rub_to_usdt(price_rub)
    w_str = str(int(weight)) if weight == int(weight) else str(weight)
    order_id = f"SWILL_{call.from_user.id}_{int(datetime.now().timestamp())}"

    await call.message.edit_text("⏳ Создаю платёж...")

    body = {
        "token": CACTUS_TOKEN,
        "amount": price_rub,
        "order_id": order_id,
        "description": f"Order {order_id}",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(CACTUS_API_URL, json=body) as resp:
                data = await resp.json()
        except:
            await call.message.edit_text("❌ Ошибка. Попробуйте позже.", reply_markup=back_to_main_btn())
            return

    if data.get("status") != "success":
        await call.message.edit_text("❌ Ошибка создания платежа.", reply_markup=back_to_main_btn())
        return

    payment_url = data["response"]["url"]

    caption = (
        f"🛒 <b>ЗАКАЗ СФОРМИРОВАН</b>\n\n"
        f"📦 <b>Товар:</b> {prod['name']}\n"
        f"⚖️ <b>Вес:</b> {w_str} г\n"
        f"💎 <b>Сумма:</b> {price_usdt} USDT (~{price_rub:,} ₽)\n\n"
        f"<i>❗❗❗ОПЛАТА ЧЕРЕЗ СБП. ПРОСЬБА ВЫБРАТЬ ВАРИАНТ КАК НА ФОТО, С ОСТАЛЬНЫМИ ВРЕМЕННЫЕ ПРОБЛЕМЫ❗❗❗ \n"
        f"ПОСЛЕ ВЫБОРА НАЖМИТЕ НА ОТКРЫТЬ ДЛЯ ОПЛАТЫ, ПОД QR-КОДОМ \n"
        f"Нажмите кнопку ниже и следуйте инструкции.</i>\n\n"
        f"<i>После оплаты заказ автоматически уйдет на модерацию.</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 ОПЛАТИТЬ", url=payment_url)],
        [InlineKeyboardButton(text="◀️ ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])

    await call.message.delete()
    try:
        with open("sbp.jpg", "rb") as photo:
            await call.message.answer_photo(
                photo=types.BufferedInputFile(photo.read(), filename="sbp.jpg"),
                caption=caption,
                reply_markup=kb,
                parse_mode="html",
            )
    except FileNotFoundError:
        await call.message.answer(caption, reply_markup=kb, parse_mode="html")

# ==================== ПОДДЕРЖКА ====================
SUPPORT_USERNAME = "greenman_help"  # юзернейм менеджера без @

@dp.callback_query(lambda c: c.data == "menu_support")
async def support(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 НАПИСАТЬ В ПОДДЕРЖКУ", url=f"https://t.me/{SUPPORT_USERNAME}")],
        [InlineKeyboardButton(text="◀️ НАЗАД", callback_data="back_main")],
    ])
    await call.message.edit_text(
        "💬 <b>ПОДДЕРЖКА</b>\n\n"
        "Нажмите кнопку ниже, чтобы перейти в чат с оператором.\n\n"
        "<i>Время ответа: до 10 минут.</i>",
        reply_markup=kb,
        parse_mode="html",
    )
    await call.answer()

# ==================== ОТЗЫВЫ ====================
@dp.callback_query(lambda c: c.data == "menu_reviews")
async def reviews(call: CallbackQuery):
    await call.message.edit_text(
        "⭐️ <b>ОТЗЫВЫ</b>\n\n"
        "<i>Выберите действие:</i>",
        reply_markup=reviews_menu(),
        parse_mode="html",
    )
    await call.answer()


@dp.callback_query(lambda c: c.data == "show_reviews")
async def show_reviews(call: CallbackQuery):
    selected = random.sample(FAKE_REVIEWS, 5)
    msg = "💬 <b>ЧТО ПИШУТ ЛЮДИ</b>\n\n"

    for review in selected:
        fake_time = datetime.now() - timedelta(minutes=random.randint(2, 5))
        time_str = fake_time.strftime("%H:%M")
        msg += f"🕐 {time_str} МСК — {review}\n\n"

    msg += "<i>🔒 Все отзывы анонимны в целях конфиденциальности.</i>"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ НАЗАД", callback_data="menu_reviews")],
    ])
    await call.message.edit_text(msg, reply_markup=kb, parse_mode="html", disable_web_page_preview=True)
    await call.answer()

@dp.callback_query(lambda c: c.data == "write_review")
async def write_review(call: CallbackQuery):
    await call.message.edit_text(
        "📝 <b>НАПИСАТЬ ОТЗЫВ</b>\n\n"
        "<i>Отправьте текст вашего отзыва одним сообщением. Он будет опубликован после модерации.</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ НАЗАД", callback_data="menu_reviews")],
        ]),
        parse_mode="html",
    )
    await call.answer()

# Обработка текста отзыва
@dp.message(lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_review(message: types.Message):
    await message.answer(
        "✅ <i>Спасибо! Отзыв отправлен на модерацию. Появится в ленте в течение 24 часов.</i>",
        reply_markup=main_menu(),
        parse_mode="html",
    )

# ==================== FSM ДЛЯ ВЕСА ====================
@dp.message(OrderStates.waiting_for_weight)
async def process_weight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    prod_key = data.get("prod_key")
    prod = PRODUCTS[prod_key]
    try:
        weight = float(message.text.replace(",", "."))
    except:
        await message.answer("❌ Укажите число (например: 1 или 0.5)", reply_markup=weights_menu(prod_key))
        return

    if weight not in prod["prices"]:
        available = ", ".join([str(int(k) if k == int(k) else k) for k in prod["prices"].keys()])
        await message.answer(f"❌ Недоступный вес. Доступные: {available} г.", reply_markup=weights_menu(prod_key))
        return

    price = prod["prices"][weight]
    w_str = str(int(weight)) if weight == int(weight) else str(weight)
    await state.clear()
    await message.answer(
        f"🛒 <b>ЗАКАЗ СФОРМИРОВАН</b>\n\n"
        f"📦 <b>Товар:</b> {prod['name']}\n"
        f"⚖️ <b>Вес:</b> {w_str} г\n"
        f"💵 <b>Сумма к оплате:</b> {price:,} ₽\n\n"
        f"💎 <b>USDT (TRC20):</b>\n"
        f"<code>{CRYPTO_WALLET}</code>\n\n"
        f"⚠️ <i>Переведите точную сумму. После оплаты заказ автоматически уйдет на модерацию.</i>\n\n"
        f"🕒 <i>Ожидайте подтверждения в течение 15-60 минут.</i>",
        reply_markup=back_to_main_btn(),
        parse_mode="html",
    )

# ==================== ЗАПУСК ====================
async def main():
    print("⚡ SWILL BOT ЗАПУЩЕН")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
