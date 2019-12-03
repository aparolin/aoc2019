import re
import numpy as np

def parse_instruction(i):
  groups = re.search(r'(\w)(\d+)', i).groups()
  direction = groups[0]
  steps = int(groups[1])
  return {
    'dir': direction,
    'steps': steps
  }

def create_map_of_points(intruction_set):
  intersections = set()
  points = {}

  for wire, intructions in enumerate(intruction_set):
    pos = np.array([0,0])
    for raw_instruction in intructions:
      instruction = parse_instruction(raw_instruction)

      dir_vector = [0,0]
      if instruction['dir'] == 'R':
        dir_vector = [1,0]
      elif instruction['dir'] == 'L':
        dir_vector = [-1,0]
      elif instruction['dir'] == 'U':
        dir_vector = [0,-1]
      elif instruction['dir'] == 'D':
        dir_vector = [0,1]

      for _ in range(0, instruction['steps']):
        pos += dir_vector
        if tuple(pos) in points:
          # make sure it's not the same wire
          if points[tuple(pos)] != wire:
            intersections.add(tuple(pos))
        else:
          points[tuple(pos)] = wire

  return {
    'map': points,
    'intersections': list(intersections)
  }

def manhattan_distance_to_origin(point):
  return abs(point[0] - 0) + abs(point[1] - 0)

def find_closest_intersection(intersections):
  return min(list(map(manhattan_distance_to_origin, intersections)))

if __name__ == '__main__':
  lines = open('input.txt').read().splitlines()
  instruction_set = list(map(lambda s: s.split(','), lines))
  points = create_map_of_points(instruction_set)
  print(find_closest_intersection(points['intersections']))