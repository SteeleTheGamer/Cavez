import random

player = {'location': 'start', 'inventory': [], 'hp': 5}

game_map = {'start': {'east': 'paper', 'south': 'abandoned-lab', 'west': 'cliff'},
            'paper': {'south': 'torn-room', 'east': 'paper', 'west': 'start'},
            'abandoned-lab': {'north': 'start', 'east': 'torn-room', 'south': 'bushes'},
            'bushes': {'north': 'abandoned-lab'},
            'cliff': {'east': 'start'},
            'torn-room': {'east': 'reward', 'north': 'paper', 'west': 'abandoned-lab'},
            'reward': {'east': 'empty', 'south': 'shop'},
            'shop': {'north': 'reward'},
            'empty': {'north': 'abandoned-???', 'east': 'boss-room', 'south': 'cabin', 'west': 'reward'},
            'cabin': {'north': 'empty'},
            'boss-room': {'west': 'empty'},
            'abandoned-???': {'north': 'dark-room', 'south': 'empty'},
            'dark-room': {'south': 'abandoned-???', 'west': 'vault'}, 'vault': {'east': 'dark-room'}}

description = {'start': 'you find yourself waking up in this room, there is a door to the east, south, and west',
               'paper': 'you find a paper in this room, there is a door to the south and west',
               'cliff': 'you find yourself looking at a huge cliff with only darkness in the distance, there is a door to the east',
               'abandoned-lab': 'you find yourself in a lab that seems to have been abandoned for years, there is a door to the north, east, and bushes to the south',
               'bushes': 'you find yourself in a hidden room with a key on the floor, a bunny in a corner, and the entrance to the north',
               'torn-room': 'you find yourself in a room that was torn apart by a monster that is in front of you, there are doors to the north, east, and west. the one on the east looks locked, you might need a black key',
               'reward': 'you find yourself rewarded with coins by a treasure chest in front of you, there are doors to the east, south, and west',
               'shop': 'you see a merchant in front of you encouraging you to shop, there is a door to the north',
               'empty': 'you find yourself in a empty room with only doors to your north, south, east, and west. the one to the east seems locked, you might need a red key, maybe ask the traveller?',
               'cabin': 'you see a traveller in front of you who seems sad, there is a door to the north',
               'boss-room': 'you stand upon the big leader, or shall I say the final boss, there is a door to the west',
               'abandoned-???': 'you see yourself in a abandoned room and you try to see what it was originally but you cant find a answer, there is a door to the north and south',
               'dark-room': 'the room is very dark and you stumble upon a stuffie, there is a door to the south and west. the door to the left seems to be locked but you cant see fully',
               'vault': 'you find yourself in a secret vault and in front of you is a key that seems to match the locked door',
               'god': 'you have hurten a poor innocent soul of a bunny. So you now will pay the price >:('}

items = {'start': [], 'paper': ['paper'], 'cliff': [], 'abandoned-lab': [], 'bushes': ['black-key'], 'torn-room': [],
         'reward': ['100-coins'], 'shop': [], 'empty': [], 'cabin': [], 'boss-room': [], 'abandoned-???': [],
         'dark-room': ['stuffie'], 'vault': ['red-key']}

npcMap = {'start': [], 'paper': [], 'cliff': [], 'abandoned-lab': [], 'bushes': ['bunny'], 'torn-room': ['enemy'],
          'reward': [], 'shop': ['merchant'], 'empty': [], 'cabin': ['traveller'], 'boss-room': ['final-boss'],
          'abandoned-???': [], 'dark-room': [], 'vault': [], 'god': ['god'], 'traveller-boss-room': ['traveller-boss']}

npcs = {'merchant': {'location': 'shop', 'inventory': ['sword - 100-coins', 'bow - 100-coins'],
                     'description': "\"Hello young traveller, would you care to shop at my fancy..ish shop?\""},
        'traveller': {'location': 'cabin', 'inventory': ['green-key'],
                      'description': "\"Finally, somebody that can help me and is nice, unlike the shopkeeper, perhaps can you help me find this stuffie? I will give you a green key for reward if you do!\""},
        'enemy': {'location': 'torn-room', 'hp': 3},

        'final-boss': {'location': 'boss-room', 'hp': 5},

        'bunny': {'location': 'bushes', 'hp': 1},

        'god': {'location': 'god', 'hp': 10},

        'traveller-boss': {'location': 'traveller-boss-room', 'hp': 7}}
