import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

BOT_TOKEN = os.getenv("8248718556:AAGyxQyL-q8iCy34ChBJ5CWQ1SYcT7X8gps")

CATEGORIES = {
    "hoodies": "Худи и Свитшоты",
    "tshirts": "Футболки",
    "accessories": "Аксессуары",
    "exclusive": "Эксклюзивный мерч",
}

PRODUCTS = {
    "hoodie_black": {
        "name": "Худи ICE Чёрное",
        "cat": "hoodies",
        "desc": "Премиальное худи из плотного футера. Вышивка, не линяет. S-XXL.",
        "price": 4500,
    },
    "hoodie_white": {
        "name": "Худи AK-47 Белое",
        "cat": "hoodies",
        "desc": "Лимитированная серия. Плотный материал, высокая детализация.",
        "price": 4900,
    },
    "tshirt_premium": {
        "name": "Футболка 3.0 Premium",
        "cat": "tshirts",
        "desc": "Премиальный хлопок. Не садится после стирки. Яркий принт.",
        "price": 2900,
    },
    "tshirt_alpha": {
        "name": "Футболка Alpha",
        "cat": "tshirts",
        "desc": "Уникальный дизайн. Ограниченный тираж.",
        "price": 3200,
    },
    "exclusive_rolls": {
        "name": "Лонгслив Rolls Royce",
        "cat": "exclusive",
        "desc": "Эксклюзивный лонгслив. Премиальный материал, ручная работа.",
        "price": 6500,
    },
    "tshirt_muka": {
        "name": "Футболка Muka VIP",
        "cat": "tshirts",
        "desc": "Высокое качество печати. Премиальный крой.",
        "price": 2800,
    },
    "tshirt_crystal": {
        "name": "Футболка Crystal VIP",
        "cat": "tshirts",
        "desc": "Уникальный дизайн с кристаллами. Наша гордость.",
        "price": 3500,
    },
    "accessory_punisher": {
        "name": "Рюкзак Punisher",
        "cat": "accessories",
        "desc": "Качественный рюкзак. Прочные материалы, удобные лямки.",
        "price": 4200,
    },
    "accessory_case": {
        "name": "Чехол для телефона 300",
        "cat": "accessories",
        "desc": "Ударопрочный чехол. Точная подгонка под iPhone и Samsung.",
        "price": 1900,
    },
    "exclusive_jeeter": {
        "name": "Стикер-пак Jeeter Juice",
        "cat": "exclusive",
        "desc": "Эксклюзивный набор стикеров. Лимитированная серия.",
        "price": 1500,
    },
}

CITIES = [
    "Москва", "Санкт-Петербург", "Екатеринбург", "Казань",
    "Нижний Новгород", "Новосибирск", "Краснодар", "Ростов-на-Дону",
    "Челябинск", "Уфа", "Самара", "Омск", "Красноярск",
    "Воронеж", "Пермь", "Волгоград",
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def safe_answer(call: CallbackQuery, text: str = None, show_alert: bool = False):
    try:
        await call.answer(text, show_alert=show_alert)
    except TelegramBadRequest:
        pass


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="КАТАЛОГ", callback_data="menu_catalog")],
        [InlineKeyboardButton(text="ПОДДЕРЖКА", callback_data="menu_support")],
        [InlineKeyboardButton(text="ОТЗЫВЫ", callback_data="menu_reviews")],
    ])


def cities_menu():
    buttons = []
    row = []
    for city in CITIES:
        row.append(InlineKeyboardButton(text=city, callback_data=f"city_{city}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="НАЗАД", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def categories_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Худи и Свитшоты", callback_data="cat_hoodies")],
        [InlineKeyboardButton(text="Футболки", callback_data="cat_tshirts")],
        [InlineKeyboardButton(text="Аксессуары", callback_data="cat_accessories")],
        [InlineKeyboardButton(text="Эксклюзивный мерч", callback_data="cat_exclusive")],
        [InlineKeyboardButton(text="ВЫБРАТЬ ДРУГОЙ ГОРОД", callback_data="menu_catalog")],
        [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])


