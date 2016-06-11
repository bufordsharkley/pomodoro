import random
#import tkinter as tk
#import Tkinter as tk
import time

from prompt_toolkit import prompt
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys

manager = KeyBindingManager.for_prompt()

@manager.registry.add_binding(Keys.Any)
def _(event):
    def wind_up():
      print('WINDING UP')
      for _ in range(3):
        time.sleep(.5)
        print('<crank>')
      time.sleep(.5)
    event.cli.run_in_terminal(wind_up)
    event.cli.current_buffer.reset()
    event.cli.exit()

# TODOs:
# integrate with actual clock.
# enforce user to actually wind up each time.


def demand_wind_up():
  try:
    text = prompt(u'Press Ctrl-T to wind up> ',
                  key_bindings_registry=manager.registry)
  except EOFError:
    pass


def main(args):
  if len(args) > 1:
    if args[1] == 'start':
      do_work(12.5 * 60)
      do_not_work(5 * 60)
    if args[1] == 'end':
      do_work(12.5 * 60)
      return
  while True:
    do_work(25 * 60)
    do_not_work(5 * 60)


def ring():
  ring_count = 200
  for _ in range(ring_count):
    spaces = ' ' * random.randint(0, 20)
    print(spaces + 'ring')
    time.sleep(.5 / float(ring_count))


def do_work(time_left):
  #demand_wind_up()
  while time_left:
    if not time_left % 60:
      print((str(time_left // 60) + '  ') * 100)
    print('tick')
    time.sleep(1)
    time_left -= 1
  ring()


def do_not_work(time_left):
  while time_left:
    if not time_left % 60:
      print(str(time_left // 60) * 100)
    if time_left <= 30:
      print(str(time_left) * 100)
    time.sleep(1)
    time_left -= 1


# starting with: http://stackoverflow.com/a/31086299
def graphics():
  # TODO - implement with tomato graphics
  root = tk.Tk()
  root.attributes('-alpha', 0.0) # For icon
  #root.lower()
  root.iconify()
  window = tk.Toplevel(root)
  window.geometry("100x100") #Whatever size
  window.overrideredirect(1) #Remove border
  #window.attributes('-topmost', 1)
  #Whatever buttons, etc
  close = tk.Button(window, text="Close Window",
                    bg='blue', fg='white',
                    command = lambda: root.destroy())
  close.pack(fill = tk.BOTH, expand = 1)
  window.mainloop()

if __name__ == "__main__":
  import sys
  main(sys.argv)
  #graphics()
