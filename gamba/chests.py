import chances
import random

class Chest:
    def open(self):
        raise NotImplementedError("Subclasses must implement this method")

#opens and returns just money value depending on chances and ranges
#chances are stored in chance, whereas ranges are stored in chest
class BasicChest:

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
    def customizeRewards(self, chance:chances.Chance, lowestReward:int, highestReward):
        self.ranges[chance] = [lowestReward, highestReward]
    
    #increase by percentage (any)
    def increaseRewardsByPercentage(self, chance:chances.Chance, lowestRewardBy:float, highestRewardBy:float):
        self.ranges[chance] = [self.ranges[chance][0] * (1 + lowestRewardBy), self.ranges[chance][1] * (1 + highestRewardBy),]

    #calculates how much you are expected to gain from this chest, cost is not deducted
    def getExpectedWinPerChest(self) -> float:
        sum = 0
        for i in range(len(6)):
           sum += chances.globalChances.getPercentage(i) * self.randomInRange(i)
        return sum
    
    #return random value in specified range
    #use half if you need just middle value
    def randomInRange(self, chance:chances.Chance, half:bool) -> int:
        r = random.random()
        range = self.ranges[chance]
        diff = range[1] - range[0]
        if half:
            return round(range[0] + diff/2)
        randVal = round(r * diff)
        return range[0] + randVal


    #opens and returns how money have you won and of what rarity
    def open(self) -> tuple[int, chances.Chance]:
        rarity = chances.globalChances.rollOne()
        return (self.randomInRange(rarity,False), rarity)

class UltraChest:
    def open(self):
        pass

class PremiumChest:
    def open(self):
        pass