# -*- coding: cp1251 -*-
import logging
import math
import os
import pole
import random
import datetime
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

if not os.path.exists('users'):
    os.mkdir('users')

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1957878149:AAH4OYE0JMITxUulgjESb1Cu131hLtwSVbc'

bot = Bot(token=API_TOKEN)


class game(StatesGroup):
    waitingGame = State()
    confirm = State()
    confirmsell = State()
    bussines = State()
    investment = State()
    investmentsell = State()


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def profession():
    num = random.randint(0, 11)
    profes = [['Стройщик', 'Менеджер продаж', 'Бариста', 'Продавец-консультант', 'Администратор магазина',
               'Бармен', 'Банкир', 'Юрист', 'Копирайтер', 'Логопед', 'Системный администратор', 'Педагог'],
              [25000, 20000, 15000, 18000, 17000, 19000, 23000, 22000, 20000, 16000, 17000, 21000]]
    return profes[0][num] + ' ' + str(profes[1][num])


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    with open(f'users_id.txt', 'r') as users:
        users = users.read().split()
    if not str(message.chat.id) in users:
        with open(f'users_id.txt', 'a') as users:
            users.write(str(message.chat.id) + ' ')
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Введите комманду еще раз что бы продожить', reply_markup=markup)
        if not os.path.exists(f'users/{message.chat.id}/last_action.txt'):
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
        with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
            last = last.read()
        if last == '':
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
            with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
                last = last.read()
        if last.split()[0] == 'Акция':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == 'Облигация':
            async with state.proxy() as data:
                data['stocks'] = False
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = True
                data['insurances'] = False
                data['investment'] = last
        await bot.send_message(message.chat.id, last)
        await game.waitingGame.set()
        return
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


