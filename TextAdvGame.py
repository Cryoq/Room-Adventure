##################################################################################
# Name: Alan Dreher
# Date: 1/09/24
# Description: A dungeon, text adventure game where you get you fight enemies, explore, and fight the final boss to beat the game.
#################################################################################

import random, os, time

# Just cleared the screen
CLEAR = lambda: os.system('cls')

# A random number generator that inputs a max number and the % change per interval
def randomNum(end: int, chance: int, guarentee = False):
    # if guarentee is true, there is always atleast 2 enemies
    if guarentee:
        x = 2
    else:
        x = 0
    for i in range(end):
        num = random.randint(0,100)
        if num > chance:
            return i + x
        elif num <= chance:
            pass
    return end + x

# The weapon class for the weapon list in the room class
class weapon:
    def __init__(self, atk, name) -> None:
        self.atk = atk
        self.name = name
        
    @property
    def atk(self):
        return self._atk
    @atk.setter
    def atk(self, attack):
        self._atk = attack

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, newName):
        self._name = newName

# Creates all the weapons using the weapons class and returns it as a list of objects
def createWeapons():
    gloves = weapon(3, "pair of Gloves")
    kitchenKnife = weapon(5, "Kitchen Knife")
    dagger = weapon(8, "Dagger")
    sword = weapon(12, "Sword")
    katana = weapon(15, "Katana")
    
    weaponList = [gloves, kitchenKnife, dagger, sword, katana]
    return weaponList

# Super class that both enemies and the main character shares, hp, atk, and name  
class character:
    def __init__(self, hp: int, atk: int, lvl: int, Name = None) -> None:
        self.hp = hp
        self.atk = atk
        self.lvl = lvl
        self.Name = Name
        self.isAlive = True
    
    @property
    def isAlive(self):
        return self._isAlive
    @isAlive.setter
    def isAlive(self, alive):
        self._isAlive = alive
        
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, nHp):
        self._hp = nHp

    @property
    def atk(self):
        return self._atk
    @atk.setter
    def atk(self, nAtk):
        self._atk = nAtk

    @property
    def lvl(self):
        return self._lvl
    @lvl.setter
    def lvl(self, nLvl):
        self._lvl = nLvl

    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, nName):
        self._Name = nName
        
    def __str__(self):
        return self._Name
    
    # attack move
    def attack(self, defender):
        defender.hp -= self.atk
        # calls every time when there is an attack on the defender
        defender.ifDead()
        
    # checks if self is dead
    def ifDead(self):
        if self.hp <= 0:
            self.isAlive = False

# child class of character
class enemy(character):
    def __init__(self, hp, atk, lvl, Name, xp) -> None:
        super().__init__(hp, atk, lvl, Name)
        self.xp = xp
    
# chuld class of character
class human(character):
    def __init__(self, hp, atk, lvl, Name) -> None:
        super().__init__(hp, atk, lvl, Name)
        self.weaponInventory = []
        self.potionInventory = 0
        self.maxHp = hp
        # sets the current weapon as fists, which does 0 atk
        self.currentWeapon = weapon(0, "fists")

    @property
    def currentWeapon(self):
        return self._currentWeapon
    @currentWeapon.setter
    def currentWeapon(self, weapon):
        self._currentWeapon = weapon
        
    @property
    def maxHp(self):
        return self._maxHp
    @maxHp.setter
    def maxHp(self, hp):
        self._maxHp = hp
         
    @property
    def weaponInventory(self):
        return self._weaponInventory
    @weaponInventory.setter
    def weaponInventory(self, addItem):
        self._weaponInventory = addItem
        
    @property
    def potionInventory(self):
        return self._potionInventory
    @potionInventory.setter
    def potionInventory(self, addItem):
        self._potionInventory = addItem
        
    # prints inventory when called
    def printInventory(self):
        for i,v in enumerate(self._weaponInventory):
            print(f"{i + 1}: {v.name}\tatk: {v.atk}")
        self.printPotions()
        
    # prints potions
    def printPotions(self):
        print(f"You have {self.potionInventory} potion in your inventory!")
        
    # uses potions
    def usePotion(self):
        # checks if the user has more than 0 potions, else returns false as a potion cannot be used
        if self.potionInventory != 0:
            self.potionInventory -= 1
            self._hp += self._maxHp / 2
            return True
        else:
            print("You have no potions.")
            return False
    
    # equips a new weapon on call
    def equipWeapon(self):
        print("What weapon would you like to equip?\n")
        for i,v in enumerate(self._weaponInventory):
            print(f"{i + 1}: {v.name}\tatk: {v.atk}")
        userInput = int(input(""))
        userInput -= 1
        # changes atk back to before with fists, then adds the new weapon atk
        self._atk -= self._currentWeapon.atk
        self._currentWeapon = self._weaponInventory[userInput]
        self._atk += self._currentWeapon.atk
        CLEAR()
        print(f"You equiped a {self._currentWeapon.name}")
        time.sleep(2)
        CLEAR()
        
