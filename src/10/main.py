# this code was developed based on 
# https://github.com/joelgrus/advent2019/blob/master/day10/day10.py

import math
from typing import NamedTuple
from collections import defaultdict

class Asteroid():
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return f'({self.x},{self.y})'
  
  def __repr__(self):
    return self.__str__()

def get_asteroids_set(input):
  s = set()
  with open(input, 'r') as f:
    for y, line in enumerate(f):
      for x, char in enumerate(line):
        if char == '#':
          s.add(Asteroid(x, y))
  return s

def count_visible(asteroids, asteroid):
  slopes = set()
  
  for neighbor in asteroids:
    if neighbor == asteroid:
      continue
    
    dx = neighbor.x - asteroid.x
    dy = neighbor.y - asteroid.y

    # normalize by greates common denominator
    gcd = math.gcd(dx, dy)
    slopes.add((dx/gcd, dy/gcd))

  return len(slopes)

def find_station(asteroids):
  results = [(a, count_visible(asteroids, a)) for a in asteroids]
  return max(results, key=lambda a: a[1])

def distance(ast1, ast2):
  return math.sqrt((ast1.x - ast2.x)**2 + (ast1.y - ast2.y)**2)

def vaporize(asteroids, station, n):
  asteroids_by_angle = defaultdict(list)

  for a in asteroids:
    dx = a.x - station.x
    dy = a.y - station.y

    # rotate 90 degrees leftwise as the angle is zero in respect to the vertical axis
    angle = math.atan2(dy, dx)
    asteroids_by_angle[angle].append((a, angle))

  for angles in asteroids_by_angle.values():
    angles.sort(key=lambda a: distance(station, a[0]), reverse=True)

  i = 0
  keys = sorted(list(asteroids_by_angle.keys()), key=lambda k: (2 * math.pi) + k if k < -math.pi/2 else k)
  while i < n:
    if i == len(keys):
      i = 0
    key = keys[i]
    asteroids = asteroids_by_angle[key]
    a = asteroids.pop()
    i += 1

  return a

if __name__ == '__main__':
    asteroids = get_asteroids_set('input.txt')
    station = find_station(asteroids)
    print(f'Part 1: {station}')

    destroyed = vaporize(asteroids, station[0], 200)[0]
    print(f'Part 2: {destroyed.x * 100 + destroyed.y}')
