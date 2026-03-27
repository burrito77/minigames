from enum import IntEnum
import random
import copy

#enumerate id
class Chance(IntEnum):
        COMMON = 0
        RARE = 1
        EPIC = 2
        LEGENDARY = 3
        ELITE = 4
        MYTHIC = 5

#class of all the total chances, and util functions
class GameChances():
    _chances = [72,20,5,2.75,0.249,0.001]
    
    #get current value of your specified chance
    def getRaw(self, chance:Chance):
          return self._chances[chance]
    
    #get real % of your chance, returns chance as 0-1
    def getPercentage(self, chance:Chance):
          return self._chances[chance] / sum(self._chances)

    #set what should be the final chance of specified chance, this WILL change percentage of the other values, ofc
    #percentage must be between 0 - 1
    def setToPercent(self, chance, percentage):
        if percentage == 0:
              for i in len(self._chances):
                  if i == chance:
                        self._chances[i] = 1
                  else:
                        self._chances[i] = 0

        if percentage < 0 or percentage > 1:
              return
        self._chances[chance] = percentage * (sum(self._chances) - self._chances[chance]) / (1 - percentage) 
    
    #set your specified chance with set += suppliedParam, may be negative thus substracting
    #raw chance can never be negative even after suppliing -suppliedParam negative
    def increaseByRaw(self, chance, value):
          self._chances[chance] += value
          self._chances[chance] = max(0, self._chances[chance])

    #percentageIncrease must be (-1, infinite), increases raw value by x percent
    def increaseByMultiplier(self, chance, percentageIncrease):
          if percentageIncrease < -1:
                return
          self._chances[chance] = self._chances[chance] * (1 + percentageIncrease)
    
    #rolls one chance randomly, returns chance enum
    def rollOne(self) -> Chance:
          r = random.random()
          cursum = 0
          for i in range(len(self._chances)):
                cursum+=self._chances[i]
                if r * sum(self._chances) <= cursum:
                      return i
    
    #print many iterations
    def test(self, iterations):
          for i in range(iterations):
                c = self.rollOne()
                print("Rolled: " + c)
    
    def getBackup(self) -> list:
         return copy.deepcopy(self._chances)
          
    def load(self, chances:list):
        self._chances = chances
          
#### THIS ONE IS THE GLOBAL REFERENCE TO CHANCES ####
globalChances = GameChances()
