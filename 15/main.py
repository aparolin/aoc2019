import numpy as np
from enum import Enum
from collections import defaultdict

import sys
sys.path.append('..')

from queue import Queue, Empty
from computer import Computer

def manhattan_distance(a, b):
  return sum(abs(a-b))

class Node():
  class StatusCode(Enum):
    wall = 0
    free = 1
    oxygen = 2

  def __init__(self, pos, status_code):
    self.pos = np.array(pos)
    self.status_code == status_code

class Droid():
  def __init__(self):
    self.pos = np.array([0, 0])
    self.dir = np.array([0, 1]) # starts pointing north
    self.map = defaultdict(Node)

  def turn_left(self):
    self.dir = self.calculate_dir(-90)

  def turn_right(self):
    self.dir = self.calculate_dir(90)

  def calculate_dir(self, angle_deg):
    angle_rad = np.radians(angle_deg)
    rot_mat = np.matrix([[np.cos(angle_rad), -np.sin(angle_rad)], [np.sin(angle_rad), np.cos(angle_rad)]])
    return np.array(rot_mat.dot(self.dir)).flatten().astype(int)

  def run(self, instructions):
    in_queue = Queue()
    out_queue = Queue()

    c = Computer(0, instructions, in_queue, out_queue)
    c.start()

    starting_point = Node([0, 0])
    oxygen_pos = self.__search_oxygen(starting_point)
    print(f'Result Part 1: {manhattan_distance(oxygen_pos, starting_point)}')

  def __search_oxygen(self, c):
    def reject_candidate(c):
      next_pos = tuple(self.pos + self.dir)
      left_pos = tuple(self.pos + self.calculate_dir(-90))
      right_pos = tuple(self.pos + self.calculate_dir(90))
      if self.map[next_pos] == Node.StatusCode.wall and self.map[left_pos] == '#' and self.map[right_pos] == '#':
        return True
      return False

    def accept()
      

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  droid = Droid()
  droid.run(instructions)