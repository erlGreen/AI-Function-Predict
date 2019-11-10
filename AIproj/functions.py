import pandas as pd
def getData(file):
    df = pd.read_csv(file)
    values = df["Zamkniecie"]
    return values

def EMA(samples, currentDay, numberOfDays):
    a = 0.0 #licznik
    b = 0.0 #mianownik
    oneMinusAlfa = 1 - (2 / (numberOfDays + 1))
    for i in range(0, numberOfDays + 1, 1):
        component = oneMinusAlfa**i
        if (currentDay >= i):
            a += component * samples[currentDay - i]
        else:
            a += component * samples[0]
        b += component
    return a / b

def MACD(samples, currentDay):
    return EMA(samples, currentDay, 12) - EMA(samples, currentDay, 26)


def SIGNAL(samples, currentDay):
    return EMA(samples, currentDay, 9)


def Sell(money, nrOfActions, actionValue):
    money += nrOfActions * actionValue
    return money, 0


def Buy(money, nrOfActions, actionValue):
    while money >= actionValue:
        nrOfActions += 1
        money -= actionValue
    return money, nrOfActions

