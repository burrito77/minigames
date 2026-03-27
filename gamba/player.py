import chests
import random
from enum import IntEnum
class Player():

    #player values
    money = 100


    #inventory

    #all together
    basicChests = 0
    ultraChests = 0
    premiumChests = 0

    #buys basic chest and appends to inventory
    #return 0 if no were bought
    #return -1 if insufficient funds
    #return 1 if success
    def buyBasicChest(self, amount) -> int:
        if amount < 1:
            return 0
        if amount * chests.BasicChest.cost > self.money:
            return -1
        for i in range(amount):
            self.money -= chests.BasicChest.cost
            self.basicChests += 1
        
        self.tryBonusChest(amount)

        return 1     

    
    #when you buy an amount of chests you may get bonus ones for free
    #this function gives you more chest into your inventory
    #returns how much chests you got
    def tryBonusChest(self, amount) -> int:
        r = random.random()
        if amount < 5:
            pass
        elif amount < 20 and r > 0.66:
            self.basicChests += 1
            return 1
        elif amount < 30 and r > 0.66:
            self.basicChests += 3
            return 3
        return 0
            
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

    effectValues = [0,0,0,0,0,0,0,0]

    




