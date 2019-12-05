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

def get_params_3(mem, ip, modes):
  params = []
  params.append(mem[mem[ip+1]] if modes[0] == 0 else mem[ip+1])
  params.append(mem[mem[ip+2]] if modes[1] == 0 else mem[ip+2])
  params.append(mem[ip+3])
  return params

def run_program(instructions):
  mem = init_memory(instructions)

  ip = 0
  cur_input = 1
  while True:
    inst = mem[ip]
    [op_code, modes] = parse_instruction(inst)

    if op_code == 99:
      break
    elif op_code == 1:
      params = get_params_3(mem, ip, modes)
      mem[params[2]] = params[0] + params[1]
      ip += 4
    elif op_code == 2:
      params = get_params_3(mem, ip, modes)
      mem[params[2]] = params[0] * params[1]
      ip += 4
    elif op_code == 3:
      param = mem[ip+1]
      mem[param] = cur_input
      ip += 2
    elif op_code == 4:
      param = mem[ip+1]
      print(mem[param])
      ip += 2
    else:
      raise Exception(f'Unexpected code {op_code}')

def run_part1(instructions):
  run_program(instructions)

if __name__ == '__main__':
  instructions = list(map(int, open('input.txt').read().split(',')))

  print('Part 1:')
  run_part1(instructions)
