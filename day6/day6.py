class Orb_Map:
  def __init__(self, raw_data):
    self.map = [line.split(")") for line in raw_data.split("\n")]

  def find(self, key):
    return list(filter(lambda orb: orb[0] == key, self.map))

  def get_orbit(self, key):
    return next(filter(lambda orb: orb[1] == key, self.map))[0]

  def part1(self, orb, depth):
    result = 0
    for _, body in self.find(orb):
      result += self.part1(body, depth + 1)

    return result + depth

  def get_hierarchy(self, orb):
    ret = [orb]
    while ret[0] != "COM":
      ret.insert(0, self.get_orbit(ret[0]))

    return ret


def part2(orb_map):
  hier_you = orb_map.get_hierarchy("YOU")
  hier_san = orb_map.get_hierarchy("SAN")

  com_anc = [y for y, s in zip(hier_you, hier_san) if y == s][-1]
  print(f"Common Ancestor: {com_anc}")
  path_you = hier_you[hier_you.index(com_anc) + 1:]
  path_san = hier_san[hier_san.index(com_anc) + 1:]
  print(f"Total distance {len(path_you) + len(path_san) - 2}")


# fp = "day6/sample1.txt"
# fp = "day6/sample2.txt"
fp = "day6/input.txt"
with open(fp) as fd:
  orb_map = Orb_Map(fd.read())

# orb_map.part1("COM", 0)
part2(orb_map)
