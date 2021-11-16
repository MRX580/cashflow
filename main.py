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
    profes = [['��������', '�������� ������', '�������', '��������-�����������', '������������� ��������',
               '������', '������', '�����', '����������', '�������', '��������� �������������', '�������'],
              [25000, 20000, 15000, 18000, 17000, 19000, 23000, 22000, 20000, 16000, 17000, 21000]]
    return profes[0][num] + ' ' + str(profes[1][num])


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    with open(f'users_id.txt', 'r') as users:
        users = users.read().split()
    if not str(message.chat.id) in users:
        with open(f'users_id.txt', 'a') as users:
            users.write(str(message.chat.id) + ' ')
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '������� �������� ��� ��� ��� �� ���������', reply_markup=markup)
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
        if last.split()[0] == '�����':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == '���������':
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
    markup.add('�����')
    await dp.bot.set_my_commands([
        types.BotCommand("rules", "������� ����"),
    ])
    await message.reply('������! ��� ��� � ���������� �����������, � ���� ����� �� ������ ����� �������, '
                        '� �� ������ ���� �� �������� �� ��������, ����� ����� �������� ����������� ����������� � '
                        '�������� �����, �� ����� ���� ����� �� ����� �������!\n���� �� ������� �� ������ � �������� '
                        '���� ���������� ������������ � ��������� - /rules\n��� �� �������������� � ������ - join ('
                        'id)\n��� ������� ����� - �����',
                        reply_markup=markup)


