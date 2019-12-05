def part1_criteria(n):
  double_fg = False
  n_str = str(n)

  for d0, d1 in zip(n_str, n_str[1:]):
    if int(d0) > int(d1):
      return False
    if d0 == d1:
      double_fg = True

  return double_fg


def part2_criteria(n):
  digits = [int(d) for d in str(n)]

  for d0, d1 in zip(digits, digits[1:]):
    if d0 > d1:
      return False

  digitCnt = [0] * 10
  for n in digits:
    digitCnt[n] += 1

  return 2 in digitCnt


# results = [n for n in range(134792, 675810) if part1_criteria(n)]
results = [n for n in range(134792, 675810) if part2_criteria(n)]
print(results)
print(len(results))
