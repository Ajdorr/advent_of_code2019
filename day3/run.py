def is_between(t, a0, a1):
  return a0 <= t and t <= a1 if a0 < a1 else a1 <= t and t <= a0


def parse_line(line):
  x = 0
  y = 0
  d = 0
  vert = []
  horz = []
  for word in line.split(","):
    w = int(word[1:])
    if word[0] == "U":
      vert.append((x, y, y + w, d))
      y += w
    elif word[0] == "D":
      vert.append((x, y, y - w, d))
      y -= w
    elif word[0] == "R":
      horz.append((x, x + w, y, d))
      x += w
    elif word[0] == "L":
      horz.append((x, x - w, y, d))
      x -= w
    d += w

  return {"vert": vert, "horz": horz}


def parse_input(fp):
  with open(fp) as fd:
    lines = fd.readlines()

  return [parse_line(line) for line in lines]


def find_intersection(vert, horz):

  intr = []
  for x, y0, y1, dv in vert:
    for x0, x1, y, dh in horz:
      if is_between(x, x0, x1) and is_between(y, y0, y1):
        intr.append((x, y))

  lowest = (1e10, 1e10)
  for x, y in intr:
    if x == 0 and y == 0:
      continue
    if abs(x) + abs(y) < abs(lowest[0]) + abs(lowest[1]):
      lowest = x, y

  return lowest, abs(lowest[0]) + abs(lowest[1])


def find_intr_dist(vert, horz):

  intr = []
  for x, y0, y1, dv in vert:
    for x0, x1, y, dh in horz:
      if is_between(x, x0, x1) and is_between(y, y0, y1):
        intr.append((x, y, dh + abs(x - x0) + dv + abs(y - y0)))

  lowest = (0, 0, 1e10)
  for x, y, d in intr:
    if x == 0 and y == 0:
      continue
    if d < lowest[2]:
      lowest = x, y, d

  return lowest


w1, w2 = parse_input("day4/input.txt")
# w1, w2 = parse_input("day4/sample1.txt")
# w1, w2 = parse_input("day4/sample2.txt")

# print(find_intersection(w1["vert"], w2["horz"]))
# print(find_intersection(w2["vert"], w1["horz"]))
print(find_intr_dist(w1["vert"], w2["horz"]))
print(find_intr_dist(w2["vert"], w1["horz"]))
