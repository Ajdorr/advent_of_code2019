import math
from asteroid_map import Ast_Map

# fp = "day10/ex4.txt"
fp = "day10/in.txt"
with open(fp) as fd:
  ast_map = Ast_Map([
      [p == "#" for p in l]
      for l in fd.read().splitlines()])
# mx = 13
# my = 11
mx = 11
my = 13


def part1():
  totals = ast_map.compute_total()
  mx = max([max(row) for row in totals])
  for j, row in enumerate(totals):
    if mx in row:
      i = row.index(mx)
      print(f"Max: {mx} - ({i}, {j})")
      return i, j


def sort_clockwise(e):
  dx = e[0] - mx
  dy = e[1] - my

  if dx == 0:
    val = math.pi / 2 if dy > 0 else 3 * math.pi / 2
  else:
    val = math.atan(dy / dx)
    if dy < 0 and dx < 0:
      val += math.pi
    elif dx < 0:
      val += math.pi
    elif dy < 0:
      val += 2 * math.pi

  if val >= 3 * math.pi / 2:
    return val - (3 * math.pi / 2)
  else:
    return val + (math.pi / 2)


def part2():
  vics = ast_map.get_detects(mx, my)
  vics.sort(key=sort_clockwise)
  print(vics[199])


part2()
