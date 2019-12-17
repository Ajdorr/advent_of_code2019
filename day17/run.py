from droid import Droid


fp = "day17/in.txt"
with open(fp) as fd:
  code = fd.read()


def part1():
  droid = Droid(code)
  # droid.update_feed()
  print(droid)
  print(f"Alignment: {droid.get_alignment()}")


def part2():
  droid = Droid(code, 2)
  droid.program(
      "A,B,C,A,B",
      "L,12,R,4,R,4,R,8,R,6,R,6,R,4,L,2",
      "10,L,12,R,4,L,12,L,12,R,4,L,4,R,2,L,8",
      "R,12,R,4,L,6,L,8,L,8,L,12,R,4,R,4", False)


# part1()
part2()
