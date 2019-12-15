import sys
sys.path.insert(0,'../09')

import time
import numpy as np
import math
from collections import defaultdict
from computer import Computer
from queue import Queue

class Robot:
  def __init__(self, instructions, grid, init_pos=[0,0]):
    self.__in_com_channel = Queue()
    self.__out_com_channel = Queue()
    self.__cpu = Computer(0, instructions, self.__out_com_channel, self.__in_com_channel)
    self.__grid = grid
    self.__pos = np.array(init_pos)
    self.__dir = np.array([-1, 0])
    self.__panels_painted = defaultdict(int)
    self.__min_row = self.__min_col = math.inf
    self.__max_row = self.__max_col = -math.inf
    self.__white_panels = []

  def get_white_panels(self):
    return self.__white_panels

  def update_grid_boundaries(self):
    if self.__pos[0] > self.__max_row:
      self.__max_row = self.__pos[0]
    if self.__pos[0] < self.__min_row:
      self.__min_row = self.__pos[0]
    if self.__pos[1] > self.__max_col:
      self.__max_col = self.__pos[1]
    if self.__pos[1] < self.__min_col:
      self.__min_col = self.__pos[1]

  def print_grid(self):
    for row in range(self.__min_row, self.__max_row+1):
      for col in range(self.__min_col, self.__max_col+1):
        if self.__grid[(row,col)] == 1:
          self.__white_panels.append((row,col))
          print('#',end='')
        else:
          print('.', end='')
      print()

  def start(self):
    self.__cpu.start()

    while True:
      self.update_grid_boundaries()
      pos_as_tuple = (self.__pos[0], self.__pos[1])

      # print(f'Sending color {self.__grid[pos_as_tuple]}')
      self.__out_com_channel.put(self.__grid[pos_as_tuple])

      color = self.__in_com_channel.get()
      # print(f'Received color {color}')
      if color is None:
        break
      self.__grid[pos_as_tuple] = color
      # print(f'Painted pos {pos_as_tuple} as {color}')
      self.__panels_painted[pos_as_tuple] += 1

      turn_instruction = self.__in_com_channel.get()
      # print(f'Received turn instruction {turn_instruction}')
      self.turn(turn_instruction)
      self.__pos += self.__dir
      # print(f'Now in new position ({self.__pos[0]},{self.__pos[1]})')
      # color = self.__in_com_channel.get()

    print(f'Part 1: {len(self.__panels_painted.keys())}')

  def turn(self, code):
    angle = -math.pi/2 if code == 1 else math.pi/2
    rot_mat = np.matrix([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])
    new_dir = np.array(np.matmul(rot_mat, self.__dir))
    self.__dir = np.array([int(round(new_dir[0][0])), int(round(new_dir[0][1]))])

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  grid = defaultdict(int)
  robot = Robot(instructions, grid)
  robot.start()
  robot.print_grid()
  white_pannels = robot.get_white_panels()
  robot2 = Robot(instructions, grid, list(white_pannels[0]))
  robot2.start()
  print('\n\n\n\n')
  robot2.print_grid()