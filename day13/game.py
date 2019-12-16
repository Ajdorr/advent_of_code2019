import numpy as np
from cpu import Intcode
_board_sz = 2898
_id_to_tile = [" ", "#", "X", "=", "O"]


class Game:

  def __init__(self, code, game_mode=1):
    code[0] = game_mode
    self.comp = Intcode(code, halt_on_output=True)
    out_raw = [self.comp.exec()]
    for _ in range(_board_sz - 1):
      out_raw.append(self.comp.resume())

    out = np.array(out_raw)
    out = out.reshape(len(out) // 3, 3)
    x_mx = np.argmax(out[:, 0]) + 1
    y_mx = np.argmax(out[:, 1]) + 1
    self.board = [[0 for _ in range(x_mx)] for _ in range(y_mx)]

    for x, y, tile_id in out:
      self.board[y][x] = tile_id

    if game_mode == 2:
      _, _, self.score = self.step()
    else:
      self.score = 0

  def step(self):
    return self.comp.resume(), self.comp.resume(), self.comp.resume()

  def step_with_input(self, joy_in):
    return self.comp.resume(joy_in), self.comp.resume(), self.comp.resume()

  def update(self, joy_in):
    x, y, arg = self.step_with_input(joy_in)
    self.board[y][x] = arg

    if joy_in != 0:
      x, y, arg = self.step()
      self.board[y][x] = arg

      x, y, arg = self.step()
      self.board[y][x] = arg

    x, y, arg = self.step()
    while x == -1 and y == 0:
      # Update sore
      self.score = arg

      # Delete the block
      x, y, arg = self.step()
      if not self.comp.halt_fg:
        return
      self.board[y][x] = arg

      # Update ball
      x, y, arg = self.step()

    self.board[y][x] = arg

  def get_ball_loc(self):
    for j, row in enumerate(self.board):
      if 4 in row:
        return row.index(4), j

    raise Exception("No ball found")

  def get_paddle_loc(self):
    return self.board[21].index(3)

  def __repr__(self):
    return "\n".join([
        "".join([_id_to_tile[i] for i in row])
        for row in self.board[:23]]) + f"\nScore: {self.score}"
