import math
import numpy as np

def distance(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))

def module(v):
  return math.sqrt(v[0]*v[0]+v[1]*v[1])

def get_detection_count2(grid, row, col):
    up_vector = np.array([-1,0])
    up_vector[0] = up_vector[0]/module(up_vector)
    up_vector[1] = up_vector[1]/module(up_vector)

    detections = []
    dir_vector = up_vector
    step = 0
    angle = 0
    angle_step = 0.01
    
    print(f'using angle step {angle_step}')

    print(f'\ncalculating for point {row},{col}')
    while angle > -2*math.pi:
        # print(f'Trying with angle {angle}')
        while True:
            step += 0.5
            # print(f'Increasing step to {step}')
            pos = np.array([row,col]) + (dir_vector * step)


            # print(pos)

            if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] > len(grid[0]):
              break

            upper_limit = 0.9
            lower_limit = 1 - upper_limit
            frac, whole = math.modf(pos[0])
            if frac > upper_limit:
              possible_row = int(math.ceil(pos[0]))
            elif frac < lower_limit:
              possible_row = int(math.floor(pos[0]))
            else:
              continue
            
            frac, whole = math.modf(pos[1])
            if frac > upper_limit:
              possible_col = int(math.ceil(pos[1]))
            elif frac < lower_limit:
              possible_col = int(math.floor(pos[1]))
            else:
              continue
            
            print(f'{pos[0]},{pos[1]} ===> {possible_row},{possible_col}')
            # possible_row = int(math.floor(pos[0]))
            # possible_col = int(math.floor(pos[1]))
            # threshold = 0.02


            # if distance((pos[0],pos[1]), (possible_row, possible_col)) < threshold:
            if possible_row == row and possible_col == col:
                continue
  
            # print(f'Considering point {possible_row},{possible_col}')
            if possible_row < 0 or possible_row >= len(grid) or possible_col < 0 or possible_col >= len(grid[0]):
                break

            if grid[possible_row][possible_col] == '#' and (possible_row,possible_col) not in detections:
                print(f'detection against point {possible_row},{possible_col}')
                detections.append((possible_row, possible_col))
                break
        
        step = 0
        angle -= angle_step
        rot_mat = np.matrix([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])
        dir_vector = np.array(np.matmul(rot_mat, up_vector))[0]
    
    return detections

def get_detection_count(grid, row, col):
    step = 1
    detections = []

    visibles = set()
    while True:
        outside_grid = True
        row_ranges = list(range(row-step, row+step+1))

        for i in range(len(row_ranges)):
            for c in range(col-step, col+step+1):
                half_range = math.floor(len(row_ranges)/2)
                idx = (half_range + i) % len(row_ranges)
                r = row_ranges[idx]
                # r = (i%(row+step+1))+row-step

                # 4,5,6,7
                # 6,7,4,5

                # i%8-begin

                # ensure checking borders only
                if c > col-step and c < col+step and r > row-step and r < row+step:
                    continue

                # outside grid
                if r >= len(grid) or r < 0 or c >= len(grid[0]) or c < 0:
                    continue
                outside_grid = False

                if grid[r][c] == '#':
                    # check if previous asteroids are not blocking the current one
                    collision = False
                    for asteroid in visibles:
                        if distance(asteroid, (row,col)) + distance(asteroid, (r,c)) < 1.0000001*distance((row,col), (r,c)):
                            collision = True
                    if not collision:
                        detections.append((r,c))
                        visibles.add((r,c))

        if outside_grid:
            break
        step += 1

    # print(f'Point {row},{col} has {detections} detections')
    return detections

def find_best_asteroid(grid):
    max_detections = -math.inf
    best_asteroid_pos = None

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '#':
                detections = len(get_detection_count2(grid, row, col))
                print(detections)
                if detections > max_detections:
                    max_detections = detections
                    best_asteroid_pos = (row,col)

    return {
        'pos': best_asteroid_pos,
        'detections': max_detections
    }

def vaporize_asteroids(grid, best):
    total_vaporized = 0

    done = False
    while not done:
        detections = get_detection_count(grid, best[0], best[1])
        
        for asteroid in detections:
            grid[asteroid[0]][asteroid[1]] = '.'
            total_vaporized += 1

            print(f'{asteroid[0]}, {asteroid[1]}')

            if total_vaporized == 200:
                print(f'Part 2: {asteroid[0]}{asteroid[1]}')
                done = True
                break

if __name__ == '__main__':
    grid = list(map(lambda line: list(line[:-1]), open('input.txt').readlines()))

    best_asteroid = find_best_asteroid(grid)
    print(f'Part 1: {best_asteroid["detections"]}')

    # vaporize_asteroids(grid, best_asteroid['pos'])
    