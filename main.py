import assets
import config
import data
import datetime
import level.choicelevel as levels
import logging

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
    sells = State()
    sellsBusiness = State()
    resetCredit = State()
    sellOrBuy = State()
    insurance = State()
    defeat = State()
    defeatSell = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'start')
    data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
              userLast=message.chat.last_name).databaseNewUser()
    try:
        dataUser = data.data(message.chat.id).dataUser()
        if dataUser[7] >= 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            if dataUser[11] > 0:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение', 'погасить кредит')
            else:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение')
            await bot.send_message(message.chat.id, 'Бот был перезапущен, игра продолжена', reply_markup=markup)
            await game.waitingGame.set()
            return
    except TypeError:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    data.data(message.chat.id).donate()
    markup.add('Начать игру')
    await dp.bot.set_my_commands([
        types.BotCommand("rules", "Правила игры"),
        types.BotCommand("donate", "Покупка премиума"),
    ])
    await message.reply('Привет! Это бот о финансовой грамотности, в этом курсе вы будете иначе мыслить, '
                        'и не будете жить от зарплаты до зарплаты.\nЗдесь будут ситуации максимально приближённые к '
                        'реальной жизни, поэтому курс точно не будет скучным!\nЕсли вы никогда не играли в подобные '
                        'игры рекомендую ознакомиться с правилами - /rules\nДонат - /donate\nЧто бы присоедениться к группе - join ('
                        'id)\nЧто начать игру введите - Начать игру',
                        reply_markup=markup)


@dp.message_handler(commands='rules',
                    state=[game.buys, game.buysBusiness, game.waitingGame, game.choiceLevel, game.buysBusiness,
                           game.sellsBusiness, game.sells, game.resetCredit, game.sellOrBuy])
async def rules(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'rules')
    data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
              userLast=message.chat.last_name).databaseNewUser()
    try:
        dataUser = data.data(message.chat.id).dataUser()
        if dataUser[7] >= 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            if dataUser[11] > 0:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение', 'погасить кредит')
            else:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение')
            await bot.send_message(message.chat.id, 'Бот был перезапущен, игра продолжена', reply_markup=markup)
            await game.waitingGame.set()
            return
    except TypeError:
        pass
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands='donate',
                    state=[game.buys, game.buysBusiness, game.waitingGame, game.choiceLevel, game.buysBusiness,
                           game.sellsBusiness, game.sells, game.resetCredit, game.sellOrBuy])
async def donate(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'donate')
    data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
              userLast=message.chat.last_name).databaseNewUser()
    try:
        dataUser = data.data(message.chat.id).dataUser()
        if dataUser[7] >= 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            if dataUser[11] > 0:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение', 'погасить кредит')
            else:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение')
            await bot.send_message(message.chat.id, 'Бот был перезапущен, игра продолжена', reply_markup=markup)
            await game.waitingGame.set()
            return
    except TypeError:
        pass
    await bot.send_message(message.chat.id, data.data(message.chat.id, money=200).donate())


@dp.message_handler(content_types='text')
async def main(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'text')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Начать игру')
    data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
              userLast=message.chat.last_name).databaseNewUser()
    try:
        dataUser = data.data(message.chat.id).dataUser()
        if dataUser[7] >= 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            if dataUser[11] > 0:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение', 'погасить кредит')
            else:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение')
            await bot.send_message(message.chat.id, 'Бот был перезапущен, игра продолжена', reply_markup=markup)
            await game.waitingGame.set()
            return
    except TypeError:
        pass
    if message.text.lower() == 'начать игру':
        dataU = data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
                          userLast=message.chat.last_name).dataUser()
        mass = []
        for i in range(1, dataU[6] + 1):
            mass.append(str(i))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
        markup.add(*mass)
        await bot.send_message(message.chat.id,
                               f'Для начала вам нужно выбрать уровень\nВаши доступные уровни {dataU[6]}\n(Максимальный 30)',
                               reply_markup=markup)
        await game.choiceLevel.set()
        return
    await bot.send_message(message.chat.id, 'Введите "Начать игру" что бы начать игру', reply_markup=markup)


@dp.message_handler(lambda message: not message.text.isdigit(), state=game.choiceLevel)
async def errordigit(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + '(errordigit)')
    await bot.send_message(message.chat.id, 'Не правильно введен уровень, повторите еще раз')


@dp.message_handler(state=game.choiceLevel)
async def choicelevel(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'choicelevel')
    dataU = data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
                      userLast=message.chat.last_name).dataUser()
    if int(dataU[6]) < int(message.text) or int(message.text) == 0:
        await bot.send_message(message.chat.id, 'Вам еще не доступен этот уровень')
        return
    elif int(message.text) >= 31:
        await bot.send_message(message.chat.id, 'Максимальный уровень 30')
        return
    elif int(message.text) >= 3 and dataU[8] == False:
        await bot.send_message(message.chat.id, 'Что бы играть дальше вам нужно купить премиум - /donate')
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3)
    markup.add('Продолжить')
    levels.choiceLevel(int(message.text), message.chat.id).work()
    data.data(message.chat.id, column='levelNow', changes=int(message.text)).dataChanges()
    dataU = data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
                      userLast=message.chat.last_name).dataUser()
    dataGame = data.data(message.chat.id, userName=message.chat.username, userFirst=message.chat.first_name,
                         userLast=message.chat.last_name).dataGame()
    levels.choiceLevel(dataU[7], message.chat.id).dataBaseUpt()
    await bot.send_message(message.chat.id, f'Уровень - {dataU[7]}\nПрофессия - ' + ' '.join(dataGame[9].split()[:-1]) +
                           f' зарплата - {"{0:,}".format(int(dataGame[9].split()[-1])).replace(",", " ")} $' + f''
                                                                                                               f'\nВаша цель собрать наличных(кредит учитывается) - ' + '{0:,}'.format(
        dataGame[8]).replace(',', ' ') + f' $\nЗа {dataGame[5]} месяцев\nВаши наличные - {dataU[4]}',
                           reply_markup=markup)
    await game.waitingGame.set()