game_over = False


def help():
    print("Enter 'go <'north', 'east', 'south', or 'west'>' to move.")
    print("Enter 'collect' to collect an item")
    print("Enter 'talk' to talk to npc")
    print("Enter 'use <'item name' to use an item")
    print("Enter 'inventory' to check your inventory")
    print("Enter 'look' to look around the room")
    print("Enter 'fight' to engage combat")
    print("Enter 'quit' to stop running the game")
    print("Enter 'buy' to purchase a item")

def talk():
    if npcMap[player['location']]:
        if player['location'] == 'shop':
            choice = input(''.join(npcs['merchant']['description'])+"\n")
            if choice == 'yes':
               choice = input(' '.join(npcs['merchant']['inventory'])+"\n")
               if choice == 'buy bow':
                   player['inventory'].append('bow')
                   npcs['merchant']['inventory'].remove('bow - 100-coins')
                   player['inventory'].remove('100-coins')
                   print('thanks for shopping!')
               if choice == 'buy sword':
                   if '100-coins' in player['inventory']:
                       player['inventory'].append('sword')
                       npcs['merchant']['inventory'].remove('sword - 100-coins')
                       player['inventory'].remove('100-coins')
                       print('thanks for shopping!')
                   else:
                       print('stop trying to buy things WHEN YOU ARE POOR')
        elif player['location'] == 'cabin':
            choice = input(''.join(npcs['traveller']['description'])+"\n")
            if choice == 'yes':
               print("Thank you so much!")
               choice = input("do you have the stuffie?"+"\n")
               if choice == 'yes':
                   if 'stuffie' in player['inventory']:
                       print("Thank you, here you go!")
                       player['inventory'].append('green-key')
                       npcs['traveller']['inventory'].remove('green-key')
                       player['inventory'].remove('stuffie')
                   else:
                       #steal item (make replica but different) and cant be used in battle. If you have this item in god fight, god is unbeatable, and you get crime commiter ending
                       print("you dirty lier ;(")
        else:
            print('Yet again you remind yourself that you have no friends in here..')


def go(direction):
    if direction in game_map[player['location']]:
        #if npc in room:
        if game_map[player['location']][direction] == 'reward' and 'black-key' not in player['inventory']:
            print('find the black key that\'s hidden')
        elif game_map[player['location']][direction] == 'boss-room' and 'red-key' not in player['inventory']:
            print('find the red key that\'s hidden')
        elif game_map[player['location']][direction] == 'vault' and 'green-key' not in player['inventory']:
            print('find the green key from the traveller')
        elif player['location'] == 'torn-room' and 'enemy' in npcs:
            print('the disgusting creature blocks you from leaving')
        elif player['location'] == 'boss-room' and 'final-boss' in npcs:
            print('you try to escape but there is no door, and the boss is waiting to fight')

        else:
            player['location'] = game_map[player['location']][direction]
            look(player['location'])
    else:
        print('stop trying to run into a wall🤦')


def look(location):
    print(description[location])
    if len(items[location]) > 0:
        for item in items[location]:
            if location == 'reward':
                print(" there are {} in this room".format(item))
            else:
                print(" there is a {} in this room".format(item))


def inventory():
    if len(player['inventory']) > 0:
        print(player['inventory'])
    else:
        print('you are to broke to use this message')

def npcAttack(name):
    if name == 'enemy':
        listOfDeath = ['attack', 'block', 'heal']
        gambling = random.choice(listOfDeath)
    else:
        listOfDeath = ['attack', 'block', 'heal', 'special']
        gambling = random.choice(listOfDeath)

    return gambling

def battle(name, enemyhp):
    isBattleOver = True
