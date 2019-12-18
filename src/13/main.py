import sys
sys.path.append('..')

from computer import Computer
from queue import Queue
from tkinter import *
import random

def print_grid(grid):
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      print('#' if grid[r][c] != 0 else '.', end='')
    print()

def run_game(instructions):
  in_queue = Queue()
  out_queue = Queue()

  c = Computer(0, instructions, in_queue, out_queue)
  c.start()
  c.wait_until_finished()

  return out_queue

def create_canvas(width, height):
  tk = Tk()
  tk.configure(background='black')
  canvas = Canvas(tk, width=width, height=height)
  canvas.pack()
  return tk, canvas

def run_part1(instruction):
  total_blocks = 0

  width = 800
  height = 800
  grid = [[0] * width] * height

  scale = 20
  outputs = run_game(instructions)
  tk, canvas = create_canvas(width, height)
  while True:
    x = outputs.get()
    # computer ended execution
    if x is None:
      break
    y = outputs.get()
    tile_id = outputs.get()

    rescaled_x1 = (x+1) * scale
    rescaled_x2 = rescaled_x1 + scale
    rescaled_y1 = (y+1) * scale
    rescaled_y2 = rescaled_y1 + scale

    grid[y][x] = tile_id
    if tile_id == 1:
      object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray25')
    if tile_id == 2:
      object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray65')
      total_blocks += 1
    if tile_id == 3:
      object_id = canvas.create_rectangle(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='gray90')
    if tile_id == 4:
      object_id = canvas.create_oval(rescaled_x1, rescaled_y1, rescaled_x2, rescaled_y2, fill='LightSkyBlue1')

    tk.update_idletasks()
    tk.update()

  print(f'Part 1: {total_blocks}')
  mainloop()

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))
  run_part1(instructions)

