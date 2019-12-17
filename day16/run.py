bp = [0, 1, 0, -1]
with open("day16/in.txt") as fd:
  in_arr = [int(c) for c in fd.read()]

# in_arr = [int(c) for c in "12345678"]
# in_arr = [int(c) for c in "80871224585914546619083218645595"]
# in_arr = [int(c) for c in "19617804207202209144916044189917"]
# in_arr = [int(c) for c in "69317163492948606335995924319873"]

# in_arr = [int(c) for c in "03036732577212944063491565474664"]
# in_arr = [int(c) for c in "02935109699940807407585447034323"]
# in_arr = [int(c) for c in "03081770884921959731165446850517"]


def fft(in_arr):
  return [
      (abs(sum([
          v * bp[(((i + 1) // (j + 1))) % 4]
          for i, v in enumerate(in_arr)]))) % 10
      for j in range(len(in_arr))]


def fft_phase(in_arr, phase_cnt):
  for _ in range(phase_cnt):
    in_arr = fft(in_arr)

  return in_arr


def fft_light(in_arr, sig_rep, phase_cnt, offset):
  arr_mod = (in_arr * sig_rep)[offset:][::-1]
  for _ in range(phase_cnt):
    total = 0
    for i, v in enumerate(arr_mod):
      total = (total + v) % 10
      arr_mod[i] = total

  return arr_mod[::-1]


def part1():
  out_arr = fft_phase(in_arr, 100)
  print("".join(str(d) for d in out_arr))
  print("".join(str(d) for d in out_arr[:8]))


def part2():
  msg_off = int("".join(str(d) for d in in_arr[:7]))
  out_arr = fft_light(in_arr, 10000, 100, msg_off)
  print("".join(str(d) for d in out_arr[:8]))


# part1()
part2()