@dp.message_handler(commands='rules')
async def rules(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '������� �������� ��� ��� ��� �� ���������', reply_markup=markup)
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
        if last.split()[0] == '�����':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == '���������':
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
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if os.path.exists(f'users/{message.chat.id}/game.txt') or os.path.exists(f'users/{message.chat.id}/move.txt'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '������� �������� ��� ��� ��� �� ���������', reply_markup=markup)
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
        if last.split()[0] == '�����':
            async with state.proxy() as data:
                data['stocks'] = True
                data['bussiness'] = False
                data['realestates'] = False
                data['investments'] = False
                data['insurances'] = False
                data['stock'] = last
        if last.split()[0] == '���������':
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
    if message.text.lower() == '�����':
        await dp.bot.set_my_commands([
            types.BotCommand("rules", "������� ����"),
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
            markup.add('������ ����')
        with open(f'users/{message.chat.id}/income.txt', 'w') as income:
            income.write(f'�������� 20000\n�������� 0\n��������� '
                         f'0\n������������ 0\n������ 0\n��������� ����� 0')
        with open(f'users/{message.chat.id}/consumption.txt', 'w') as consumption:
            consumption.write(f'����� 15000\n������ 0\n������ 0\n������_������� 0\n�������(����) 0')
        with open(f'users/{message.chat.id}/stock.txt', 'w') as stock:
            stock.write('')
        with open(f'users/{message.chat.id}/players.txt', 'w') as player:
            player.write('')
        with open(f'users/{message.chat.id}/investment.txt', 'w') as investment:
            investment.write('')
        with open(f'users/{message.chat.id}/progress.txt', 'w') as progress:
            progress.write(str(await randProgress()) + ' stock ' + str(await randProgress()) + ' 3')
        await bot.send_message(message.chat.id, f"�� �������������� � ����. ��� id - {message.chat.id}, "
                                                f"����������� ��� ��� �� ������ ����� "
                                                f"�������������� � ����, ��� �� ������ ���� ������� "
                                                f"\"������ ����\"\n���������� ����� �������� - players",
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
                    types.BotCommand("rules", "������� ����"),
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
                    markup.add('����������')
                with open(f'users/{message.chat.id}/income.txt', 'w') as income:
                    income.write(f'�������� 20000\n�������� 0\n��������� '
                                 f'0\n������������ 0\n������ 0\n��������� ����� 0')
                with open(f'users/{message.chat.id}/consumption.txt', 'w') as consumption:
                    consumption.write(f'����� 15000\n������ 0\n������ 0\n������_������� 0\n�������(����) 0')
                with open(f'users/{message.chat.id}/players.txt', 'w') as player:
                    player.write('')
                with open(f'users/{message.chat.id}/investment.txt', 'w') as investment:
                    investment.write('')
                with open(f'users/{message.chat.id}/progress.txt', 'w') as progress:
                    progress.write(str(await randProgress()) + ' stock ' + str(await randProgress()) + ' 3')
            if message.text.lower().split()[1] == str(message.chat.id):
                await bot.send_message(message.chat.id, '�� �� ������ �������������� � ����� ����')
                return
            with open(f'users/{message.text.lower().split()[1]}/players.txt', 'r') as player:
                if len(player.read().split()) >= 6:
                    await bot.send_message(message.chat.id, '������� �����������')
                    return
            with open(f'users/{message.text.lower().split()[1]}/players.txt', 'a') as player:
                player.write(str(message.chat.id) + ' ')
            with open(f'users/{message.text.lower().split()[1]}/playersName.txt', 'a') as player:
                player.write(str(message.chat.username) + ' ')
            with open(f'users/{message.chat.id}/game.txt', 'w') as games:
                games.write(message.text.lower().split()[1])
            await bot.send_message(message.text.lower().split()[1], f'{message.chat.username}, �������������')
            await bot.send_message(message.chat.id,
                                   '�� �������������� � ����, ��������� ���� ����� ������ ������ ����\n��� �� '
                                   '�������� ���� - leave')
            with open(f'users/{message.chat.id}/statistic.txt', 'r') as statistics:
                statTemp = statistics.read().split()
                statTemp[len(statTemp) - 1] = '1'
            with open(f'users/{message.chat.id}/statistic.txt', 'w') as statistics:
                statistics.write(' '.join(statTemp))
                await dp.bot.delete_my_commands()
                await game.waitingGame.set()
            return
    except FileNotFoundError as e:
        await bot.send_message(message.chat.id, '�� ��������� ������ id')
    except IndexError as e:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('�����')
    await bot.send_message(message.chat.id, '������� "�����" ������� �����\n��� join ��� �� ��������������',
                           reply_markup=markup)


@dp.message_handler(state=game.waitingGame)
async def waitingGame(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
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
        await bot.send_message(message.chat.id, '���������')
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
                await bot.send_message(i, '����� ����� � �����, ������ ���������')
                state = dp.current_state(chat=i, user=i)
                await state.set_state(await state.finish())
        else:
            await state.finish()
            await bot.send_message(message.chat.id, '�� ����� �� �����')
        return
    if message.text.lower() == 'leave':
        with open(f'users/{message.chat.id}/game.txt', 'r') as games:
            games = games.read()
            with open(f'users/{games}/playersName.txt', 'r') as playersName:
                playersName = playersName.read().split()
            with open(f'users/{games}/players.txt', 'r') as players:
                players = players.read().split()
        await bot.send_message(message.chat.id, '���� ��������')
        with open(f'users/{games}/playersName.txt', 'w') as pn:
            with open(f'users/{games}/players.txt', 'w') as pl:
                for i in range(len(players)):
                    if str(players[i]) != str(message.chat.id):
                        pn.write(playersName[i])
                        pl.write(players[i] + ' ')
        await bot.send_message(players[0], message.chat.username + '������� �����')
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
            await bot.send_message(message.chat.id, '� ����� ������ ����')
        else:
            await bot.send_message(message.chat.id, vivod + '\n��� �� ������� ������������ ������� kick (id)')
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
            await bot.send_message(message.chat.id, '����� ������')
            await bot.send_message(players[int(message.text.lower().split()[1])], '��� ������� � �����')
            return
        else:
            await bot.send_message(message.chat.id, '����������� ������ id')
            return
    if statistic[len(statistic) - 1] == '0' and message.text.lower() == '������ ����' and not os.path.exists(
            f'users/{message.chat.id}/move.txt'):
        with open(f'users/{message.chat.id}/players.txt', 'r') as players:
            players = players.read().split()
            with open(f'users/{message.chat.id}/move.txt', 'w') as move:
                move.write(str(len(players)) + ' 0')
        for i in players:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('����������')
            with open(f'users/{i}/statistic.txt', 'r') as stat:
                stat = stat.read().split()
            if len(stat) == 5:
                await bot.send_message(i,
                                       f'���� ������\n���� ���������:{stat[0]}. �������� - {stat[1]}\n��� �� �������� '
                                       f'���� ������� leave',
                                       reply_markup=markup)
            else:
                await bot.send_message(i,
                                       f'���� ������\n���� ���������: {stat[0]} {stat[1]}. �������� - {stat[2]}\n��� '
                                       f'�� �������� ���� ������� leave',
                                       reply_markup=markup)
        return
    if '�����������' in message.text.lower() and message.chat.id == 951679992:
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
                if message.text.lower() == '����������':
                    async with state.proxy() as data:
                        data['time'] = datetime.datetime.now()
                    with open(f'users/{message.chat.id}/progress.txt', 'r') as progress:
                        progress = progress.read().split()
                    if progress[int(progress[
                                        3]) - 1] == 'unexpectedexpenses':  ####################################### ������������� �������
                        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                                insurance.write('�� 00\n�� 00')
                        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
                            insurance = insurance.read().split()
                        unexpectedexpenses = str(pole.firstCircleFuncStockMarket()[6])
                        if unexpectedexpenses.split()[0] == '(��)':
                            if int(insurance[1]) > 0:
                                await bot.send_message(message.chat.id,
                                                       unexpectedexpenses + '\n� ��� ���� ���������, ������� ��������')
                                await nextprogress()
                                return
                        elif unexpectedexpenses.split()[0] == '(��)':
                            if int(insurance[3]) > 0:
                                await bot.send_message(message.chat.id,
                                                       unexpectedexpenses + '\n� ��� ���� ���������, ������� ��������')
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
                                        3]) - 1] == 'stock':  ######################################################## �����
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('������', '����������', '�������', '����������',
                                   '���������/�������� �������������', '������� ���������')
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
                        int(progress[3]) - 1] == 'business':  ################################################### ������
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('������', '����������', '����������',
                                   '���������/�������� �������������', '������� ���������')
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
                                          3]) - 1] == 'investment':  ################################################# ���������
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('������', '����������', '�������', '����������',
                                   '���������/�������� �������������', '������� ���������')
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
                                          3]) - 1] == 'realestate':  ################################################# �����������
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                        markup.add('������', '����������', '����������',
                                   '���������/�������� �������������', '������� ���������')
                        realestate = str(pole.firstCircleFuncStockMarket()[3])
                        with open(f'users/{message.chat.id}/last_action.txt', 'w') as last:
                            last.write(realestate)
                        async with state.proxy() as data:
                            data['realestate'] = realestate
                        await bot.send_message(message.chat.id, realestate + '(�����������)\ncoming soon',
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
                               3]) <= 0:  ########################################################################## ����� ������
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
                                               f'����� �� �����!\n������ {sum} ���\n������� {con[1]} ���\n����� {str(int(sum) - int(con[1]))} ���')
                        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                                insurance.write('�� 00\n�� 00')
                        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
                            insurance = insurance.read().split()
                            if int(insurance[1]) == 1 and insurance[1] != '00':
                                await bot.send_message(message.chat.id, '� ��� ����������� ��������� (��)')
                                insurance[1] = '00'
                            elif int(insurance[1]) >= 1:
                                insurance[1] = str(int(insurance[1]) - 1)
                            if int(insurance[3]) == 1 and insurance[3] != '00':
                                await bot.send_message(message.chat.id, '� ��� ����������� ��������� (��)')
                                insurance[3] = '00'
                            elif int(insurance[3]) >= 1:
                                insurance[3] = str(int(insurance[3]) - 1)
                        with open(f'users/{message.chat.id}/insurance.txt', 'w') as insuranceW:
                            insuranceW.write(
                                insurance[0] + ' ' + insurance[1] + '\n' + insurance[2] + ' ' + insurance[3])
                        return
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == '������� ���������':  ##################### ������� ���������
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        markup.add('��������� �� �����', '��������� �� ���������', '����������')
        await bot.send_message(message.chat.id, '��������� �� ����� - 3000 ���\n��������� �� ��������� - 5000 ���',
                               reply_markup=markup)
        async with state.proxy() as data:
            data['magazine'] = True
        return
    async with state.proxy() as data:
        try:
            if os.path.exists(
                    f'users/{games}/move.txt') and message.text.lower() == '��������� �� �����' and data['magazine']:  ##################### ��������� �� �����
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                           '������� ���������')
                if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                    with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                        insurance.write('�� 00\n�� 00')
                with open(f'users/{message.chat.id}/income.txt', 'r') as incomeR:
                    incomeR = incomeR.read().split()
                if int(incomeR[1]) <= 3000:
                    await bot.send_message(message.chat.id, '� ��� ��������� ��������', reply_markup=markup)
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
                await bot.send_message(message.chat.id, '�� ������ ��������� �� ����� �� 1 ���', reply_markup=markup)
                return
            if os.path.exists(
                    f'users/{games}/move.txt') and message.text.lower() == '��������� �� ���������' and data['magazine']:  ################# ��������� �� ���������
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                           '������� ���������')
                if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
                    with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                        insurance.write('�� 00\n�� 00')
                with open(f'users/{message.chat.id}/income.txt', 'r') as incomeR:
                    incomeR = incomeR.read().split()
                if int(incomeR[1]) <= 3000:
                    await bot.send_message(message.chat.id, '� ��� ��������� ��������', reply_markup=markup)
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
                await bot.send_message(message.chat.id, '�� ������ ��������� �� ��������� �� 1 ���', reply_markup=markup)
                return
        except KeyError:
            async with state.proxy() as data:
                data['magazine'] = False
            pass
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == '����������':  ############################ ����������
        vivod = ''
        with open(f'users/{games}/consumption.txt', 'r') as consumption:
            for i in consumption.readlines():
                vivod += i
        await bot.send_message(message.chat.id,
                               f'�������\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        vivod = ''
        with open(f'users/{games}/income.txt', 'r') as income:
            for i in income.readlines():
                vivod += i
        await bot.send_message(message.chat.id, f'������\n{vivod}')
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
                                   f'�����:\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        else:
            await bot.send_message(message.chat.id, '� ��� ��� �����')
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
                                   f'���������:\n{vivod.replace("_", " ").replace("(", " ").replace(")", "")}')
        else:
            await bot.send_message(message.chat.id, '� ��� ��� ���������')
        if not os.path.exists(f'users/{message.chat.id}/insurance.txt'):
            with open(f'users/{message.chat.id}/insurance.txt', 'w') as insurance:
                insurance.write('�� 00\n�� 00')
        with open(f'users/{message.chat.id}/insurance.txt', 'r') as insurance:
            insurance = insurance.read().split()
        if insurance[1] == '00' and insurance[3] != '00':
            await bot.send_message(message.chat.id,
                                   f'� ��� ���� ��������� �� �����\n��������� �� ��������� ����� ����������� {insurance[3]} �������')
        elif insurance[3] == '00' and insurance[1] != '00':
            await bot.send_message(message.chat.id,
                                   f'��������� �� ����� ����� ����������� {insurance[1]} �������\n� ��� ���� ��������� �� ���������')
        elif insurance[3] == '00' and insurance[1] == '00':
            await bot.send_message(message.chat.id, '� ��� ���� ���������')
        else:
            await bot.send_message(message.chat.id,
                                   f'��������� �� ����� ����� ����������� {insurance[1]} �������\n��������� �� ��������� ����� ����������� {insurance[3]} �������')
        return
    if os.path.exists(
            f'users/{games}/move.txt') and message.text.lower() == '���������/�������� �������������':  ####### ��������� �������� �������������
        with open(f'users/{games}/data.txt', 'r') as dataR:
            dataR = dataR.read().split()
        if dataR[4] == 'True':
            dataR[4] = 'False'
            vivod = ''
            for i in dataR:
                vivod += i + ' '
            with open(f'users/{games}/data.txt', 'w') as dataW:
                dataW.write(vivod)
            await bot.send_message(message.chat.id, '������������� ���������')
        else:
            dataR[4] = 'True'
            vivod = ''
            for i in dataR:
                vivod += i + ' '
            with open(f'users/{games}/data.txt', 'w') as dataW:
                dataW.write(vivod)
            await bot.send_message(message.chat.id, '������������� ��������')
        return
    async with state.proxy() as data:
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == '������' and data[
            'stocks'] == True:  ## ������ �����
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('������', '������ �� ���')
            await bot.send_message(message.chat.id, '������� ����� �� ������ ������?',
                                   reply_markup=markup)
            await game.confirm.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == '�������' and data[
            'stocks'] == True:  ## ������� �����
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('������', '������� ���')
            await bot.send_message(message.chat.id, '������� ����� �� ������ �������?',
                                   reply_markup=markup)
            await game.confirmsell.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == '������' and data[
            'investments'] == True:  ## ������ ���������
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('������', '������ �� ���')
            await bot.send_message(message.chat.id, '������� ��������� �� ������ ������?',
                                   reply_markup=markup)
            await game.investment.set()
            return
        if os.path.exists(f'users/{games}/move.txt') and message.text.lower() == '�������' and data[
            'investments'] == True:  ## ������� ���������
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('������', '������� ���')
            await bot.send_message(message.chat.id, '������� ��������� �� ������ �������'
                                                    '?',
                                   reply_markup=markup)
            await game.investmentsell.set()
            return
        if os.path.exists(f'users/{games}/move.txt'):
            await bot.send_message(message.chat.id, '�������� ������ �������')
            return
        await bot.send_message(message.chat.id, '�� �������������� � ����, ����� ���� ����� ������ ������ ����\n��� '
                                                '�� ����� �� ������ - leave')