def products_menu(cat_key):
    buttons = []
    for key, prod in PRODUCTS.items():
        if prod["cat"] == cat_key:
            buttons.append([InlineKeyboardButton(text=prod["name"], callback_data=f"prod_{key}")])
    buttons.append([InlineKeyboardButton(text="НАЗАД К КАТЕГОРИЯМ", callback_data="show_categories")])
    buttons.append([InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_detail_menu(prod_key):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ЗАКАЗАТЬ", callback_data=f"order_{prod_key}")],
        [InlineKeyboardButton(text="НАЗАД К ТОВАРАМ", callback_data=f"cat_{PRODUCTS[prod_key]['cat']}")],
        [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])


def back_btn():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ГЛАВНОЕ МЕНЮ", callback_data="back_main")],
    ])


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "MERCH STORE 24/7\n\nДоставка по РФ\nРаботаем круглосуточно\n\nВыберите действие:",
        reply_markup=main_menu(),
    )


@dp.callback_query(lambda c: c.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text(
            "MERCH STORE 24/7\n\nРаботаем круглосуточно\n\nВыберите действие:",
            reply_markup=main_menu(),
        )
    except TelegramBadRequest:
        pass
    await safe_answer(call)


@dp.callback_query(lambda c: c.data == "menu_catalog")
async def show_cities(call: CallbackQuery):
    await call.message.edit_text("Выберите ваш город:", reply_markup=cities_menu())
    await safe_answer(call)


@dp.callback_query(lambda c: c.data.startswith("city_"))
async def city_selected(call: CallbackQuery):
    city = call.data.split("_", 1)[1]
    await call.message.edit_text(
        f"Город: {city}\n\nВыберите категорию:",
        reply_markup=categories_menu(),
    )
    await safe_answer(call)


@dp.callback_query(lambda c: c.data == "show_categories")
async def show_categories(call: CallbackQuery):
    await call.message.edit_text("Выберите категорию:", reply_markup=categories_menu())
    await safe_answer(call)


@dp.callback_query(lambda c: c.data.startswith("cat_"))
async def show_products(call: CallbackQuery):
    cat_key = call.data.replace("cat_", "")
    await call.message.edit_text(
        f"{CATEGORIES.get(cat_key, 'Товары')}\n\nВыберите товар:",
        reply_markup=products_menu(cat_key),
    )
    await safe_answer(call)


@dp.callback_query(lambda c: c.data.startswith("prod_"))
async def show_product(call: CallbackQuery):
    prod_key = call.data.replace("prod_", "")
    prod = PRODUCTS[prod_key]
    await call.message.edit_text(
        f"{prod['name']}\n\n{prod['desc']}\n\nЦЕНА: {prod['price']:,} руб.\n\nНажмите ЗАКАЗАТЬ.",
        reply_markup=product_detail_menu(prod_key),
    )
    await safe_answer(call)


@dp.callback_query(lambda c: c.data.startswith("order_"))
async def order_product(call: CallbackQuery):
    await call.message.edit_text(
        "РАЗДЕЛ В РАЗРАБОТКЕ\n\nОплата временно недоступна.\nПопробуйте позже.",
        reply_markup=back_btn(),
    )
    await safe_answer(call)


@dp.callback_query(lambda c: c.data == "menu_support")
async def support(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="НАПИСАТЬ В ПОДДЕРЖКУ", url="https://t.me/merch_support")],
        [InlineKeyboardButton(text="НАЗАД", callback_data="back_main")],
    ])
    await call.message.edit_text(
        "ПОДДЕРЖКА\n\nНажмите кнопку для связи с оператором.\nВремя ответа: до 10 минут.",
        reply_markup=kb,
    )
    await safe_answer(call)


@dp.callback_query(lambda c: c.data == "menu_reviews")
async def reviews(call: CallbackQuery):
    await call.message.edit_text(
        "ОТЗЫВЫ — В РАЗРАБОТКЕ\n\nРаздел временно недоступен.",
        reply_markup=back_btn(),
    )
    await safe_answer(call)


@dp.message(lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_message(message: types.Message):
    await message.answer("Используйте кнопки меню.", reply_markup=main_menu())


async def main():
    print("MERCH BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())