import sqlite3, logging, math, os, random, datetime, config
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
   money INT);
""")
conn.commit()
logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(config.TOKEN)
dp = Dispatcher(bot=bot, storage=memory)
@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    try:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", (message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name, 0))
        conn.commit()
    except sqlite3.InternalError:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Старт')
    await dp.bot.set_my_commands([
        types.BotCommand("rules", "Правила игры"),
    ])
    await message.reply('Привет! Это бот о финансовой грамотности, в этом курсе вы будете иначе мыслить, '
                        'и не будете жить от зарплаты до зарплаты, здесь будут ситуации максимально приближённые к '
                        'реальной жизни, по этому курс точно не будет скучным!\nЕсли вы никогда не играли в подобные '
                        'игры рекомендую ознакомиться с правилами - /rules\nЧто бы присоедениться к группе - join ('
                        'id)\nЧто создать лобби - старт',
                        reply_markup=markup)
    await bot.send_message(message.chat.id, 'Work')

@dp.message_handler(commands='rules')
async def rules(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