# function that creates all enemies, inputs it into a list and returns a random enemy within that list using the random module
def createEnemies():
    Zombie = enemy(35, 5, 1, "Zombie", 10)
    Skeleton = enemy(20, 8, 1, "Skeleon", 10)
    ZombieTank = enemy(45, 3, 1, "Zombie Tank", 10)
    enemies = [Zombie, Skeleton, ZombieTank]
    
    return random.choice(enemies)

# Main room class
class room:
    totalEnemies = 3
    weaponList = createWeapons()
    def __init__(self, numOfEnemies = 1, isBoss = False, isPuzzle = False, chestRarity = 0) -> None:
        self.enemiesOnFloor = []
        self.isBoss = isBoss
        
        # determines what the best item you can get per room
        self.chestRarity = chestRarity
        self.isPuzzle = isPuzzle
        self.numOfEnemies = numOfEnemies
        self.exits = {}
        self.enemiescleared = False
        
        # Checks if there are enemies when the roomed is created, if not, there is no chests that spawn
        if numOfEnemies == 0:
            self.chestSearched = True
        else:
            self.chestSearched = False
        

    @property
    def chestSearched(self):
        return self._chestSearched
    @chestSearched.setter
    def chestSearched(self, chestBool):
        self._chestSearched = chestBool
        
    @property
    def enemiescleared(self):
        return self._enemiescleared
    @enemiescleared.setter
    def enemiescleared(self, enemiesbool):
        self._enemiescleared = enemiesbool
        
    @property
    def chestRarity(self):
        return self._chestRarity
    @chestRarity.setter
    def chestRarity(self, changeChestRarity):
        self._chestRarity = changeChestRarity
    
    @property
    def isPuzzle(self):
        return self._isPuzzle
    @isPuzzle.setter
    def isPuzzle(self, puzzleBool):
        self._isPuzzle = puzzleBool
        
    @property
    def isBoss(self):
        return self._isBoss
    @isBoss.setter
    def isBoss(self, bossBool):
        self._isBoss = bossBool
        
    @property
    def exits(self):
        return self._exits
    @exits.setter
    def exits(self, newExits):
        self._exits = newExits
        
    @property
    def enemiesOnFloor(self):
        return self._enemiesOnFloor
    @enemiesOnFloor.setter
    def enemiesOnFloor(self, newEnemy):
        self._enemiesOnFloor = newEnemy
    
    @property
    def numOfEnemies(self):
        return self._numOfEnemies
    @numOfEnemies.setter
    def numOfEnemies(self, newNum):
        self._numOfEnemies = newNum
        
        # Checks if its the boss room, if so, it summons the boss and only the boss in the room
        if self._isBoss:
            self.enemiesOnFloor.append(enemy(100, 8, 1, "livid", 0))
        else:
            # gets the number of enemies that is randomly generated and calls the createEnemies function that many times and appends
            for _ in range(self._numOfEnemies):
                self._enemiesOnFloor.append(createEnemies())
        
    # sets all exits (as a dictionary)
    def setExits(self, exits):
        self._exits = exits
        
    # clears room by setting enemies to none
    def clearedRoom(self):
        self._numOfEnemies = 0
        self._enemiesOnFloor = []
        
        # if its the boss room, you beat the game
        if self._isBoss:
            print("CONGRATS!!! YOU HAVE BEATEN THE GAME!")
            time.sleep(5)
            exit()
    
    # Opens the chest when the room is cleared and the user types "search chest"
    def openChest(self):
        # calls the chest class
        roomChest = chest(room.weaponList, self._chestRarity)
        roomLoot, roomPotion = roomChest.chestLoot()
        roomLoot = room.weaponList[roomLoot]
        return roomLoot, roomPotion
        
    def __str__(self):
        s = ''
        # if no enemies are present this is called
        if self._numOfEnemies == 0:
            self._enemiescleared = True
            s += "There are no enemies on this floor.\n"
            s += "You can go: "
            for _,v in enumerate(self._exits):
                s += v + ' '
        # if there is atleast 1 enemy present, this segment is called
        else:
            # called when there is 1 (because 2+ is pluar and 1 isnt)
            if self._numOfEnemies == 1:
                s += "There is 1 enemy in this room\n"
            # called when there is 2+ enemies
            else:
                s += f"There are {str(self._numOfEnemies)} enemies in this room.\n"
            s += "There is a: "
            for _,v in enumerate(self._enemiesOnFloor):
                s += v.Name + ', '
        return s
    
