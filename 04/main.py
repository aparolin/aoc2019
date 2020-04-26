def valid_adjascent_digits(p):
  total_repeating = 1
  for i in range(1, len(p)):
    if p[i] == p[i-1]:
      total_repeating += 1
    else:
      if total_repeating == 2:
        return True
      total_repeating = 1

  return True if total_repeating == 2 else False

def valid_password(p, part2):
  no_decreasing_digits = True
  adjascent_digits = False
  for i in range(1, len(p)):
    if int(p[i]) < int(p[i-1]):
      no_decreasing_digits = False
    if p[i] == p[i-1]:
      adjascent_digits = True

  if part2:
    adjascent_digits = valid_adjascent_digits(p)

  return adjascent_digits and no_decreasing_digits

def get_total_passwords_in_range(l1, l2, part2=False):
  #134792 to 675810
  total = 0
  for p in range(l1, l2+1):
    valid = valid_password(str(p), part2)
    # print(f'{p}, {valid}')
    if valid_password(str(p), part2):
      total += 1
  
  return total

if __name__ == '__main__':
  print(f'Part 1: {get_total_passwords_in_range(134792, 675810)}')
  print(f'Part 2: {get_total_passwords_in_range(134792, 675810, True)}')