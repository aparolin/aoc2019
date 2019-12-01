import math

def fuel_required(mass):
  return math.floor(mass/3) - 2

def fuel_required_with_additional_fuel(mass):
  total = 0
  fuel = fuel_required(mass)
  while (fuel > 0):
    total += fuel
    fuel = fuel_required(fuel)
  return total

def sum_fuel_requirements(input_file, part1):
  lines = open(input_file).read().splitlines()
  masses = list(map(int, lines))

  if part1:
    fuel_requirements = list(map(fuel_required, masses))
  else:
    fuel_requirements = list(map(fuel_required_with_additional_fuel, masses))

  return sum(fuel_requirements)

if __name__ == '__main__':
  part1_result = sum_fuel_requirements('input.txt', True)
  print(f'Part 1: {part1_result}')

  part2_result = sum_fuel_requirements('input.txt', False)
  print(f'Part 2: {part2_result}')