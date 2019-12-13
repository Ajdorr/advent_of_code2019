import math


def lcm(a, b):
  return abs(a * b) // math.gcd(a, b)


x = 2028
y = 5898
z = 4702
p = x * y * 7

print(lcm(lcm(x, y), z))