#attack vs attack deal 1 damage each
#attack vs block reflects damage to attacker
#attack vs heal prevents healing for 1 turn
#block vs block does nothing
#block vs heal makes healer gain 1 life
#heal vs heal makes both healers gain 1 life
    print('attack vs attack deal 1 damage each\n attack vs block reflects damage to attacker\n attack vs heal prevents healing for 1 turn\n block vs block does nothing\n block vs heal makes healer gain 1 life\n heal vs heal makes both healers gain 1 life\n')
    while isBattleOver:
        if player['hp'] <= 0:
            print("you fall to the ground then you see darkness..")
            exit()
        elif enemyhp <= 0:
            npcs.pop(name)
            if player['location'] == 'boss-room' and 'final-boss' not in npcs:
                print('you see the boss fall to the floor and vanish. A door appears out of thin air and it leads to the real world. You step through and win.')
                exit()
            else:
                print("the enemy falls to the ground and turns to ashes")
                break
        fighter = input('what technique would you like to do\n')
        if fighter == 'attack':
            print("You attacked")
            move = npcAttack(name)
            if move == 'attack':
                if 'bow' not in player['inventory'] and 'sword' not in player['inventory']:
                    player["hp"] -= 1
                    enemyhp -= 1
                    print(name+" attacked, 1 damage taken each")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
                else:
                    player["hp"] -= 1
                    enemyhp -= 2
                    print(name + " attacked, you took 1 damage but hit " + name + " for 2")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")
            elif move == 'block':
                if 'bow' not in player['inventory'] and 'sword' not in player['inventory']:
                    player["hp"] -= 1
                    print(name+" blocked, 1 damage taken")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
                else:
                    enemyhp -= 1
                    print(name + " blocked, but your weapon goes straight through it, making the enemy lose 1 hp")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")
            elif move == 'heal':
                if 'bow' not in player['inventory'] and 'sword' not in player['inventory']:
                    print(name+" healed, nothing happend")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
                else:
                    enemyhp -= 1
                    print(name+" healed, but you cancelled the spell making the enemy lose 1 hp")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
            elif move == 'special':
                if name == 'final-boss':
                    if 'bow' not in player['inventory'] and 'sword' not in player['inventory']:
                        player["hp"] -= 2
                        print(name + " smashed, countering your attack and causing the ground to shake making you lose 2 hp")
                        print(name + " has " + str(enemyhp) + " hp")
                        print("you have " + str(player['hp']) + " hp")
                    else:
                        player["hp"] -= 1
                        print(name + " smashed, causing the ground to shake but you were able to lose a little less hp, causing you to lose only 1 hp")
                        print(name + " has " + str(enemyhp) + " hp")
                        print("you have " + str(player['hp']) + " hp")
                elif name == 'bunny':
                    player["hp"] -= 5
                    print(name + "countered then ate you")
                    print("gg, wait, are you alive?")
                elif name == 'god':
                    player["hp"] -= 100000
                    print(name + " used divine smash, countering your attack and causing the ground to shake making you lose your balance and fall for what seems as eternity")
                else:
                    player["hp"] -= 4
                    print(name + "dodged then stabbed you with the key")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")

        elif fighter == 'block':
            move = npcAttack(name)
            if move == 'attack':
                if 'bow' not in player['inventory'] and 'sword' not in player['inventory']:
                    enemyhp -=1
                    print(name+" attacked, "+name+" took 1 damage")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
                else:
                    enemyhp -=2
                    print(name+" attacked, "+name+" took 2 damage because the weapon you blocked with stabbed them")
                    print(name+" has "+str(enemyhp)+" hp")
                    print("you have "+str(player['hp'])+" hp")
            elif move == 'block':
                print(name+" blocked, nothing happend")
                print(name+" has "+str(enemyhp)+" hp")
                print("you have "+str(player['hp'])+" hp")
            elif move == 'heal':
                enemyhp +=0.5
                print(name+" healed, "+name+" gained 0.5 hp caused by you able to stopp a full health regeneration.")
                print(name+" has "+str(enemyhp)+" hp")
                print("you have "+str(player['hp'])+" hp")
            elif move == 'special':
                if name == 'final-boss':
                    player["hp"] -= 2
                    print(name + " smashed, causing the ground to shake not allowing you to block and you lose 2 hp")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")
                elif name == 'bunny':
                    player["hp"] -= 5
                    print(name + "chomped you before you could heal making you lose 5 hp")
                    print("gg")
                elif name == 'god':
                    player["hp"] -= 100000
                    print(name + " used divine smash, not allowing you to heal while causing the ground to shake making you lose your balance and fall for what seems as eternity")
                else:
                    player["hp"] -= 4
                    print(name + "stabbed with the key so fast you couldn't heal, you lose 4 hp")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")
        elif fighter == 'heal':
            move = npcAttack(name)
            if move == 'attack':
                print(name+" attacked, nothing happend")
                print(name+" has "+str(enemyhp)+" hp")
                print("you have "+str(player['hp'])+" hp")
            if move == 'block':
                player["hp"] +=1
                print(name+" blocked, +1 health")
                print(name+" has "+str(enemyhp)+" hp")
                print("you have "+str(player['hp'])+" hp")
            if move == 'heal':
                enemyhp +=1
                player["hp"] +=1
                print(name+" healed, +1 health each ")
                print(name+" has "+str(enemyhp)+" hp")
                print("you have "+str(player['hp'])+" hp")
            elif move == 'special':
                if name == 'final-boss':
                    player["hp"] -= 2
                    print(name + " smashed, and causing the ground to shake so you cant heal and you lose 2 hp")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")
                elif name == 'bunny':
                    player["hp"] -= 5
                    print(name + "countered then ate you")
                    print("gg")
                elif name == 'god':
                    player["hp"] -= 100000
                    print(name + " used divine smash, countering your attack and causing the ground to shake making you lose your balance and fall for what seems as eternity")
                else:
                    player["hp"] -= 4
                    print(name + "dodged then stabbed you with the key")
                    print(name + " has " + str(enemyhp) + " hp")
                    print("you have " + str(player['hp']) + " hp")

        elif fighter == 'help':
            print('attack vs attack deal 1 damage each\n attack vs block reflects damage to attacker\n attack vs heal prevents healing for 1 turn\n block vs block does nothing\n block vs heal makes healer gain 1 life\n heal vs heal makes both healers gain 1 life\n')
        else:
            print("CHOOSE A MOVE-")

