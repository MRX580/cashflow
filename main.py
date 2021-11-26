import sqlite3, logging, math, os, random, datetime, config, level.choicelevel as levels, data, assets
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(config.TOKEN)
dp = Dispatcher(bot=bot, storage=memory)


class game(StatesGroup):
    choiceLevel = State()
    waitingGame = State()
    buys = State()
    buysBusiness = State()



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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Начать игру')
    data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).databaseNewUser()
    if message.text.lower() == 'начать игру':
        dataU = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).dataUser()
        await bot.send_message(message.chat.id, f'Для начала вам нужно выбрать уровень\nВаши доступные уровни {dataU[6]}', reply_markup=markup)
        await game.choiceLevel.set()
        return
    await bot.send_message(message.chat.id, 'Введите "Начать игру" что бы начать игру', reply_markup=markup)


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
    data.data(message.chat.id, column='levelNow', changes=dataU[7]).dataChanges()
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
    dataGame = data.data(message.chat.id).dataGame()
    dataStock = data.data(message.chat.id).dataStock()
    dataUser = data.data(message.chat.id).dataUser()
    dataCoins = data.data(message.chat.id).dataCoins()
    dataBonds = data.data(message.chat.id).dataBonds()
    dataBusinesses = data.data(message.chat.id).dataBusinesses()
    async with state.proxy() as datas:
        if message.text.lower() == 'Статистика':
            await bot.send_message(message.chat.id, '')
        if message.text.lower() == 'продолжить':
            levels.choiceLevel(dataUser[7], message.chat.id).dataBaseUpt()
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
            markup.add('Продолжить')
            if dataGame[4] != 4:
                if dataGame[dataGame[4]].split()[0].lower() == 'акция':
                    datas['stock'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
                elif dataGame[dataGame[4]].split()[0].lower() == 'облигация':
                    datas['bonds'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
                elif dataGame[dataGame[4]].split()[0].lower() == 'бизнес':
                    datas['business'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика')
                await bot.send_message(message.chat.id, dataGame[dataGame[4]], reply_markup=markup)
                datas['time'] = datetime.datetime.now()
                return
            else:
                await bot.send_message(message.chat.id, 'Итоги месяца')
                return
        try:
            if message.text.lower() == 'купить' and datas['stock']:
                await bot.send_message(message.chat.id, 'Сколько акций хотите купить?')
                await game.buys.set()
            elif message.text.lower() == 'купить' and datas['bonds']:
                await bot.send_message(message.chat.id, 'Сколько облигаций хотите купить?')
                await game.buys.set()
            elif message.text.lower() == 'купить' and datas['business']:
                await game.buysBusiness.set()
        except KeyError:
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False


@dp.message_handler(lambda message: not message.text.isdigit(), state=game.buys)
async def error(message: types.Message):
    await bot.send_message(message.chat.id, 'Не коректно указано количевство')

@dp.message_handler(lambda message: int(message.text) > 0)
async def error(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите число больше 0')

@dp.message_handler(state=[game.buys, game.buysBusiness])
async def buys(message: types.Message):
    dataGame = data.data(message.chat.id).dataGame()
    if dataGame[dataGame[4]-1].split()[0].lower() == 'акция':
        assets.assets(userid=message.chat.id, number=int(message.text), price=int(dataGame[dataGame[4]-1].split()[3]), coin=dataGame[dataGame[4]-1].split()[1]).database_buys_stock()
    elif dataGame[dataGame[4]-1].split()[0].lower() == 'облигация':
        assets.assets(userid=message.chat.id, number=int(message.text), price=int(dataGame[dataGame[4] - 1].split()[3]),
                      bondes=dataGame[dataGame[4] - 1].split()[1]).database_buys_bondes()
    await bot.send_message(message.chat.id,'buys')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)