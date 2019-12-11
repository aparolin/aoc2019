import sys
sys.path.append('../../src/03')

import main

def test_intersections():
  res = main.create_map_of_points(['R8','U5','L5','D3'])
  print(res['intersections'])
