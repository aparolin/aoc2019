import sys
sys.path.append('..')

from computer import Computer
from queue import Queue
from tkinter import *
import random
import time
import sys

WIDTH = 800
HEIGHT = 800
SCALE = 20

tk = None
canvas = None
ball = None
paddle = None
last_key_pressed = None
game_started = False

def print_grid(grid):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      print('#' if grid[r][c] != 0 else '.', end='')
    print()

def create_canvas():
  global tk
  global canvas

  tk = Tk()
  tk.configure(background='black')
  canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
  canvas.pack()

def run_part1(instruction):
  total_blocks = 0

  # grid = [[0] * WIDTH] * HEIGHT
  in_queue = Queue()
  out_queue = Queue()

  c = Computer(0, instructions, in_queue, out_queue)
  c.start()
  c.wait_until_finished()

  while True:
    x = out_queue.get()
    # computer ended execution
    if x is None:
      break
    y = out_queue.get()
    tile_id = out_queue.get()

    if tile_id == 2:
      total_blocks += 1

  print(f'Part 1: {total_blocks}')
  # return grid

def draw_on_screen(state):
  global ball, paddle

  i = 0
  # print('entrou no while')
  while i < len(state):
    x = state[i]
    y = state[i+1]
    tile_id = state[i+2]
    i += 3

    # if tile_id == 4:
    #   print(f'ball to {x},{y}')

    rescaled_x1 = (x+1) * SCALE
    rescaled_x2 = rescaled_x1 + SCALE
    rescaled_y1 = (y+1) * SCALE
    rescaled_y2 = rescaled_y1 + SCALE

    if x >= 0:
      if tile_id == 1:
        object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray25')
      if tile_id == 2:
        object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray65')
      if tile_id == 3:
        if paddle:
          canvas.coords(paddle, rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2)
        else:
          paddle = object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray90')
      if tile_id == 4:
        # print(f'updating ball to {rescaled_x1},{rescaled_y1}')
        if ball:
          # print('updating ball')
          canvas.coords(ball, rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2)
        else:
          # print('creating new ball')
          ball = canvas.create_oval(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='LightSkyBlue1')

    tk.update_idletasks()
    tk.update()

def run_part2(instructions):
  global last_key_pressed

  def callback(event):
    print(event.__dict__)
    global last_key_pressed
    global game_started
    last_key_pressed = event.keysym

    if last_key_pressed == 'Return':
      game_started = True
      print('Starting game')

  in_queue = Queue()
  out_queue = Queue()

  create_canvas()

  c = Computer(0, instructions, in_queue, out_queue)
  c.update_memory_address(0, 2)
  # in_queue.put(0)
  c.start()
  
  ball = None
  state = []

  canvas.bind("<1>", lambda event: canvas.focus_set())
  canvas.bind("<Left>", callback)
  canvas.bind("<Right>", callback)
  canvas.bind("<Return>", callback)
  
  while True:
    data_available = True

    try:
      x = out_queue.get(False)
      # computer ended execution
      if x is None:
        break
      y = out_queue.get(False)
      tile_id = out_queue.get(False)
      # print('got data')
      state.append(x)
      state.append(y)
      state.append(tile_id)
    except Exception:
      # print('drawing')
      draw_on_screen(state)
      time.sleep(0.15)

      if not game_started:
        continue

      if last_key_pressed is not None:
        # print('something was pressed')
        if last_key_pressed == 'Left':
          in_queue.put(-1)
        elif last_key_pressed == 'Right':
          in_queue.put(1)
        last_key_pressed = None
      else:
        in_queue.put(0)
          
      state = []


if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))
  # run_part1(instructions)
  run_part2(instructions)