@dp.message_handler(lambda message: message.text.lower() == '������',
                    state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
               '������� ���������')
    await bot.send_message(message.chat.id, '������� ��������', reply_markup=markup)
    await game.waitingGame.set()


@dp.message_handler(
    lambda message: not message.text.isdigit() and message.text.lower() != '������� ���' and message.text.lower() != '����� ������' and message.text.lower() == '����� ������' and message.text.lower() != '��' and message.text.lower() != '���' and message.text.lower() != '������ �� ���',
    state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    await bot.send_message(message.chat.id, '����������� ������� ����������')


@dp.message_handler(
    lambda message: message.text.lower() != '������� ���' and message.text.lower() != '������ �� ���' and message.text.lower() != '����� ������' and  message.text.lower() == '����� ������' and message.text.lower() != '��' and message.text.lower() != '���' and int(
        message.text) <= 0, state=[game.confirm, game.confirmsell, game.investment, game.investmentsell])
async def process_age_invalid(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    await bot.send_message(message.chat.id, '����������� ������� ����������')


@dp.message_handler(state=game.investment)
async def confirm(message: types.Message,
                  state: FSMContext):  ########################################################## ������� ���������
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    buyall = False
    if message.text.lower() == '������ �� ���':
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
    if datas[4] == 'False' and message.text.lower() == '��':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    elif datas[4] == 'False' and message.text.lower() == '���':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == '��' or buyall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������',
                           '���������/�������� �������������', '������� ���������')
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
                                           f'�� ������ {str(num[0])} ��������� {str(data["investment"]).split()[1]}. �� ���� ' + str(
                                               data["investment"].split()[
                                                   3]) + f' �� ����� {str(int(oldIncome) - int(income[1]))} ��������� ����� {int(data["num"]) * int(data["investment"].split()[11])}\n'
                                                         f'������� �������� {income[1]}', reply_markup=markup)
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
                        stock.write(str(data["investment"]).split()[1] + f' {str(num[0])} ��. �� ���� ' + str(
                            data["investment"].split()[3]) + '\n')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('������', '����� ������')
                    await bot.send_message(message.chat.id,
                                           '� ��� �� ������� ��������, ������� ����������� ��� ���\n���� ������ ����� ������� '
                                           '"������" ��� �� '
                                           '�����. ��� �� ������ ����� ������', reply_markup=markup)
                return
    if message.text.lower() == '���':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '�������� ��������', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('��', '���')
    await bot.send_message(message.chat.id,
                           f'������ ������ {str(data["num"])} ��������� {str(data["investment"]).split()[1]}. �� ���� ' + str(
                               data["investment"].split()[
                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["investment"].split()[3]))} ��������� ����� {int(data["num"]) * int(data["investment"].split()[11])}\n'
                                         f'������� �������� {str(int(income[1]) - int(data["num"]) * int(data["investment"].split()[3]))}\n��/��� (������� ����� ����� ��� ��� ���� ������ ������ ������ �����������)\n��� ��������� ����� ��������� ������� "���������/�������� �������������"',
                           reply_markup=markup)


