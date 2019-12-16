from reactions import Reaction_Table


# fp = "day14/ex5.txt"
fp = "day14/in.txt"
with open(fp) as fd:
  table = Reaction_Table(fd.read())


def part1():
  ore_req = table.run_process("FUEL", 10)
  print(table)
  print(ore_req)


def part2(ore_cnt):
  fuel_produced = ore_cnt // table.run_process("FUEL", 1)
  ore_req = 0

  while ore_req < ore_cnt:
    table.clear()
    fuel_produced += 1000
    ore_req = table.run_process("FUEL", fuel_produced)

  while ore_req > ore_cnt:
    table.clear()
    fuel_produced -= 1
    ore_req = table.run_process("FUEL", fuel_produced)

  print(table)
  print(ore_req)
  print(f"Fuel produced: {fuel_produced}")


# part1()
# part2(1000000000000)
