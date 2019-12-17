# Up, Right, Down, Left
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
with open("day17/map.txt") as fd:
  area_map = [
      [c for c in line]
      for line in fd.read().splitlines()]


def adv(pos, d):
  return (pos[0] + dirs[d][0], pos[1] + dirs[d][1])


def get_map(x, y):
  if x < 0 or x >= 59 or y < 0 or y >= 39:
    return "."
  else:
    return area_map[y][x]


def set_map(x, y, sym):
  area_map[y][x] = sym


def next_rotation(x, y, d):
  if get_map(x - 1, y) == "#":
    return "L" if d == 0 else "R"
  elif get_map(x + 1, y) == "#":
    return "R" if d == 0 else "L"
  elif get_map(x, y - 1) == "#":
    return "L" if d == 1 else "R"
  elif get_map(x, y + 1) == "#":
    return "R" if d == 1 else "L"
  else:
    return "DONE"


def rotate(d, turn):
  if turn == "R":
    return (d + 1) % 4
  elif turn == "L":
    return (d + 3) % 4
  else:
    raise RuntimeError(f"Invalid turn: {turn}")


def print_map():
  print("\n".join([
      "".join([c for c in line])
      for line in area_map]))


def main():
  d = 0
  pos = (58, 18)
  steps = 0
  movements = []

  while True:
    next_pos = adv(pos, d)
    sym = get_map(*next_pos)

    if sym == "#":
      pos = next_pos
      set_map(*pos, "$")
      steps += 1
    elif sym == "$":
      pos = next_pos
      set_map(*pos, "O")
      steps += 1
    else:
      movements.append(str(steps))
      steps = 0
      rot = next_rotation(*pos, d)
      if rot == "DONE":
        break
      d = rotate(d, rot)
      movements.append(rot)
    # print_map()

  print_map()
  print(",".join(movements))


main()