@dp.message_handler(
    state=game.investmentsell)  ############################################################################ ������� ���������
async def confirm(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    sellall = False
    if message.text.lower() == '������� ���':
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
                await bot.send_message(message.chat.id, '� ��� ��� ���������')
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
    if datas[4] == 'False' and message.text.lower() == '��':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    elif datas[4] == 'False' and message.text.lower() == '���':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == '��' or sellall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������',
                           '���������/�������� �������������', '������� ���������')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/investment.txt', 'r') as stock:
                    stock = stock.read().split()
                if int(num[0]) <= int(num[1]):
                    stock[int(num[2])] = str(int(num[1]) - int(num[0]))
                    await bot.send_message(message.chat.id,
                                           f'�� ������� {str(data["num"])} ��������� {str(data["investment"]).split()[1]}. �� ���� ' + str(
                                               data["investment"].split()[
                                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["investment"].split()[3]))} ��������� ����� -{int(data["num"]) * int(data["investment"].split()[11])}\n'
                                                         f'������� �������� {str(int(income[1]) + int(data["num"]) * int(data["investment"].split()[3]))}',
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
                    markup.add('������', '����������', '�������', '����������',
                               '���������/�������� �������������', '������� ���������')
                    await bot.send_message(message.chat.id,
                                           '� ��� �� ������� ���������, ������� ����������� ��� ���\n��� ������� '
                                           '"������" ��� �� '
                                           '�����', reply_markup=markup)
                    await game.waitingGame.set()
                return
    if message.text.lower() == '���':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '�������� ��������', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('��', '���')
    await bot.send_message(message.chat.id,
                           f'������ ������� {str(data["num"])} ��������� {str(data["investment"]).split()[1]}. �� ���� ' + str(
                               data["investment"].split()[
                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["investment"].split()[3]))} ��������� ����� -{int(data["num"]) * int(data["investment"].split()[11])}\n'
                                         f'������� �������� {str(int(income[1]) + int(data["num"]) * int(data["investment"].split()[3]))}\n��/��� (������� ����� ����� ��� ��� ���� ������ ������� ������ �����������)\n��� ��������� ����� ��������� ������� "���������/�������� �������������"',
                           reply_markup=markup)



