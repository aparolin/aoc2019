from itertools import permutations
from queue import Queue
from threading import Thread
from collections import defaultdict
import time

class Computer(Thread):

  def __init__(self, id, program, in_queue, out_queue, max_mem_size=1000000):
    Thread.__init__(self)

    self.__mem = defaultdict(int)
    self.__id = id
    self.__in_queue = in_queue
    self.__out_queue = out_queue
    self.__max_mem_size = max_mem_size
    self.__ip = 0
    self.__last_output = None
    self.__program_finished = None
    self.__inputs = Queue
    self.__relative_base = 0

    self.__instructions = instructions
    self.__mem = self.__init_memory(instructions)

  def __parse_instruction(self, i):
    i_str = str(i)
    op_code = int(i_str[-2:])

    mode1 = int(i_str[-3]) if len(i_str) >= 3 else 0
    mode2 = int(i_str[-4]) if len(i_str) >= 4 else 0
    mode3 = int(i_str[-5]) if len(i_str) >= 5 else 0

    return [op_code, [mode1, mode2, mode3]]

  def __init_memory(self, instructions):
    for idx, instruction in enumerate(instructions):
      self.__mem[idx] = instruction
    return self.__mem

  def __get_n_params(self, n, ip, modes):
    params = []

    if str(self.__mem[ip])[-1] == '3':
      if modes[0] != 2:
        params.append(self.__mem[ip+1])
      else:
        params.append(self.__mem[ip+1] + self.__relative_base)
      return params

    for i in range(0, n):
      if i == len(modes) -1:
        if modes[i] == 0:
          params.append(self.__mem[ip+1+i])
        else:
          params.append(self.__mem[ip+1+i] + self.__relative_base)
      else:
        if modes[i] == 0:
          params.append(self.__mem[self.__mem[ip+1+i]])
        elif modes[i] == 1:
          params.append(self.__mem[ip+1+i])
        elif modes[i] == 2:
            params.append(self.__mem[self.__mem[ip+1+i] + self.__relative_base])
      
    return params

  def run(self):
    # for some unknown reason, threads need this sleep
    time.sleep(0.000001)
    self.__program_finished = False

    mem = self.__mem
    ip = self.__ip

    while True:
      inst = mem[ip]

      # print(inst)
      [op_code, modes] = self.__parse_instruction(inst)

      if op_code == 99:
        # self.__out_queue.put(self.__last_output)
        break
      elif op_code == 1:
        params = self.__get_n_params(3, ip, modes)
        mem[params[2]] = params[0] + params[1]
        ip += 4
      elif op_code == 2:
        params = self.__get_n_params(3, ip, modes)
        mem[params[2]] = params[0] * params[1]
        ip += 4
      elif op_code == 3:
        params =self.__get_n_params(1, ip, modes)
        print(f'Computer {self.__id} going to read from queue')
        mem[params[0]] = self.__in_queue.get()
        print(f'Computer {self.__id} got value {mem[params[0]]}')
        ip += 2
      elif op_code == 4:
        params =self.__get_n_params(1, ip, modes)
        self.__last_output = params[0]
        print(f'Computer {self.__id} going to print {self.__last_output} to queue')
        self.__out_queue.put(self.__last_output)
        ip += 2
      elif op_code == 5:
        params = self.__get_n_params(2, ip, modes)
        if params[0] != 0:
          ip = params[1]
        else:
          ip += 3
      elif op_code == 6:
        params = self.__get_n_params(2, ip, modes)
        if params[0] == 0:
          ip = params[1]
        else:
          ip += 3
      elif op_code == 7:
        params = self.__get_n_params(3, ip, modes)
        if params[0] < params[1]:
          mem[params[2]] = 1
        else:
          mem[params[2]] = 0
        ip += 4
      elif op_code == 8:
        params = self.__get_n_params(3, ip, modes)
        if params[0] == params[1]:
          mem[params[2]] = 1
        else:
          mem[params[2]] = 0
        ip += 4
      elif op_code == 9:
        params =self.__get_n_params(1, ip, modes)
        self.__relative_base += params[0]
        ip += 2
      else:
        raise Exception(f'Unexpected code {op_code}')

def run_part1(instructions):
  queue = Queue()
  queue.put(1)
  computer = Computer(0, instructions, queue, queue)

  computer.start()
  computer.join()

  print(f'Part 1: {queue.get()}')

def run_part2(instructions):
  queue = Queue()
  queue.put(2)
  computer = Computer(0, instructions, queue, queue)

  computer.start()
  computer.join()

  print(f'Part 2: {queue.get()}')

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  run_part1(instructions)
  run_part2(instructions)