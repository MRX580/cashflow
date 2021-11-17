class level:
    def __init__(self, moves, target, salary, expenses):
        self.moves = moves
        self.target = target
        self.zp = salary
        self.rasxodi = expenses
    def vivod(self):
        print('У вас %s ходов ваша цель %s\nВаша зарплата %s, расходы %s' % (self.moves,self.target,self.zp,self.rasxodi))

levelOne = level(32, '100к', 10000, 5000)

levelOne.vivod()