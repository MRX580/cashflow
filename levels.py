import math
import random

class Level:
    def __init__(self, moves, target, salary, expenses, money):
        self.moves = moves
        self.target = target
        self.zp = salary
        self.rasxodi = expenses
        self.money = money

    def vivod(self):
        
        print('У вас %s ходов ваша цель %s\nВаша зарплата %s, расходы %s\nВаш баланс %s' % (self.moves,self.target,self.zp,self.rasxodi,self.money))
    def level_1(self):
        level = 0



levelOne = Level(32, '100к', random.randint(10000,20000), 5000, 0)
levelOne.vivod()
