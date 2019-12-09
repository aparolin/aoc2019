import math
from functools import reduce

def get_total_digits(n, layer):
  total = 0
  for r in range(len(layer)):
    for c in range(len(layer[0])):
      if layer[r][c] == n:
        total += 1
  return total

def find_layers(pixels, width, height):
  layers = []

  pixel_idx = 0
  offset = 0

  while pixel_idx < len(pixels)-1:
    layer = [[0 for c in range(width)] for w in range(height)]
    total_zero_digits = 0

    for row in range(height):
      for col in range(width):
        pixel_idx = (width * row) + col + offset
        layer[row][col] = pixels[pixel_idx]
    
        if pixels[pixel_idx] == 0:
          total_zero_digits += 1
    
    layers.append(layer)
    offset += width * height
  
  return layers

def run_part1(layers):
  total_zeros_by_layer = []

  for l in layers:
    total_zero_digits = reduce(lambda a,b: a + b.count(0), l, 0)
    total_zeros_by_layer.append(total_zero_digits)

  layer_fewest_zero_digits = total_zeros_by_layer.index(min(total_zeros_by_layer))
  total_ones = get_total_digits(1, layers[layer_fewest_zero_digits])
  total_twos = get_total_digits(2, layers[layer_fewest_zero_digits])
  print(f'Part 1: {total_ones * total_twos}')

if __name__ == '__main__':
  pixels = list(map(int,open('input.txt').read()))
  layers = find_layers(pixels, 25, 6)
  run_part1(layers)
  
