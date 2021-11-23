import sqlite3, logging, math, os, random, datetime, config, level.choicelevel as levels, data, assets
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

import level.levels

logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(config.TOKEN)
dp = Dispatcher(bot=bot, storage=memory)


class game(StatesGroup):
    choiceLevel = State()
    waitingGame = State()



@dp.message_handler(commands='start')
async def start(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast=message.chat.last_name).databaseNewUser()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    data.data(message.chat.id).donate()
    markup.add('Начать игру')
    await dp.bot.set_my_commands([
        types.BotCommand("rules", "Правила игры"),
        types.BotCommand("donate", "Покупка премиума"),
    ])
    await message.reply('Привет! Это бот о финансовой грамотности, в этом курсе вы будете иначе мыслить, '
                        'и не будете жить от зарплаты до зарплаты, здесь будут ситуации максимально приближённые к '
                        'реальной жизни, по этому курс точно не будет скучным!\nЕсли вы никогда не играли в подобные '
                        'игры рекомендую ознакомиться с правилами - /rules\nДонат - /donate\nЧто бы присоедениться к группе - join ('
                        'id)\nЧто начать игру введите - Начать игру',
                        reply_markup=markup)


@dp.message_handler(commands='rules')
async def rules(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).databaseNewUser()
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands='donate')
async def donate(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).databaseNewUser()
    await bot.send_message(message.chat.id, data.data(message.chat.id, money=200).donate())

@dp.message_handler(content_types='text')
async def main(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).databaseNewUser()
    if message.text.lower() == 'начать игру':
        dataU = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).dataUser()
        await bot.send_message(message.chat.id, f'Для начала вам нужно выбрать уровень\nВаши доступные уровни {dataU[6]}')
        await game.choiceLevel.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=game.choiceLevel)
async def errordigit(message: types.Message):
    await bot.send_message(message.chat.id, 'Не правильно введен уровень, повторите еще раз')


@dp.message_handler(state=game.choiceLevel)
async def choicelevel(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    dataU = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).dataUser()
    if int(dataU[6]) < int(message.text):
        await bot.send_message(message.chat.id, 'Вам еще не доступен этот уровень')
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add('Продолжить')
    await bot.send_message(message.chat.id, levels.choiceLevel(dataU[6], message.chat.id).work(), reply_markup=markup)
    data.data(message.chat.id, column='levelNow', changes=dataU[6]).dataChanges()
    await game.waitingGame.set()


@dp.message_handler(state=game.waitingGame)
async def choicelevel(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    try:
        async with state.proxy() as datas:
            if float(str(datetime.datetime.now()-datas['time']).replace(':', '')) < 0.3:
                return
    except Exception:
        async with state.proxy() as datas:
            datas['time'] = datetime.datetime.now()
        pass
    dataU = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name,
                      userLast=message.chat.last_name).dataUser()
    levels.choiceLevel(dataU[6], message.chat.id).dataBaseUpt()
    dataG = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name,
                      userLast=message.chat.last_name).dataGame()
    async with state.proxy() as datas:
        data.data(message.chat.id).dataStock()
        data.data(message.chat.id).dataUser()
        data.data(message.chat.id).dataCoins()
        data.data(message.chat.id).dataBonds()
        data.data(message.chat.id).dataBusinesses()
        data.data(message.chat.id).dataGame()
        if dataG[4] == 4:
            await bot.send_message(message.chat.id, 'Итоги месяца')
            return
        if message.text.lower() == 'Статистика':
            await bot.send_message(message.chat.id, '')
        if message.text.lower() == 'продолжить':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
            markup.add('Продолжить')
            if dataG[dataG[4]].split()[0].lower() == 'акция':
                datas['stock'] = True
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
            elif dataG[dataG[4]].split()[0].lower() == 'облигация':
                datas['stock'] = True
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
            elif dataG[dataG[4]].split()[0].lower() == 'бизнес':
                datas['stock'] = True
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
            await bot.send_message(message.chat.id, dataG[dataG[4]], reply_markup=markup)
            datas['time'] = datetime.datetime.now()
            return
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)