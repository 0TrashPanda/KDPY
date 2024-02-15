from classes import *
import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def chose_tile(player, stack):
    clear()
    print(f"{player.name} choose a tile")
    for index, domino in enumerate(stack):
        print(f"{index}\t\t{domino.domino.tile0.type.value}\t{domino.domino.tile1.type.value}\t\t{domino.player_name if domino.player_id != None else ''}".expandtabs(2))
    tile = int(input("choose a tile: "))
    if stack[tile].player_id != None:
        input("Tile already taken")
        chose_tile(player)
    stack[tile].player_id = player.id
    stack[tile].player_name = player.name

def new_stack():
    stack = []
    for _ in range(total_kings):
        stack.append(StackPeace(Domino()))
    stack.sort(key=lambda x: x.domino.number)
    global cards
    cards -= total_kings
    return stack

def get_player(player_id):
    for player in player_cage:
        if player.id == player_id:
            return player

def show_board(player):
    for i in range(5):
        for j in range(5):
            print(f"{player.board.tiles[i][j].type.name}\t", end="")
        print()

def place_domino(stack, index):
    clear()
    player = get_player(stack[index].player_id)
    print(f"{player.name} place a domino")
    domino = stack[index].domino
    print(f"{domino.tile0.type.name}\t{domino.tile1.type.name}")
    show_board(player)

clear()
# players = int(input("Enter the number of players: "))
# match players:
#     case 2:
#         total_kings = 4
#         cards = 24
#     case 3:
#         total_kings = 3
#         cards = 36
#     case 4:
#         total_kings = 4
#         cards = 48
#     case _:
#         raise ValueError("Invalid number of players")

# player_cage = []
# for i in range(players):
#     i = Player(input(f"Enter the name of player {i + 1}: "), i, 0, [])
#     player_cage.append(i)

players = 2
total_kings = 4
cards = 24
player_cage = [Player("Bob", 0, 0, Board()), Player("Alice", 1, 0, Board())]
player_lounge = player_cage

random.shuffle(player_cage)
if players == 2:
    player_cage += player_cage

old_stack = new_stack()
for i in player_cage:
    chose_tile(i, old_stack)

while cards > 0:
    stack = new_stack()
    for i in range(total_kings):
        player = place_domino(old_stack, i)
        chose_tile(player, stack)
