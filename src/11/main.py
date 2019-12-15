import sys
sys.path.insert(0,'../09')

import numpy as np
import math
from collections import defaultdict
from computer import Computer
from queue import Queue

class Robot:
  def __init__(self, instructions, grid):
    self.__com_channel = Queue()
    self.__cpu = Computer(0, instructions, self.__com_channel, self.__com_channel)
    self.__grid = grid
    self.__pos = np.array([0,0])
    self.__dir = np.array([-1, 0])
    self.__panels_painted = defaultdict(int)

  def start(self):
    self.__com_channel.put(0)
    self.__cpu.run()

    color = self.__com_channel.get()

    while color is not None:
      pos_as_tuple = (self.__pos[0], self.__pos[1])
      self.__grid[pos_as_tuple] = color
      self.__panels_painted[pos_as_tuple] += 1

      turn_instruction = self.__com_channel.get()
      self.turn(turn_instruction)
      color = self.__com_channel.get()

    print(f'Part 1: {len(self.__panels_painted.keys())}')

  def turn(self, code):
    angle = math.pi/2 if code == 1 else math.pi/2
    rot_mat = np.matrix([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])
    new_dir = np.array(np.matmul(rot_mat, self.__dir))
    self.__dir = np.round(new_dir)

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  grid = defaultdict(int)
  robot = Robot(instructions, grid)
  robot.start()

