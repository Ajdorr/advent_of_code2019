import math
import numpy as np


def part1(fuels):
  print((np.floor((np.array(fuels) / 3)) - 2).sum())


def part2(fuels):
  def compute(f):
    res = math.floor(f / 3) - 2
    return res + compute(res) if res > 0 else 0

  print(np.array([compute(f) for f in fuels]).sum())


with open("day1/input.txt") as fd:
  fuels = [int(line) for line in fd.readlines()]
  fd.close()

part1(fuels)
part2(fuels)
