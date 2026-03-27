import player
class Shop:
    served_player:player.Player = None
    def assignCustomer(self, _player):
        self.served_player = _player
        
    #warn the shop that the player has no funds
    def noFundsWarning(self):
        pass

globalShop = Shop()

class VIP:
    price = 250
    name = "Open Premium account"
    description = f"For just small price of {price}$* gain noticable gambling advantage\n* Fees excluded"
    vipRoundlyFee = 1


    def onBuy(self):
        

        globalShop.served_player.increaseEffect(globalShop.served_player.Effects.VIPPower)
        
    
    def onUpdate(self):
        globalShop.served_player.money -= self.vipRoundlyFee

    
    def onSell(self):

    