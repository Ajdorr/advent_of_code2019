from droid import Droid

fp = "day15/in.txt"
with open(fp) as fd:
  droid = Droid([int(w) for w in fd.read().split(",")], 50)


def part1():
  # droid.explore_ai(1337)
  droid.explore_man()


part1()

print(droid)