def fight(location):
    if location == 'torn-room' and 'enemy' in npcs:
        battle('enemy', npcs['enemy']['hp'])
    elif location == 'bushes' and 'bunny' in npcs:
        print("you go to fight the bunny, but god himself stops you.")
        battle('god', npcs['god']['hp'])
    elif location == 'cabin' and 'traveller-boss' in npcs:
        battle('traveller-boss', npcs['traveller-boss']['hp'])
    elif location == 'boss-room' and 'final-boss' in npcs:
        battle('final-boss', npcs['final-boss']['hp'])
    else:
        print("lil bros fighting his inner demons💀")



def collect(item, location):
    if item in items[location]:
        player['inventory'].append(item)
        items[location].remove(item)
        print('you added a {} to your inventory to carry for who knows how long'.format(item))


def main():
    global game_over
    print('you found yourself in a cave after adventuring in the forest. Type help for more info.')
    while not game_over:
        choice = input("what would you like to do?\n").split(" ")
        if choice[0] == 'go':
            if len(choice) == 2:
                go(choice[1])
            else:
                print("dont worry, I mistyped that too when i first did it")
        elif choice[0] == 'collect':
            if len(choice) == 2:
                collect(choice[1], player['location'])
            else:
                print("dont worry, I mistyped that too when i first did it")
        elif choice[0] == 'talk':
            talk()
        elif choice[0] == 'use':
            pass
        elif choice[0] == 'inventory':
            inventory()
        elif choice[0] == 'look':
            look(player['location'])
        elif choice[0] == 'help':
            help()
        elif choice[0] == 'fight':
            fight(player['location'])
        elif choice[0] == 'quit':
            print("you decide to take a nap and never wake up..")
            game_over = True
        else:
            print("please type an option that is available")


if __name__ == '__main__':
    main()
