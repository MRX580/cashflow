import sqlite3, logging, math, os, random, datetime, config, level.choicelevel as levels, data
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   username TEXT,
   fname TEXT,
   lname TEXT,
   money INT,
   isgame BOOLEAN,
   levelOpen INT,
   levelNow INT);
""")
conn.commit()
logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
API_TOKEN = '2053817098:AAEnEIiZno_7vwOCusmq1KBehlpjrS0WkM8'
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot, storage=memory)


class game(StatesGroup):
    choiceLevel = State()
    waitingGame = State()



@dp.message_handler(commands='start')
async def start(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Начать игру')
    await dp.bot.set_my_commands([
        types.BotCommand("rules", "Правила игры"),
    ])
    await message.reply('Привет! Это бот о финансовой грамотности, в этом курсе вы будете иначе мыслить, '
                        'и не будете жить от зарплаты до зарплаты, здесь будут ситуации максимально приближённые к '
                        'реальной жизни, по этому курс точно не будет скучным!\nЕсли вы никогда не играли в подобные '
                        'игры рекомендую ознакомиться с правилами - /rules\nЧто бы присоедениться к группе - join ('
                        'id)\nЧто начать игру введите - Начать игру',
                        reply_markup=markup)
    await bot.send_message(message.chat.id, 'Work')


@dp.message_handler(commands='rules')
async def rules(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name).databaseNewUser()
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types='text')
async def main(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    data.data(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name).databaseNewUser()
    if message.text.lower() == 'начать игру':
        dataU = data.data(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name).dataUser()
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
    dataU = data.data(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name).dataUser()
    if int(dataU[6]) < int(message.text):
        await bot.send_message(message.chat.id, 'Вам еще не доступен этот уровень')
        return
    await bot.send_message(message.chat.id, levels.choiceLevel(int(dataU[6])).work())
    await game.waitingGame.set()


@dp.message_handler(state=game.waitingGame)
async def choicelevel(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
