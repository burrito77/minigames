import player
from abc import ABC, abstractmethod
import random
import casino
import chances
import output



        
#warn the shop that the player has no funds
def noFundsWarning():
    pass

# --- Item Classes ---

class ShopItem(ABC):
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def buy(self):
        """The standard transaction logic for all items."""
        if player.subtractFunds(self.price):
            self._on_purchased() 
            return True
        else:
            noFundsWarning()
            return False

    @abstractmethod
    def _on_purchased(self):
        """Internal hook for item-specific effects."""
        pass

    @abstractmethod
    def onUpdate(self):
        pass

    @abstractmethod
    def onSell(self):
        pass

class VIP(ShopItem):
    def __init__(self):
        price = 250
        desc = f"For just small price of {price}$* gain noticeable gambling advantage\n* Fees excluded"
        super().__init__(name="Open Premium account", price=price, description=desc)
        self.vipRoundlyFee = 1

    #increase chances and price, decrease some of the costs
    def _on_purchased(self):
        player.increaseEffect(player.Effects.VIPPower)
        chances.globalChances.increaseByRaw(chances.Chance.RARE, 2.25)
        chances.globalChances.increaseByRaw(chances.Chance.EPIC, 0.78)
        chances.globalChances.increaseByRaw(chances.Chance.LEGENDARY, 0.39)
        chances.globalChances.increaseByRaw(chances.Chance.ELITE, 0.032)
        chances.globalChances.increaseByRaw(chances.Chance.MYTHIC, 0.001)
        self.price += 100 + self.price * 2
        casino.basicChest.cost -= 1
        vip.price += 0.1

    def onUpdate(self):
        player.subtractFunds(self.vipRoundlyFee, True)

    def onSell(self):
        pass

class ENERGY(ShopItem):
    def __init__(self):
        price = 4.99
        desc = "We know that gambling can be exhausting. Enjoy nice and cool white monster energy drink"
        super().__init__(name="Energy drink", price=price, description=desc)
        self.smallEnergyFee = 0
        self.largeEnergyFee = 0

    #increase energy fees and self price slighlty
    def _on_purchased(self):
        player.increaseEffect(player.Effects.EnergyLevel)
        self.price = self.price*1.15
        self.smallEnergyFee += 1
        self.largeEnergyFee += 3

    #if unlucky subtract energy fee
    def onUpdate(self):
        r = random.random()
        if r > 0.75:
            output.print_n("Small fee for overusage of energy drinks will be applied")
            player.subtractFunds(self.smallEnergyFee, True)
        if r > 0.92:
            output.print_n("Large fee for overusage of energy drinks will be applied")
            player.subtractFunds(self.largeEnergyFee, True)
        
    def onSell(self):
        pass

class VODKA(ShopItem):
    def __init__(self):
        price = 4.99
        self.power = 0
        desc = "Make your gambling moments more memorable with alcoholic beverage of your choosing"
        super().__init__(name="Alcoholic beverage", price=price, description=desc)
        
    #increase power of the item, power decides how much money player will get from vodka transaction
    #also decrease money from the basic chest chances
    def _on_purchased(self):
        player.increaseEffect(player.Effects.DrunkLevel)
        r = random.random()
        value = round(20 + r * 40 - self.power)
        output.print_n("You became somehow richer in your drunk state")
        player.addFunds(value)
        self.price+=10
        self.power+=5
        russian.price -= 20
        cigs.price *= 0.5
        energy.price *= 0.9

        #decrease winnings by a lot
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.COMMON, 0.5 - 1, 1 - 1)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.RARE, 0.75 - 1, 0.9 - 1)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.EPIC, 0.85 - 1, 0.95 - 1)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.LEGENDARY, 0.85 - 1, 0.85 - 1)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.ELITE, 0.65 - 1, 0.75 - 1)
        casino.basicChest.increaseRewardsByPercentage(chances.Chance.MYTHIC, 0.01 - 1, 0.02 - 1)
        
    def onUpdate(self):
        pass
        
    def onSell(self):
        pass

