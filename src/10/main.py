import math

class Asteroid:
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

def distance(ast1, ast2):
  return math.sqrt((ast1.x - ast2.x)**2 + (ast1.y - ast2.y)**2)

def in_the_way(ast1, ast2, blocker, slope):
  distance_between_asteroids = distance(ast1, ast2)
  distance_to_blocker = distance(ast1, blocker)

  try:
    same_side_of_line = (ast2.x - ast1.x)/abs(ast2.x - ast1.x) == (blocker.x - ast1.x)/abs(blocker.x - ast1.x)
    if ast2.y != ast1.y:
      same_side_of_line = same_side_of_line and (ast2.y - ast1.y)/abs(ast2.y - ast1.y) == (blocker.y - ast1.y)/abs(blocker.y - ast1.y)
  except ZeroDivisionError:
    return False
  
  return distance_to_blocker < distance_between_asteroids and \
    same_side_of_line and (blocker.y - ast1.y) == slope * (blocker.x - ast1.x)

def calculate_line_of_sight(asteroid_set, ast):
  line_of_sight = 0

  for neighbor in asteroid_set:
    # print(f'Checking neighbor {neighbor}')

    # same asteroid, skip it
    if neighbor == ast:
      continue

    direct_sight = True
    if ast.x != neighbor.x:
      slope = (ast.y - neighbor.y) / (ast.x - neighbor.x)

      for possible_blocker in asteroid_set:
        # print(f'Checking possible blocker {possible_blocker}')
        # avoid checking for asteroids in the edges of the line
        if possible_blocker in [ast, neighbor]:
          continue

        if in_the_way(ast, neighbor, possible_blocker, slope):
          direct_sight = False
          break
    else:
      asteroids_distance = abs(ast.y - neighbor.y)
      for possible_blocker in asteroid_set:
        # avoid checking for asteroids in the edges of the line
        if possible_blocker in [ast, neighbor]:
          continue
        
        # avoid checking if there's a blocker on the other side of the y axis in relation to the neighbor being evaluated
        if (neighbor.y > ast.y and possible_blocker.y < ast.y) or (neighbor.y < ast.y and possible_blocker.y > ast.y):
          continue

        if possible_blocker.x == ast.x and abs(possible_blocker.y - ast.y) < asteroids_distance:
          direct_sight = False
          break
    
    if direct_sight:
      line_of_sight += 1

  return line_of_sight

def find_best_asteroid(asteroids_set):
  best_asteroid = None
  max_line_of_sight = 0

  for asteroid in asteroids_set:
    # print(f'Checking asteroid {asteroid}')
    line_of_sight = calculate_line_of_sight(asteroids_set, asteroid)

    if line_of_sight > max_line_of_sight:
      best_asteroid = asteroid
      max_line_of_sight = line_of_sight

    # print(f'Asteroid {asteroid} has line of sight of {line_of_sight}')

  return best_asteroid, max_line_of_sight

if __name__ == '__main__':
    asteroids_set = get_asteroids_set('input.txt')
    print(f'Part 1: {find_best_asteroid(asteroids_set)}')

    # best_asteroid = find_best_asteroid(grid)
    # print(f'Part 1: {best_asteroid["detections"]}')