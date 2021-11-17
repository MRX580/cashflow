import random
class level:
    def __init__(self, moves, target, salary, expenses, money):
        self.moves = moves
        self.target = target
        self.zp = salary
        self.rasxodi = expenses
        self.money = money
    def vivod(self):
        print('У вас %s ходов ваша цель %s\nВаша зарплата %s, расходы %s\nВаш баланс %s' % (self.moves,self.target,self.zp,self.rasxodi,self.money))

levelOne = level(32, '100к', 10000, 5000, 0)
levelOne.vivod()