@dp.message_handler(commands='rules')
async def rules(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Введите комманду еще раз что бы продожить', reply_markup=markup)
        if not os.path.exists(f'users/{message.chat.id}/last_action.txt'):
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
        with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
            last = last.read()
        if last == '':
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
            with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
                last = last.read()
        if last.split()[0] == 'Акция':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == 'Облигация':
            async with state.proxy() as data:
                data['stocks'] = False
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = True
                data['insurances'] = False
                data['investment'] = last
        await bot.send_message(message.chat.id, last)
        await game.waitingGame.set()
        return
    await bot.send_message(message.chat.id, md.text('coming soon'),
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def letsgo(message: types.Message, state: FSMContext):
    async def randProgress():
        mass = ['business', 'realestate', 'investment', 'unexpectedexpenses', 'stock']
        # , 'business', 'bigbusiness', 'realestate', 'bonds', 'investment', 'unexpectedexpenses', 'present'
        random.shuffle(mass)
        return mass[0]

    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Введите комманду еще раз что бы продожить', reply_markup=markup)
        if not os.path.exists(f'users/{message.chat.id}/last_action.txt'):
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
        with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
            last = last.read()
        if last == '':
            with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                stock = str(pole.firstCircleFuncStockMarket()[0])
                last.write(stock)
            with open(f'users/{message.chat.id}/last_action.txt', 'r') as last:
                last = last.read()
        if last.split()[0] == 'Акция':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == 'Облигация':
            async with state.proxy() as data:
                data['stocks'] = False
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = True
                data['insurances'] = False
                data['investment'] = last
        await bot.send_message(message.chat.id, last)
        await game.waitingGame.set()
        return
    if message.text.lower() == 'старт':
        await dp.bot.set_my_commands([
            types.BotCommand("rules", "Правила игры"),
        ])
        if not os.path.exists(f'users/{message.chat.id}'):
            os.mkdir(f'users/{message.chat.id}')
        with open(f'users/{message.chat.id}/data.txt', 'w') as data:
            data.write(
                str(message.chat.id) + ' ' + str(message.chat.username) + ' ' + str(message.chat.bio) + ' ' + str(
                    message.chat.photo) + ' True')
        with open(f'users/{message.chat.id}/statistic.txt', 'w') as statistics:
            prof = await profession()
            statistics.write(prof + ' 0 0 0')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Начать игру')
        with open(f'users/{message.chat.id}/income.txt', 'w') as income:
            income.write(f'Наличные 20000\nПроценты 0\nДивиденды '
                         f'0\nНедвижимость 0\nБизнес 0\nПассивный доход 0')
        with open(f'users/{message.chat.id}/consumption.txt', 'w') as consumption:
            consumption.write(f'Общие 15000\nНалоги 0\nКредит 0\nПрочие_расходы 0\nРасходы(дети) 0')
        with open(f'users/{message.chat.id}/stock.txt', 'w') as stock:
            stock.write('')
        with open(f'users/{message.chat.id}/players.txt', 'w') as player:
            player.write('')
        with open(f'users/{message.chat.id}/investment.txt', 'w') as investment:
            investment.write('')
        with open(f'users/{message.chat.id}/progress.txt', 'w') as progress:
            progress.write(str(await randProgress()) + ' stock ' + str(await randProgress()) + ' 3')
        await bot.send_message(message.chat.id, f"Вы присоеденились к игре. Ваш id - {message.chat.id}, "
                                                f"используйте его что бы другие могли "
                                                f"присоедениться к игре, что бы начать игру введите "
                                                f"\"Начать игру\"\nУправление всеми игроками - players",
                               reply_markup=markup)
        with open(f'users/{message.chat.id}/players.txt', 'w') as player:
            player.write(str(message.chat.id) + ' ')
        with open(f'users/{message.chat.id}/playersName.txt', 'w') as player:
            player.write(str(message.chat.username) + ' ')
        await dp.bot.delete_my_commands()
        await game.waitingGame.set()
        return
    try:
        if 'join' in message.text.lower().split():
            if not os.path.exists(f'users/{message.chat.id}'):
                await dp.bot.set_my_commands([
                    types.BotCommand("rules", "Правила игры"),
                ])
                os.mkdir(f'users/{message.chat.id}')
                with open(f'users/{message.chat.id}/data.txt', 'w') as data:
                    data.write(
                        str(message.chat.id) + ' ' + str(message.chat.username) + ' ' + str(
                            message.chat.bio) + ' ' + str(
                            message.chat.photo) + ' True')
                with open(f'users/{message.chat.id}/statistic.txt', 'w') as statistics:
                    prof = await profession()
                    statistics.write(prof + ' 0 0 0')
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Продолжить')
                with open(f'users/{message.chat.id}/income.txt', 'w') as income:
                    income.write(f'Наличные 20000\nПроценты 0\nДивиденды '
                                 f'0\nНедвижимость 0\nБизнес 0\nПассивный доход 0')
                with open(f'users/{message.chat.id}/consumption.txt', 'w') as consumption:
                    consumption.write(f'Общие 15000\nНалоги 0\nКредит 0\nПрочие_расходы 0\nРасходы(дети) 0')
                with open(f'users/{message.chat.id}/players.txt', 'w') as player:
                    player.write('')
                with open(f'users/{message.chat.id}/investment.txt', 'w') as investment:
                    investment.write('')
                with open(f'users/{message.chat.id}/progress.txt', 'w') as progress:
                    progress.write(str(await randProgress()) + ' stock ' + str(await randProgress()) + ' 3')
            if message.text.lower().split()[1] == str(message.chat.id):
                await bot.send_message(message.chat.id, 'Вы не можете присоедениться к своей игре')
                return
            with open(f'users/{message.text.lower().split()[1]}/players.txt', 'r') as player:
                if len(player.read().split()) >= 6:
                    await bot.send_message(message.chat.id, 'Комната переполнена')
                    return
            with open(f'users/{message.text.lower().split()[1]}/players.txt', 'a') as player:
                player.write(str(message.chat.id) + ' ')
            with open(f'users/{message.text.lower().split()[1]}/playersName.txt', 'a') as player:
                player.write(str(message.chat.username) + ' ')
            with open(f'users/{message.chat.id}/game.txt', 'w') as games:
                games.write(message.text.lower().split()[1])
            await bot.send_message(message.text.lower().split()[1], f'{message.chat.username}, присоеденился')
            await bot.send_message(message.chat.id,
                                   'Вы присоеденились к игре, подождите пока лидер группы начнет игру\nЧто бы '
                                   'покинуть игру - leave')
            with open(f'users/{message.chat.id}/statistic.txt', 'r') as statistics:
                statTemp = statistics.read().split()
                statTemp[len(statTemp) - 1] = '1'
            with open(f'users/{message.chat.id}/statistic.txt', 'w') as statistics:
                statistics.write(' '.join(statTemp))
                await dp.bot.delete_my_commands()
                await game.waitingGame.set()
            return
    except FileNotFoundError as e:
        await bot.send_message(message.chat.id, 'Не правильно введен id')
    except IndexError as e:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Старт')
    await bot.send_message(message.chat.id, 'Введите "Старт" создать лобби\nИли join что бы присоедениться',
                           reply_markup=markup)


@dp.message_handler(state=game.waitingGame)
async def waitingGame(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    try:
        async with state.proxy() as data:
            if float(str(datetime.datetime.now()-data['time']).replace(':', '')) < 0.3:
                return
    except Exception:
        async with state.proxy() as data:
            data['time'] = datetime.datetime.now()
        pass
    global flagStock, bonds, investment, realEstate
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    with open(f'users/{message.chat.id}/statistic.txt', 'r') as statistic:
        statistic = statistic.read().split()
    if message.text.lower() == 'leave' and statistic[len(statistic) - 1] == '0':
        with open(f'users/{message.chat.id}/playersName.txt', 'r') as playersName:
            playersName = playersName.read().split()
        with open(f'users/{message.chat.id}/players.txt', 'r') as players:
            players = players.read().split()
        os.remove(f'users/{message.chat.id}/move.txt')
        if len(playersName) > 1:
            for i in players:
                await bot.send_message(i, 'Лидер вышел с лобби, группа распущена')
                state = dp.current_state(chat=i, user=i)
                await state.set_state(await state.finish())
        else:
            await state.finish()
            await bot.send_message(message.chat.id, 'Вы вышли из лобби')
        return
    if message.text.lower() == 'leave':
        with open(f'users/{message.chat.id}/game.txt', 'r') as games:
            games = games.read()
            with open(f'users/{games}/playersName.txt', 'r') as playersName:
                playersName = playersName.read().split()
            with open(f'users/{games}/players.txt', 'r') as players:
                players = players.read().split()
        await bot.send_message(message.chat.id, 'Игра покинута')
        with open(f'users/{games}/playersName.txt', 'w') as pn:
            with open(f'users/{games}/players.txt', 'w') as pl:
                for i in range(len(players)):
                    if str(players[i]) != str(message.chat.id):
                        pn.write(playersName[i])
                        pl.write(players[i] + ' ')
        await bot.send_message(players[0], message.chat.username + 'покинул лобби')
        await state.finish()
        return
    if statistic[len(statistic) - 1] == '0' and message.text.lower() == 'players':
        vivod = ''
        with open(f'users/{message.chat.id}/playersName.txt', 'r') as playersName:
            playersName = playersName.read().split()
        for id, i in enumerate(playersName):
            if id == 0: continue
            vivod += str(id) + ' ' + str(i)
        if len(playersName) == 1:
            await bot.send_message(message.chat.id, 'В лобби никого нету')
        else:
            await bot.send_message(message.chat.id, vivod + '\nЧто бы выгнать пользователя введите kick (id)')
        return
    if statistic[len(statistic) - 1] == '0' and len(message.text.lower().split()) == 2 and message.text.lower().split()[
        0] == 'kick':
        with open(f'users/{message.chat.id}/playersName.txt', 'r') as playersName:
            playersName = playersName.read().split()
        with open(f'users/{message.chat.id}/players.txt', 'r') as players:
            players = players.read().split()
        if len(playersName) - 1 >= int(message.text.lower().split()[1]) >= 1:
            state = dp.current_state(chat=players[int(message.text.lower().split()[1])],
                                     user=players[int(message.text.lower().split()[1])])
            await state.set_state(await state.finish())
            await bot.send_message(message.chat.id, 'Игрок выгнан')
            await bot.send_message(players[int(message.text.lower().split()[1])], 'Вас выгнали с лобби')
            return
        else:
            await bot.send_message(message.chat.id, 'Неправильно введен id')
            return
    if statistic[len(statistic) - 1] == '0' and message.text.lower() == 'начать игру' and not os.path.exists(
            f'users/{message.chat.id}/move.txt'):
        with open(f'users/{message.chat.id}/players.txt', 'r') as players:
            players = players.read().split()
            with open(f'users/{message.chat.id}/move.txt', 'w') as move:
                move.write(str(len(players)) + ' 0')
        for i in players:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Продолжить')
            with open(f'users/{i}/statistic.txt', 'r') as stat:
                stat = stat.read().split()
            if len(stat) == 5:
                await bot.send_message(i,
                                       f'Игра начата\nВаша профессия:{stat[0]}. Зарплата - {stat[1]}\nЧто бы покинуть '
                                       f'игру введите leave',
                                       reply_markup=markup)
            else:
                await bot.send_message(i,
                                       f'Игра начата\nВаша профессия: {stat[0]} {stat[1]}. Зарплата - {stat[2]}\nЧто '
                                       f'бы покинуть игру введите leave',
                                       reply_markup=markup)
        return
    if 'уведомление' in message.text.lower() and message.chat.id == 951679992:
        with open(f'users_id.txt', 'r') as users:
            for i in users.read().split():
                await bot.send_message(i, message.text[12:])
                pass
        return
    if statistic[len(statistic) - 1] != '0':
        with open(f'users/{message.chat.id}/game.txt', 'r') as games:
            games = games.read()
    else:
        games = message.chat.id

    async def randProgress():
        mass = ['business', 'realestate', 'investment', 'unexpectedexpenses', 'stock']
        # 'bigbusiness', 'bonds', 'present'
        random.shuffle(mass)
        return mass[0]

    async def nextprogress():
        with open(f'users/{message.chat.id}/progress.txt', 'w') as progressW:
            progress[3] = str(int(progress[3]) - 1)
            for i in progress:
                progressW.write(i + ' ')

    if os.path.exists(f'users/{games}/move.txt'):
        with open(f'users/{games}/move.txt', 'r') as move:
            move = move.read().split()
            if str(move[0]) == '1':
                if message.text.lower() == 'продолжить':
                    async with state.proxy() as data:
                        data['time'] = datetime.datetime.now()
                    with open(f'users/{message.chat.id}/progress.txt', 'r') as progress:
                        progress = progress.read().split()
                    if progress[int(progress[
                                        3]) - 1] == 'unexpectedexpenses':  ####################################### НЕПРЕДВИДИНЫЕ РАСХОДЫ
                        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                                insurance.write('СЖ 00\nСИ 00')
                        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
                            insurance = insurance.read().split()
                        unexpectedexpenses = str(pole.firstCircleFuncStockMarket()[6])
                        if unexpectedexpenses.split()[0] == '(СЖ)':
                            if int(insurance[1]) > 0:
                                await bot.send_message(message.chat.id,
                                                       unexpectedexpenses + '\nУ вас была страховка, расходы погашены')
                                await nextprogress()
                                return
                        elif unexpectedexpenses.split()[0] == '(СИ)':
                            if int(insurance[3]) > 0:
                                await bot.send_message(message.chat.id,
                                                       unexpectedexpenses + '\nУ вас была страховка, расходы погашены')
                                await nextprogress()
                                return
                        await bot.send_message(message.chat.id, unexpectedexpenses)
                        with open(f'users/{message.chat.id}/income.txt', 'r') as incomeR:
                            incomeR = incomeR.read().split()
                            incomeR[1] = str(
                                int(incomeR[1]) + int(unexpectedexpenses.split()[len(unexpectedexpenses.split()) - 1]))
                        with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                            for i in range(len(incomeR)):
                                if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                    incomeW.write(incomeR[i] + '\n')
                                    continue
                                incomeW.write(incomeR[i] + ' ')
                        await nextprogress()
                        return
                    if progress[int(progress[
                                        3]) - 1] == 'stock':  ######################################################## АКЦИИ
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                                   'Отключить/включить подтверждение', 'Магазин страховок')
                        stock = str(pole.firstCircleFuncStockMarket()[0])
                        with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                            last.write(stock)
                        async with state.proxy() as data:
                            data['stock'] = stock
                        await bot.send_message(message.chat.id, stock, reply_markup=markup)
                        async with state.proxy() as data:
                            data['stocks'] = True
                            data['bussiness'] = False
                            data['realestates'] = False
                            data['investments'] = False
                            data['insurances'] = False
                        await nextprogress()
                        return
                    elif progress[
                        int(progress[3]) - 1] == 'business':  ################################################### БИЗНЕС
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Купить', 'Продолжить', 'Статистика',
                                   'Отключить/включить подтверждение', 'Магазин страховок')
                        business = str(pole.firstCircleFuncStockMarket()[1])
                        with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                            last.write(business)
                        async with state.proxy() as data:
                            data['business'] = business
                        await bot.send_message(message.chat.id, business + '\ncoming soon', reply_markup=markup)
                        async with state.proxy() as data:
                            data['stocks'] = False
                            data['bussiness'] = True
                            data['realestates'] = False
                            data['investments'] = False
                            data['insurances'] = False
                        await nextprogress()
                        return
                    elif progress[int(progress[
                                          3]) - 1] == 'investment':  ################################################# ОБЛИГАЦИИ
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                                   'Отключить/включить подтверждение', 'Магазин страховок')
                        investment = str(pole.firstCircleFuncStockMarket()[5])
                        with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                            last.write(investment)
                        async with state.proxy() as data:
                            data['investment'] = investment
                        await bot.send_message(message.chat.id, investment + '\ncoming soon', reply_markup=markup)
                        async with state.proxy() as data:
                            data['stocks'] = False
                            data['bussiness'] = False
                            data['realestates'] = False
                            data['investments'] = True
                            data['insurances'] = False
                        await nextprogress()
                        return
                    elif progress[int(progress[
                                          3]) - 1] == 'realestate':  ################################################# ВОЗМОЖНОСТИ
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('Купить', 'Продолжить', 'Статистика',
                                   'Отключить/включить подтверждение', 'Магазин страховок')
                        realestate = str(pole.firstCircleFuncStockMarket()[3])
                        with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                            last.write(realestate)
                        async with state.proxy() as data:
                            data['realestate'] = realestate
                        await bot.send_message(message.chat.id, realestate + '(Возможности)\ncoming soon',
                                               reply_markup=markup)
                        async with state.proxy() as data:
                            data['stocks'] = False
                            data['bussiness'] = False
                            data['realestates'] = True
                            data['investments'] = False
                            data['insurances'] = False
                        await nextprogress()
                        return
                    if int(progress[
                               3]) <= 0:  ########################################################################## ИТОГИ МЕСЯЦА
                        with open(f'users/{message.chat.id}/progress.txt', 'w') as progress:
                            progress.write(str(await randProgress()) + ' stock ' + str(await randProgress()) + ' 3')
                        with open(f'users/{message.chat.id}/statistic.txt', 'r') as static:
                            static = static.read().split()
                        with open(f'users/{message.chat.id}/consumption.txt', 'r') as con:
                            con = con.read().split()
                        with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                            income = income.read().split()
                            income[1] = str(
                                int(income[1]) + int(static[len(static) - 4]) - int(con[1]) + int(income[12]))
                        sum = str(int(static[len(static) - 4]) + int(income[12]))
                        with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                            for i in range(len(income)):
                                if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                    incomeW.write(income[i] + '\n')
                                    continue
                                incomeW.write(income[i] + ' ')
                        await bot.send_message(message.chat.id,
                                               f'Итоги за месяц!\nДоходы {sum} руб\nРасходы {con[1]} руб\nИтого {str(int(sum) - int(con[1]))} руб')
                        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                                insurance.write('СЖ 00\nСИ 00')
                        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
                            insurance = insurance.read().split()
                            if int(insurance[1]) == 1 and insurance[1] != '00':
                                await bot.send_message(message.chat.id, 'У вас закончилась страховка (СЖ)')
                                insurance[1] = '00'
                            elif int(insurance[1]) >= 1:
                                insurance[1] = str(int(insurance[1]) - 1)
                            if int(insurance[3]) == 1 and insurance[3] != '00':
                                await bot.send_message(message.chat.id, 'У вас закончилась страховка (СИ)')
                                insurance[3] = '00'
                            elif int(insurance[3]) >= 1:
                                insurance[3] = str(int(insurance[3]) - 1)
                        with open(f'users/{message.chat.id}/insurance.txt', 'w') as insuranceW:
                            insuranceW.write(
                                insurance[0] + ' ' + insurance[1] + '\n' + insurance[2] + ' ' + insurance[3])
                        return
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == 'магазин страховок':  ##################### МАГАЗИН СТРАХОВОК
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add('Страховка на жизнь', 'Страховка на имущество', 'Продолжить')
        await bot.send_message(message.chat.id, 'Страховка на жизнь - 3000 руб\nСтраховка на имущество - 5000 руб',
                               reply_markup=markup)
        async with state.proxy() as data:
            data['magazine'] = True
        return
    async with state.proxy() as data:
        try:
            if os.path.exists(
                    f'users/{games}/move.txt') and message.text.lower() == 'страховка на жизнь' and data['magazine']:  ##################### СТРАХОВКА НА ЖИЗНТ
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                           'Магазин страховок')
                if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                    with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                        insurance.write('СЖ 00\nСИ 00')
                with open(f'users/{message.chat.id}/income.txt', 'r') as incomeR:
                    incomeR = incomeR.read().split()
                if int(incomeR[1]) <= 3000:
                    await bot.send_message(message.chat.id, 'У вас нехватает наличных', reply_markup=markup)
                    return
                else:
                    incomeR[1] = str(int(incomeR[1]) - 3000)
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(incomeR)):
                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(incomeR[i] + '\n')
                                continue
                            incomeW.write(incomeR[i] + ' ')
                with open(f'users/{message.chat.id}/insurance.txt', 'r') as insuranceR:
                    insuranceR = insuranceR.read().split()
                with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                    insurance.write(
                        insuranceR[0] + ' ' + str(int(insuranceR[1]) + 12) + '\n' + insuranceR[2] + ' ' + insuranceR[3])
                await bot.send_message(message.chat.id, 'Вы купили страховку на жизнь на 1 год', reply_markup=markup)
                return
            if os.path.exists(
                    f'users/{games}/move.txt') and message.text.lower() == 'страховка на имущество' and data['magazine']:  ################# СТРАХОВКА НА ИМУЩЕСТВО
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                           'Магазин страховок')
                if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                    with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                        insurance.write('СЖ 00\nСИ 00')
                with open(f'users/{message.chat.id}/income.txt', 'r') as incomeR:
                    incomeR = incomeR.read().split()
                if int(incomeR[1]) <= 3000:
                    await bot.send_message(message.chat.id, 'У вас нехватает наличных', reply_markup=markup)
                    return
                else:
                    incomeR[1] = str(int(incomeR[1]) - 3000)
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(incomeR)):
                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(incomeR[i] + '\n')
                                continue
                            incomeW.write(incomeR[i] + ' ')
                with open(f'users/{message.chat.id}/insurance.txt', 'r') as insuranceR:
                    insuranceR = insuranceR.read().split()
                with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                    insurance.write(
                        insuranceR[0] + ' ' + insuranceR[1] + '\n' + insuranceR[2] + ' ' + str(int(insuranceR[3]) + 12))
                await bot.send_message(message.chat.id, 'Вы купили страховку на имущество на 1 год', reply_markup=markup)
                return
        except KeyError:
            async with state.proxy() as data:
                data['magazine'] = False
            pass
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == 'статистика':  ############################ СТАТИСТИКА
        vivod = ''
        with open(f'users/{games}/consumption.txt', 'r') as consumption:
            for i in consumption.readlines():
                vivod += i
        await bot.send_message(message.chat.id,
                               f'РАСХОДЫ\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        vivod = ''
        with open(f'users/{games}/income.txt', 'r') as income:
            for i in income.readlines():
                vivod += i
        await bot.send_message(message.chat.id, f'ДОХОДЫ\n{vivod}')
        with open(f'users/{message.chat.id}/stock.txt', 'r') as stockR:
            stockR = stockR.read().split()
            for j in range(0, (int(len(stockR) / 6))):
                for i in range(len(stockR)):
                    if i % 6 == 0:
                        if stockR[i + 1] == '0':
                            del stockR[i], stockR[i], stockR[i], stockR[i], stockR[i], stockR[i]
                            break
        with open(f'users/{message.chat.id}/stock.txt', 'w') as stockW:
            for i in range(len(stockR)):
                if i % 6 == 0 and i != 0:
                    stockW.write('\n' + str(stockR[i]) + ' ')
                    continue
                stockW.write(str(stockR[i]) + ' ')
        vivod = ''
        with open(f'users/{games}/stock.txt', 'r') as stock:
            for i in stock.readlines():
                vivod += i
        if vivod != '':
            await bot.send_message(message.chat.id,
                                   f'Акции:\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        else:
            await bot.send_message(message.chat.id, 'У вас нет акций')
        with open(f'users/{message.chat.id}/investment.txt', 'r') as stockR:
            stockR = stockR.read().split()
            for j in range(0, (int(len(stockR) / 6))):
                for i in range(len(stockR)):
                    if i % 6 == 0:
                        if stockR[i + 1] == '0':
                            del stockR[i], stockR[i], stockR[i], stockR[i], stockR[i], stockR[i]
                            break
        with open(f'users/{message.chat.id}/investment.txt', 'w') as investmentW:
            for i in range(len(stockR)):
                if i % 6 == 0 and i != 0:
                    investmentW.write('\n' + str(stockR[i]) + ' ')
                    continue
                investmentW.write(str(stockR[i]) + ' ')
        vivod = ''
        with open(f'users/{games}/investment.txt', 'r') as investment:
            for i in investment.readlines():
                vivod += i
        if vivod != '':
            await bot.send_message(message.chat.id,
                                   f'Облигации:\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        else:
            await bot.send_message(message.chat.id, 'У вас нет облигаций')
        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                insurance.write('СЖ 00\nСИ 00')
        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
            insurance = insurance.read().split()
        if insurance[1] == '00' and insurance[3] != '00':
            await bot.send_message(message.chat.id,
                                   f'У вас нету страховки на жизнь\nСтраховка на имущество будет действовать {insurance[3]} месяцев')
        elif insurance[3] == '00' and insurance[1] != '00':
            await bot.send_message(message.chat.id,
                                   f'Страховка на жизнь будет действовать {insurance[1]} месяцев\nУ вас нету страховки на имущество')
        elif insurance[3] == '00' and insurance[1] == '00':
            await bot.send_message(message.chat.id, 'У вас нету страховок')
        else:
            await bot.send_message(message.chat.id,
                                   f'Страховка на жизнь будет действовать {insurance[1]} месяцев\nСтраховка на имущество будет действовать {insurance[3]} месяцев')
        return
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == 'отключить/включить подтверждение':  ####### ОТКЛЮЧИТЬ ВКЛЮЧИТЬ ПОДТВЕРЖДЕНИЕ
        with open(f'users/{games}/data.txt', 'r') as dataR:
            dataR = dataR.read().split()
        if dataR[4] == 'True':
            dataR[4] = 'False'
            vivod = ''
            for i in dataR:
                vivod += i + ' '
            with open(f'users/{games}/data.txt', 'w') as dataW:
                dataW.write(vivod)
            await bot.send_message(message.chat.id, 'Подтверждение выключено')
        else:
            dataR[4] = 'True'
            vivod = ''
            for i in dataR:
                vivod += i + ' '
            with open(f'users/{games}/data.txt', 'w') as dataW:
                dataW.write(vivod)
            await bot.send_message(message.chat.id, 'Подтверждение включено')
        return
    async with state.proxy() as data:
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == 'купить' and data[
            'stocks'] == True:  ## КУПИТЬ АКЦИИ
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена', 'Купить на все')
            await bot.send_message(message.chat.id, 'Сколько акций вы хотите купить?',
                                   reply_markup=markup)
            await game.confirm.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == 'продать' and data[
            'stocks'] == True:  ## ПРОДАТЬ АКЦИИ
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена', 'Продать все')
            await bot.send_message(message.chat.id, 'Сколько акций вы хотите продать?',
                                   reply_markup=markup)
            await game.confirmsell.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == 'купить' and data[
            'investments'] == True:  ## КУПИТЬ ОБЛИГАЦИИ
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена', 'Купить на все')
            await bot.send_message(message.chat.id, 'Сколько облигаций вы хотите купить?',
                                   reply_markup=markup)
            await game.investment.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == 'продать' and data[
            'investments'] == True:  ## ПРОДАТЬ ОБЛИГАЦИИ
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('Отмена', 'Продать все')
            await bot.send_message(message.chat.id, 'Сколько облигаций вы хотите продать'
                                                    '?',
                                   reply_markup=markup)
            await game.investmentsell.set()
            return
        if os.path.exists(f'users/{games}/move.txt'):
            await bot.send_message(message.chat.id, 'Выберите другое дейсвие')
            return
        await bot.send_message(message.chat.id, 'Вы присоеденились к игре, ждите пока лидер группы начнет игру\nЧто '
                                                'бы выйти из группы - leave')


@dp.message_handler(lambda message: message.text.lower() == 'отмена',
                    state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
               'Магазин страховок')
    await bot.send_message(message.chat.id, 'Дейсвие отменено', reply_markup=markup)
    await game.waitingGame.set()


@dp.message_handler(
    lambda message: not message.text.isdigit() and message.text.lower() != 'продать все' and message.text.lower() != 'взять кредит' and message.text.lower() == 'взять кредит' and message.text.lower() != 'да' and message.text.lower() != 'нет' and message.text.lower() != 'купить на все',
    state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    await bot.send_message(message.chat.id, 'Некорректно введено количество')


@dp.message_handler(
    lambda message: message.text.lower() != 'продать все' and message.text.lower() != 'купить на все' and message.text.lower() != 'взять кредит' and  message.text.lower() == 'взять кредит' and message.text.lower() != 'да' and message.text.lower() != 'нет' and int(
        message.text) <= 0, state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    await bot.send_message(message.chat.id, 'Некорректно введено количество')


@dp.message_handler(state=game.investment)
async def confirm(message: types.Message,
                  state: FSMContext):  ########################################################## ПОКУПКА ОБЛИГАЦИЙ
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    buyall = False
    if message.text.lower() == 'купить на все':
        with open(f'users/{message.chat.id}/income.txt', 'r') as income:
            income = income.read().split()
        async with state.proxy() as data:
            data['num'] = str(math.floor(int(income[1]) / int(data["investment"].split()[3])))
        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(str(math.floor(int(income[1]) / int(data["investment"].split()[3]))))
        buyall = True
    if message.text.isdigit():
        async with state.proxy() as data:
            data['num'] = message.text
        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(message.text)
    with open(f'users/{message.chat.id}/data.txt', 'r') as datas:
        datas = datas.read().split()
    if datas[4] == 'False' and message.text.lower() == 'да':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    elif datas[4] == 'False' and message.text.lower() == 'нет':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == 'да' or buyall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                           'Отключить/включить подтверждение', 'Магазин страховок')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                    oldIncome = income[1]
                if int(num[0]) * int(data["investment"].split()[3]) <= int(income[1]):
                    income[1] = str(int(income[1]) - int(num[0]) * int(data["investment"].split()[3]))
                    income[12] = str(int(income[12]) + int(data["num"]) * int(data["investment"].split()[11]))
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(income)):

                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(income[i] + '\n')
                                continue
                            incomeW.write(income[i] + ' ')
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {str(num[0])} облигаций {str(data["investment"]).split()[1]}. По цене ' + str(
                                               data["investment"].split()[
                                                   3]) + f' на сумму {str(int(oldIncome) - int(income[1]))} Пассивный доход {int(data["num"]) * int(data["investment"].split()[11])}\n'
                                                         f'Остаток наличных {income[1]}', reply_markup=markup)
                    with open(f'users/{message.chat.id}/investment.txt', 'a') as stock:
                        with open(f'users/{message.chat.id}/investment.txt', 'r') as stockR:
                            stockR = stockR.read().split()
                            for i in range(len(stockR)):
                                if i % 6 == 0:
                                    if stockR[i] == str(data["investment"]).split()[1]:
                                        with open(f'users/{message.chat.id}/investment.txt', 'w') as stockW:
                                            stockR[i + 5] = str(int((int(stockR[i + 1]) * int(stockR[i + 5]) + int(
                                                num[0]) * int(data["investment"].split()[3])) / (
                                                                            int(stockR[i + 1]) + int(num[0]))))
                                            stockR[i + 1] = str(int(stockR[i + 1]) + int(str(num[0])))
                                            for i in range(len(stockR)):
                                                if i % 6 == 0 and i != 0:
                                                    stockW.write('\n' + str(stockR[i]) + ' ')
                                                    continue
                                                stockW.write(str(stockR[i]) + ' ')
                                            stockW.write('\n')
                                            await game.waitingGame.set()
                                            return
                        stock.write(str(data["investment"]).split()[1] + f' {str(num[0])} шт. По цене ' + str(
                            data["investment"].split()[3]) + '\n')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Отмена', 'Взять кредит')
                    await bot.send_message(message.chat.id,
                                           'У вас не хватает наличных, введите количевство еще раз\nЕсли хотите выйти введите '
                                           '"Отмена" что бы '
                                           'выйти. Или же можете взять кредит', reply_markup=markup)
                return
    if message.text.lower() == 'нет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Да', 'Нет')
    await bot.send_message(message.chat.id,
                           f'Хотите купить {str(data["num"])} облигаций {str(data["investment"]).split()[1]}. По цене ' + str(
                               data["investment"].split()[
                                   3]) + f' на сумму {str(int(data["num"]) * int(data["investment"].split()[3]))} Пассивный доход {int(data["num"]) * int(data["investment"].split()[11])}\n'
                                         f'Остаток наличных {str(int(income[1]) - int(data["num"]) * int(data["investment"].split()[3]))}\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"',
                           reply_markup=markup)