# The chest class that determins the loot in each floor
class chest:
    def __init__(self,loot,rarity) -> None:
        self.loot = loot
        self.rarity = rarity
        
    @property
    def loot(self):
        return self._loot
    @loot.setter
    def loot(self, newLoot):
        self._loot = newLoot
        
    @property
    def rarity(self):
        return self._rarity
    @rarity.setter
    def rarity(self, changeRarity):
        self._rarity = changeRarity
        
    # The chest loot function that determins the loot in each floor
    def chestLoot(self):
        # generates a random number given from self.rarity and there is a 50 precent chance of it being it, starting from 0
        loot = randomNum(self._rarity, 50)
        # 35 % chance of each chest containing a potion
        potion = randomNum(1, 35)
        return loot, potion

# main battle function
def battle(enemies: list[object], user: object):
    global currentRoom
    fighting = True
    aliveEnemies = enemies
    moved = False
    while fighting:
        while not moved:
            CLEAR()
            print(f"Your hp: {user.hp}")
            for i,v in enumerate(aliveEnemies):
                print(f"{i+1}: {v.Name} HP: {v.hp}")
            print("")
            user.printPotions()
            move = input('Would you like to use a potion or attack? ("potion", "attack") ')
            move.lower()
            if move == "potion":
                CLEAR()
                usePotion = user.usePotion()
                if usePotion:
                    moved = True
            elif move == "attack":
                CLEAR()
                print(f"Your hp: {user.hp}")
                for i,v in enumerate(aliveEnemies):
                    print(f"{i+1}: {v.Name} HP: {v.hp}")
                print("\nWho would you like to attack? ")
                userInput = int(input(" "))
                userInput -= 1
                for i,v in enumerate(aliveEnemies):
                    if userInput == i:
                        CLEAR()
                        print(f"You attacked {v.Name} for {user.atk} damage")
                        time.sleep(2)
                        user.attack(aliveEnemies[i])
                        moved = True
            else:
                print("You cannot do that command.")
        CLEAR()
        enemies = aliveEnemies
        aliveEnemies = []
        for _,v in enumerate(enemies):
            if v.isAlive:
                aliveEnemies.append(v)
        if len(aliveEnemies) == 0:
            fighting = False
        else:
            enemyMove = random.choice(aliveEnemies)
            enemyMove.attack(user)
            print(f"{enemyMove.Name} has hit you for {enemyMove.atk} damage")
            time.sleep(2)
            moved = False
            if not user.isAlive:
                print("You have died...\nGAME OVER")
                exit()
    CLEAR()
    print("You defeated all the enemies on this floor!")
    time.sleep(2)
    CLEAR()
    print("A chest has spawned in this room!!!")    

# Creates all the rooms for the game
def createRooms():
    
    # first argument gives the number of enemies spawned in the rooms and 2nd determins the best item avaliable per room
    r1 = room(0)
    r2 = room(randomNum(2,50))
    r3 = room(randomNum(2,50), chestRarity=1)
    r4 = room(1, chestRarity=2)
    r5 = room(randomNum(2,75,True), chestRarity=2)
    r6 = room(randomNum(2,50), chestRarity=1)
    r7 = room(randomNum(2,75,True), chestRarity=3)
    r8 = room(1, chestRarity=3)
    r9 = room(randomNum(2,75,True), chestRarity=3)
    r10 = room(1, chestRarity=4)
    r11 = room(randomNum(2,50), chestRarity=4)
    r12 = room(0)
    r13 = room(isBoss=True)

    # sets exits, uses dictionaries
    r1.setExits({"North": r2})
    r2.setExits({"North": r5, "South": r1, "West": r3})
    r3.setExits({"East": r2, "West": r4})
    r4.setExits({"East": r3})
    r5.setExits({"East": r6, "South": r2})
    r6.setExits({"North": r9, "East": r7, "South": r8, "West": r5})
    r7.setExits({"West": r6})
    r8.setExits({"North": r6})
    r9.setExits({"East": r10, "South": r6, "West": r11})
    r10.setExits({"West": r9})
    r11.setExits({"East": r9, "West": r12})
    r12.setExits({"North": r13})
    
    # returns the first room
    return r1

