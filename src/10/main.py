import math
import numpy as np

def distance(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))

def get_detection_count2(grid, row, col):
    up_vector = np.array([-0.1,0])

    detections = []
    dir_vector = up_vector
    step = 0.1
    angle = 0
    
    while angle < 360:
        while True:
            pos = np.array([row,col]) + dir_vector * step

            possible_row = int(round(pos[0]))
            possible_col = int(round(pos[1]))
            threshold = 0.01

            if abs(possible_row - pos[0]) < threshold and abs(possible_col - pos[1]) < threshold:
                if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
                    break

                if grid[possible_row][possible_col] == '#':
                    detections.append((pos[0], pos[1]))
                    break
            step += 0.1
        
        angle += 0.1
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
                if detections > max_detections:
                    max_detections = detections
                    best_asteroid_pos = (row,col)

    # print(detections)
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
    