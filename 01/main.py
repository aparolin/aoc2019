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

def sum_fuel_requirements(input_file):
  lines = open(input_file).read().splitlines()
  masses = list(map(int, lines))

  total_part1 = 0
  total_part2 = 0
  for m in masses:
    total_part1 += fuel_required(m)
    total_part2 += fuel_required_with_additional_fuel(m)

  return {
    'part1': total_part1,
    'part2': total_part2
  }

if __name__ == '__main__':
  results = sum_fuel_requirements('input.txt')
  print(f"Part 1: {results['part1']}")
  print(f"Part 2: {results['part2']}")