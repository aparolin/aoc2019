def run_program(memory):
    pointer = 0

    while True:
        op_code = memory[pointer]
        if op_code == 99:
            break

        value1_idx = memory[pointer+1]
        value2_idx = memory[pointer+2]
        result_idx = memory[pointer+3]

        if op_code == 1:
            result = memory[value1_idx] + memory[value2_idx]
        elif op_code == 2:
            result = memory[value1_idx] * memory[value2_idx]
        else:
            raise Exception(f'Unexpected opcode: {op_code}')
        memory[result_idx] = result
        pointer += 4

    return memory[0]

def run_part1(memory):
    memcopy = memory[:]
    memcopy[1] = 12
    memcopy[2] = 2
    return run_program(memcopy)

def run_part2(memory):
    expected_result_part2 = 19690720
    done = False
    for noun in range(0, 100):
        for verb in range(0, 100):
            memcopy = memory[:]

            memcopy[1] = noun
            memcopy[2] = verb

            if run_program(memcopy) == expected_result_part2:
                result_part2 = (100 * noun) + verb
                done = True
                break

        if done:
            break

    return result_part2

if __name__ == '__main__':
    memory = list(map(int, open('input.txt').read().split(',')))

    print(f'Part 1: {run_part1(memory)}')
    print(f'Part 2: {run_part2(memory)}')
