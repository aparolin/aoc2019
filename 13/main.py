import sys
sys.path.append('..')
import math
import time

from queue import Queue, Empty
from computer import Computer

from msvcrt import getch

class ExecutionFinished(Exception):
  pass

class InputRequired(Exception):
  pass

def draw_grid():
  for r in range(grid_size[0]+1):
    for c in range(grid_size[1]+1):
      print(grid[(r, c)], end='')
    print()

def read_output(out_queue, timeout=None):
  global grid, grid_size
  n_rows = 0
  n_cols = 0
  output = {}
  paddle_pos = None
  ball_pos = None
  score = -1

  while True:
    try:
      x = out_queue.get(timeout=timeout)
      # computer ended execution
      if x is None:
        grid_size = (n_rows, n_cols)

        output['status'] = 'DONE'
        output['score'] = score
        return output

      y = out_queue.get()
      tile_id = out_queue.get()

      if y > n_rows:
        n_rows = y
      if x > n_cols:
        n_cols = x

      if x == -1 and y == 0:
        score = tile_id

      if tile_id == 0:
        grid[(y, x)] = ' '
      elif tile_id == 1:
        grid[(y, x)] = '#'
      elif tile_id == 2:
        grid[(y, x)] = '@'
      elif tile_id == 3:
        grid[(y, x)] = '_'
        paddle_pos = (y, x)
      elif tile_id == 4:
        grid[(y, x)] = 'o'
        ball_pos = (y, x)
    except Empty:
      output['status'] = 'WAITING_FOR_INPUT'
      output['paddle_position'] = paddle_pos
      output['ball_position'] = ball_pos
      output['score'] = score
      return output

def run_part1(instructions):
  total_blocks = 0

  in_queue = Queue()
  out_queue = Queue()

  c = Computer(0, instructions, in_queue, out_queue)
  c.start()
  c.wait_until_finished()

  while True:
    output = read_output(out_queue)
    if output['status'] == 'DONE':
      break

  total_blocks = 0
  for element in grid.values():
    if element == '@':
      total_blocks += 1

  draw_grid()
  print(f'Part 1: {total_blocks}')

def run_part2(instructions):
  in_queue = Queue()
  out_queue = Queue()

  # insert coins
  instructions[0] = 2

  c = Computer(0, instructions, in_queue, out_queue)
  c.start()

  paddle_pos = None
  ball_pos = None
  while True:
    draw_grid()

    output = read_output(out_queue, 1e-6)
    if output['status'] == 'DONE':
      print(f'Part 2: {output["score"]}')
      break
    elif output['status'] == 'WAITING_FOR_INPUT':
      if output['paddle_position'] is not None:
        paddle_pos = output ['paddle_position']
      ball_pos = output['ball_position']

      if paddle_pos[1] < ball_pos[1]:
        command = 1
      elif paddle_pos[1] > ball_pos[1]:
        command = -1
      else:
        command = 0

      in_queue.put(command)

grid = {}
grid_size = None

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))
  run_part1(instructions)
  run_part2(instructions)
