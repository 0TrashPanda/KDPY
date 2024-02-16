from classes import Player, Board, Domino, StackPeace
import random
import os
import unicurses

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    pass

def choose_tile(player, stack):
    clear()
    print(f"{player.name} choose a tile")
    for index, domino in enumerate(stack):
        print(f"{index + 1}\t\t{domino.domino.tile0}\t{domino.domino.tile1}\t\t{domino.player_name if domino.player_id != None else ''}".expandtabs(2))
    tile_str = input("choose a tile: ")
    if not tile_str.strip():  # Check if the input is empty
            input("Input cannot be empty. Please enter a number.")
            choose_tile(player, stack)
            return
    try:
        tile = int(tile_str) - 1
    except ValueError:
        input("Invalid input. Please enter a number.")
        choose_tile(player, stack)
        return

    if tile < 0 or tile >= len(stack):
        input("Invalid tile. Please choose a tile within the range.")
        choose_tile(player, stack)
        return

    if stack[tile].player_id is not None:
        input("Tile already taken. Please choose another tile.")
        choose_tile(player, stack)
        return
    stack[tile].player_id = player.id
    stack[tile].player_name = player.name

def get_new_stack():
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

def interactive_board(board, domino, player):
    unicurses.initscr()
    unicurses.curs_set(0)
    unicurses.clear()
    unicurses.noecho()
    unicurses.cbreak()

    unicurses.mvaddstr(0, 0, player.name)
    unicurses.mvaddstr(1, 0, str(board))
    y0, x0, y1, x1 = 2, 1, 2, 2
    unicurses.mvaddstr(y0, x0, domino.tile0)
    unicurses.mvaddstr(y1, x1, domino.tile1)
    y0, x0, y1, x1 = 0, 0, 0, 1
    unicurses.refresh()
    msg = ""
    while True:
        key = unicurses.getch()
        if key == ord('w'):
            ofset = board.up(y0, x0, y1, x1)
            y0, x0, y1, x1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == ord('r'):
            ofset = board.down(y0, x0, y1, x1)
            y0, x0, y1, x1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == ord('a'):
            ofset = board.left(y0, x0, y1, x1)
            y0, x0, y1, x1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == ord('s'):
            ofset = board.right(y0, x0, y1, x1)
            y0, x0, y1, x1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == ord('r') or key == ord(' '):
            ofset = board.rotate(y0, x0, y1, x1)
            y0, x0, y1, x1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == 10:
            if board.place(y0, x0, y1, x1, tile0=domino.tile0, tile1=domino.tile1):
                break
            else:
                msg = "Invalid placement"
        elif key == ord('x'):
            break

        unicurses.clear()
        unicurses.mvaddstr(0, 0, player.name)
        unicurses.mvaddstr(1, 0, str(board))
        unicurses.mvaddstr(y0 + 2, x0 + 1, domino.tile0)
        unicurses.mvaddstr(y1 + 2, x1 + 1, domino.tile1)
        if msg:
            unicurses.mvaddstr(0, 0, msg)
            msg = ""
        unicurses.refresh()
    unicurses.endwin()


def place_domino(stack, index):
    clear()
    player = get_player(stack[index].player_id)
    print(f"{player.name} place a domino")
    domino = stack[index].domino
    print(f"{domino.tile0}\t{domino.tile1}")
    print(player.board)
    interactive_board(player.board, domino, player)
    return stack[index].player_id

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

old_stack = get_new_stack()
for player in player_cage:
    choose_tile(player, old_stack)

while cards > 0:
    new_stack = get_new_stack()
    for i in range(total_kings):
        player_id = place_domino(old_stack, i)
        player = get_player(player_id)
        choose_tile(player, new_stack)
    old_stack = new_stack
