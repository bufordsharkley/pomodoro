import collections
import curses
import datetime
import enum
import multiprocessing
import os
import select
import subprocess
import time
import sys
import random


class Ring(Exception):
  """A pomodoro has ended."""


class Ennui(Exception):
  """It is time for a new pomodoro."""


class Dispair(Exception):
  """You missed your chance for a new pomodoro."""


class Hope(Exception):
  """Even though you have failed, you can still do another pomodoro."""

STATES = enum.Enum('State', 'sleep live notwork nagging gnashing')

NAG_TIME = 120


def align(minutes: int, alignment: int) -> int:
  return (minutes - alignment) % 30


PomodoroState = collections.namedtuple('PomodoroState', ['state', 'seconds'])


def create_ring():
    d = multiprocessing.Process(target=play_ring_audio)
    d.daemon = True
    d.start()
    import random
    ring_count = 200
    for _ in range(ring_count):
        spaces = ' ' * random.randint(0, 20)
        print(spaces + 'ring')
        time.sleep(.5 / float(ring_count))


def play_ring_audio():
    devnull = open(os.devnull, 'w')
    subprocess.call("mplayer audio/ring.m4a", shell=True,
                    stdout=devnull, stderr=devnull)


def advance_state(state: PomodoroState, seconds: int) -> PomodoroState:
  current_state = state.state
  if current_state == STATES.sleep:
    return state
  seconds = state.seconds - seconds
  if seconds <= 0:
    if current_state == STATES.live:
      create_ring()
      raise Ring
    elif current_state == STATES.notwork:
      raise Ennui
    elif current_state == STATES.nagging:
      raise Dispair
    elif current_state == STATES.gnashing:
      raise Hope
  return PomodoroState(state=current_state, seconds=seconds)


def wind_up(seconds: int=0, minutes: int=0) -> PomodoroState:
  return PomodoroState(state=STATES.live, seconds=seconds + minutes * 60)


def update_visuals(state):
    current_state = state.state
    if current_state == STATES.live:
        print('tick')


class Pomodoro:

  def __init__(self, alignment=0):
    self.alignment = alignment
    self.log = []
    self.state = PomodoroState(state=STATES.sleep, seconds=0)
    self.final = False

  def run_forever(self):
    create_ring()
    self.screen = initialize_graphics()
    while True:
      try:
        self.state = blocking_input_if_needed(self.state,
                                              self.screen,
                                              self.log,
                                              self.alignment)
        self.state = advance_state(self.state, 1)
        # Update visuals:
        # TODO actual visuals
        update_visuals(self.state)
        time.sleep(1)
      except Ring:
        if self.final:
          self.final = False
          self.state = PomodoroState(state=STATES.sleep, seconds=0)
          #raise StopIteration
        else:
          now = datetime.datetime.now()
          self.state = PomodoroState(
              state=STATES.notwork,
              seconds=seconds_til_next_alignment(now, self.alignment))
      except (Ennui, Hope):
        self.state = PomodoroState(state=STATES.nagging, seconds=NAG_TIME)
      except Dispair:
        now = datetime.datetime.now()
        self.state = PomodoroState(
            state=STATES.gnashing,
            seconds=seconds_til_next_alignment(now, self.alignment))
      except KeyboardInterrupt:
        # Go into close:
        # TODO proper display
        print
        for dt, entry in self.log:
          print('    {}\n    {}'.format(dt.strftime('%H:%M'), entry))
        print
        self.final = True
        self.state = PomodoroState(state=STATES.live, seconds=12.5 * 60)


def seconds_til_next_alignment(time_: datetime.datetime, alignment: int) -> int:
  return 60 * (alignment + 30) - (time_.minute * 60 + time_.second) % (30 * 60)


def blocking_input_if_needed(state: PomodoroState,
                             screen,
                             log: list,
                             alignment: int) -> PomodoroState:
  if state.state == STATES.sleep:
    return block_in_sleep(screen, log)
  elif state.state == STATES.nagging:
    return block_in_nagging(screen, state.seconds, log, alignment)
  return state


def block_in_sleep(screen, log):
  while log:
    log.pop()
  screen.addstr(2, 3, 'Enter something to wake up')
  screen.getch()
  screen.clear()
  screen.refresh()
  return wind_up(minutes=12, seconds=30)


def block_in_nagging(screen,
                     timeout: int, log: list, alignment: int) -> PomodoroState:
  screen.addstr(2, 3, ("What's this pomodoro for? "
                       "You have {} seconds to answer!").format(timeout))

  answer, _, _ = select.select([sys.stdin], [], [], timeout)

  if (answer):
    now = datetime.datetime.now()
    seconds = seconds_til_next_alignment(now, alignment)
    seconds = calculate_work_seconds(seconds)
    log.append((now, sys.stdin.readline().strip()))
    return PomodoroState(state=STATES.live, seconds=seconds)
  else:
    raise Dispair


def calculate_work_seconds(total_seconds: int) -> int:
  return 25 * 60


def calculate_work_minutes(seconds: int) -> float:
  delay = 30 * 60 - seconds
  return (23 * 60 + delay * 2.5) / 60.


def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    resp = stdscr.getstr(r + 1, c, 200)
    curses.noecho()
    return resp


def initialize_graphics():
    screen = curses.initscr()
    screen.clear()
    return screen


def huthuthut():
    stdscr.addstr(5, 3," Invalid input")
    stdscr.refresh()
    stdscr.getch()
    # Clear:
    curses.endwin()
