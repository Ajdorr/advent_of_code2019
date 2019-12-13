import re
import math
from functools import reduce
from celestial_bodies import Bodies

vec_pttrn = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
fp = "day12/in.txt"
with open(fp) as fd:
  bodies = Bodies([
      (int(m.group(1)), int(m.group(2)), int(m.group(3)))
      for m in vec_pttrn.finditer(fd.read())])


def part1():
  # print("After 0 steps:")
  # print(bodies)
  for i in range(1000):
    bodies.apply_motion()
    # print(f"After {i + 1} steps:")
    # print(bodies)

  print(f"Total Energy: {bodies.calc_total_energy()}")


def lcm(a, b):
  return abs(a * b) // math.gcd(a, b)


def find_cycle(arr, vec):
  if vec not in arr:
  # if vec != arr[0]:
    return None
  i = arr.index(vec)

  # i_1 = arr[i + 1:].index(vec) + i + 1
  arr_len2 = (len(arr) - i) // 2
  eq_fg = reduce(
      lambda a, b: a and b,
      map(lambda a: a[0] == a[1],
          zip(arr[i:arr_len2], arr[arr_len2:])))
  # start position and length
  if eq_fg:
    return i, arr_len2
  else:
    return None


def part2():

  x, y, z = bodies.get_planet_vectors()
  x_arr = [x]
  y_arr = [y]
  z_arr = [z]
  res_x, res_y, res_z = (None, None, None)

  i = 1
  while True:
    bodies.apply_motion()
    x, y, z = bodies.get_planet_vectors()
    if res_x is None:
      res_x = find_cycle(x_arr, x)
      x_arr.append(x)
    if res_y is None:
      res_y = find_cycle(y_arr, y)
      y_arr.append(y)
    if res_z is None:
      res_z = find_cycle(z_arr, z)
      z_arr.append(z)

    if res_x and res_y and res_z:
      print(f"Cycle repeat x: start({res_x[0]}) length({res_x[1]})")
      print(f"Cycle repeat y: start({res_y[0]}) length({res_y[1]})")
      print(f"Cycle repeat z: start({res_z[0]}) length({res_z[1]})")
      print(f"Repeat at {lcm(lcm(res_x[1], res_y[1]), res_z[1])}")
      break
    i += 1


part2()
