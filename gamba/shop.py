import Player
from abc import ABC, abstractmethod
import random

class Shop:
    served_player:Player.Player = None
    def assignCustomer(self, _player):
        self.served_player = _player
        
    #warn the shop that the player has no funds
    def noFundsWarning(self):
        pass

globalShop = Shop()


class ShopItem(ABC):
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def buy(self):
        """The standard transaction logic for all items."""
        if globalShop.served_player.subtractFunds(self.price):
            self._on_purchased() 
            return True
        else:
            globalShop.noFundsWarning()
            return False

    @abstractmethod
    def _on_purchased(self):
        """Internal hook for item-specific effects."""
        pass

    @abstractmethod
    def onUpdate(self, player):
        pass

    @abstractmethod
    def onSell(self, player):
        pass

class VIP(ShopItem):
    def __init__(self):
        price = 250
        desc = f"For just small price of {price}$* gain noticeable gambling advantage\n* Fees excluded"
        super().__init__(name="Open Premium account", price=price, description=desc)
        self.vipRoundlyFee = 1

    def _on_purchased(self):
        globalShop.served_player.increaseEffect(globalShop.served_player.Effects.VIPPower)

    def onUpdate(self):
        globalShop.served_player.subtractFunds(self.vipRoundlyFee, True)

    def onSell(self):
        pass

class ENERGY(ShopItem):
    def __init__(self):
        price = 4.99
        desc = f"We know that gambling can be exhausting. Enjoy nice and cool white monster energy drink"
        super().__init__(name="Energy drink", price=price, description=desc)
        self.smallEnergyFee = 0
        self.largeEnergyFee = 0

    def _on_purchased(self):
        globalShop.served_player.increaseEffect(globalShop.served_player.Effects.EnergyLevel)
        price = price*1.15
        self.smallEnergyFee += 1
        self.largeEnergyFee += 3

    def onUpdate(self):
        r = random.random()
        if r > 0.75:
            globalShop.served_player.subtractFunds(self.smallEnergyFee, True)
        if r > 0.92:
            globalShop.served_player.subtractFunds(self.largeEnergyFee, True)
        

    def onSell(self):
        pass

class VODKA(ShopItem):
    def __init__(self):
        price = 4.99
        self.power = 0
        desc = f"Make your gambling moments more memorable with alcoholic beverage of your choosing"
        super().__init__(name="Alcoholic beverage", price=price, description=desc)
        

    def _on_purchased(self):
        globalShop.served_player.increaseEffect(globalShop.served_player.Effects.DrunkLevel)
        r = random.random()
        value = round(20 + r * 40 - self.power)
        globalShop.served_player.addFunds(value)
        price+=10
        self.power+=5

    def onUpdate(self):
        pass
        

    def onSell(self):
        pass