@dp.message_handler(state=game.waitingGame)
async def choicelevel(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'waitingGame')
    try:
        async with state.proxy() as datas:
            if float(str(datetime.datetime.now() - datas['time']).replace(':', '')) < 0.3:
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
    dataInsurance = data.data(message.chat.id).dataInsurance()
    dataBuying = data.data(message.chat.id).dataBuing()
    bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (
            dataBusinesses[5] * dataBusinesses[6]) + (dataBusinesses[7] * dataBusinesses[8])
    async with state.proxy() as datas:
        if dataUser[4] <= -1:
            await bot.send_message(message.chat.id, 'вы проиграли, начните игру еще раз')
            text = ''
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            mass = ['0', 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром', 'Bitcoin', 'XRP', 'Avalanche',
                    'Solana', 'Ethereum', 'Вексель']
            async with state.proxy():
                if dataStock[1] == 0 and dataStock[2] == 0 and dataStock[3] == 0 and dataStock[4] == 0 and dataStock[
                    5] == 0:
                    pass
                else:
                    markup.add('Акции')
                    stockMass1 = ['Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
                    stockMass2 = [dataStock[1], dataStock[2], dataStock[3], dataStock[4], dataStock[5]]
                    stock = ''
                    massive = [[],[]]
                    for i in enumerate(stockMass2):
                        if i[1] >= 1:
                            massive[0].append(stockMass1[i[0]])
                            massive[1].append(stockMass2[i[0]])
                            text += 'Акция: ' + stockMass1[i[0]] + f' {stockMass2[i[0]]} шт\n'
                            stock += 'Акция: ' + stockMass1[i[0]] + f' {stockMass2[i[0]]} шт\n'
                if dataBonds[1] == 0:
                    pass
                else:
                    bondes = ''
                    markup.add('Облигации')
                    massive[0].append(stockMass1[i[0]])
                    massive[1].append(stockMass2[i[0]])
                    text += 'Облигация: Вексель: ' + str(dataBonds[1]) + ' шт\n'
                    bondes += 'Облигация: Вексель: ' + str(dataBonds[1]) + ' шт\n'
                if dataCoins[2] == 0 and dataCoins[3] == 0 and dataCoins[4] == 0 and dataCoins[5] == 0 and dataCoins[
                    6] == 0:
                    pass
                else:
                    markup.add('Криптовалюты')
                    coinMass1 = ['Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum']
                    coinMass2 = [dataCoins[2], dataCoins[3], dataCoins[4], dataCoins[5], dataCoins[6]]
                    kripta = ''
                    for i in enumerate(coinMass2):
                        if i[1] >= 1:
                            massive[0].append(stockMass1[i[0]])
                            massive[1].append(stockMass2[i[0]])
                            text += 'Криптовалюта: ' + coinMass1[i[0]] + f' {coinMass2[i[0]]} шт\n'
                            kripta += 'Криптовалюта: ' + coinMass1[i[0]] + f' {coinMass2[i[0]]} шт\n'
                if dataBusinesses[1] == 0 and dataBusinesses[3] == 0 and dataBusinesses[5] == 0 and dataBusinesses[
                    7] == 0:
                    pass
                else:
                    markup.add('Бизнесы')
                    massBussines1 = ['AMD', 'Intel', 'Nvidia', 'Apple']
                    massBussines2 = [dataBusinesses[2], dataBusinesses[4], dataBusinesses[6], dataBusinesses[8]]
                    for i in enumerate(massBussines2):
                        if i[1] >= 1:
                            massive[0].append(stockMass1[i[0]])
                            massive[1].append(stockMass2[i[0]])
                            text += 'Бизнес: ' + massBussines1[i[0]] + '\n'

            if text != '':
                general = []
                for i in enumerate(mass):
                    if i[1].lower() in text.lower() and i[0] != 0:
                        for j in enumerate(massive[0]):
                            if j[1].lower() in i[1].lower():
                                general.append(float(dataBuying[i[0]].split()[0]) / float(dataBuying[i[0]].split()[1]) * massive[1][j[0]])
                if sum(general) < -(dataUser[4]):
                    print(general)
                    data.data(message.chat.id).dataNewGame()
                    await state.finish()
                    return
                await bot.send_message(message.chat.id,
                                       'Выбирите актив для продажи что бы погасить вернуть долг:\n' + text + f'\nВам нужно погасить {-(dataUser[4])} $',
                                       reply_markup=markup)
                await game.defeat.set()
            else:
                data.data(message.chat.id).dataNewGame()
                await state.finish()
            return
        try:
            if datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                if dataUser[11] > 0:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение', 'Погасить кредит')
                else:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение')
                if message.text.lower() == 'отмена':
                    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                    return
        except Exception:
            pass
        try:
            if message.text.lower() == '1' and datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                markup.add('Купить', 'Продать', 'Отмена')
                await bot.send_message(message.chat.id, f'Выберите дейсвие купить/продать {dataCoins[1].split()[3]}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='choice',
                          changes=dataCoins[1].split()[3] + ' ' + dataCoins[1].split()[4]).dataChangesCoin()
                datas['iscoin'] = True
                datas['ismagazine'] = False
                await game.sellOrBuy.set()
            elif message.text.lower() == '2' and datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                markup.add('Купить', 'Продать', 'Отмена')
                await bot.send_message(message.chat.id, f'Выберите дейсвие купить/продать {dataCoins[1].split()[6]}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='choice',
                          changes=dataCoins[1].split()[6] + ' ' + dataCoins[1].split()[7]).dataChangesCoin()
                datas['iscoin'] = True
                datas['ismagazine'] = False
                await game.sellOrBuy.set()
            elif message.text.lower() == '3' and datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                markup.add('Купить', 'Продать', 'Отмена')
                await bot.send_message(message.chat.id, f'Выберите дейсвие купить/продать {dataCoins[1].split()[9]}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='choice',
                          changes=dataCoins[1].split()[9] + ' ' + dataCoins[1].split()[10]).dataChangesCoin()
                datas['iscoin'] = True
                datas['ismagazine'] = False
                await game.sellOrBuy.set()
            elif message.text.lower() == '4' and datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                markup.add('Купить', 'Продать', 'Отмена')
                await bot.send_message(message.chat.id, f'Выберите дейсвие купить/продать {dataCoins[1].split()[12]}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='choice',
                          changes=dataCoins[1].split()[12] + ' ' + dataCoins[1].split()[13]).dataChangesCoin()
                datas['iscoin'] = True
                datas['ismagazine'] = False
                await game.sellOrBuy.set()
            elif message.text.lower() == '5' and datas['ismagazine']:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                markup.add('Купить', 'Продать', 'Отмена')
                await bot.send_message(message.chat.id, f'Выберите дейсвие купить/продать {dataCoins[1].split()[15]}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='choice',
                          changes=dataCoins[1].split()[15] + ' ' + dataCoins[1].split()[16]).dataChangesCoin()
                datas['iscoin'] = True
                datas['ismagazine'] = False
                await game.sellOrBuy.set()
        except Exception:
            pass
        if message.text.lower() == 'погасить кредит':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Погасить на все', 'Отмена')
            await bot.send_message(message.chat.id,
                                   f'Ваш кредит {"{0:,}".format(int(dataUser[11])).replace(",", " ")} $'
                                   f'\nВаш баланс {"{0:,}".format(round(dataUser[4], 4)).replace(",", " ")} $'
                                   f'\nНа какую сумму хотите погасить?', reply_markup=markup)
            await game.resetCredit.set()
        if message.text.lower() == 'отключить/включить подтверждение':
            if dataUser[10] == True:
                data.data(message.chat.id, column='notification', changes=False).dataChanges()
                await bot.send_message(message.chat.id, 'Уведомления выключены')
            else:
                data.data(message.chat.id, column='notification', changes=True).dataChanges()
                await bot.send_message(message.chat.id, 'Уведомления включены')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        if dataUser[11] > 0:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение', 'Погасить кредит')
        else:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение')
        if message.text.lower() == 'статистика':
            datas['ismagazine'] = False
            await bot.send_message(message.chat.id,
                                   'Профессия - ' + ' '.join(dataGame[9].split()[:-1]) + f'\nЗарплата: '
                                                                                         f'{"{0:,}".format(int(dataGame[9].split()[-1])).replace(",", " ")} $'
                                                                                         f'\nНаличные: {"{0:,}".format(round(dataUser[4], 4)).replace(",", " ")} $\nОбщий доход: '
                                                                                         f'{"{0:,}".format((int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines))} $'
                                                                                         f'\nРасходы: {"{0:,}".format(int(dataGame[7] + (dataUser[11] / 100 * 4))).replace(",", " ")} $'
                                                                                         f'\nКредит: {"{0:,}".format(int(dataUser[11])).replace(",", " ")} $')
            if dataStock[1] == 0 and dataStock[2] == 0 and dataStock[3] == 0 and dataStock[4] == 0 and dataStock[
                5] == 0:
                await bot.send_message(message.chat.id, 'У вас нет акций')
            else:
                try:
                    stock1 = round(float(dataBuying[1].split()[0]) / float(dataBuying[1].split()[1]), 2)
                except ZeroDivisionError:
                    stock1 = 0
                try:
                    stock2 = round(float(dataBuying[2].split()[0]) / float(dataBuying[2].split()[1]), 2)
                except ZeroDivisionError:
                    stock2 = 0
                try:
                    stock3 = round(float(dataBuying[3].split()[0]) / float(dataBuying[3].split()[1]), 2)
                except ZeroDivisionError:
                    stock3 = 0
                try:
                    stock4 = round(float(dataBuying[4].split()[0]) / float(dataBuying[4].split()[1]), 2)
                except ZeroDivisionError:
                    stock4 = 0
                try:
                    stock5 = round(float(dataBuying[5].split()[0]) / float(dataBuying[5].split()[1]), 2)
                except ZeroDivisionError:
                    stock5 = 0
                await bot.send_message(message.chat.id,
                                       f'Связьком: {"{0:,}".format(dataStock[1]).replace(",", " ")} по цене {stock1} $\nНефтехим: {"{0:,}".format(dataStock[2]).replace(",", " ")} по цене {stock2} $\n'
                                       f'Инвестбанк: {"{0:,}".format(dataStock[3]).replace(",", " ")} по цене {stock3} $\nАгросбыт: {"{0:,}".format(dataStock[4]).replace(",", " ")} по цене {stock4} $\n'
                                       f'Металлпром: {"{0:,}".format(dataStock[5]).replace(",", " ")} по цене {stock5} $')
            if dataBonds[1] == 0:
                await bot.send_message(message.chat.id, 'У вас нет облигаций')
            else:
                try:
                    stock1 = round(float(dataBuying[11].split()[0]) / float(dataBuying[11].split()[1]), 2)
                except ZeroDivisionError:
                    stock1 = 0
                await bot.send_message(message.chat.id,
                                       f'Вексель: {"{0:,}".format(dataBonds[1]).replace(",", " ")} доход - {"{0:,}".format(dataBonds[1] * 300).replace(",", " ")} $ по цене {stock1} $')
            if dataCoins[2] == 0 and dataCoins[3] == 0 and dataCoins[4] == 0 and dataCoins[5] == 0 and dataCoins[
                6] == 0:
                await bot.send_message(message.chat.id, 'У вас нету криптовалюты')
            else:
                try:
                    stock1 = round(float(dataBuying[6].split()[0]) / float(dataBuying[6].split()[1]), 2)
                except ZeroDivisionError:
                    stock1 = 0
                try:
                    stock2 = round(float(dataBuying[7].split()[0]) / float(dataBuying[7].split()[1]), 2)
                except ZeroDivisionError:
                    stock2 = 0
                try:
                    stock3 = round(float(dataBuying[8].split()[0]) / float(dataBuying[8].split()[1]), 2)
                except ZeroDivisionError:
                    stock3 = 0
                try:
                    stock4 = round(float(dataBuying[9].split()[0]) / float(dataBuying[9].split()[1]), 2)
                except ZeroDivisionError:
                    stock4 = 0
                try:
                    stock5 = round(float(dataBuying[10].split()[0]) / float(dataBuying[10].split()[1]), 2)
                except ZeroDivisionError:
                    stock5 = 0
                await bot.send_message(message.chat.id,
                                       f'{dataCoins[1].split()[3]}: {dataCoins[2]} по цене {stock1} $\n'
                                       f'{dataCoins[1].split()[6]}: {dataCoins[3]} по цене {stock2} $\n'
                                       f'{dataCoins[1].split()[9]}: {dataCoins[4]} по цене {stock3} $\n'
                                       f'{dataCoins[1].split()[12]}: {dataCoins[5]} по цене {stock4} $\n'
                                       f'{dataCoins[1].split()[15]}: {dataCoins[6]} по цене {stock5} $',
                                       reply_markup=markup)
            if dataBusinesses[1] == 0 and dataBusinesses[3] == 0 and dataBusinesses[5] == 0 and dataBusinesses[7] == 0:
                await bot.send_message(message.chat.id, 'У вас нету бизнесов')
            else:
                await bot.send_message(message.chat.id,
                                       f'AMD: {"{0:,}".format(dataBusinesses[1]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[1] * dataBusinesses[2]).replace(",", " ")} $ '
                                       f'\nIntel: {"{0:,}".format(dataBusinesses[3]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[3] * dataBusinesses[4]).replace(",", " ")} $'
                                       f'\nNvidia: {"{0:,}".format(dataBusinesses[5]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[5] * dataBusinesses[6]).replace(",", " ")} $'
                                       f'\nApple: {"{0:,}".format(dataBusinesses[7]).replace(",", " ")} пассивный доход: {"{0:,}".format(dataBusinesses[7] * dataBusinesses[8]).replace(",", " ")} $')
            if dataInsurance[1] == 0 and dataInsurance[2] == 0:
                await bot.send_message(message.chat.id, 'У вас нету страховок')
            else:
                await bot.send_message(message.chat.id,
                                       f'Страховка на жизнь будет длиться: {dataInsurance[1]} месяцев\nСтраховка на имущевство будет длиться: {dataInsurance[2]} месяцев')
        if message.text.lower() == 'магазин страховок':
            datas['ismagazine'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=5)
            markup.add('Страховка на жизнь', 'Страховка на имущевство', 'Отмена')
            await bot.send_message(message.chat.id, f'Выберите что купить:\nСтраховка на жизнь/имущевство на 1 год '
                                                    f'{"{0:,}".format((int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20).replace(",", " ")} $',
                                   reply_markup=markup)
            await game.insurance.set()
            return

        def TestFunc(number):
            if dataUser[4] <= dataUser[4] / int(number):
                return 0
            else:
                return dataUser[4] / int(number)
            pass

        if message.text.lower() == 'магазин криптовалют':
            datas['ismagazine'] = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=5)
            markup.add('1', '2', '3', '4', '5', 'Отмена')
            await bot.send_message(message.chat.id,
                                   f'Выберите криптовалюту:\n1 - {dataCoins[1].split()[3]} цена: {"{0:,}".format(int(dataCoins[1].split()[4])).replace(",", " ")} $ У вас {dataCoins[2]}. Можете купить: {round(TestFunc(dataCoins[1].split()[4]), 7)}'
                                   f'\n2 - {dataCoins[1].split()[6]} цена: {"{0:,}".format(int(dataCoins[1].split()[7])).replace(",", " ")} $ У вас {dataCoins[3]}. Можете купить: {round(TestFunc(dataCoins[1].split()[7]), 7)}'
                                   f'\n3 - {dataCoins[1].split()[9]} цена: {"{0:,}".format(int(dataCoins[1].split()[10])).replace(",", " ")} $ У вас {dataCoins[4]}. Можете купить: {round(TestFunc(dataCoins[1].split()[10]), 7)}'
                                   f'\n4 - {dataCoins[1].split()[12]} цена: {"{0:,}".format(int(dataCoins[1].split()[13])).replace(",", " ")} $ У вас {dataCoins[5]}. Можете купить: {round(TestFunc(dataCoins[1].split()[13]), 7)}'
                                   f'\n5 - {dataCoins[1].split()[15]} цена: {"{0:,}".format(int(dataCoins[1].split()[16])).replace(",", " ")} $ У вас {dataCoins[6]}. Можете купить: {round(TestFunc(dataCoins[1].split()[16]), 7)}\n(Обновляется каждый месяц)',
                                   reply_markup=markup)
        if message.text.lower() == 'продолжить':
            datas['ismagazine'] = False
            if dataGame[5] == 0:
                if dataGame[8] <= dataUser[4]:
                    if dataUser[6] == dataUser[7]:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Начать игру')
                        await bot.send_message(message.chat.id,
                                               f'Поздравляю! Вы прошли {dataUser[7]} уровень\nВам открыт {dataUser[7] + 1} уровень',
                                               reply_markup=markup)
                        data.data(message.chat.id, column='levelOpen', changes=dataUser[6] + 1).dataChanges()
                        data.data(message.chat.id).dataNewGame()
                        await state.finish()
                        return
                    else:
                        await bot.send_message(message.chat.id,
                                               f'Поздравляю! Вы прошли {dataUser[7]} уровень\nНовый уровень не '
                                               f'открыт. Пройдите {dataUser[6]} уровень что бы открыть новый уровень',
                                               reply_markup=markup)
                        data.data(message.chat.id).dataNewGame()
                        await state.finish()
                        return
                else:
                    await bot.send_message(message.chat.id, f'Вы не достигли цели, попробуйте еще раз')
                    data.data(message.chat.id).dataNewGame()
                    await state.finish()
                    return
            elif dataGame[8] <= dataUser[4] - dataUser[11]:
                if dataUser[6] == dataUser[7]:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Начать игру')
                    await bot.send_message(message.chat.id,
                                           f'Поздравляю! Вы прошли {dataUser[7]} уровень\nВам открыт {dataUser[7] + 1} уровень',
                                           reply_markup=markup)
                    data.data(message.chat.id, column='levelOpen', changes=dataUser[6] + 1).dataChanges()
                    data.data(message.chat.id).dataNewGame()
                    await state.finish()
                    return
                else:
                    await bot.send_message(message.chat.id,
                                           f'Поздравляю! Вы прошли {dataUser[7]} уровень\nНовый уровень не '
                                           f'открыт. Пройдите {dataUser[6]} уровень что бы открыть новый уровень',
                                           reply_markup=markup)
                    data.data(message.chat.id).dataNewGame()
                    await state.finish()
                    return

            levels.choiceLevel(dataUser[7], message.chat.id).dataBaseUpt()
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False
            datas['iscoin'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add('Продолжить')
            if dataGame[4] != 4:
                text = ''
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                               'Погасить кредит')
                else:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                mass = list(dataGame[dataGame[4]].split())
                print(dataGame[dataGame[4]].split()[0].lower())
                if not mass[1].lower() == 'непредвиденные':
                    if dataGame[dataGame[4]].split()[0].lower() == 'акция':
                        datas['stock'] = True
                        stockMass = [0, 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        mass[3] = "{0:,}".format(int(mass[3])).replace(",", " ")
                        mass[7] = "{0:,}".format(int(mass[7])).replace(",", " ")
                        for i in mass:
                            text += i + ' '
                        for i in range(len(stockMass)):
                            if dataGame[dataGame[4]].split()[1] == stockMass[i]:
                                text += '\nУ вас акций: ' + str(dataStock[i])
                    elif dataGame[dataGame[4]].split()[0].lower() == 'облигация':
                        datas['bonds'] = True
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        mass[3] = "{0:,}".format(int(mass[3])).replace(",", " ")
                        mass[7] = "{0:,}".format(int(mass[7])).replace(",", " ")
                        mass[11] = "{0:,}".format(int(mass[11])).replace(",", " ")
                        for i in mass:
                            text += i + ' '
                        text += '\nУ вас облигаций: ' + str(dataBonds[1])
                    elif dataGame[dataGame[4]].split()[0].lower() == 'бизнес':
                        datas['business'] = True
                        bussines = ['0', 'AMD', '5000', 'Intel', '7000', 'Nvidia', '9000', 'Apple', '12000']
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        mass = list(dataGame[dataGame[4]].split())
                        mass[3] = "{0:,}".format(int(mass[3])).replace(",", " ")
                        mass[7] = "{0:,}".format(int(mass[7])).replace(",", " ")
                        mass[10] = "{0:,}".format(int(mass[10])).replace(",", " ")
                        mass[14] = "{0:,}".format(int(mass[14])).replace(",", " ")
                        for i in mass:
                            text += i + ' '
                        for i in range(len(bussines)):
                            if dataGame[dataGame[4]].split()[1] == bussines[i]:
                                if dataBusinesses[i] == 1:
                                    text += '\nУ вас есть этот бизнес'
                                else:
                                    text += '\nУ вас нету этого бизнеса'
                elif dataGame[dataGame[4]].split()[0].lower() == '(си)':
                    print(1)
                    if text == '':
                        text = dataGame[dataGame[4]]
                    if text.split()[0] == '(СИ)' and dataInsurance[1] > 0:
                        pass
                    else:
                        data.data(message.chat.id, column='money', changes=dataUser[4] - (
                                int(dataGame[9].split()[-1]) + int(
                            dataBonds[1] * 300 + bussines)) / 10).dataChanges()
                elif dataGame[dataGame[4]].split()[0].lower() == '(сж)':
                    print(2)
                    if text == '':
                        text = dataGame[dataGame[4]]
                    if text.split()[0] == '(СЖ)' and dataInsurance[1] > 0:
                        pass
                    else:
                        data.data(message.chat.id, column='money', changes=dataUser[4] - (
                                int(dataGame[9].split()[-1]) + int(
                            dataBonds[1] * 300 + bussines)) / 10).dataChanges()
                elif dataGame[dataGame[4]].split()[0].lower() == '(нд)':
                    print(3)
                    if text == '':
                        text = dataGame[dataGame[4]]
                    data.data(message.chat.id, column='money', changes=dataUser[4] + (
                            int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10).dataChanges()
                if text == '':
                    text = dataGame[dataGame[4]]
                dataUser = data.data(message.chat.id).dataUser()
                if text.split()[0] == '(СЖ)' and dataInsurance[1] > 0:
                    await bot.send_message(message.chat.id,
                                           text + f'\nУ вас была страховка наличные не сняты\nВаш баланс: {"{0:,}".format(round(dataUser[4], 4)).replace(",", " ")}')
                    return
                elif text.split()[0] == '(СИ)' and dataInsurance[2] > 0:
                    await bot.send_message(message.chat.id,
                                           text + f'\nУ вас была страховка наличные не сняты\nВаш баланс: {"{0:,}".format(round(dataUser[4], 4)).replace(",", " ")}')
                    return
                await bot.send_message(message.chat.id,
                                       text + f'\nВаш баланс: {"{0:,}".format(round(dataUser[4], 4)).replace(",", " ")}',
                                       reply_markup=markup)
                datas['time'] = datetime.datetime.now()
                return
            else:
                levels.choiceLevel(dataUser[7], message.chat.id).dataBaseMoves()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                               'Погасить кредит')
                else:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                await bot.send_message(message.chat.id,
                                       f'Итоги месяца. Осталось месяцев - {dataGame[5]}\nВаш прошлый баланс: {"{0:,}".format(round(dataUser[4]), 4).replace(",", " ")} $\nОбщий доход: '
                                       f'{"{0:,}".format(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)).replace(",", " ")} $'
                                       f'\nРасходы: {"{0:,}".format((dataGame[7] + (dataUser[11] / 100 * 4))).replace(",", " ")}'
                                       f' $\nИтог: {"{0:,}".format(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines) - (dataGame[7] + (dataUser[11] / 100 * 4))).replace(",", " ")} $\nВаш '
                                       f'текущий баланс: {"{0:,}".format(int(int(dataUser[4]) + int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines) - (dataGame[7] + (dataUser[11] / 100 * 4)))).replace(",", " ")} $',
                                       reply_markup=markup)
                data.data(message.chat.id, column='money',
                          changes=int(dataUser[4]) + int(dataGame[9].split()[-1]) + int(
                              dataBonds[1] * 300 + bussines) - (dataGame[7] + (dataUser[11] / 100 * 4))).dataChanges()
                if dataInsurance[1] > 0:
                    data.data(message.chat.id, column='СЖ',
                              changes=dataInsurance[1] - 1).dataChangesInsurance()
                if dataInsurance[2] > 0:
                    data.data(message.chat.id, column='СИ',
                              changes=dataInsurance[2] - 1).dataChangesInsurance()
                assets.assets(message.chat.id, 0, 0).random_criptWrite()
                return
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена')
            if message.text.lower() == 'купить' and datas['stock']:
                datas['ismagazine'] = False
                await bot.send_message(message.chat.id, 'Сколько акций хотите купить?', reply_markup=markup)
                await game.buys.set()
            elif message.text.lower() == 'продать' and datas['stock']:
                datas['ismagazine'] = False
                await bot.send_message(message.chat.id, 'Сколько акций хотите продать?', reply_markup=markup)
                await game.sells.set()
            elif message.text.lower() == 'купить' and datas['bonds']:
                datas['ismagazine'] = False
                await bot.send_message(message.chat.id, 'Сколько облигаций хотите купить?', reply_markup=markup)
                await game.buys.set()
            elif message.text.lower() == 'продать' and datas['bonds']:
                datas['ismagazine'] = False
                await bot.send_message(message.chat.id, 'Сколько облигаций хотите продать?', reply_markup=markup)
                await game.sells.set()
            try:
                if message.text.lower() == 'отмена' and datas['isbusiness']:
                    datas['ismagazine'] = False
                    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                    datas['isbusiness'] = False
                    datas['isbusinessell'] = False
                    return
                if message.text.lower() == 'купить' and datas['business'] or datas['isbusiness']:
                    datas['isbusiness'] = True
                    datas['ismagazine'] = False
                    if int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3]) < 0:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Продолжить', 'Взять кредит')
                        await bot.send_message(message.chat.id,
                                               'У вас нехватает наличных, но вы можете взять кредит - "Взять кредит"',
                                               reply_markup=markup)
                        datas['isbusiness'] = False
                        return
                    if dataUser[10] == False:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        if dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                            await bot.send_message(message.chat.id,
                                                   f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                            datas['isbusiness'] = False
                            return
                    else:
                        if message.text.lower() == 'да':
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            if dataUser[11] > 0:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                                           'Погасить кредит')
                            else:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                            await bot.send_message(message.chat.id,
                                                   f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                            datas['isbusiness'] = False
                            return
                        elif message.text.lower() == 'нет':
                            await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                            datas['isbusiness'] = False
                            return
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Да', 'Нет', 'Отмена')
                        await bot.send_message(message.chat.id,
                                               f'Хотите купить бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                               f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                               f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                               f'подтверждение"', reply_markup=markup)
                if message.text.lower() == 'продать' and datas['business'] or datas['isbusinessell']:
                    datas['ismagazine'] = False
                    datas['isbusinessell'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    if dataUser[11] > 0:
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                   'Магазин страховок',
                                   'Отключить/включить подтверждение', 'погасить кредит')
                    else:
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                   'Магазин страховок',
                                   'Отключить/включить подтверждение')
                    massBussines = ['0', 'AMD', dataBusinesses[2], 'Intel', dataBusinesses[4], 'Nvidia',
                                    dataBusinesses[6],
                                    'Apple', dataBusinesses[8]]
                    for i in range(len(massBussines)):
                        if dataGame[dataGame[4] - 1].split()[1] == massBussines[i]:
                            if dataBusinesses[i] >= 1:
                                pass
                            else:
                                await bot.send_message(message.chat.id, 'У вас нету этого бизнеса',
                                                       reply_markup=markup)
                                datas['isbusinessell'] = False
                                return
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    if dataUser[10] == False:
                        await bot.send_message(message.chat.id,
                                               f'Вы продали бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                               reply_markup=markup)
                        assets.assets(userid=message.chat.id, number=1,
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).database_sell_businesses()
                        datas['isbusinessell'] = False
                        return
                    else:
                        if message.text.lower() == 'да':
                            await bot.send_message(message.chat.id,
                                                   f'Вы продали бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[
                                              1]).database_sell_businesses()
                            datas['isbusinessell'] = False
                            return
                        elif message.text.lower() == 'нет':
                            await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                            await game.waitingGame.set()

                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            markup.add('Да', 'Нет', 'Отмена')
                        await bot.send_message(message.chat.id,
                                               f'Хотите продать бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                               f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                               f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                               f'подтверждение"', reply_markup=markup)
                        return
                elif message.text.lower() == 'взять кредит' and datas['business']:
                    datas['ismagazine'] = False
                    if (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[4] >= int(
                            dataGame[dataGame[4] - 1].split()[3]) and (
                            int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] + \
                            dataUser[4] >= int(
                        dataGame[dataGame[4] - 1].split()[3]):
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        assets.assets(userid=message.chat.id, number=1, price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).crediUser()
                        dataUser = data.data(message.chat.id).dataUser()
                        await bot.send_message(message.chat.id,
                                               f'Кредит взят теперь будет сниматься 4 % от вашей суммы '
                                               f'кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                               reply_markup=markup)
                        return
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        await bot.send_message(message.chat.id, 'Ваш общий доход должен быть больше чем сумма кредита '
                                                                'или больше чем сама сумма кредита',
                                               reply_markup=markup)
                        await game.waitingGame.set()
                        return
            except Exception:
                datas['isbusinessell'] = False
                datas['isbusiness'] = False
                if message.text.lower() == 'отмена' and datas['isbusiness']:
                    datas['ismagazine'] = False
                    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                    datas['iscoin'] = False
                    datas['isbusiness'] = False
                    datas['isbusinessell'] = False
                    return
                if message.text.lower() == 'купить' and datas['business'] or datas['isbusiness']:
                    datas['ismagazine'] = False
                    datas['isbusiness'] = True
                    if int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3]) < 0:
                        if (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[4] >= (
                                int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20 and (
                                int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] + \
                                dataUser[4] >= (
                                int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            markup.add('Продолжить', 'Взять кредит')
                            await bot.send_message(message.chat.id,
                                                   'У вас нехватает наличных, но вы можете взять кредит - "Взять кредит"',
                                                   reply_markup=markup)
                            datas['isbusiness'] = False
                            return
                        else:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            if dataUser[11] > 0:
                                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                           'Магазин страховок',
                                           'Отключить/включить подтверждение', 'погасить кредит')
                            else:
                                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                           'Магазин страховок',
                                           'Отключить/включить подтверждение')
                            await bot.send_message(message.chat.id,
                                                   'Ваш общий доход должен быть больше чем сумма кредита или больше чем сама сумма кредита',
                                                   reply_markup=markup)
                            await game.waitingGame.set()
                            datas['isbusiness'] = False
                            return
                    if dataUser[10] == False:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        if dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                            await bot.send_message(message.chat.id,
                                                   f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                            datas['isbusiness'] = False
                            return
                    else:
                        if message.text.lower() == 'да':
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            if dataUser[11] > 0:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                                           'Погасить кредит')
                            else:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                            await bot.send_message(message.chat.id,
                                                   f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                            datas['isbusiness'] = False
                            return
                        elif message.text.lower() == 'нет':
                            await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                            datas['iscoin'] = False
                            datas['isbusiness'] = False
                            return
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Да', 'Нет', 'Отмена')
                        await bot.send_message(message.chat.id,
                                               f'Хотите купить бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                               f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                               f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                               f'подтверждение"', reply_markup=markup)
                if message.text.lower() == 'продать' and datas['business'] or datas['isbusinessell']:
                    datas['isbusinessell'] = True
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    if dataUser[11] > 0:
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                   'Магазин страховок',
                                   'Отключить/включить подтверждение', 'погасить кредит')
                    else:
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                   'Магазин страховок',
                                   'Отключить/включить подтверждение')
                    massBussines = ['0', 'AMD', dataBusinesses[2], 'Intel', dataBusinesses[4], 'Nvidia',
                                    dataBusinesses[6],
                                    'Apple', dataBusinesses[8]]
                    for i in range(len(massBussines)):
                        if dataGame[dataGame[4] - 1].split()[1] == massBussines[i]:
                            if dataBusinesses[i] >= 1:
                                pass
                            else:
                                await bot.send_message(message.chat.id, 'У вас нету этого бизнеса',
                                                       reply_markup=markup)
                                datas['isbusinessell'] = False
                                return
                    if dataUser[10] == False:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        await bot.send_message(message.chat.id,
                                               f'Вы продали бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                               reply_markup=markup)
                        assets.assets(userid=message.chat.id, number=1,
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).database_sell_businesses()
                        datas['isbusinessell'] = False
                        return
                    else:
                        if message.text.lower() == 'да':
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            if dataUser[11] > 0:
                                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                           'Магазин страховок',
                                           'Отключить/включить подтверждение', 'погасить кредит')
                            else:
                                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                           'Магазин страховок',
                                           'Отключить/включить подтверждение')
                            await bot.send_message(message.chat.id,
                                                   f'Вы продали бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                                   f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                                   f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                                   reply_markup=markup)
                            assets.assets(userid=message.chat.id, number=1,
                                          price=int(dataGame[dataGame[4] - 1].split()[3]),
                                          business=dataGame[dataGame[4] - 1].split()[
                                              1]).database_sell_businesses()
                            datas['isbusinessell'] = False
                            return
                        elif message.text.lower() == 'нет':
                            await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                            datas['iscoin'] = False
                            await game.waitingGame.set()
                            return
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Да', 'Нет', 'Отмена')
                        await bot.send_message(message.chat.id,
                                               f'Хотите продать бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                               f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                               f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                               f'подтверждение"', reply_markup=markup)
                        return
                elif message.text.lower() == 'взять кредит' and datas['business']:
                    if (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[4] >= \
                            dataGame[dataGame[4] - 1].split()[3] and (
                            int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] >= \
                            dataGame[dataGame[4] - 1].split()[3]:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        assets.assets(userid=message.chat.id, number=1, price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).crediUser()
                        dataUser = data.data(message.chat.id).dataUser()
                        await bot.send_message(message.chat.id,
                                               f'Кредит взят теперь будет сниматься 4 % от вашей суммы кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                               reply_markup=markup)
                        return
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение', 'погасить кредит')
                        else:
                            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                                       'Магазин страховок',
                                       'Отключить/включить подтверждение')
                        await bot.send_message(message.chat.id,
                                               'Ваш общий доход должен быть больше чем сумма кредита или больше чем сама сумма кредита',
                                               reply_markup=markup)
                        await game.waitingGame.set()
                        return
        except KeyError:
            datas['stock'] = False
            datas['bonds'] = False
            datas['business'] = False


@dp.message_handler(lambda message: message.text.lower() == 'отмена',
                    state=[game.buys, game.buysBusiness, game.sells, game.sellsBusiness, game.resetCredit,
                           game.sellOrBuy, game.insurance])
async def cancel(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    markup.add('Продолжить')
    await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
    async with state.proxy() as datas:
        datas['iscoin'] = False
    await game.waitingGame.set()


@dp.message_handler(state=game.insurance)
async def insurance(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'insurance')
    dataGame = data.data(message.chat.id).dataGame()
    dataBonds = data.data(message.chat.id).dataBonds()
    dataBusinesses = data.data(message.chat.id).dataBusinesses()
    dataUser = data.data(message.chat.id).dataUser()
    bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (
            dataBusinesses[5] * dataBusinesses[6]) + (dataBusinesses[7] * dataBusinesses[8])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    if dataUser[11] > 0:
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                   'Отключить/включить подтверждение', 'Погасить кредит')
    else:
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                   'Отключить/включить подтверждение')
    async with state.proxy() as datas:
        if message.text.lower() == 'страховка на жизнь':
            datas['insurance'] = 'СЖ'
        if message.text.lower() == 'страховка на имущевство':
            datas['insurance'] = 'СИ'
        if message.text.lower() == 'взять кредит':
            if (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[4] >= (
                    int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20 and (
                    int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] + dataUser[4] >= (
                    int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20:
                assets.assets(userid=message.chat.id, number=0,
                              price=(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20,
                              insurance=datas['insurance']).crediUser()
                await bot.send_message(message.chat.id,
                                       f'Кредит взят теперь будет сниматься 4 % от вашей суммы кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                       reply_markup=markup)
                await game.waitingGame.set()
                return
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение', 'погасить кредит')
                else:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение')
                await bot.send_message(message.chat.id,
                                       'Ваш общий доход должен быть больше чем сумма кредита или больше чем сама сумма кредита',
                                       reply_markup=markup)
                await game.waitingGame.set()
                return
        if int(dataUser[4]) < (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
            markup.add('Отмена', 'Взять кредит')
            await bot.send_message(message.chat.id,
                                   'У вас нехватает наличных, но вы можете взять кредит - "Взять кредит"',
                                   reply_markup=markup)
            return
        if message.text.lower() == 'страховка на жизнь':
            assets.assets(userid=message.chat.id, number=0,
                          price=(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20,
                          insurance='СЖ').database_buys_insurance()
            data.data(message.chat.id, column='money', changes=int(dataUser[4]) - (
                    (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20)).dataChanges()
            dataUser = data.data(message.chat.id).dataUser()
            await bot.send_message(message.chat.id,
                                   f'Страховка на жизнь куплена\nОстаток наличных: {"{0:,}".format(dataUser[4]).replace(",", " ")}',
                                   reply_markup=markup)
            await game.waitingGame.set()
            datas['insurance'] = 'СЖ'
            return
        if message.text.lower() == 'страховка на имущевство':
            assets.assets(userid=message.chat.id, number=0,
                          price=(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20,
                          insurance='СИ').database_buys_insurance()
            data.data(message.chat.id, column='money', changes=int(dataUser[4]) - (
                    (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 100 * 20)).dataChanges()
            dataUser = data.data(message.chat.id).dataUser()
            await bot.send_message(message.chat.id,
                                   f'Страховка на имущевство куплена\nОстаток наличных: {"{0:,}".format(dataUser[4]).replace(",", " ")}',
                                   reply_markup=markup)
            await game.waitingGame.set()
            datas['insurance'] = 'СИ'
            return


@dp.message_handler(
    lambda message: not message.text.replace('.', '').replace(',',
                                                              '').isdigit() and message.text.lower() != 'да' and message.text.lower() != 'нет' and message.text.lower() != 'взять кредит' and message.text.lower() != 'погасить на все',
    state=[game.buys, game.sells, game.resetCredit, game.defeatSell])
async def error(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите число')


@dp.message_handler(state=game.sellOrBuy)
async def buyOrSell(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + 'buyOrSell')
    dataCoin = data.data(message.chat.id).dataCoins()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Отмена')
    if message.text.lower() == 'купить':
        await bot.send_message(message.chat.id,
                               f'Сколько {dataCoin[7].split()[0]} хотите купить?\nЦена: {dataCoin[7].split()[1]}',
                               reply_markup=markup)
        await game.buys.set()
        return
    elif message.text.lower() == 'продать':
        await bot.send_message(message.chat.id,
                               f'Сколько {dataCoin[7].split()[0]} хотите продать?\nЦена: {dataCoin[7].split()[1]}',
                               reply_markup=markup)
        await game.sells.set()
        return


@dp.message_handler(state=game.resetCredit)
async def resetCredit(message: types.Message):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + '(resetCredit)')
    dataUser = data.data(message.chat.id).dataUser()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    if dataUser[11] > 0:
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                   'Отключить/включить подтверждение', 'погасить кредит')
    else:
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                   'Отключить/включить подтверждение')
    if message.text.lower() == 'погасить на все':
        if dataUser[4] > 0:
            summ = dataUser[11] - dataUser[4]
            if summ <= 0:
                await bot.send_message(message.chat.id,
                                       f'Кредит погашен на {"{0:,}".format(int(dataUser[11])).replace(",", " ")} $\n'
                                       f'Остаток кредита - {"{0:,}".format(int(0)).replace(",", " ")}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='credit', changes=0).dataChanges()
                data.data(message.chat.id, column='money', changes=-(summ)).dataChanges()
                await game.waitingGame.set()
                return
            else:
                await bot.send_message(message.chat.id,
                                       f'Кредит погашен на {"{0:,}".format(int(dataUser[4])).replace(",", " ")} $\n'
                                       f'Остаток кредита - '
                                       f'{"{0:,}".format(int(dataUser[11]) - int(dataUser[4])).replace(",", " ")}',
                                       reply_markup=markup)
                data.data(message.chat.id, column='credit', changes=dataUser[11] - dataUser[4]).dataChanges()
                data.data(message.chat.id, column='money', changes=0).dataChanges()
                await game.waitingGame.set()
                return
        else:
            await bot.send_message(message.chat.id, 'У вас нету наличных', reply_markup=markup)
            await game.waitingGame.set()
            return
    if int(message.text) > dataUser[11]:
        await bot.send_message(message.chat.id, f'Ваш кредит {dataUser[11]} вы не можете погасить больше')
        return
    elif int(message.text) <= 0:
        await bot.send_message(message.chat.id, 'Число должно быть больше 0')
        return
    elif int(message.text) > dataUser[4]:
        await bot.send_message(message.chat.id, 'Нехватает наличных')
        return
    data.data(message.chat.id, column='money', changes=dataUser[4] - int(message.text)).dataChanges()
    data.data(message.chat.id, column='credit', changes=dataUser[11] - int(message.text)).dataChanges()
    await bot.send_message(message.chat.id, f'Кредит погашен на {message.text} $', reply_markup=markup)
    await game.waitingGame.set()


@dp.message_handler(state=[game.buys, game.buysBusiness])
async def buys(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + '(buys)')
    dataGame = data.data(message.chat.id).dataGame()
    dataUser = data.data(message.chat.id).dataUser()
    dataCoin = data.data(message.chat.id).dataCoins()
    dataBonds = data.data(message.chat.id).dataBonds()
    dataBusinesses = data.data(message.chat.id).dataBusinesses()
    bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (
            dataBusinesses[5] * dataBusinesses[6]) + (dataBusinesses[7] * dataBusinesses[8])
    if message.text == '0':
        await bot.send_message(message.chat.id, 'Число не может быть 0')
        return
    if message.text.replace('.', '').replace(',', '').isdigit():
        async with state.proxy() as datas:
            datas['num'] = message.text
    async with state.proxy() as datas:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        if dataUser[11] > 0:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение', 'Погасить кредит')
        else:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение')

        if message.text.lower() == 'взять кредит':
            if not datas['iscoin'] and (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[
                4] >= int(datas['num']) * int(dataGame[dataGame[4] - 1].split()[3]) and (
                    int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] + dataUser[
                4] >= int(datas['num']) * int(dataGame[dataGame[4] - 1].split()[3]):
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    assets.assets(userid=message.chat.id, number=datas['num'],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  coin=dataGame[dataGame[4] - 1].split()[1]).crediUser()
                    dataUser = data.data(message.chat.id).dataUser()
                    await bot.send_message(message.chat.id,
                                           f'Кредит взят теперь будет сниматься 4 % от вашей суммы кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                           reply_markup=markup)
                    await game.waitingGame.set()
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    assets.assets(userid=message.chat.id, number=datas['num'],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  bondes=dataGame[dataGame[4] - 1].split()[1]).crediUser()
                    dataUser = data.data(message.chat.id).dataUser()
                    await bot.send_message(message.chat.id,
                                           f'Кредит взят теперь будет сниматься 4 % от вашей суммы кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                           reply_markup=markup)
                    await game.waitingGame.set()
                return
            elif datas['iscoin'] and (int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) + dataUser[
                4] >= float(datas['num'].replace(',', '.')) * float(dataCoin[7].split()[1]) and (
                    int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300) + bussines) - dataUser[11] + dataUser[
                4] >= float(
                datas['num'].replace(',', '.')) * float(dataCoin[7].split()[1]):
                assets.assets(userid=message.chat.id, number=datas['num'].replace(",", "."),
                              price=float(dataCoin[7].split()[1])).crediUser()
                dataUser = data.data(message.chat.id).dataUser()
                await bot.send_message(message.chat.id,
                                       f'Кредит взят теперь будет сниматься 4 % от вашей суммы кредита\nРассходы с кредитом - {dataUser[11] / 100 * 4}',
                                       reply_markup=markup)
                await game.waitingGame.set()
                return
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение', 'погасить кредит')
                else:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение')
                await bot.send_message(message.chat.id,
                                       'Ваш общий доход должен быть больше чем сумма кредита или больше чем сама сумма кредита',
                                       reply_markup=markup)
                await game.waitingGame.set()
                return
        if not datas['iscoin']:
            if int(dataUser[4]) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]) < 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Отмена', 'Взять кредит')
                await bot.send_message(message.chat.id,
                                       'У вас нехватает наличных, введите количевство еще раз'
                                       '\nЧто бы отменить покупку введите "Отмена"\nИли возьмите кредит "Взять кредит"',
                                       reply_markup=markup)
                return
            if int(dataUser[4]) - int(dataGame[dataGame[4] - 1].split()[3]) < 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Отмена', 'Взять кредит')
                await bot.send_message(message.chat.id,
                                       'У вас нехватает наличных, введите количевство еще раз\nИли'
                                       ' введите "Отмена" что бы отменить покупку\nИли возьмите кредит - "Взять кредит"',
                                       reply_markup=markup)
                return
        else:
            if int(dataUser[4]) - float(datas['num'].replace(',', '.')) * float(dataCoin[7].split()[1]) < 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Отмена', 'Взять кредит')
                await bot.send_message(message.chat.id,
                                       'У вас нехватает наличных, введите количевство еще раз\nИли'
                                       ' введите "Отмена" что бы отменить покупку\nИли возьмите кредит - "Взять кредит"',
                                       reply_markup=markup)
                return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        if dataUser[11] > 0:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение', 'погасить кредит')
        else:
            markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                       'Отключить/включить подтверждение')
        if dataUser[10] == False:
            if not datas['iscoin']:
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  coin=dataGame[dataGame[4] - 1].split()[1]).database_buys_stock()
                    await game.waitingGame.set()
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  bondes=dataGame[dataGame[4] - 1].split()[1]).database_buys_bondes()
                    await game.waitingGame.set()
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение', 'погасить кредит')
                else:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение')
                await bot.send_message(message.chat.id,
                                       f'Вы купили монету {dataCoin[7].split()[0]}.'
                                       f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                       f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}',
                                       reply_markup=markup)
                assets.assets(userid=message.chat.id, number=datas['num'].replace(",", "."),
                              price=float(dataCoin[7].split()[1]),
                              coin=dataCoin[7].split()[0]).database_buys_coin()
                await game.waitingGame.set()
                return
            await game.waitingGame.set()
        else:
            if message.text.lower() == 'да':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение', 'погасить кредит')
                else:
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют',
                               'Магазин страховок',
                               'Отключить/включить подтверждение')
                if datas['iscoin'] == True:
                    await bot.send_message(message.chat.id,
                                           f'Вы купили монету {dataCoin[7].split()[0]}.'
                                           f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                           f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}'
                                           f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                           f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                           f'подтверждение"', reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"].replace(",", "."),
                                  price=float(dataCoin[7].split()[1]), coin=dataCoin[7].split()[0]).database_buys_coin()
                    await game.waitingGame.set()
                    return
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  coin=dataGame[dataGame[4] - 1].split()[1]).database_buys_stock()
                    await game.waitingGame.set()
                    return
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  bondes=dataGame[dataGame[4] - 1].split()[1]).database_buys_bondes()
                    await game.waitingGame.set()
                    return
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                    await bot.send_message(message.chat.id,
                                           f'Вы купили бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                           f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=1,
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  business=dataGame[dataGame[4] - 1].split()[1]).database_buys_businesses()
                    await game.waitingGame.set()
                    return
            elif message.text.lower() == 'нет':
                await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                await game.waitingGame.set()
                return
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Да', 'Нет', 'Отмена')
            if not datas['iscoin']:
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Хотите купить {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                                             f'\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение '
                                             f'можно отключить кнопкой "Отключить/включить подтверждение"',
                                           reply_markup=markup)
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Хотите купить {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) - int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                                             f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                             f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                             f'подтверждение"', reply_markup=markup)
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                    await bot.send_message(message.chat.id,
                                           f'Хотите купить бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. С пассивным доходом {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                           f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                           f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                           f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                           f'подтверждение"', reply_markup=markup)
            else:
                await bot.send_message(message.chat.id,
                                       f'Хотите купить монету {dataCoin[7].split()[0]}.'
                                       f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                       f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) - float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}'
                                       f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                       f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                       f'подтверждение"', reply_markup=markup)


@dp.message_handler(state=[game.sells, game.sellsBusiness])
async def sells(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()) + '(sells)')
    dataGame = data.data(message.chat.id).dataGame()
    dataUser = data.data(message.chat.id).dataUser()
    dataStock = data.data(message.chat.id).dataStock()
    dataBondes = data.data(message.chat.id).dataBonds()
    dataCoin = data.data(message.chat.id).dataCoins()
    if message.text == '0':
        await bot.send_message(message.chat.id, 'Введите число больше 0')
        return
    if message.text.replace('.', '').replace(',', '').isdigit():
        async with state.proxy() as datas:
            datas['num'] = message.text
    async with state.proxy() as datas:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add('Отмена')
        if not datas['iscoin']:
            if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                stockMass = [0, 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
                for i in range(len(stockMass)):
                    if dataGame[dataGame[4] - 1].split()[1] == stockMass[i]:
                        if dataStock[i] <= 1:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                            if dataUser[11] > 0:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                                           'Погасить кредит')
                            else:
                                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                            await bot.send_message(message.chat.id, 'У вас нету этой акции', reply_markup=markup)
                            await game.waitingGame.set()
                            return
                        if int(datas['num']) <= dataStock[i]:
                            pass
                        else:
                            await bot.send_message(message.chat.id,
                                                   'Нехватает акций, введите количевство еще раз или введите "Отмена" для выхода',
                                                   reply_markup=markup)
                            return
            elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                if dataBondes[1] <= 0:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    if dataUser[11] > 0:
                        markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                                   'Погасить кредит')
                    else:
                        markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                    await bot.send_message(message.chat.id, 'У вас нету этой облигации', reply_markup=markup)
                    await game.waitingGame.set()
                    return
                if int(datas['num']) <= dataBondes[1]:
                    pass
                else:
                    await bot.send_message(message.chat.id,
                                           'Нехватает облигаций, введите количевство еще раз или введите "Отмена" для выхода',
                                           reply_markup=markup)
                    return
        else:
            coinMass = [0, 0, 'Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum']
            for i in range(len(coinMass)):
                if dataCoin[7].split()[0] == coinMass[i]:
                    if dataCoin[i] == 0:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        if dataUser[11] > 0:
                            markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                                       'Погасить кредит')
                        else:
                            markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                        await bot.send_message(message.chat.id, 'У вас нету этой криптовалюты', reply_markup=markup)
                        await game.waitingGame.set()
                        return
                    if float(datas['num'].replace(",", ".")) <= dataCoin[i]:
                        pass
                    else:
                        await bot.send_message(message.chat.id, 'Нехватает монет, введите количевство '
                                                                'еще раз или введите "Отмена" для выхода',
                                               reply_markup=markup)
                        return
        if dataUser[10] == False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            if dataUser[11] > 0:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок', 'Погасить кредит')
            else:
                markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
            if not datas['iscoin']:
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Вы продали {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  coin=dataGame[dataGame[4] - 1].split()[1]).database_sell_stock()
                    await game.waitingGame.set()
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Вы продали {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. Пассивный доход {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                           reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas["num"],
                                  price=int(dataGame[dataGame[4] - 1].split()[3]),
                                  bondes=dataGame[dataGame[4] - 1].split()[1]).database_sell_bondes()
                    await game.waitingGame.set()
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                if dataUser[11] > 0:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                               'Погасить кредит')
                else:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок')
                await bot.send_message(message.chat.id,
                                       f'Вы продали монету {dataCoin[7].split()[0]}.'
                                       f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                       f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}',
                                       reply_markup=markup)
                assets.assets(userid=message.chat.id, number=datas['num'].replace(",", "."),
                              price=float(dataCoin[7].split()[1]),
                              coin=dataCoin[7].split()[0]).database_sell_coin()
                await game.waitingGame.set()
                return
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            if dataUser[11] > 0:
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение', 'погасить кредит')
            else:
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                           'Отключить/включить подтверждение')
            if message.text.lower() == 'да':
                if not datas['iscoin']:
                    if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                        await bot.send_message(message.chat.id,
                                               f'Вы продали {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' По цене ' + str(
                                                   "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(
                                                       ",", " "))
                                               + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                                 f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                               reply_markup=markup)
                        assets.assets(userid=message.chat.id, number=datas["num"],
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      coin=dataGame[dataGame[4] - 1].split()[1]).database_sell_stock()
                        await game.waitingGame.set()
                        return
                    elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                        await bot.send_message(message.chat.id,
                                               f'Вы продали {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' По цене ' + str(
                                                   "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(
                                                       ",",
                                                       " "))
                                               + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                                 f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}',
                                               reply_markup=markup)
                        assets.assets(userid=message.chat.id, number=datas["num"],
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      bondes=dataGame[dataGame[4] - 1].split()[1]).database_sell_bondes()
                        await game.waitingGame.set()
                        return
                    elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                        await bot.send_message(message.chat.id,
                                               f'Вы продали бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                               f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                               f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}',
                                               reply_markup=markup)
                        assets.assets(userid=message.chat.id, number=datas['num'],
                                      price=int(dataGame[dataGame[4] - 1].split()[3]),
                                      business=dataGame[dataGame[4] - 1].split()[1]).database_sell_businesses()
                        await game.waitingGame.set()
                        return
                else:
                    await bot.send_message(message.chat.id,
                                           f'Вы продали монету {dataCoin[7].split()[0]}.'
                                           f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                           f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}'
                                           f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                           f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                           f'подтверждение"', reply_markup=markup)
                    assets.assets(userid=message.chat.id, number=datas['num'].replace(",", "."),
                                  price=float(dataCoin[7].split()[1]),
                                  coin=dataCoin[7].split()[0]).database_sell_coin()
                    await game.waitingGame.set()
                    return
            elif message.text.lower() == 'нет':
                await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
                await game.waitingGame.set()
                return
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Да', 'Нет', 'Отмена')
            if not datas['iscoin']:
                if dataGame[dataGame[4] - 1].split()[0].lower() == 'акция':
                    await bot.send_message(message.chat.id,
                                           f'Хотите продать {"{0:,}".format(int(datas["num"])).replace(",", " ")} акций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                                             f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                             f'количвество)\nЭто сообщение '
                                             f'можно отключить кнопкой "Отключить/включить подтверждение"',
                                           reply_markup=markup)
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'облигация':
                    await bot.send_message(message.chat.id,
                                           f'Хотите продать {"{0:,}".format(int(datas["num"])).replace(",", " ")} облигаций {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' По цене ' + str(
                                               "{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",",
                                                                                                                 " "))
                                           + f' на сумму {"{0:,}".format(int(int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " ")}. Пассивный доход {"{0:,}".format(int(datas["num"]) * 300).replace(",", " ")}\n'
                                             f'Остаток наличных {str("{0:,}".format(int(round(dataUser[4], 4) + int(datas["num"]) * int(dataGame[dataGame[4] - 1].split()[3]))).replace(",", " "))}'
                                             f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                             f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                             f'подтверждение"', reply_markup=markup)
                elif dataGame[dataGame[4] - 1].split()[0].lower() == 'бизнес':
                    await bot.send_message(message.chat.id,
                                           f'Хотите продать бизнес {dataGame[dataGame[4] - 1].split()[1]}.'
                                           f' по цене {"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " ")}. Пассивный доход -{"{0:,}".format(int(dataGame[dataGame[4] - 1].split()[14])).replace(",", " ")}\n'
                                           f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + int(dataGame[dataGame[4] - 1].split()[3])).replace(",", " "))}'
                                           f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                           f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                           f'подтверждение"', reply_markup=markup)
            else:
                await bot.send_message(message.chat.id,
                                       f'Хотите продать монету {dataCoin[7].split()[0]}.'
                                       f' по цене {"{0:,}".format(float(dataCoin[7].split()[1])).replace(",", " ")}.\n'
                                       f'Остаток наличных {str("{0:,}".format(round(dataUser[4], 4) + float(datas["num"].replace(",", ".")) * float(dataCoin[7].split()[1])).replace(",", " "))}'
                                       f'\nДа/Нет (Введите число акций еще раз если хотите купить другое '
                                       f'количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить '
                                       f'подтверждение"', reply_markup=markup)


