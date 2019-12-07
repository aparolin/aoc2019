import sys
sys.path.append("../..")

import importlib
from itertools import permutations
computer = importlib.import_module('src.05.main')

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  possible_settings = list(permutations([0,1,2,3,4]))
  outputs = []

  for settings in possible_settings:
    output = 0
    for s in settings:
      inputs = [s, output]
      output = computer.run_program(instructions, inputs)
      outputs.append(output)

  print(f'Part 1: {max(outputs)}')
