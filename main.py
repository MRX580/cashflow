import sqlite3, logging, math, os, random, datetime, config, level.choicelevel as levels
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
bot = Bot(config.TOKEN)
dp = Dispatcher(bot=bot, storage=memory)


class game(StatesGroup):
    choiceLevel = State()
    waitingGame = State()


async def datebase_user(userid):
    sqlite_select_query = """SELECT * FROM users"""
    cur.execute(sqlite_select_query)
    record = cur.fetchall()
    print(record)
    for i in record:
        if i[0] == userid:
            return i


async def addDatebase(userid, userName, userFirst, userLast):
    try:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (userid, userName, userFirst, userLast, 0, False, 1, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        pass


@dp.message_handler(commands='start')
async def start(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    await addDatebase(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
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
    await addDatebase(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types='text')
async def main(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    await addDatebase(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
    if message.text.lower() == 'начать игру':
        await addDatebase(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
        data = await datebase_user(message.chat.id)
        print(data[0])
        await bot.send_message(message.chat.id, f'Для начала вам нужно выбрать уровень\nВаши доступные уровни {data[6]}')
        await game.choiceLevel.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=game.choiceLevel)
async def errordigit(message: types.Message):
    await bot.send_message(message.chat.id, 'Не правильно введен уровень, повторите еще раз')


@dp.message_handler(state=game.choiceLevel)
async def choicelevel(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    await addDatebase(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
    data = await datebase_user(message.chat.id)
    if int(data[6]) < int(message.text):
        await bot.send_message(message.chat.id, 'Вам еще не доступен этот уровень')
        return
    await bot.send_message(message.chat.id, levels.choiceLevel(int(data[6])).work())
    await game.waitingGame.set()


@dp.message_handler(state=game.waitingGame)
async def choicelevel(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