@dp.message_handler(state=game.defeat)
async def defeat(message: types.Message, state: FSMContext):
    dataUser = data.data(message.chat.id).dataUser()
    dataStock = data.data(message.chat.id).dataStock()
    dataBonds = data.data(message.chat.id).dataBonds()
    dataBusinesses = data.data(message.chat.id).dataBusinesses()
    dataCoins = data.data(message.chat.id).dataCoins()
    async with state.proxy() as datas:
        stockMass1 = ['Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
        stockMass2 = [dataStock[1], dataStock[2], dataStock[3], dataStock[4], dataStock[5]]
        for i in enumerate(stockMass1):
            if message.text.lower() in i[1].lower() and stockMass2[i[0]] >= 1:
                await bot.send_message(message.chat.id, 'Сколько акций ' + message.text.lower() + ' хотите продать')
                datas['choice'] = 'stock'
                datas['coind'] = stockMass2[i[0]]
                datas['choiceCoin'] = message.text
                await game.defeatSell.set()
        bondes = dataBonds[1]
        if message.text.lower() in 'вексель' and bondes >= 1:
            await bot.send_message(message.chat.id, 'Сколько облигаций ' + message.text.lower() + ' хотите продать')
            datas['choice'] = 'bondes'
            datas['coind'] = 'Вексель'
            datas['choiceCoin'] = message.text
            await game.defeatSell.set()
        coinMass1 = ['Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum']
        coinMass2 = [dataCoins[2], dataCoins[3], dataCoins[4], dataCoins[5], dataCoins[6]]
        for i in enumerate(coinMass1):
            if message.text.lower() in i[1].lower() and coinMass2[i[0]] >= 1:
                await bot.send_message(message.chat.id,
                                       'Сколько криптовалюты ' + message.text.lower() + ' хотите продать')
                datas['choice'] = 'kripta'
                datas['coind'] = coinMass2[i[0]]
                datas['choiceCoin'] = message.text
                await game.defeatSell.set()
        massBussines1 = ['AMD', 'Intel', 'Nvidia', 'Apple']
        massBussines2 = [dataBusinesses[2], dataBusinesses[4], dataBusinesses[6], dataBusinesses[8]]
        massBussines3 = [100000, 110000, 125000, 150000]
        for i in enumerate(massBussines1):
            if message.text.lower() in i[1].lower() and massBussines2[i[0]] >= 1:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
                if dataUser[11] > 0:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                               'Отключить/включить подтверждение', 'погасить кредит')
                else:
                    markup.add('Продолжить', 'Статистика', 'Магазин криптовалют', 'Магазин страховок',
                               'Отключить/включить подтверждение')
                data.data(message.chat.id, column='money', changes=dataUser[4] + massBussines3[i[0]]).dataChanges()
                data.data(message.chat.id, column=f'{massBussines1[i[0]]}', changes=0).dataChangesBussines()
                await bot.send_message(message.chat.id, 'Бизнес продан', reply_markup=markup)
                await game.waitingGame.set()