@dp.message_handler(
    state=game.investmentsell)  ############################################################################ ПРОДАЖА ОБЛИГАЦИЙ
async def confirm(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    sellall = False
    if message.text.lower() == 'продать все':
        numstock = 0
        ids = 0
        async with state.proxy() as data:
            with open(f'users/{message.chat.id}/investment.txt', 'r') as stock:
                stock = stock.read().split()
                for i in range(len(stock)):
                    if i % 6 == 0:
                        if stock[i] == data['investment'].split()[1]:
                            numstock = stock[i + 1]
                            ids = i + 1
            if str(numstock) == '0':
                await bot.send_message(message.chat.id, 'У вас нет облигаций')
                return
            data['num'] = str(numstock)
            with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
                temp.write(str(numstock) + ' ' + str(numstock) + ' ' + str(ids))
            sellall = True
    if message.text.isdigit():
        async with state.proxy() as data:
            data['num'] = message.text
        numstock = 0
        ids = 0
        with open(f'users/{message.chat.id}/investment.txt', 'r') as stock:
            stock = stock.read().split()
            for i in range(len(stock)):
                if i % 6 == 0:
                    if stock[i] == data['investment'].split()[1]:
                        numstock = stock[i + 1]
                        ids = i + 1

        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(message.text + ' ' + str(numstock) + ' ' + str(ids))
    with open(f'users/{message.chat.id}/data.txt', 'r') as datas:
        datas = datas.read().split()
    if datas[4] == 'False' and message.text.lower() == 'да':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    elif datas[4] == 'False' and message.text.lower() == 'нет':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == 'да' or sellall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                           'Отключить/включить подтверждение', 'Магазин страховок')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/investment.txt', 'r') as stock:
                    stock = stock.read().split()
                if int(num[0]) <= int(num[1]):
                    stock[int(num[2])] = str(int(num[1]) - int(num[0]))
                    await bot.send_message(message.chat.id,
                                           f'Вы продали {str(data["num"])} облигаций {str(data["investment"]).split()[1]}. По цене ' + str(
                                               data["investment"].split()[
                                                   3]) + f' на сумму {str(int(data["num"]) * int(data["investment"].split()[3]))} Пассивный доход -{int(data["num"]) * int(data["investment"].split()[11])}\n'
                                                         f'Остаток наличных {str(int(income[1]) + int(data["num"]) * int(data["investment"].split()[3]))}',
                                           reply_markup=markup)
                    with open(f'users/{message.chat.id}/investment.txt', 'w') as stockW:
                        for i in range(len(stock)):
                            if i % 6 == 0 and i != 0:
                                stockW.write('\n' + str(stock[i]) + ' ')
                                continue
                            stockW.write(str(stock[i]) + ' ')
                        stockW.write('\n')
                    income[1] = str(int(income[1]) + (int(data["num"]) * int(data["investment"].split()[3])))
                    income[12] = str(int(income[12]) - int(data["num"]) * int(data["investment"].split()[11]))
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(income)):
                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(income[i] + '\n')
                                continue
                            incomeW.write(income[i] + ' ')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                               'Отключить/включить подтверждение', 'Магазин страховок')
                    await bot.send_message(message.chat.id,
                                           'У вас не хватает облигаций, введите количевство еще раз\nИли введите '
                                           '"Отмена" что бы '
                                           'выйти', reply_markup=markup)
                    await game.waitingGame.set()
                return
    if message.text.lower() == 'нет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Да', 'Нет')
    await bot.send_message(message.chat.id,
                           f'Хотите продать {str(data["num"])} облигаций {str(data["investment"]).split()[1]}. По цене ' + str(
                               data["investment"].split()[
                                   3]) + f' на сумму {str(int(data["num"]) * int(data["investment"].split()[3]))} Пассивный доход -{int(data["num"]) * int(data["investment"].split()[11])}\n'
                                         f'Остаток наличных {str(int(income[1]) + int(data["num"]) * int(data["investment"].split()[3]))}\nДа/Нет (Введите число акций еще раз если хотите продать другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"',
                           reply_markup=markup)



