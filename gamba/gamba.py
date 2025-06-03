# open -> OTEVŘEŠ CHESTU
# open ultra -> OTEVŘEŠ ULTRA CHESTU
# shop -> KOUKNI SE NA NABÍDKU
# basic -> NAKOUPÍŠ JEDNU KLASICKOU TRUHLU
# basic 5 -> nakoupíš 5 chestek
# basic 20 -> nakoupíš 20 chestek
# ultra 2 -> nakoupíš 2 ultra chesty
# vip -> zakoupíš vip
# energy -> koupíš energy drink
# drugs -> koupíš si drogy
# vodka -> koupíš si vodku
# russian -> zkusíš své štěští v praxi
# bank -> podíváš se na svůj účet
# open all -> otevři vše na jednou (drahé a potřebuješ vip)
# borrow -> půjčíš si (nedoporučuji)





import math
import random
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import time


colorama_init()

money = 100

common = 72
rare = 20
epic = 5
legendary = 2.75
elite =  0.249
mythic = 0.001

totalSumChance = common + rare + epic + legendary + elite + mythic

commonRange = [0,4]
rareRange = [10,20]
epicRange = [20,50]
legendaryRange = [50,150]
eliteRange = [300,1000]
mythicRange = [20000,40000]

basicChest = 10
ultraChest = 25

vip = 250
energydrink = 4.99
vodkashot = 5
russianRoulete = 100
heroin = 999

basicChestCount=0
ultraChestCount=0
prostituteCount=0
vipactive=False
energydrinkactive=False
heroinActive = False

secondDelay = 10

drugfine = 50
energyfine = 2
vipmembership = 1


def wait():
    totalTime = random.random()*secondDelay
    r = random.randint(14,36)

    randomCols=[Fore.WHITE,Fore.GREEN,Fore.BLUE,Fore.YELLOW,Fore.RED,Fore.MAGENTA]

    for x in range(r):
        rx = random.randint(0,len(randomCols)-1)
        print(f"{randomCols[rx]}##")
        time.sleep(totalTime/r)
    print(Style.RESET_ALL)

def openBox():
    global money
    global totalSumChance
    total = 0
    r = random.random()
    totalSumChance = common + rare + epic + legendary + elite + mythic
    if r < common/totalSumChance:
        print("you won common rarity money")
        rcash = random.randint(commonRange[0],commonRange[1])
        money += rcash
        print(f"REWARD: {rcash}$")
        return
    total+=common
    if r < (common+rare)/totalSumChance:
        print(f"you won:{Fore.GREEN} RARE {Style.RESET_ALL}rarity money")
        rcash = random.randint(rareRange[0],rareRange[1])
        money += rcash
        print(f"REWARD: {Fore.GREEN}{rcash}{Style.RESET_ALL}$")
        return
    total+=rare
    if r < (common+rare+epic)/totalSumChance:
        print(f"{Fore.BLUE}YOU WON: [[__EPIC__]] RARITY MONEY{Style.RESET_ALL}")
        rcash = random.randint(epicRange[0],epicRange[1])
        money += rcash
        print(f"REWARD: {Fore.BLUE}{rcash}{Style.RESET_ALL}$")
        return
    total+=epic
    if r < (common+rare+epic+legendary)/totalSumChance:
        print(F"{Fore.YELLOW}********** YOU WON: ###[LEGENDARY]### RARITY MONEY ********")
        print(f"********** YOU WON: ###[LEGENDARY]### RARITY MONEY ********")
        print(f"********** YOU WON: ###[LEGENDARY]### RARITY MONEY ********")
        print(f"*************************JACKPOT***************************")
        rcash = random.randint(50,150)
        money += rcash
        print(f"REWARD: {rcash}{Style.RESET_ALL}")
        return
    total+=legendary
    if r < (common+rare+epic+legendary+elite)/totalSumChance:
        print(f"{Fore.RED}**ELITE WINNINGS**")
        rcash = random.randint(eliteRange[0],eliteRange[1])
        money += rcash
        print(f"REWARD: {rcash}{Style.RESET_ALL}$")
        return
    total+=elite
    if r <= (common+rare+epic+legendary+elite+mythic)/totalSumChance:
        print(f"{Fore.MAGENTA}mythical...")
        rcash = random.randint(mythicRange[0],mythicRange[1])
        money += rcash
        time.sleep(2)
        print(f"REWARD: {rcash}$")
        return

