from cpu import Intcode

# fp = "day9/ex1.txt"
fp = "day9/in.txt"
with open(fp) as fd:
  code = [int(x) for x in fd.read().split(",")]

comp = Intcode(code, True)


def part1(comp):
  print(comp.exec(1))


def part2(comp):
  print(comp.exec(2))


# part1(comp)
part2(comp)
