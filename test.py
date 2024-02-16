# grid = [[(y,x) for x in range(5)] for y in range(5)]
# for row in grid:
#     print(*row)
#     print()
# cords = [(-1, 0),(0, -1),(1, 0),(0, 1)]
# for cord in cords:
#     print(cord)
#     print()

import unicurses

def main(stdscr):
    # Turn off cursor blinking
    unicurses.curs_set(0)

    # Set up the screen
    unicurses.clear()
    unicurses.noecho()
    unicurses.cbreak()
    unicurses.refresh()

    # Print a prompt
    unicurses.mvaddstr(0, 0, "Press the arrow keys. Press 'q' to quit.")

    # Capture arrow keys
    while True:
        key = unicurses.wgetch(stdscr)
        if key == ord('w'):
            unicurses.mvaddstr(0, 0, "Up arrow key pressed")
        elif key == ord('r'):
            unicurses.mvaddstr(0, 0, "Down arrow key pressed")
        elif key == ord('a'):
            unicurses.mvaddstr(0, 0, "Left arrow key pressed")
        elif key == ord('s'):
            unicurses.mvaddstr(0, 0, "Right arrow key pressed")
        elif key == ord('q'):
            break
        unicurses.clrtoeol()
        unicurses.refresh()

if __name__ == "__main__":
    main(unicurses.initscr())