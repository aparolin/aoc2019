from itertools import permutations
from queue import Queue
from threading import Thread

class Computer(Thread):

  def __init__(self, program, outputs, max_mem_size=5000):
    Thread.__init__(self)

    self.__mem = None
    self.__outputs = outputs
    self.__max_mem_size = max_mem_size
    self.__ip = 0
    self.__last_output = None
    self.__program_finished = None

    self.__instructions = instructions
    self.__mem = self.__init_memory(instructions)

  def __parse_instruction(self, i):
    i_str = str(i)
    op_code = int(i_str[-2:])

    mode1 = int(i_str[-3]) if len(i_str) >= 3 else 0
    mode2 = int(i_str[-4]) if len(i_str) >= 4 else 0

    return [op_code, [mode1, mode2]]

  def __init_memory(self, instructions):
    mem = [None] * self.__max_mem_size
    for idx, instruction in enumerate(instructions):
      mem[idx] = instruction
    return mem

  def __get_n_params(self, n, ip, modes):
    params = []

    for i in range(0, n):
      #write address parameter
      if i >= len(modes):
        params.append(self.__mem[ip+i+1])
      else:
        params.append(self.__mem[self.__mem[ip+1+i]] if modes[i] == 0 else self.__mem[ip+1+i])
    
    return params

  def set_inputs(self, inputs):
    self.__inputs = inputs

  def run(self):
    self.__program_finished = False

    mem = self.__mem
    ip = self.__ip

    input_counter = 0

    while True:
      inst = mem[ip]
      [op_code, modes] = self.__parse_instruction(inst)

      if op_code == 99:
        self.__outputs.append(self.__last_output)
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
        param = mem[ip+1]
        mem[param] = self.__inputs[input_counter]
        input_counter += 1
        ip += 2
      elif op_code == 4:
        param = mem[ip+1]
        self.__last_output = mem[param]
        print(self.__last_output)
        ip += 2
      elif op_code == 5:
        params = self.__get_n_params(2, ip, modes)
        if params[0] != 0:
          ip = params[1]
        else:
          ip+=3
      elif op_code == 6:
        params = self.__get_n_params(2, ip, modes)
        if params[0] == 0:
          ip = params[1]
        else:
          ip+=3
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
      else:
        raise Exception(f'Unexpected code {op_code}')

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  possible_settings = list(permutations([0,1,2,3,4]))
  outputs = []
  
  for settings in possible_settings:
    output = 0
    for s in settings:
      inputs = [s, output]
      computer = Computer(instructions, outputs)
      computer.set_inputs(inputs)
      computer.start()
      computer.join()
      output = outputs[-1]
      # outputs.append(output)

  print(f'Part 1: {max(outputs)}')
