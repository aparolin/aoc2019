def run_program(input_file):
    int_codes = list(map(int, open(input_file).read().split(',')))

    pointer = 0

    while True:
        op_code = int_codes[pointer]
        if op_code == 99:
            break

        value1_idx = int_codes[pointer+1]
        value2_idx = int_codes[pointer+2]
        result_idx = int_codes[pointer+3]

        if op_code == 1:
            result = int_codes[value1_idx] + int_codes[value2_idx]
        elif op_code == 2:
            result = int_codes[value1_idx] * int_codes[value2_idx]
        else:
            raise Exception(f'Unexpected opcode: {op_code}')
        int_codes[result_idx] = result

        pointer += 4

    return int_codes

if __name__ == '__main__':
    result_part1 = run_program('input.txt')
    print(f'Part 1: {result_part1[0]}')