@dp.message_handler(state=game.confirm)
async def confirm(message: types.Message,
                  state: FSMContext):  ########################################################## ПОКУПКА АКЦИИ
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    buyall = False
    if message.text.lower() == 'купить на все':
        with open(f'users/{message.chat.id}/income.txt', 'r') as income:
            income = income.read().split()
        async with state.proxy() as data:
            data['num'] = str(math.floor(int(income[1]) / int(data["stock"].split()[3])))
        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(str(math.floor(int(income[1]) / int(data["stock"].split()[3]))))
        buyall = True
    if message.text.isdigit():
        async with state.proxy() as data:
            data['num'] = message.text
        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(message.text)
    with open(f'users/{message.chat.id}/data.txt', 'r') as datas:
        datas = datas.read().split()
    if datas[4] == 'False' and message.text.lower() == 'да':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    elif datas[4] == 'False' and message.text.lower() == 'нет':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == 'да' or buyall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                           'Отключить/включить подтверждение', 'Магазин страховок')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                    oldIncome = income[1]
                if int(num[0]) * int(data["stock"].split()[3]) <= int(income[1]):
                    income[1] = str(int(income[1]) - int(num[0]) * int(data["stock"].split()[3]))
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(income)):
                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(income[i] + '\n')
                                continue
                            incomeW.write(income[i] + ' ')
                    await bot.send_message(message.chat.id,
                                           f'Вы купили {str(num[0])} акций {str(data["stock"]).split()[1]}. По цене ' + str(
                                               data["stock"].split()[
                                                   3]) + f' на сумму {str(int(oldIncome) - int(income[1]))}\n'
                                                         f'Остаток наличных {income[1]}', reply_markup=markup)
                    with open(f'users/{message.chat.id}/stock.txt', 'a') as stock:
                        with open(f'users/{message.chat.id}/stock.txt', 'r') as stockR:
                            stockR = stockR.read().split()
                            for i in range(len(stockR)):
                                if i % 6 == 0:
                                    if stockR[i] == str(data["stock"]).split()[1]:
                                        with open(f'users/{message.chat.id}/stock.txt', 'w') as stockW:
                                            stockR[i + 5] = str(int((int(stockR[i + 1]) * int(stockR[i + 5]) + int(
                                                num[0]) * int(data["stock"].split()[3])) / (
                                                                            int(stockR[i + 1]) + int(num[0]))))
                                            stockR[i + 1] = str(int(stockR[i + 1]) + int(str(num[0])))
                                            for i in range(len(stockR)):
                                                if i % 6 == 0 and i != 0:
                                                    stockW.write('\n' + str(stockR[i]) + ' ')
                                                    continue
                                                stockW.write(str(stockR[i]) + ' ')
                                            stockW.write('\n')
                                            await game.waitingGame.set()
                                            return
                        stock.write(str(data["stock"]).split()[1] + f' {str(num[0])} шт. По цене ' + str(
                            data["stock"].split()[3]) + '\n')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Отмена', 'Взять кредит')
                    await bot.send_message(message.chat.id,
                                           'У вас не хватает наличных, введите количевство акций еще раз\nВведите '
                                           '"Отмена" что бы '
                                           'выйти. Или возьмите кредит', reply_markup=markup)
                    async with state.proxy() as data:
                        data['credit'] = True
                return
    async with state.proxy() as data:
        try:
            if message.text.lower() == 'взять кредит' and data['credit']:
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/consumption.txt', 'r') as consumption:
                    consumption = consumption.read().split()
                consumptionCredit = int(consumption[1]) + int(consumption[3]) + int(consumption[5]) + int(consumption[7]) + int(consumption[9])
                incomeCredit = int(income[1]) + int(income[3]) + int(income[5]) + int(income[7]) + int(income[9]) + int(income[12])
                with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                    num = num.read().split()
                    if -incomeCredit - -consumptionCredit < int(income[1]) - int(num[0]) * int(data["stock"].split()[3]):# Остаток наличных
                        await bot.send_message(message.chat.id, 'Вы взяли кредит')
                return
        except Exception:
            data['credit'] = False
            return
    if message.text.lower() == 'нет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Да', 'Нет')
    await bot.send_message(message.chat.id,
                           f'Хотите купить {str(data["num"])} акций {str(data["stock"]).split()[1]}. По цене ' + str(
                               data["stock"].split()[
                                   3]) + f' на сумму {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                         f'Остаток наличных {str(int(income[1]) - int(data["num"]) * int(data["stock"].split()[3]))}\nДа/Нет (Введите число акций еще раз если хотите купить другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"',
                           reply_markup=markup)


@dp.message_handler(
    state=game.confirmsell)  ############################################################################ ПРОДАЖА АКЦИИ
async def confirm(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + 'написал: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, 'Повторите')
        await state.finish()
        return
    sellall = False
    if message.text.lower() == 'продать все':
        numstock = 0
        ids = 0
        async with state.proxy() as data:
            with open(f'users/{message.chat.id}/stock.txt', 'r') as stock:
                stock = stock.read().split()
                for i in range(len(stock)):
                    if i % 6 == 0:
                        if stock[i] == data['stock'].split()[1]:
                            numstock = stock[i + 1]
                            ids = i + 1
            if str(numstock) == '0':
                await bot.send_message(message.chat.id, 'У вас нет акций этой компании')
                return
            data['num'] = str(numstock)
            with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
                temp.write(str(numstock) + ' ' + str(numstock) + ' ' + str(ids))
            sellall = True
    if message.text.isdigit():
        async with state.proxy() as data:
            data['num'] = message.text
        numstock = 0
        ids = 0
        with open(f'users/{message.chat.id}/stock.txt', 'r') as stock:
            stock = stock.read().split()
            for i in range(len(stock)):
                if i % 6 == 0:
                    if stock[i] == data['stock'].split()[1]:
                        numstock = stock[i + 1]
                        ids = i + 1

        with open(f'users/{message.chat.id}/temp.txt', 'w') as temp:
            temp.write(message.text + ' ' + str(numstock) + ' ' + str(ids))
    with open(f'users/{message.chat.id}/data.txt', 'r') as datas:
        datas = datas.read().split()
    if datas[4] == 'False' and message.text.lower() == 'да':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    elif datas[4] == 'False' and message.text.lower() == 'нет':
        await bot.send_message(message.chat.id, 'Некорректно введено количество')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == 'да' or sellall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                           'Отключить/включить подтверждение', 'Магазин страховок')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/stock.txt', 'r') as stock:
                    stock = stock.read().split()
                if int(num[0]) <= int(num[1]):
                    stock[int(num[2])] = str(int(num[1]) - int(num[0]))
                    await bot.send_message(message.chat.id,
                                           f'Вы продали {str(data["num"])} акций {str(data["stock"]).split()[1]}. По цене ' + str(
                                               data["stock"].split()[
                                                   3]) + f' на сумму {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                                         f'Остаток наличных {str(int(income[1]) + int(data["num"]) * int(data["stock"].split()[3]))}',
                                           reply_markup=markup)
                    with open(f'users/{message.chat.id}/stock.txt', 'w') as stockW:
                        for i in range(len(stock)):
                            if i % 6 == 0 and i != 0:
                                stockW.write('\n' + str(stock[i]) + ' ')
                                continue
                            stockW.write(str(stock[i]) + ' ')
                        stockW.write('\n')
                    income[1] = str(int(income[1]) + (int(data["num"]) * int(data["stock"].split()[3])))
                    with open(f'users/{message.chat.id}/income.txt', 'w') as incomeW:
                        for i in range(len(income)):
                            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 12:
                                incomeW.write(income[i] + '\n')
                                continue
                            incomeW.write(income[i] + ' ')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('Купить', 'Продолжить', 'Продать', 'Статистика',
                               'Отключить/включить подтверждение', 'Магазин страховок')
                    await bot.send_message(message.chat.id,
                                           'У вас не хватает акций, введите количевство еще раз\nили введите '
                                           '"Отмена" что бы '
                                           'выйти', reply_markup=markup)

                return
    if message.text.lower() == 'нет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('Купить', 'Продолжить', 'Продать', 'Статистика', 'Отключить/включить подтверждение',
                   'Магазин страховок')
        await bot.send_message(message.chat.id, 'Действие отменено', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Да', 'Нет')
    await bot.send_message(message.chat.id,
                           f'Хотите продать {str(data["num"])} акций {str(data["stock"]).split()[1]}. По цене ' + str(
                               data["stock"].split()[
                                   3]) + f' на сумму {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                         f'Остаток наличных {str(int(income[1]) + int(data["num"]) * int(data["stock"].split()[3]))}\nДа/Нет (Введите число акций еще раз если хотите продать другое количвество)\nЭто сообщение можно отключить кнопкой "Отключить/включить подтверждение"',
                           reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)