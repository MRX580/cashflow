import levels

def choiceLevel(num):
    if num == 1:
        return levels.Level(35, 5000, 4000, 50000)
    elif num == 2:
        return levels.Level(36, 5500, 4400, 60000)
    elif num == 3:
        return levels.Level(32, 6000, 4800, 70000)
    elif num == 4:
        return levels.Level(35, 6500, 5200, 80000)
    elif num == 5:
        return levels.Level(35, 7000, 5600, 90000)
    elif num == 6:
        return levels.Level(35, 7500, 6000, 100000)
    elif num == 7:
        return levels.Level(34, 8000, 6400, 120000)
    elif num == 8:
        return levels.Level(35, 8500, 6800, 140000)
    elif num == 9:
        return levels.Level(36, 9000, 7200, 160000)
    elif num == 10:
        return levels.Level(40, 9500, 7600, 180000)
    elif num == 11:
        return levels.Level(45, 10000, 8000, 200000)
    elif num == 12:
        return levels.Level(40, 11000, 8800, 225000)
    elif num == 13:
        return levels.Level(35, 12000, 9600, 250000)
    elif num == 14:
        return levels.Level(35, 13000, 10400, 275000)
    elif num == 15:
        return levels.Level(33, 14000, 11200, 300000)
    elif num == 16:
        return levels.Level(40, 15000, 12000, 350000)
    elif num == 17:
        return levels.Level(42, 16000, 12800, 400000)
    elif num == 18:
        return levels.Level(32, 17000, 13600, 450000)
    elif num == 19:
        return levels.Level(42, 18000, 14400, 500000)
    elif num == 20:
        return levels.Level(42, 19000, 15200, 550000)
    elif num == 21:
        return levels.Level(40, 20000, 16000, 600000)
    elif num == 22:
        return levels.Level(40, 22000, 17600, 650000)
    elif num == 23:
        return levels.Level(34, 25000, 20000, 700000)
    elif num == 24:
        return levels.Level(42, 25000, 20000, 750000)
    elif num == 25:
        return levels.Level(33, 28000, 22400, 800000)
    elif num == 26:
        return levels.Level(42, 30000, 24000, 850000)
    elif num == 27:
        return levels.Level(40, 33000, 26400, 900000)
    elif num == 28:
        return levels.Level(38, 36000, 28800, 950000)
    elif num == 29:
        return levels.Level(32, 39000, 31200, 1000000)
    elif num == 30:
        return levels.Level(42, 40000, 32000, 1100000)
choiceLevel(1)