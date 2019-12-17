import numpy as np
import re
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

def run_simulation(moons, steps):
  for i in range(steps):
    moons_combinations = combinations(moons, 2)
    for c in moons_combinations:
      apply_gravity(c[0], c[1])
    
    for m in moons:
      m.update_pos()
    
    # print(f'After step {i+1}')
    # print_moons(moons)

if __name__ == '__main__':
  moons = parse_input_file('input.txt')
  run_simulation(moons, 1000)
  total_energy = total_system_energy(moons)
  print(f'Part 1: {total_energy}')