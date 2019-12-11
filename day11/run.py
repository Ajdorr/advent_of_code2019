from cpu import Intcode

fp = "day11/code.txt"
with open(fp) as fd:
  text = fd.read()
  bot = Intcode(
      [int(d) for d in text.split(",")],
      halt_on_output=True)
sz = 200


class Navigation:
  x = int(sz / 2)
  y = int(sz / 2)
  direction = "UP"

  def advance(self):
    if self.direction == "UP":
      self.y -= 1
    elif self.direction == "DOWN":
      self.y += 1
    elif self.direction == "RIGHT":
      self.x += 1
    elif self.direction == "LEFT":
      self.x -= 1

  def rotate(self, turn_right_fg):
    if turn_right_fg:
      if self.direction == "UP":
        self.direction = "RIGHT"
      elif self.direction == "RIGHT":
        self.direction = "DOWN"
      elif self.direction == "DOWN":
        self.direction = "LEFT"
      elif self.direction == "LEFT":
        self.direction = "UP"
    else:
      if self.direction == "UP":
        self.direction = "LEFT"
      elif self.direction == "LEFT":
        self.direction = "DOWN"
      elif self.direction == "DOWN":
        self.direction = "RIGHT"
      elif self.direction == "RIGHT":
        self.direction = "UP"


def paint(starting_color):
  hull = [
      [0 for _ in range(sz)]
      for _ in range(sz)]
  nav = Navigation()
  painted_panels = []

  hull[nav.y][nav.x] = starting_color
  hull[nav.y][nav.x] = bot.exec(hull[nav.y][nav.x])
  painted_panels.append((nav.x, nav.y))
  nav.rotate(bot.resume())
  nav.advance()

  while bot.halt_fg:
    hull[nav.y][nav.x] = bot.resume(hull[nav.y][nav.x])
    if (nav.x, nav.y) not in painted_panels:
      painted_panels.append((nav.x, nav.y))
    nav.rotate(bot.resume())
    nav.advance()

  out = "\n".join([
      "".join(["##" if colour else ".." for colour in row])
      for row in hull])
  with open("out.txt", "w+") as fd:
    fd.write(out)
  print(f"Total panels painted: {len(painted_panels)}")


# part 1
# paint(0)

# part 2
paint(1)