# cleans up the message and determines if you used a verb and noun.
def cleanMessage(uinput, directions):
    exitGame = ["exit", "bye", "quit"]
    CLEAR()
    uinput.lower()
    noun = ''
    # exits the game if you typed, extit, bye, or quit
    if uinput in exitGame:
        print("GOOD BYE!")
        exit()
    allInput = uinput.split(" ")
    # tries to run, but if a noun and verb isnt entered, it throws an error and user has to reinput their command
    try:
        verb = allInput[0]
        verb = verb.lower()
        noun = allInput[1]
    except:
        noun = noun.capitalize()
        return verb, noun
    else:
        noun = noun.capitalize()
        return verb, noun

# main action function
def action(directions, previousRoom = None):
    global currentRoom
    global user
    
    # Checks if the room is cleared or if it has enemies in the room
    if currentRoom._enemiescleared:
        # sets all cordinated in a list
        cardinalDirections = ["North", "East", "South", "West"]
        userInput = input("What would you like to do?(Verbs: \"Go\", \"Search\", \"Show\" \"equip\")  (Nouns: \"direction\", \"chest\", \"inventory\" \"item\") \n")
        verb, noun = cleanMessage(userInput, directions)

        # moves to another room
        if verb == "go":
            
            # tests if the given noun is a possible direction
            if noun not in cardinalDirections:
                print("That is not a direction.\n")
                action(directions)
                
            # tests if the given direction is an exit in your current room
            if noun not in directions:
                print("You cannot go that direction.\n")
                action(directions)
            print(f"You went {noun}!\n")
            previousRoom = currentRoom
            
            # goes through every exit available and sets current room if it equals to the user direction inputed
            for _, (k, v) in enumerate(currentRoom.exits.items()):
                if k == noun:
                    currentRoom = v
            return previousRoom
        
        # searches chest
        elif verb == "search":
            # checks if there is a chest in the room
            if currentRoom.chestSearched:
                print("There is nothing to search.\n")
                action(directions)
            else:
                
                # opens the chest in the current room
                loot, potion = currentRoom.openChest()
                CLEAR()
                print(f"You searched the chest!\n   You got a {loot.name} and {potion} potion")
                time.sleep(2)
                CLEAR()
                
                # go ahead and appens the chest loot into the user's inventory
                user.weaponInventory.append(loot)
                user.potionInventory += potion
                
        # shows user inventory
        elif verb == "show":
            user.printInventory()
            
        # equips an item
        elif verb == "equip":
            user.equipWeapon()
        else:
            print("You cannot do this action.\n")
            print(currentRoom)
            action(directions)
            
    # ran if there are enemies in this room
    else:
        
        # if its a boss room, you cannot run
        if currentRoom.isBoss:
            battle(currentRoom.enemiesOnFloor, user)
        else:
            exitGame = ["exit", "bye", "quit"]
            userInput = input('What would you like to do? (Verbs: \"Run\", \"Fight\")\n')
            userInput.lower()
            
            # exits game
            if userInput in exitGame:
                print("GOOD BYE!")
                exit()
                
            # Run just puts the user back into their previous room
            if userInput == "run":
                currentRoom = previousRoom
                CLEAR()
                
            # The player fights the enemies in the floor
            elif userInput == "fight":
                battle(currentRoom.enemiesOnFloor, user)
                currentRoom.clearedRoom()

CLEAR()
GameIsRunning = True

# initalizes the game's room
currentRoom = createRooms()
username = input("What is your name? ")
CLEAR()
user = human(50, 20, 1, username)
previousRoom = None

# Runs the game through a loop
while GameIsRunning:
    
    # grabs all the directions in the current room
    directions = currentRoom.exits.keys()
    print(currentRoom)
    
    # lets user to chose an action
    prevRoom = action(directions, previousRoom)
    if prevRoom != None:
        previousRoom = prevRoom
       
CLEAR()         