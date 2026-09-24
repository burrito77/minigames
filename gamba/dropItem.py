import player
from abc import ABC, abstractmethod
import random
import casino
import chances
import output



class DropItem(ABC):
    def __init__(self, name, description, chance):
            self.name = name
            self.description = description
            #in %
            self.chance = chance
    
    def try_drop_chance(self) -> bool:
        if random.random() < self.chance / 100 :
             return True
        return False
    
    @abstractmethod
    def _on_drop_(self):
        """Internal hook for item-specific effects."""
        pass
    
    @abstractmethod
    def onUpdate(self):
        pass

    @abstractmethod
    def onUse(self):
        pass
    
    @abstractmethod
    def onSell(self):
        pass

# reduce winnings in higher chance brackets, gain immunity against unfortunate events
class SecurityGuard(DropItem):
    def __init__(self):
        name="Security Guard"
        description="Casino assigns a supervisor to monitor your activity. Your winnings may decrease slightly, however your own security will improve."
        chance = 0.017
        self.reduceMythic = 100
        self.reduceElite = 100
        self.reduceLegendary = 50
        self.reduceEpic = 40
        self.reduceRare = 20
        self.reduceCommon = 10

    def _on_drop_(self):
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.COMMON, -self.reduceCommon/100, -self.reduceCommon/100)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.RARE, -self.reduceRare/100, -self.reduceRare/100)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.EPIC, -self.reduceEpic/100, -self.reduceEpic/100)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.LEGENDARY, -self.reduceLegendary/100, -self.reduceLegendary/100)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.ELITE, -self.reduceElite/100, -self.reduceElite/100)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.MYTHIC, -self.reduceMythic/100, -self.reduceMythic/100)
         

# increase game time, + add exhaustion 
class InstagramReels(DropItem):
    def __init__(self):
        name="Instagram Reels"
        description="You aquired access to the 'Instagram Reels' platform. Usage wastes a lot of time be careful."
        chance = 0.01
        self.roundSkip = 10000
        self.exhaustion = 10


class Grandma(DropItem):
    def __init__(self):
        name="Rich Grandma"
        description="Marry the rich old lady. Each round costs you mental health and healthcare money, however one day she might die and makes the wait worth."
        chance = 0.02
        self.deathChance = 0.5
        self.roundExhaustion = 0.1
        self.roundFee = 33
        self.win = 10000000
        
        
class ToiletMafia(DropItem):
    def __init__(self):
            name="Toilet Mafia"
            description="Make a deal with mafia. Increase your income altogether. Their terms are for you to complete your part."
            chance = 0.016
            self.needMoneyRound = 200
            self.needPremiumChestRound = 5
            self.needGoldDiggerRound = 2
            self.failMoney = 10000
            self.failExhaustion = 100
            self.failMultiplier = 0.5
            self.failChestCount = -50
            self.successMultiplier = 1.2

class Insurance(DropItem):
     def __init__(self):
          name="Insurance"
          chance = 0.04
          description=f"Pay for insurance and be safe just in case. Might be worth in the long run. Cancels automatically with payout. Must be paid regulary."
          self.dailyInsuranceRatio = 0.01
          self.payout = 0.6
                     
                              
        
class Portfolio(DropItem):
     def __init__(self):
               name="Stock portfolio"
               description=f"Invest all of your money into generic stock portfolio. Large risk of winning small and small risk of losing large"
               chance = 0.055
               self.winRange = [1.002, 1.016]
               self.loseChance = 1

class Jesus(DropItem):
     def __init__(self):
               name="A Miracle"
               description=f"Negates your bank account value."
               chance = 0.01

class Acid(DropItem):
     def __init__(self):
          name="Battery Acid"
          description=f"Completely burns all effects from your body"
          chance = 0.008

class Gun(DropItem):
     def __init__(self):
          name="Gun"
          description="With great power comes great jackpot"
          chance = 0.021
          self.basicChestStealChance = 12.5
          self.ultraChestStealChance = 1.75
          
               