import collections
import datetime
import enum
import os
import time
import sys
import random


states = enum.Enum('State', 'sleep live')


def align(minutes: int, alignment: int) -> int:
  return (minutes - alignment) % 30


PomodoroState = collections.namedtuple('PomodoroState', ['state', 'seconds'])


def advance(state: PomodoroState, seconds: int) -> PomodoroState:
  if state.state != states.live:
    return state
  seconds = state.seconds - seconds
  if seconds <= 0:
    raise Ring
  return PomodoroState(state=states.live, seconds=seconds)


def wind_up(seconds: int=0, minutes: int=0) -> PomodoroState:
  return PomodoroState(state=states.live, seconds=seconds + minutes * 60)


class Pomodoro:

  def __init__(self, alignment=0):
    self.alignment = alignment
    self.state = PomodoroState(state=states.sleep, seconds=0)


class Ring(Exception):
  pass


def demand_wind_up(timeout):
  import select
  print ("What's this pomodoro for? "
         "You have {} seconds to answer!").format(timeout)

  i, o, e = select.select( [sys.stdin], [], [], timeout)

  if (i):
    return sys.stdin.readline().strip()
  else:
    print("You said nothing!")


def calculate_work_minutes(seconds: int) -> int:
  delay = 30 * 60 - seconds
  return (23 * 60 + delay * 2.5) / 60.


def main(args):
  todos = []
  with pomodoro_lock():
    if len(args) > 1:
      if args[1] == 'start':
        start()
      if args[1] == 'end':
        end(todos)
    while True:
      try:
        now = datetime.datetime.now()
        if now.minute % 30 < 3:  # in case it runs late for some reason
          try:
            todo = demand_wind_up(timeout=2*60)
            if todo is None:
              continue
            now = datetime.datetime.now()
            minutes_to_work = calculate_work_minutes(now)
            todos.append(todo)
            do_work(minutes_to_work * 60)
            do_not_work((30 - minutes_to_work) * 60)
          except TimeoutException:
            pass
        else:
          if not now.second:
            print('waiting')
          time.sleep(1)
      except KeyboardInterrupt:
        end(todos)


def start():
  do_work(12.5 * 60)
  do_not_work(5 * 60)


def end(todos):
  print(todos)
  do_work(12.5 * 60)
  raise StopIteration


def ring():
  ring_count = 200
  for _ in range(ring_count):
    spaces = ' ' * random.randint(0, 20)
    print(spaces + 'ring')
    time.sleep(.5 / float(ring_count))


def do_work(time_left):
  time_left = int(time_left)
  print(time_left)
  while time_left:
    if not time_left % 60:
      print((str(time_left // 60) + '  ') * 100)
    print('tick')
    time.sleep(1)
    time_left -= 1
  ring()


def do_not_work(time_left):
  time_left = int(time_left)
  while time_left:
    if not time_left % 60:
      print(str(time_left // 60) * 100)
    if time_left <= 30:
      print(str(time_left) * 100)
    time.sleep(1)
    time_left -= 1



class TimeoutException(Exception):
  pass

