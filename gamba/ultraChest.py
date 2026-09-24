import chances
import random
from enum import IntEnum

# ultra chests are only obtainable via 3 ways
# per VIP purchase
# per 1000 rounds
# with 'GUN' item


class Rewards(IntEnum):
    Money = 0
    Item = 1
    Multiplier = 2
    PremiumChest = 3
    EnviromentChange = 4
    

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