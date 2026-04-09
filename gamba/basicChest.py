import chances
import random

#opens and returns just money value depending on chances and ranges
#chances are stored in chance, whereas ranges are stored in chest
cost = 10

ranges = [
    [0,4],
    [10,20],
    [20,50],
    [50,150],
    [300,1000],
    [20000,40000]
]

#completely new rewards for that one specific chance
def customizeRewards(chance:chances.Chance, lowestReward:int, highestReward):
    global ranges
    ranges[chance] = [lowestReward, highestReward]

#increase by percentage (any)
def increaseRewardsByPercentage(chance:chances.Chance, lowestRewardBy:float, highestRewardBy:float):
    global ranges
    ranges[chance] = [ranges[chance][0] * (1 + lowestRewardBy), ranges[chance][1] * (1 + highestRewardBy),]

#calculates how much you are expected to gain from this chest, cost is not deducted
def getExpectedWinPerChest() -> float:
    sum = 0
    for i in range(6):
       sum += chances.globalChances.getPercentage(i) * randomInRange(i, True)
    return sum

#return random value in specified range
#use half if you need just middle value
def randomInRange(chance:chances.Chance, half:bool) -> int:
    r = random.random()
    rng = ranges[chance]
    diff = rng[1] - rng[0]
    if half:
        return round(rng[0] + diff/2)
    randVal = round(r * diff)
    return rng[0] + randVal

#opens and returns how money have you won and of what rarity
def open() -> tuple[int, chances.Chance]:
    rarity = chances.globalChances.rollOne()
    return (randomInRange(rarity,False), rarity)

def openUltra():
    pass

def openPremium():
    pass