@dp.message_handler(state=game.defeatSell)
async def defeatSell(message: types.Message, state: FSMContext):
    dataUser = data.data(message.chat.id).dataUser()
    dataGame = data.data(message.chat.id).dataGame()
    dataStock = data.data(message.chat.id).dataStock()
    dataBonds = data.data(message.chat.id).dataBonds()
    dataBusinesses = data.data(message.chat.id).dataBusinesses()
    dataCoins = data.data(message.chat.id).dataCoins()
    dataBuyed = data.data(message.chat.id).dataBuing()
    mass = ['0', 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром', 'Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum', 'Вексель']
    async with state.proxy() as datas:
        for i in enumerate(mass):
            if datas['choice'] == 'stock':
                if message.text.isdigit():
                    if i[1].lower() == datas['choiceCoin'].lower():
                        assets.assets(message.chat.id, coin=datas['choiceCoin'].lower(), number=message.text.replace(",", "."), price=float(dataBuyed[i[0]].split()[0]) / float(dataBuyed[i[0]].split()[1])).database_sell_stock()
                        await bot.send_message(message.chat.id, 'Вы продали акцию')
                        await game.waitingGame.set()
                        break
                else:
                    await bot.send_message(message.chat.id, 'Введите целое число')
            elif datas['choice'] == 'bondes':
                if message.text.isdigit():
                    if i[1].lower() == datas['choiceCoin'].lower():
                        assets.assets(message.chat.id, bondes='Вексель', number=message.text.replace(",", "."), price=float(dataBuyed[i[0]].split()[0]) / float(dataBuyed[i[0]].split()[1])).database_sell_bondes()
                        await bot.send_message(message.chat.id, 'Вы продали облигацию')
                        await game.waitingGame.set()
                        break
                else:
                    await bot.send_message(message.chat.id, 'Введите целое число')
            elif datas['choice'] == 'kripta':
                if i[1].lower() == datas['choiceCoin'].lower():
                    assets.assets(message.chat.id, coin=datas['choiceCoin'].lower(), number=message.text.replace(",", "."), price=float(dataBuyed[i[0]].split()[0]) / float(dataBuyed[i[0]].split()[1])).database_sell_coin()
                    await bot.send_message(message.chat.id, 'Вы продали криптовалюту')
                    await game.waitingGame.set()
                    break



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
