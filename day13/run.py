import numpy as np
from game import Game
from cpu import Intcode

board_sz = 2898
fp = "day13/in.txt"
with open(fp) as fd:
  code = [int(c) for c in fd.read().split(",")]

id_to_tile = [".", "#", "X", "-", "O"]


def print_board(board):
  print("\n".join(
      [
          "".join([id_to_tile[i] for i in row])
          for row in board[:23]]))


def build_board(comp_out):
  out = np.array(comp_out)
  out = out.reshape(len(out) // 3, 3)

  x_mx = np.argmax(out[:, 0]) + 1
  y_mx = np.argmax(out[:, 1]) + 1
  board = [[0 for _ in range(x_mx)] for _ in range(y_mx)]

  for x, y, tile_id in out:
    board[y][x] = tile_id

  return board


def get_update(comp, joy_in):
  return comp.resume(joy_in), comp.resume(joy_in), comp.resume(joy_in)


def update_board(comp, board, joy_in):
  for i in range(board_sz - 1):
    x, y, t_id = get_update(comp, joy_in)
    board[y][x] = t_id


def part1():
  comp = Intcode(code, halt_on_output=True)
  r = comp.exec()
  comp_out = []
  while comp.halt_fg:
    comp_out.append(r)
    r = comp.resume()

  out = np.array(comp_out)
  out = out.reshape(len(out) // 3, 3)

  unique, counts = np.unique(out[:, 2], return_counts=True)
  print(dict(zip(unique, counts)))


def part2():
  g = Game(code, 2)
  print(g)

  i = 1
  while g.comp.halt_fg:
    g.update(i)
    print(g)

    x, _ = g.get_ball_loc()
    p = g.get_paddle_loc()
    if p < x:
      i = 1
    elif p > x:
      i = -1
    else:
      i = 0

    # time.sleep(0.05)


part2()
