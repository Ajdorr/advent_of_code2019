import random
import msvcrt
from cpu import Intcode


class Droid:

  def __init__(self, code, map_sz):
    self.cpu = Intcode(code, False, True)
    # self.area_map = [["?" for _ in range(map_sz)] for _ in range(map_sz)]
    self.pos = [map_sz // 2, map_sz // 2]
    with open("day15/map.txt") as fd:
      self.area_map = [[c for c in line] for line in fd.read().splitlines()]
      fd.close()

  def explore_man(self):
    dirs = {"w": 1, "a": 3, "s": 2, "d": 4}
    direction = 1
    rtcd = self.cpu.exec(1)
    while rtcd != 2:
      new_pos = self.mark(direction, "#" if rtcd == 0 else " ")
      if rtcd != 0:
        self.pos = new_pos

      print(self)
      print("Direction (w,a,s,d): ")
      # direction = dirs.get(input("Direction (w, a, s, d): "), 1)
      # a = msvcrt.getch().decode("utf-8")
      key_in = msvcrt.getch().decode("utf-8")
      if key_in == "q":
        with open("day15/map.txt", "w+") as fd:
          fd.write(self.__repr__())
        break

      direction = dirs.get(key_in, 1)

      rtcd = self.cpu.resume(direction)

  def explore_ai(self):
    routes = []
    routes.append([1])
    rtcd = self.cpu.exec(1)
    while rtcd != 2:
      new_pos = self.mark(, "#" if rtcd == 0 else " ")
      if rtcd != 0:
        self.pos = new_pos
      direction = random.randint(1, 4)

      rtcd = self.cpu.resume(direction)
      print("Area")
      print(self)

  def mark(self, direction, char):
    new_pos = self.pos.copy()
    if direction == 1:
      new_pos[1] -= 1
    elif direction == 2:
      new_pos[1] += 1
    elif direction == 3:
      new_pos[0] -= 1
    elif direction == 4:
      new_pos[0] += 1
    else:
      raise RuntimeError(f"Unknown direction {direction}")

    self.area_map[new_pos[1]][new_pos[0]] = char
    return new_pos

  def __repr__(self):
    self.area_map[self.pos[1]][self.pos[0]] = "D"
    ret = "\n".join(["".join([c for c in line]) for line in self.area_map])
    self.area_map[self.pos[1]][self.pos[0]] = " "
    return ret
