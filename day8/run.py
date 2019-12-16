import numpy as np


def shape(img, width, height):
  layer_len = width * height
  return [
      [
          img[h + l: h + l + width]
          for h in range(0, layer_len, width)
      ]
      for l in range(0, len(img), layer_len)
  ]


def get_layers(img, width, height):
  layer_len = width * height
  return [img[l:l + layer_len] for l in range(0, len(img), layer_len)]


def count_digits(img, digit):
  return len(tuple(filter(lambda d: d == digit, img)))


def det_colour(img, x, y):

  for l in img:
    if l[y][x] == 0:
      return "  "
    elif l[y][x] == 1:
      return "XX"

  return "~~"


def part1(img, width, height):
  img_layers = get_layers(img, width, height)

  layers_zero_cnt = np.array([count_digits(img, 0) for img in img_layers])

  lowest = img_layers[np.argmin(layers_zero_cnt)]
  out = count_digits(lowest, 1) * count_digits(lowest, 2)
  print(out)


def part2(img_raw, width, height):
  img = shape(img_raw, width, height)

  render = [
      [det_colour(img, x, y) for x in range(0, width)]
      for y in range(0, height)
  ]

  for row in render:
    print("".join(row))


# fp = "day8/sample2.txt"
fp = "day8/input.txt"
with open(fp) as fd:
  text = fd.read()
  img = [int(s) for s in text]

# part1(img, 25, 6)
part2(img, 25, 6)
