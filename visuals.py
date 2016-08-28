import curses
import random
import time


def initialize_graphics():
    screen = curses.initscr()
    screen.clear()
    return screen


def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    resp = stdscr.getstr(r + 1, c, 200)
    curses.noecho()
    return resp




def huthuthut():
    stdscr.addstr(5, 3," Invalid input")
    stdscr.refresh()
    stdscr.getch()
    # Clear:
    curses.endwin()


def draw_tick(screen):
    screen.clear()
    row = random.randint(4, 9)
    screen.addstr(row, 3, 'tick')
    screen.refresh()

def ring(screen):
    ring_count = 200
    screen.clear()
    for _ in range(ring_count):
        row = random.randint(4, 9)
        column = random.randint(0, 20)
        screen.addstr(row, column, 'ring')
        time.sleep(3 / ring_count)
        screen.refresh()

def write_text(text):
    screen.clear()
    screen.addstr(2, 3, text)
    screen.refresh()


def wait_for_response(screen):
    screen.getch()
