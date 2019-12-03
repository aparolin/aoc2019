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

def get_dir_vector(direction):
  dir_vector = [0, 0]
  if direction == 'R':
    dir_vector = [1, 0]
  elif direction == 'L':
    dir_vector = [-1, 0]
  elif direction == 'U':
    dir_vector = [0, -1]
  elif direction == 'D':
    dir_vector = [0, 1]
  return dir_vector

def find_intersections(intruction_set):
  intersections = set()
  points = {}

  for wire, intructions in enumerate(intruction_set):
    pos = np.array([0, 0])
    for raw_instruction in intructions:
      instruction = parse_instruction(raw_instruction)
      dir_vector = get_dir_vector(instruction['dir'])

      for _ in range(0, instruction['steps']):
        pos += dir_vector
        if tuple(pos) in points:
          # make sure it's not the same wire
          if points[tuple(pos)] != wire:
            intersections.add(tuple(pos))
        else:
          points[tuple(pos)] = wire

  return list(intersections)

def find_min_steps_to_intersections(instructions_set, intersections):
  steps_to_intersection = {}
  steps_wire = {0: 0, 1: 0}

  for wire, intructions in enumerate(instructions_set):
    pos = np.array([0,0])
    for raw_instruction in intructions:
      instruction = parse_instruction(raw_instruction)
      dir_vector = get_dir_vector(instruction['dir'])

      for _ in range(0, instruction['steps']):
        pos += dir_vector
        steps_wire[wire] += 1

        if tuple(pos) in intersections:
          if tuple(pos) in steps_to_intersection:
            steps_to_intersection[tuple(pos)] += steps_wire[wire]
          else:
            steps_to_intersection[tuple(pos)] = steps_wire[wire]

  return min(steps_to_intersection.values())

def manhattan_distance_to_origin(point):
  return abs(point[0] - 0) + abs(point[1] - 0)

def find_closest_intersection(intersections):
  return min(list(map(manhattan_distance_to_origin, intersections)))

if __name__ == '__main__':
  lines = open('input.txt').read().splitlines()
  instruction_set = list(map(lambda s: s.split(','), lines))

  intersections = find_intersections(instruction_set)
  print(f'Part 1: {find_closest_intersection(intersections)}')

  print(f'Part 2: {find_min_steps_to_intersections(instruction_set, intersections)}')