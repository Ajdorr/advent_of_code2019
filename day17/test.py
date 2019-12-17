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


def move_a():
  turn_l()
  move_n("A", 12)
  turn_r()
  move_n("A", 4)
  turn_r()
  move_n("A", 4)
  turn_r()
  move_n("A", 8)
  turn_r()
  move_n("A", 6)
  turn_r()
  move_n("A", 6)
  turn_r()
  move_n("A", 4)
  turn_l()


def move_b():
  move_n("B", 12)
  turn_l()
  move_n("B", 12)
  turn_r()
  move_n("B", 4)
  turn_l()
  move_n("B", 12)
  turn_l()
  move_n("B", 12)
  turn_r()
  move_n("B", 4)
  turn_l()
  move_n("B", 4)
  turn_r()
  move_n("B", 2)
  turn_l()
  move_n("B", 8)


def move_c():
  turn_r()
  move_n("C", 12)
  turn_r()
  move_n("C", 4)
  turn_l()
  move_n("C", 6)
  turn_l()
  move_n("C", 8)
  turn_l()
  move_n("C", 8)
  turn_l()
  move_n("C", 12)
  turn_r()
  move_n("C", 4)
  turn_r()
  move_n("C", 4)


# Main
# L,12,R,4,R,4,R,8,R,6,R,6,R,4,L,12,L,12,R,4,L,12,L,12,R,4,L,4,R,2,L,8,R,12,R,4,L,6,L,8,L,8,L,12,R,4,R,4,L,12,R,4,R,4,R,8,R,6,R,6,R,4,L,12,L,12,R,4,L,12,L,12,R,4,L,4,R,2,L,8,
move_a()
move_b()
move_c()
move_a()
move_b()

print("\n".join([
    "".join([c for c in line])
    for line in area_map]))
