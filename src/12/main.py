# this code was developed based on 
#https://github.com/joelgrus/advent2019/blob/master/day12/day12.py

import math
import numpy as np
import re
import sys
from functools import reduce
from itertools import combinations

class Moon:
  def __init__(self, pos):
    self.pos = np.array(pos)
    self.vel = np.array([0,0,0])

  def update_pos(self):
    self.pos += self.vel

  def potential_energy(self):
    return np.sum(abs(self.pos))

  def kinetic_energy(self):
    return np.sum(abs(self.vel))

  def total_energy(self):
    return self.potential_energy() * self.kinetic_energy()

def apply_gravity(m1, m2):
  for d in range(len(m1.pos)):
    if m1.pos[d] < m2.pos[d]:
      m1.vel[d] += 1
      m2.vel[d] -= 1
    elif m1.pos[d] > m2.pos[d]:
      m2.vel[d] += 1
      m1.vel[d] -= 1

def total_system_energy(moons):
  return reduce(lambda a,b: a + b.total_energy(), moons, 0)

def parse_input_file(filename):
  lines = open(filename, 'r').readlines()
  regex = 'x=(-?\d+),.?y=(-?\d+),.?z=(-?\d+)'
  
  moons = []
  for l in lines:
    g = re.search(regex, l).groups()
    [x,y,z] = list(map(int, g))
    moons.append(Moon([x,y,z]))
  return moons

def print_moons(moons):
  for m in moons:
    print(f'pos=<x={m.pos[0]}, y={m.pos[1]}, z={m.pos[2]}>, vel=<x={m.vel[0]}, y={m.vel[1]}, z={m.vel[2]}>')
  print()

def state2hash(moons, dim):
  return tuple((m.pos[dim], m.vel[dim]) for m in moons)

def step(moons):
    moons_combinations = combinations(moons, 2)
    for c in moons_combinations:
      apply_gravity(c[0], c[1])
    
    for m in moons:
      m.update_pos()

def run_simulation(moons, steps):
  cur_step = 0
  universe = {}
  while True:
    cur_step += 1
    if cur_step == steps+1:
      break

    step(moons)

# returns the least common denominator
def lcd(numbers):
  lcd = 1
  for n in numbers:
    lcd *= n // math.gcd(lcd, n)
  return lcd

def universe_repeat_after(moons):
  cur_step = 0
  dims = [0, 1, 2]
  repeated_dimensions_at_step = [-1 for _ in dims]
  repeated = [False for _ in dims]
  seen = [set() for _ in dims]

  while not all(repeated):
    hashes = [state2hash(moons, d) for d in dims]
    for dim in range(len(dims)):
      if hashes[dim] in seen[dim] and not repeated[dim]:
        repeated[dim] = True
        repeated_dimensions_at_step[dim] = cur_step
      else:
        seen[dim].add(hashes[dim])

    cur_step += 1
    step(moons)

  return lcd(repeated_dimensions_at_step)

if __name__ == '__main__':
  filename = sys.argv[1]
  moons = parse_input_file(filename)

  moons_copy = moons[:]
  steps = int(sys.argv[2])
  run_simulation(moons_copy, steps)
  total_energy = total_system_energy(moons_copy)
  print(f'Part 1: {total_energy}')

  moons_copy = moons[:]
  print(f'Part 2: {universe_repeat_after(moons_copy)}')
