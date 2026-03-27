import shop
import Player
import chances
import chests

basicChest = chests.BasicChest()
player = Player.Player()

if player.basicChests > 0:
    am, rr = basicChest.open()
    player.addFunds(am)