class CIGS(ShopItem):
    def __init__(self):
        price = 9.99
        self.power = 0.9
        self.fee = 2
        desc = "Tabacoo products are notoriously known for focus increase and stress relieve.\nThat is why we highly encourage this product for your gambling journey."
        super().__init__(name="Nicotine products", price=price, description=desc)
        
    #decrease chill aspect of the cigs and make it very expensive
    def _on_purchased(self):
        player.increaseEffect(player.Effects.NicotineLevel)
        #chill the player
        player.increaseEffect(player.Effects.Exhaustion, -self.power)
        self.price*=2.5
        self.power = self.power / 2
        self.fee += self.price / 2
        
    def onUpdate(self):
        r = random.random()
        if r > 0.95 :
            output.print_n("No smoking in casino!")
            player.subtractFunds(round(self.fee), True)
        
    def onSell(self):
        pass

class RUSSIAN(ShopItem):
    def __init__(self):
        price = 100
        self.chance = 6
        desc = "Game is a part of the gambling process. Go enjoy quick and simple game and relax a bit"
        super().__init__(name="Russian roulette", price=price, description=desc)
        
    def _on_purchased(self):
        r = random.randrange(0,5)
        if r == 0: 
            output.print_n("Lucky you...")
            player.die()
        
        if r == 1:
            output.print_n("You have won some reward")
            player.addFunds(200)

        if r == 2:
            output.print_n("Wow you just doubled your money")
            player.addFunds(player.money * 2)

        if r == 3:
            output.print_n("You have won some larger reward")
            player.addFunds(300)
        
        if r == 4:
            output.print_n("Aren't you just a lucky one")
            player.addFunds(50)

        if r == 5:
            output.print_n("You have won some medium reward")
            player.addFunds(250)

        self.price += 40

    def onUpdate(self):
       pass
        
    def onSell(self):
        pass

class DRUGS(ShopItem):
    def __init__(self):
        price = 999
        self.funny = 0
        self.fee = 50
        desc = "Altough illegal, still a great performance enhancer"
        super().__init__(name="Powder of happiness", price=price, description=desc)
        
    #increase all and delete common chance
    def _on_purchased(self):
        self.funny += 1
        self.price = self.price + self.price ** self.funny
        chances.globalChances.increaseByMultiplier(chances.Chance.COMMON, 0)
        chances.globalChances.increaseByRaw(chances.Chance.RARE, 50)
        chances.globalChances.increaseByRaw(chances.Chance.EPIC, 50)
        chances.globalChances.increaseByRaw(chances.Chance.LEGENDARY, 40)
        chances.globalChances.increaseByRaw(chances.Chance.ELITE, 20)
        chances.globalChances.increaseByRaw(chances.Chance.MYTHIC, 1)
        casino.basicChest.cost += 1
        
        self.fee += round(self.price/20)

    #slowly increase common, apply fee
    def onUpdate(self):
        chances.globalChances.increaseByRaw(chances.Chance.COMMON, 2 * self.funny)
        player.increaseEffect(player.Effects.Exhaustion, 0.1 * self.funny)
        player.subtractFunds(self.fee)
        
    def onSell(self):
        pass

class PROSTITUTE(ShopItem):
    def __init__(self):
        price = 2
        self.count = 0
        self.winAmount = 3.9
        self.winChance = 1
        self.roundPrice = 2

        desc = "Build yourself a gambling army\nBy using your army these girls can gamble you a huge income"
        super().__init__(name="Female companion", price=price, description=desc)
        
    #increase count both for status and item count
    def _on_purchased(self):
        self.count += 1
        player.increaseEffect(player.Effects.GoldDiggerCount)
        energy.smallEnergyFee += 1
        energy.largeEnergyFee += 3

    def onUpdate(self):
        for i in range(self.count):
            player.subtractFunds(self.roundPrice, True)
            player.addFunds(self.winAmount * random.random())
        
    def onSell(self):
        pass




# --- Module Instances ---
vip = VIP()
energy = ENERGY()
vodka = VODKA()
russian = RUSSIAN()
drugs = DRUGS()
cigs = CIGS()
prostitute = PROSTITUTE()