def openUltraBox():
    global money
    r = random.randint(-190,200)
    print(f"{Fore.CYAN}congratulations you have won {r}${Style.RESET_ALL}")
    money+=r

borrowLimit = 31
totalWinnings = 0
round = 0
funny = 1
while True:
    round += 1
    for x in range(prostituteCount):
        r = (random.random() - 0.495)*2
        #more you pay at the shop, the more you win
        moneytowin = r * (money/100)
        #print(f"your girl has gambled your money and won {moneytowin} and costed you 2$")
        money-=2
        money+=moneytowin

    if money<=0 and basicChestCount <= 0 and ultraChestCount <= 0:
        print(f"one golddigger has left you, you have {prostituteCount} left")
        prostituteCount-=1

    if(heroinActive):
        money = money - heroin/1000
        common+=heroin/1000
        secondDelay += 0.05
        basicChest+=1
        ultraChest+=1
        #money-=1/(1000-round) * money

    if(vipactive):
        r = random.randint(0,5)
        if(r==3):
            print(f"{vipmembership}$ have been substracted from your account")
            money=money-vipmembership
    if(energydrinkactive):
        r = random.randint(0,20)
        if(r==3):
            print(f"{energyfine*2} have been substracted from your account due to excessive energy drink consumption")
            money=money-energyfine*2
        if(r>18):
            print(f"a energy drink fee will be substracted from your account [{energyfine}]")
            money=money-energyfine
    if(heroinActive):
            print("fine for using drugs has been substracted from your account")
            money=money-drugfine
    
            
    money=money - (31-borrowLimit)/10
    if money<=0 and basicChestCount<=0 and ultraChestCount <=0 and prostituteCount <=0:
        print("you have gone bankrupt")
        print(f"you survived to round {round}")
        exit()
    
    command = input()
    #command ="open"
    if command=="open":
        if basicChestCount<1:
            print("not enough chests")
            
        else:
            print("--------------------------------")
            print("opening....")
            wait()
            openBox()
            basicChestCount-=1
            print("--------------------------------")

    if command=="open ultra":
        if ultraChestCount < 1:
            print("not enough ultra chests")
        else:
            print("--------------------------------")
            print("opening ULTRA CHEST....")
            wait()
            openUltraBox()
            ultraChestCount-=1
            print("--------------------------------")
    if command=="bank":
        print(f"good job! current balance on your account is: {money}$")
        print("keep on gambling")
        print(f"you have {basicChestCount} basic chests and {ultraChestCount} ultra chests")
        print(f"vip: {vipactive}")
        print(f"energy drink: {energydrinkactive}")
        print(f"drugged: {heroinActive}")
    if command=="shop":
        print(f"BASIC CHEST ..... {basicChest}$ (GOOD FOR GAMBLING ENTHUSIAST WHO WANT TO QUICKLY GAIN A BIT OF MONEY)")
        print(f"ULTRA CHEST ..... {ultraChest}$ (Optimal for gambling professionals, who are not afraid of any risks)")
        print(f"---------------------")
        print(f"VIP .................. {vip}$ (enables you to outwin the competition, highly recommended)")
        print(f"Energy drink ......... {energydrink}$ (win faster than your opponents, just dont drink too much - its not healthy)")
        print(f"vodka shot ........... {vodkashot}$ (situation too tense? relax for a while with some good ol' vodka. Be careful when drunk!!!)")
        print(f"russian roulette ..... {russianRoulete}$ (5 in 6 chance you will gain easy money. Recommended for beginners)")
        print(f"drugs ................ {heroin}$ (even the best gamblers sometimes have to take edge off, highly addictive!!!)")
        print(f"BORROW {borrowLimit+4}$ ....... *free, but casino will make sure it has the money back")
        print(f"OPEN ALL COMMAND ..... 50$ -> opens all of your chests without any delay, VIP is required")
        print(f"Prostitute ........... 2$/action/prostitute (Luck in the game EQUALS luck in the love)")
        print("------------------------------------")
    if command=="basic":
        if money>=10:
            basicChestCount+=1
            money-=10
            print("thank you for buying basic chest")
        else:
            print("not enough money")
    if command=="basic 5":
        if money>=basicChest*5:
            print("thank you for buying 5 basic chests")
            r = random.randint(0,5)
            if r==1:
                basicChestCount+=1
                print("congratulations, we are giving you free chest")
            money-=basicChest*5
            basicChestCount+=5
        else:
            print("not enough money")
    if command=="basic 20":
        if money>=basicChest*20:
            print("thank you for buying 20 basic chests")
            r = random.randint(0,1)
            if r==1:
                basicChestCount+=3
                print("congratulations, we are giving you three free chests")
            money-=basicChest*20
            basicChestCount+=20
        else:
            print("not enough money")
    if command=="ultra 2":
        if money>=ultraChest*2:
            print("thank you for buying 2 ultra chests")
            money-=ultraChest*2
            ultraChestCount+=2
        else:
            print("not enough money")
    if command=="vip":
        if money>=vip:
            print("buying vip + 1 ultra chest as a gift")
            ultraChestCount+=1
            money-=vip
            vipactive=True
            secondDelay*=0.94
            
            #chacnes
            rare+=2
            epic+=0.7
            legendary+=0.4
            elite+=0.03
            mythic = mythic*1.5
            vip+=100+vip*2

            #prices
            basicChest-=1
            ultraChest-=1
            energydrink-=2
            vodkashot-=2
            russianRoulete-=40


        else:
            print("not enough money")
    if command=="energy":
        if(money>=energydrink):
            print("buying energy drink")
            basicChestCount+=1
            energydrinkactive=True
            secondDelay = secondDelay*0.9
            money-=energydrink
            energydrink = max(math.ceil(energydrink/(secondDelay/10)),1)
        else:
            print("not enough money")
    if command=="borrow":
        print("transaction complete")
        money+=borrowLimit
        borrowLimit-=11
        common+=12
        rare-=6
        epic-=4
        legendary-=2
    if command=="open all":
        if vipactive==False:
            "please pay for VIP first"
        else:
            print("substracting 50$ from your account")
            money = money-50
            totalWinnings=0
            for x in range(basicChestCount):
                basicChestCount-=1
                oldmoney=money
                openBox()
                newmoney=money
                totalWinnings+=newmoney-oldmoney-10
            print(f"total winnings: {totalWinnings}$. congratulations")
            print(f"a 0.5% fee will be substracted from your account")
            money = money*0.995
    if command=="xd":
        money = 300
    if command=="vodka":
        if money>=vodkashot:
            print("you drank shot of vodka")
            money-=vodkashot
            r = random.randint(0,int(50-(vodkashot/5)))
            print(f"you are drunk and do not remember how you got {r}$ into your bank account, but hey it definitevely wont have any side effects")
            vodkashot+=10
            money += r
            commonRange[0] -= 1
            commonRange[1] -= 0
            rareRange[0] -= 1
            rareRange[1] -= 1
            epicRange[0] -= 2
            epicRange[1] -= 2
            legendaryRange[0] -= 4
            legendaryRange[1] -= 4
            eliteRange[0] -= 7
            eliteRange[1] -= 7
            mythicRange[0] = -40000
            russianRoulete-=30
        else:
            print("not enough money")       
    if command == "russian":
        if money>= russianRoulete:
            r = random.randint(1,6)
            if(r==6):
                print("you died")
                exit()
            if(r==5):
                print("you have won 200$")
                money=money+200
            if(r==4):
                print("you have tripled your money")
                money=money*3
            if(r==3):
                print("you have won 300$")
                money=money+300
            if(r==2):
                print("you have doubled your money")
                money=money*2
            if(r==1):
                print("congratulations you have won 50$")
                money=money+50

            money-=russianRoulete
            russianRoulete+=30

        else:
            print ("sorry you are out of money")
    if command =="drugs":
        if money>=heroin:
            print("you took cocain")
            print(f"{Fore.GREEN}everything{Fore.CYAN} is{Fore.BLUE} more{Fore.MAGENTA} colorful{Fore.RED} now{Fore.YELLOW},{Fore.GREEN} shall{Fore.CYAN} we{Fore.BLUE} gamble?{Style.RESET_ALL}")
            common=0
            rare+=20
            epic+=20
            legendary+=20
            elite+=20
            mythic+=1
            heroin = heroin * 3**funny
            funny+=1
            heroinActive = True
            secondDelay = 0.5
            basicChest-=3
            ultraChest-=10
            vodkashot-=30
        else:
            print("not enough money")
    if command=="prostitute":
        if money<0:
            print("do not think about it with your money")
        else:
            print("enjoy your new girl")
            drugfine+=125
            vipmembership+=7*prostituteCount
            energyfine+=2
            prostituteCount+=1
    if command=="sell":
        print("selling house, car, child, wife")
        print("+1000$")
        money=money+1000
        energydrinkactive=True
        heroinActive=True
        vipactive=True