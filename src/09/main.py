from itertools import permutations
from queue import Queue
from computer import Computer

def execute_with_input(instructions, input):
  queue = Queue()
  queue.put(input)
  computer = Computer(0, instructions, queue, queue)

  computer.start()
  computer.join()

  return queue.get()

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  print(f'Part 1: {execute_with_input(instructions, 1)}')
  print(f'Part 2: {execute_with_input(instructions, 2)}')