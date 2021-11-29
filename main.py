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
        mass = []
        for i in range(1, dataU[6]+1):
            mass.append(str(i))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
        markup.add(*mass)
        await bot.send_message(message.chat.id, f'Для начала вам нужно выбрать уровень\nВаши доступные уровни {dataU[6]}\n(Максимальный 30)', reply_markup=markup)
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
    if int(dataU[6]) < int(message.text) and int(message.text) == 0:
        await bot.send_message(message.chat.id, 'Вам еще не доступен этот уровень')
        return
    elif int(message.text) >= 31:
        await bot.send_message(message.chat.id, 'Максимальный уровень 30')
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add('Продолжить')
    levels.choiceLevel(int(message.text),message.chat.id).work()
    data.data(message.chat.id, column='levelNow', changes=dataU[6]).dataChanges()
    dataU = data.data(message.chat.id, userName = message.chat.username, userFirst= message.chat.first_name, userLast= message.chat.last_name).dataUser()
    dataGame = data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
                      userLast=message.chat.last_name).dataGame()
    await bot.send_message(message.chat.id, f'Уровень - {dataU[7]}\nПрофессия - ' + ' '.join(dataGame[9].split()[:-1]) +
                           f' зарплата - {"{0:,}".format(int(dataGame[9].split()[-1])).replace(",", " ")} $' + f'\nВаша цель собрать наличных - ' +  '{0:,}'.format(dataGame[8]).replace(',', ' ') + ' $', reply_markup=markup)
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
    bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (dataBusinesses[5] * dataBusinesses[6]) +  (dataBusinesses[7] * dataBusinesses[8])
    async with state.proxy() as datas:
        if dataUser[4] <= -1:
            await bot.send_message(message.chat.id, 'Вы проиграли, начните игру еще раз')
            data.data(message.chat.id).dataNewGame()
            await state.finish()
            return
        '''if message.text.lower() == '1':
            await bot.send_message(message.chat.id, f'Сколько хотите купить {dataCoins[1].split()[3]}')
            datas['coin'] = dataCoins[1].split()[3]
            datas['iscoin'] = True
            await game.buys.set()
        elif message.text.lower() == '2':
            await bot.send_message(message.chat.id, f'Сколько хотите купить {dataCoins[1].split()[3]}')
            datas['coin'] = dataCoins[1].split()[3]
            datas['iscoin'] = True
            await game.buys.set()
        elif message.text.lower() == '3':
            await bot.send_message(message.chat.id, f'Сколько хотите купить {dataCoins[1].split()[3]}')
            datas['coin'] = dataCoins[1].split()[3]
            datas['iscoin'] = True
            await game.buys.set()
        elif message.text.lower() == '4':
            await bot.send_message(message.chat.id, f'Сколько хотите купить {dataCoins[1].split()[3]}')
            datas['coin'] = dataCoins[1].split()[3]
            datas['iscoin'] = True
            await game.buys.set()
        elif message.text.lower() == '5':
            await bot.send_message(message.chat.id, f'Сколько хотите купить {dataCoins[1].split()[3]}')
            datas['coin'] = dataCoins[1].split()[3]
            datas['iscoin'] = True
            await game.buys.set()'''
        if message.text.lower() == 'отключить/включить подтверждение':
            if dataUser[10] == True:
                data.data(message.chat.id, column='notification', changes=False).dataChanges()
                await bot.send_message(message.chat.id, 'Уведомления выключены')
            else:
                data.data(message.chat.id, column='notification', changes=True).dataChanges()
                await bot.send_message(message.chat.id, 'Уведомления включены')
        if message.text.lower() == 'статистика':
            await bot.send_message(message.chat.id, 'Профессия - ' + ' '.join(dataGame[9].split()[:-1]) + f'\nЗарплата: '
                                                    f'{"{0:,}".format(int(dataGame[9].split()[-1])).replace(",", " ")}\nНаличные: {"{0:,}".format(dataUser[4]).replace(",", " ")}\nОбщий доход: '
                                                    f'{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines)}\nРасходы: {"{0:,}".format(int(dataGame[7] + (dataUser[11] / 100 * 4))).replace(",", " ")}\nКредит: {"{0:,}".format(int(dataUser[11])).replace(",", " ")}')
            if dataStock[1] == 0 and dataStock[2] == 0 and dataStock[3] == 0 and dataStock[4] == 0 and dataStock[5] == 0:
                await bot.send_message(message.chat.id, 'У вас нет акций')
            else:
                await bot.send_message(message.chat.id,
                                       f'Связьком: {"{0:,}".format(dataStock[1]).replace(",", " ")}\nНефтехим: {"{0:,}".format(dataStock[2]).replace(",", " ")}\n'
                                       f'Инвестбанк: {"{0:,}".format(dataStock[3]).replace(",", " ")}\nАгросбыт: {"{0:,}".format(dataStock[4]).replace(",", " ")}\n'
                                       f'Металлпром: {"{0:,}".format(dataStock[5]).replace(",", " ")}')
            if dataBonds[1] == 0:
                await bot.send_message(message.chat.id, 'У вас нет облигаций')
            else:
                await bot.send_message(message.chat.id, f'Вексель: {"{0:,}".format(dataBonds[1]).replace(",", " ")} доход - {"{0:,}".format(dataBonds[1] * 300).replace(",", " ")}')
            if dataCoins[2] == 0 and dataCoins[3] == 0 and dataCoins[4] == 0 and dataCoins[5] == 0 and dataCoins[6] == 0:
                await bot.send_message(message.chat.id, 'У вас нету криптовалюты')
            if dataBusinesses[1] == 0 and dataBusinesses[3] == 0 and dataBusinesses[5] == 0 and dataBusinesses[7] == 0:
                await bot.send_message(message.chat.id, 'У вас нету бизнесов')
            else:
                await bot.send_message(message.chat.id, f'AMD: {"{0:,}".format(dataBusinesses[1]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[1] * dataBusinesses[2]).replace(",", " ")}'
                                                        f'\nIntel: {"{0:,}".format(dataBusinesses[3]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[3] * dataBusinesses[4]).replace(",", " ")}'
                                                        f'\nNvidia: {"{0:,}".format(dataBusinesses[5]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[5] * dataBusinesses[6]).replace(",", " ")}'
                                                        f'\nApple: {"{0:,}".format(dataBusinesses[7]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[7] * dataBusinesses[8]).replace(",", " ")}')
        if message.text.lower() == 'магазин криптовалют':
            await bot.send_message(message.chat.id, assets.assets(message.chat.id, 0, 0).enterCript())
        if message.text.lower() == 'продолжить':
            if dataGame[5] == 0:
                if dataGame[8] <= dataUser[4]:
                    if dataUser[6] == dataUser[7]:
                        await bot.send_message(message.chat.id, f'Поздравляю! Вы прошли {dataUser[7]} уровент\nВам открыт {dataUser[7] + 1} уровент')
                        data.data(message.chat.id, column='levelOpen', changes=dataUser[6] + 1).dataChanges()
                        data.data(message.chat.id).dataNewGame()
                        await state.finish()
                        return
                    else:
                        await bot.send_message(message.chat.id,
                                               f'Поздравляю! Вы прошли {dataUser[7]} уровент\nНовый уровень не '
                                               f'открыт. Пройдите {dataUser[6]} уровень что бы открыть новый уровень')
                        data.data(message.chat.id).dataNewGame()
                        await state.finish()
                        return
                else:
                    await bot.send_message(message.chat.id, f'Вы не достигли цели, попробуйте еще раз')
                    data.data(message.chat.id).dataNewGame()
                    await state.finish()
                    return
            levels.choiceLevel(dataUser[7], message.chat.id).dataBaseUpt()
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add('Продолжить')
            if dataGame[4] != 4:
                text = ''
                if dataGame[dataGame[4]].split()[0].lower() == 'акция':
                    datas['stock'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Отключить/включить подтверждение')
                elif dataGame[dataGame[4]].split()[0].lower() == 'облигация':
                    datas['bonds'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Отключить/включить подтверждение')
                    mass = list(dataGame[dataGame[4]].split())
                    mass[3] = "{0:,}".format(int(mass[3])).replace(",", " ")
                    mass[7] = "{0:,}".format(int(mass[7])).replace(",", " ")
                    mass[11] = "{0:,}".format(int(mass[11])).replace(",", " ")
                    for i in mass:
                        text += i + ' '
                elif dataGame[dataGame[4]].split()[0].lower() == 'бизнес':
                    datas['business'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Отключить/включить подтверждение')
                    mass = list(dataGame[dataGame[4]].split())
                    mass[3] = "{0:,}".format(int(mass[3])).replace(",", " ")
                    mass[7] = "{0:,}".format(int(mass[7])).replace(",", " ")
                    mass[10] = "{0:,}".format(int(mass[10])).replace(",", " ")
                    mass[14] = "{0:,}".format(int(mass[14])).replace(",", " ")
                    for i in mass:
                        text += i + ' '
                if text == '':
                    text = dataGame[dataGame[4]]
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют')
                await bot.send_message(message.chat.id, text, reply_markup=markup)
                datas['time'] = datetime.datetime.now()
                return
            else:
                levels.choiceLevel(dataUser[7], message.chat.id).dataBaseMoves()
                await bot.send_message(message.chat.id, f'Итоги месяца. Осталось месяцев - {dataGame[5]}\nВаш прошлый баланс: {"{0:,}".format(int(dataUser[4])).replace(",", " ")} $\nОбщий доход: '
                                                        f'{"{0:,}".format(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)).replace(",", " ")} $\nРасходы: {"{0:,}".format(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines - (dataGame[7] + (dataUser[11] / 100 * 4)))).replace(",", " ")} $\nИтог: {"{0:,}".format(int(dataUser[4])).replace(",", " ")} $\nВаш '
                                                        f'текущий баланс: {"{0:,}".format(int(dataUser[4]) + int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300)).replace(",", " ")} $')
                assets.assets(message.chat.id, 0, 0).random_criptWrite()
                data.data(message.chat.id, column='money', changes=int(dataUser[4]) + int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 - (dataGame[7]  + (dataUser[11] / 100 * 4))) + bussines).dataChanges()
                return
        try:
            if message.text.lower() == 'купить' and datas['stock']:
                await bot.send_message(message.chat.id, 'Сколько акций хотите купить?')
                await game.buys.set()
            elif message.text.lower() == 'купить' and datas['bonds']:
                await bot.send_message(message.chat.id, 'Сколько облигаций хотите купить?')
                await game.buys.set()
            elif message.text.lower() == 'купить' and datas['business']:
                if int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3]) < 0:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Отмена', 'Взять кредит')
                    await bot.send_message(message.chat.id,
                                           'У вас нехватает денег, введите количевство еще раз\nИли введите "Отмена" что бы отменить покупку\nИли возьмите кредит - "Взять кредит"',
                                           reply_markup=markup)
                    await game.buysBusiness.set()
                    return
                if dataUser[10] == False:
                        await bot.send_message(message.chat.id,
                                               f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[13])).replace(",", " ")}\n'
                                                 f'Остаток наличных {str("{0:,}".format(int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}')
                        assets.assets(userid=message.chat.id, number=1,
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                else:
                    await bot.send_message(message.chat.id,
                                           f'Хотите купить бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[13])).replace(",", " ")}\n'
                                                 f'Остаток наличных {str("{0:,}".format(int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                             f'\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"')
                    await game.buysBusiness.set()
        except KeyError:
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False

@dp.message_handler(lambda message: message.text.lower() == 'отмена', state=[game.buys, game.buysBusiness])
async def cancel(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    markup.add('Продолжить')
    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
    await game.waitingGame.set()
@dp.message_handler(lambda message: not message.text.isdigit() and message.text.lower() != 'да' and message.text.lower() != 'нет' and message.text.lower() != 'взять кредит',  state=game.buys)
async def error(message: types.Message):
    await bot.send_message(message.chat.id, 'Не коректно указано количевство')

@dp.message_handler(lambda message: int(message.text) > 0 and message.text.lower() != 'да' and message.text.lower() != 'нет' and message.text.lower() != 'взять кредит')
async def error(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите число больше 0')


@dp.message_handler(state=[game.buys, game.buysBusiness])
async def buys(message: types.Message, state: FSMContext):
    dataGame = data.data(message.chat.id).dataGame()
    dataUser = data.data(message.chat.id).dataUser()
    if message.text.isdigit():
        async with state.proxy() as datas:
            datas['num'] = message.text
    async with state.proxy() as datas:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                   'Отключить/включить подтверждение')
        if message.text.lower() == 'взять кредит':
            if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                assets.assets(userid=message.chat.id, number=datas['num'], price=int(dataGame[dataGame[4] - 1].split()[3]), coin=dataGame[dataGame[4]-1].split()[1]).crediUser()
            elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                assets.assets(userid=message.chat.id, number=datas['num'],
                              price=int(dataGame[dataGame[4] - 1].split()[3]),
                              bondes = dataGame[dataGame[4] - 1].split()[1]).crediUser()
            elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                assets.assets(userid=message.chat.id, number=1, price=int(dataGame[dataGame[4] - 1].split()[3]), business = dataGame[dataGame[4] - 1].split()[1]).crediUser()
            await bot.send_message(message.chat.id, 'Кредит взят', reply_markup=markup)
            await game.waitingGame.set()
            return
        if int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]) < 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена', 'Взять кредит')
            await bot.send_message(message.chat.id,
                                   'У вас нехватает денег, введите количевство еще раз\nЧто бы отменить покупку введите "Отмена"\nИли возьмите кредит "Взять кредит"',
                                   reply_markup=markup)
            return
        if dataUser[10] == False:
            if dataGame[dataGame[4]-1].split()[0].lower() == 'акция':
                await bot.send_message(message.chat.id,
                                       f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4]-1].split()[1]}.'
                                       f' По цене ' + str("{0:,}".format(dataGame[dataGame[4]-1].split()[3]).replace(",", " "))
                                       + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4]-1].split()[3]))).replace(",", " ")}\n'
                                                     f'Остаток наличных {str("{0:,}".format(int(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4]-1].split()[3]))).replace(",", " "))}')
                assets.assets(userid=message.chat.id, number=datas["num"], price=int(dataGame[dataGame[4]-1].split()[3]), coin=dataGame[dataGame[4]-1].split()[1]).database_buys_stock()
                await game.waitingGame.set()
            elif dataGame[dataGame[4]-1].split()[0].lower() == 'облигация':
                await bot.send_message(message.chat.id,
                                       f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                       f' По цене ' + str("{0:,}".format(dataGame[dataGame[4]-1].split()[3]).replace(",", " "))
                                       + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4]-1].split()[3]))).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                         f'Остаток наличных {str("{0:,}".format(int(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4]-1].split()[3]))).replace(",", " "))}')
                assets.assets(userid=message.chat.id, number=datas["num"], price=int(dataGame[dataGame[4] - 1].split()[3]),
                              bondes=dataGame[dataGame[4] - 1].split()[1]).database_buys_bondes()
                await game.waitingGame.set()
        else:
            if message.text.lower() == 'да':
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(dataGame[dataGame[4] - 1].split()[3]).replace(",", " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}')
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  coin=dataGame[dataGame[4] - 1].split()[1]).database_buys_stock()
                    await game.waitingGame.set()
                    return
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {datas["num"]} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(dataGame[dataGame[4] - 1].split()[3])
                                           + f' на сумму {int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3])}. С пассивным доходом {int(datas["num"]) * 300}\n'
                                             f'Остаток наличных {str(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))}')
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  bondes=dataGame[dataGame[4] - 1].split()[1]).database_buys_bondes()
                    await game.waitingGame.set()
                    return
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[13])).replace(",", " ")}\n'
                                           f'Остаток наличных {str("{0:,}".format(int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}')
                    assets.assets(userid=message.chat.id, number=1,
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                    await game.waitingGame.set()
                    return
            elif message.text.lower() == 'нет':
                await bot.send_message(message.chat.id, 'Действие отменено')
                await game.waitingGame.set()
            if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                await bot.send_message(message.chat.id,
                                       f'Хотите купить {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                       f' По цене ' + str(
                                           "{0:,}".format(dataGame[dataGame[4] - 1].split()[3]).replace(",", " "))
                                       + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                         f'Остаток наличных {str("{0:,}".format(int(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                    f'\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"')
            elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                await bot.send_message(message.chat.id,
                                       f'Хотите купить {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                       f' По цене ' + str(
                                           "{0:,}".format(dataGame[dataGame[4] - 1].split()[3]).replace(",", " "))
                                       + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                         f'Остаток наличных {str("{0:,}".format(int(int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                                         f'\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"')
            elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                await bot.send_message(message.chat.id,
                                       f'Хотите купить бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                       f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[13])).replace(",", " ")}\n'
                                       f'Остаток наличных {str("{0:,}".format(int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                       f'\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
