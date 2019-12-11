from itertools import permutations

class Computer:

  def __init__(self, max_mem_size=5000):
    self.__mem = None
    self.__max_mem_size = max_mem_size

  def load(self, instructions):
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

  def run_program(self, inputs):
    if self.__mem is None:
      raise Exception('No program loaded')

    mem = self.__mem
    output = None
    input_counter = 0

    ip = 0
    while True:
      inst = mem[ip]
      [op_code, modes] = self.__parse_instruction(inst)

      if op_code == 99:
        return output
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
        mem[param] = inputs[input_counter]
        input_counter += 1
        ip += 2
      elif op_code == 4:
        param = mem[ip+1]
        output = mem[param]
        print(output)
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

  computer = Computer()
  computer.load(instructions)
  for settings in possible_settings:
    output = 0
    for s in settings:
      inputs = [s, output]
      output = computer.run_program(inputs)
      outputs.append(output)

  print(f'Part 1: {max(outputs)}')
