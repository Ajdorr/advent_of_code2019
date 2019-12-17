# Up, Right, Down, Left
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
d = 0
pos = [58, 18]

with open("day17/map.txt") as fd:
  area_map = [
      [c for c in line]
      for line in fd.read().splitlines()]


def move(sym):
  pos[0] += dirs[d][0]
  pos[1] += dirs[d][1]
  area_map[pos[1]][pos[0]] = sym if area_map[pos[1]][pos[0]] != "." else "!"


def move_n(sym, n):
  for _ in range(n):
    move(sym)


def turn_r():
  global d
  d = (d + 1) % 4


def turn_l():
  global d
  d = (d + 3) % 4


def move_code(sym, code):
  for c in code.split(","):
    if c == "L":
      turn_l()
    elif c == "R":
      turn_r()
    else:
      move_n(sym, int(c))


def move_a():
  move_code("A", "L,12,R,4,R,4")


def move_b():
  move_code("B", "R,12,R,4,L,12")


def move_c():
  move_code("C", "R,12,R,4,L,6,L,8,L,8")


# Main
move_a()
move_b()
move_b()

move_c()
move_c()
move_a()
move_a()

move_b()
move_b()
move_c()

print("\n".join([
    "".join([c for c in line])
    for line in area_map]))
