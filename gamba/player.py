
from enum import IntEnum
import output
import shop
import sys

# --- Player Values ---
money = 100
rawIncomePercent = 1.0
openWait = 11

# --- Inventory ---
basicChests = 20
ultraChests = 0
premiumChests = 0

# --- Effects System ---
class Effects(IntEnum):
    VIPPower = 0
    EnergyLevel = 1
    Exhaustion = 2
    DruggedLevel = 3
    DrunkLevel = 4
    GoldDiggerCount = 5
    NicotineLevel = 6
    CasinoThreatLevel = 7

# Initialize the list with zeros for each effect
effectValues = [0] * len(Effects)

# --- Functions ---

def increaseEffect(effect: Effects, amount=1):
    global effectValues
    global openWait
    
    effectValues[effect] += amount

    if effect == Effects.NicotineLevel:
         openWait = 11/(effectValues[effectValues]/20 + 1)

def clearEffect(effect: Effects):
    global effectValues
    effectValues[effect] = 0

def subtractFunds(amount, force=False) -> bool:
    global money
    if force:
        money -= amount
        output.dPrint(f"Substracted {amount}$ from player's account")
        return money >= 0
    else:
        if money - amount < 0:
            return False
        money -= amount
        output.dPrint(f"Substracted {amount}$ from player's account")
        return True

def addFunds(amount):
    global money
    money += amount * rawIncomePercent
    output.dPrint(f"Added {amount * rawIncomePercent}$ into player's account")

def onRound():
    if effectValues[Effects.VIPPower] > 0:
        shop.vip.onUpdate()

    if effectValues[Effects.NicotineLevel] > 0:
        shop.cigs.onUpdate()

    if effectValues[Effects.DruggedLevel] > 0:
        shop.drugs.onUpdate()
    
    if effectValues[Effects.EnergyLevel] > 0:
        shop.energy.onUpdate()

    if effectValues[Effects.DrunkLevel] > 0:
        shop.vodka.onUpdate()

    if effectValues[Effects.GoldDiggerCount] > 0:
        shop.prostitute.onUpdate()

#tries to die the player
def die():
    sys.exit()