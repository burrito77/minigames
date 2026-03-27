import chests
import random
from enum import IntEnum

class Player():

    #player values
    money = 100
    
    #percentage of income actually coming to the player account
    rawIncomePercent = 1

    
    #inventory

    #all together
    basicChests = 0
    ultraChests = 0
    premiumChests = 0


            
    class Effects(IntEnum):
        VIPPower = 0
        EnergyLevel = 1
        Exhaustion = 2
        DruggedLevel = 3
        DrunkLevel = 4
        GoldDiggerCount = 5
        NicotineLevel = 6
        CasinoThreatLevel = 7

    def increaseEffect(self, effect:Effects, amount = 1):
        self.effectValues[effect] += amount
    
    def clearEffect(self, effect:Effects):
        self.effectValues[effect] = 0

    #substract funds from player, if force = true it does so forcefully even through the limit
    #return false if there is negative amount of cash after transaction
    def subtractFunds(self, amount, force = False) -> bool:
        if force:
            self.money -= amount
            if self.money < 0:
                return False
        else:
            if self.money - amount < 0:
                return False
            else:
                self.money -= amount
                return True

    def addFunds(self, amount):
        self.money += amount * self.rawIncomePercent

    effectValues = [0,0,0,0,0,0,0,0]

    