@dp.message_handler(state=game.confirm)
async def confirm(message: types.Message,
                  state: FSMContext):  ########################################################## ������� �����
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    buyall = False
    if message.text.lower() == '������ �� ���':
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
    if datas[4] == 'False' and message.text.lower() == '��':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    elif datas[4] == 'False' and message.text.lower() == '���':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == '��' or buyall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������',
                           '���������/�������� �������������', '������� ���������')
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
                                           f'�� ������ {str(num[0])} ����� {str(data["stock"]).split()[1]}. �� ���� ' + str(
                                               data["stock"].split()[
                                                   3]) + f' �� ����� {str(int(oldIncome) - int(income[1]))}\n'
                                                         f'������� �������� {income[1]}', reply_markup=markup)
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
                        stock.write(str(data["stock"]).split()[1] + f' {str(num[0])} ��. �� ���� ' + str(
                            data["stock"].split()[3]) + '\n')
                    await game.waitingGame.set()
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    markup.add('������', '����� ������')
                    await bot.send_message(message.chat.id,
                                           '� ��� �� ������� ��������, ������� ����������� ����� ��� ���\n������� '
                                           '"������" ��� �� '
                                           '�����. ��� �������� ������', reply_markup=markup)
                    async with state.proxy() as data:
                        data['credit'] = True
                return
    async with state.proxy() as data:
        try:
            if message.text.lower() == '����� ������' and data['credit']:
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/consumption.txt', 'r') as consumption:
                    consumption = consumption.read().split()
                consumptionCredit = int(consumption[1]) + int(consumption[3]) + int(consumption[5]) + int(consumption[7]) + int(consumption[9])
                incomeCredit = int(income[1]) + int(income[3]) + int(income[5]) + int(income[7]) + int(income[9]) + int(income[12])
                with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                    num = num.read().split()
                    if -incomeCredit - -consumptionCredit < int(income[1]) - int(num[0]) * int(data["stock"].split()[3]):# ������� ��������
                        await bot.send_message(message.chat.id, '�� ����� ������')
                return
        except Exception:
            data['credit'] = False
            return
    if message.text.lower() == '���':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '�������� ��������', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('��', '���')
    await bot.send_message(message.chat.id,
                           f'������ ������ {str(data["num"])} ����� {str(data["stock"]).split()[1]}. �� ���� ' + str(
                               data["stock"].split()[
                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                         f'������� �������� {str(int(income[1]) - int(data["num"]) * int(data["stock"].split()[3]))}\n��/��� (������� ����� ����� ��� ��� ���� ������ ������ ������ �����������)\n��� ��������� ����� ��������� ������� "���������/�������� �������������"',
                           reply_markup=markup)


@dp.message_handler(
    state=game.confirmsell)  ############################################################################ ������� �����
async def confirm(message: types.Message, state: FSMContext):
    print('[INFO] ' + str(
        message.chat.id) + f'({message.chat.username}|{message.chat.full_name}) ' + '�������: ' + message.text + ' ' + str(
        datetime.datetime.now()))
    if not os.path.exists(f'users/{message.chat.id}'):
        await bot.send_message(message.chat.id, '���������')
        await state.finish()
        return
    sellall = False
    if message.text.lower() == '������� ���':
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
                await bot.send_message(message.chat.id, '� ��� ��� ����� ���� ��������')
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
    if datas[4] == 'False' and message.text.lower() == '��':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    elif datas[4] == 'False' and message.text.lower() == '���':
        await bot.send_message(message.chat.id, '����������� ������� ����������')
        return
    else:
        if datas[4] == 'False' or message.text.lower() == '��' or sellall == True:
            with open(f'users/{message.chat.id}/temp.txt', 'r') as num:
                num = num.read().split()
            async with state.proxy() as data:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add('������', '����������', '�������', '����������',
                           '���������/�������� �������������', '������� ���������')
                with open(f'users/{message.chat.id}/income.txt', 'r') as income:
                    income = income.read().split()
                with open(f'users/{message.chat.id}/stock.txt', 'r') as stock:
                    stock = stock.read().split()
                if int(num[0]) <= int(num[1]):
                    stock[int(num[2])] = str(int(num[1]) - int(num[0]))
                    await bot.send_message(message.chat.id,
                                           f'�� ������� {str(data["num"])} ����� {str(data["stock"]).split()[1]}. �� ���� ' + str(
                                               data["stock"].split()[
                                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                                         f'������� �������� {str(int(income[1]) + int(data["num"]) * int(data["stock"].split()[3]))}',
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
                    markup.add('������', '����������', '�������', '����������',
                               '���������/�������� �������������', '������� ���������')
                    await bot.send_message(message.chat.id,
                                           '� ��� �� ������� �����, ������� ����������� ��� ���\n��� ������� '
                                           '"������" ��� �� '
                                           '�����', reply_markup=markup)

                return
    if message.text.lower() == '���':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('������', '����������', '�������', '����������', '���������/�������� �������������',
                   '������� ���������')
        await bot.send_message(message.chat.id, '�������� ��������', reply_markup=markup)
        await game.waitingGame.set()
        return
    with open(f'users/{message.chat.id}/income.txt', 'r') as income:
        income = income.read().split()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('��', '���')
    await bot.send_message(message.chat.id,
                           f'������ ������� {str(data["num"])} ����� {str(data["stock"]).split()[1]}. �� ���� ' + str(
                               data["stock"].split()[
                                   3]) + f' �� ����� {str(int(data["num"]) * int(data["stock"].split()[3]))}\n'
                                         f'������� �������� {str(int(income[1]) + int(data["num"]) * int(data["stock"].split()[3]))}\n��/��� (������� ����� ����� ��� ��� ���� ������ ������� ������ �����������)\n��� ��������� ����� ��������� ������� "���������/�������� �������������"',
                           reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)