def gcd(a, b):
  if a == 1 or b == 1:
    return 1
  elif a == b:
    return a
  elif a > b:
    ret = _gcd(a, b)
    return ret if ret > 0 else b
  else:
    ret = _gcd(b, a)
    return ret if ret > 0 else a


def _gcd(a, b):
  r = a % b
  if r == 0:
    return 0

  res = _gcd(b, r)
  return r if res == 0 else res


class Ast_Map:

  def __init__(self, ast_map):
    self.ast_map = ast_map
    self.width = len(ast_map[0])
    self.height = len(ast_map)

  def is_visible(self, x, y, a, b):

    d_x = x - a
    d_y = y - b

    if d_x == 0:
      r = abs(d_y)
      d_y = int(d_y / abs(d_y))
    elif d_y == 0:
      r = abs(d_x)
      d_x = int(d_x / abs(d_x))
    else:
      r = gcd(abs(d_x), abs(d_y))
      if r == 0:
        return True
      d_x = int(d_x / r)
      d_y = int(d_y / r)

    for i in range(1, r):
      if self.ast_map[i * d_y + b][i * d_x + a]:
        return False

    return True

  def clear(self, x, y):
    if self.ast_map[y][x]:
      self.ast_map[y][x] = False
    else:
      print(f"No asteroid found at ({x},{y})")

  def get_detects(self, x, y):

    ret = []
    for j in range(self.height):
      for i in range(self.width):

        # Skip all empty cells
        if not self.ast_map[j][i]:
          continue
        elif x == i and y == j:
          continue
        elif self.is_visible(x, y, i, j):
          ret.append((i, j))

    return ret

  def compute_total(self):
    return [
        [
            len(self.get_detects(i, j)) if ast else -1
            for i, ast in enumerate(row)]

        for j, row in enumerate(self.ast_map)]

  def __repr__(self):
    return "\n".join([
        "".join(["#" if ast else "." for ast in row])
        for row in self.ast_map])
