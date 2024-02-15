from classes import Player, Board, Domino, StackPeace
import random
import os
import curses

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
        chose_tile(player, stack)
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

def interactive_board(stdscr, board, domino):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, str(board))
    x0, y0, x1, y1 = 0, 0, 1, 0
    stdscr.addstr(y0, x0, domino.tile0.type.value)
    stdscr.addstr(y1, x1, domino.tile1.type.value)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            ofset = board.up(x0, y0, x1, y1)
            x0, y0, x1, y1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == curses.KEY_DOWN:
            ofset = board.down(x0, y0, x1, y1)
            x0, y0, x1, y1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == curses.KEY_LEFT:
            ofset = board.left(x0, y0, x1, y1)
            x0, y0, x1, y1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == curses.KEY_RIGHT:
            ofset = board.right(x0, y0, x1, y1)
            x0, y0, x1, y1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == ord('r') or key == ord(' '):
            ofset = board.rotate(x0, y0, x1, y1)
            x0, y0, x1, y1 = ofset[0], ofset[1], ofset[2], ofset[3]
        elif key == curses.KEY_ENTER or key == 10:
            if board.place(x0, y0, x1, y1, tile0=domino.tile0, tile1=domino.tile1):
                break
            else:
                stdscr.addstr(0, 0, "Invalid placement")
                stdscr.refresh()
                stdscr.getch()
        stdscr.clear()
        stdscr.addstr(0, 0, str(board))
        stdscr.addstr(y0, x0, domino.tile0.type.value)
        stdscr.addstr(y1, x1, domino.tile1.type.value)
        stdscr.refresh()


def place_domino(stack, index):
    clear()
    player = get_player(stack[index].player_id)
    print(f"{player.name} place a domino")
    domino = stack[index].domino
    print(f"{domino.tile0.type.name}\t{domino.tile1.type.name}")
    print(player.board)
    curses.wrapper(interactive_board, player.board, domino)

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
