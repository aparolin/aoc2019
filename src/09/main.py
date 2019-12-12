from itertools import permutations
from queue import Queue
from threading import Thread
from collections import defaultdict
import time

class Computer(Thread):

  def __init__(self, id, program, in_queue, out_queue):
    Thread.__init__(self)

    self.__mem = defaultdict(int)
    self.__id = id
    self.__in_queue = in_queue
    self.__out_queue = out_queue
    self.__ip = 0
    self.__last_output = None
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

    for i in range(0, n):
      # special handling for operator 3 or registries that will 
      # have data written to
      if i == len(modes) -1 or str(self.__mem[ip])[-1] == '3':
        if modes[i] == 0:
          params.append(self.__mem[ip+1+i])
        else:
          params.append(self.__mem[ip+1+i] + self.__relative_base)

      # for the others, regular rules apply
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

    mem = self.__mem
    ip = self.__ip

    while True:
      inst = mem[ip]
      [op_code, modes] = self.__parse_instruction(inst)

      if op_code == 99:
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
        mem[params[0]] = self.__in_queue.get()
        ip += 2
      elif op_code == 4:
        params =self.__get_n_params(1, ip, modes)
        self.__last_output = params[0]
        # print(f'Out: {self.__last_output}')
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