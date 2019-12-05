def parse_instruction(i):
  i_str = str(i)
  op_code = int(i_str[-2:])

  mode1 = int(i_str[-3]) if len(i_str) >= 3 else 0
  mode2 = int(i_str[-4]) if len(i_str) >= 4 else 0

  return [op_code, [mode1, mode2]]

def init_memory(instructions):
  mem = [None] * 5000
  for idx, instruction in enumerate(instructions):
    mem[idx] = instruction
  return mem

def get_n_params(n, mem, ip, modes):
  params = []

  for i in range(0, n):
    #write address parameter
    if i >= len(modes):
      params.append(mem[ip+i+1])
    else:
      params.append(mem[mem[ip+1+i]] if modes[i] == 0 else mem[ip+1+i])
  
  return params

def run_program(instructions, input_code):
  mem = init_memory(instructions)

  ip = 0
  while True:
    inst = mem[ip]
    [op_code, modes] = parse_instruction(inst)

    if op_code == 99:
      break
    elif op_code == 1:
      params = get_n_params(3, mem, ip, modes)
      mem[params[2]] = params[0] + params[1]
      ip += 4
    elif op_code == 2:
      params = get_n_params(3, mem, ip, modes)
      mem[params[2]] = params[0] * params[1]
      ip += 4
    elif op_code == 3:
      param = mem[ip+1]
      mem[param] = input_code
      ip += 2
    elif op_code == 4:
      param = mem[ip+1]
      print(mem[param])
      ip += 2
    elif op_code == 5:
      params = get_n_params(2, mem, ip, modes)
      if params[0] != 0:
        ip = params[1]
      else:
        ip+=3
    elif op_code == 6:
      params = get_n_params(2, mem, ip, modes)
      if params[0] == 0:
        ip = params[1]
      else:
        ip+=3
    elif op_code == 7:
      params = get_n_params(3, mem, ip, modes)
      if params[0] < params[1]:
        mem[params[2]] = 1
      else:
        mem[params[2]] = 0
      ip += 4
    elif op_code == 8:
      params = get_n_params(3, mem, ip, modes)
      if params[0] == params[1]:
        mem[params[2]] = 1
      else:
        mem[params[2]] = 0
      ip += 4
    else:
      raise Exception(f'Unexpected code {op_code}')

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  print('Part 1:')
  run_program(instructions, 1)

  print('Part 2:')
  run_program(instructions, 5)