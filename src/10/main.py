import math

def distance(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))

def get_detection_count(grid, row, col):
    step = 1
    detections = 0

    if row == 0 and col == 1:
        x = 2

    visibles = set()
    while True:
        outside_grid = True
        for r in range(row-step, row+step+1):
            for c in range(col-step, col+step+1):
                # ensure checking borders only
                if c > col-step and c < col+step and r > row-step and r < row+step:
                    continue

                # print(f'Checking pos {r},{c}')
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
                        detections += 1
                        visibles.add((r,c))

        if outside_grid:
            break
        step += 1

    # print(f'Point {row},{col} has {detections} detections')
    return detections

def find_best_asteroid(grid):
    detections = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '#':
                detections.append(get_detection_count(grid, row, col))

    # print(detections)
    return max(detections)

if __name__ == '__main__':
    grid = list(map(lambda line: list(line[:-1]), open('input.txt').readlines()))

    max_detections = find_best_asteroid(grid)
    print(f'Part 1: {max_detections}')