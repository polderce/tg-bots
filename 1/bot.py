import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="your_token")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    photo = FSInputFile(r'C:\Users\polde\PycharmProjects\bots\key.png')  # добавление фото в переменную

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="GTA V", callback_data='GTA V_250'),
        types.InlineKeyboardButton(text="RUST", callback_data='RUST_150')
    )
    builder.row(
        types.InlineKeyboardButton(text="Phasmophobia", callback_data='Phasmophobia_50'),
        types.InlineKeyboardButton(text="Terraria", callback_data='Terraria_75')
    )

    await bot.send_photo(message.chat.id, photo, caption=f'Приветсвтую тебя, {message.from_user.first_name}!'
                                                         f'\nНаш ассортимент товаров:'  # caption - описание к фото
                                                         f'\n'
                                                         f'\n       GTA V — <b>250₽</b>'
                                                         f'\n       RUST — <b>150₽</b>'
                                                         f'\n       Phasmophobia — <b>50₽</b>'
                                                         f'\n       Terraria — <b>75₽</b>'
                                                         f'\n'
                                                         f'\nВыбери ключ для оплаты ↓', parse_mode='html',
                         reply_markup=builder.as_markup())


@dp.callback_query(F.data == "GTA V_250")
async def game_select(query: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="/ЮKassa"),
        types.KeyboardButton(text="Тинькофф")
    )

    await bot.send_message(chat_id=query.from_user.id, text="Вы выбрали ключ от «GTA V» за 250₽."
                                                            "\nТеперь выберите способ оплаты ↓",
                           reply_markup=builder.as_markup())


@dp.callback_query(F.data == "RUST_150")
async def game_select(query: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="/ЮKassa"),
        types.KeyboardButton(text="Тинькофф")
    )

    await bot.send_message(chat_id=query.from_user.id, text="Вы выбрали ключ от «RUST» за 150₽."
                                                            "\nТеперь выберите способ оплаты ↓",
                           reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Phasmophobia_50")
async def game_select(query: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="/ЮKassa"),
        types.KeyboardButton(text="Тинькофф")
    )

    await bot.send_message(chat_id=query.from_user.id, text="Вы выбрали ключ от «Phasmophobia» за 50₽."
                                                            "\nТеперь выберите способ оплаты ↓",
                           reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Terraria_75")
async def game_select(query: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="/ЮKassa"),
        types.KeyboardButton(text="Тинькофф")
    )

    await bot.send_message(chat_id=query.from_user.id, text="Вы выбрали ключ от «Terraria» за 75₽."
                                                            "\nТеперь выберите способ оплаты ↓",
                           reply_markup=builder.as_markup())


@dp.message(F.text.lower() == 'тинькофф')
async def tink(message: Message):
    await message.reply('К сожалению, банк «Тинькофф» не выдает API (даже тестовые), чтобы '
                        'их можно было интегрировать для оплаты, кто не является юр. лицом и т.д., '
                        'приносим свои извинения!')


@dp.message(Command(commands=['ЮKassa']))
async def pay(message: Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка ключа',
        description='Оплата ключа от игры через ЮKassa.',
        payload='Payment through a bot',
        provider_token='381764678:TEST:86728',
        currency='rub',
        prices=[
            LabeledPrice(
                label='Доступ к платежной информации',
                amount=27000
            ),
            LabeledPrice(
                label='НДС',
                amount=2000
            )
        ],
        max_tip_amount=10000,
        suggested_tip_amounts=[500, 2500, 5000, 10000],
        start_parameter='SEmIE',
        provider_data=None,
        photo_url='https://med-pro-ves.ru/wp-content/uploads/2023/03/p1_3224302_e5787b21-1024x576.jpg',
        photo_size=100,
        photo_width=1024,
        photo_height=576,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )


@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f'{k} = {v}')
    await bot.send_message(message.chat.id, f'Платёж на сумму {message.successful_payment.total_amount // 100} '
                                            f'{message.successful_payment.currency} прошел успешно!')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
