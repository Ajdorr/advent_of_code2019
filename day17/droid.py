from cpu import Intcode


class Droid:

  def __init__(self, code, mode=1):
    self.cpu = Intcode(code, halt_on_output=True)
    self.cpu._code[0] = mode
    self.update_feed()

  def update_feed(self):
    out = [str(chr(self.cpu.exec()))]
    for _ in range(2340):
      out.append(str(chr(self.cpu.resume())))

    out_str = "".join(out)
    self.area_map = [
        [c for c in line]
        for line in out_str.splitlines()]
    print(self)

  def read_line(self):
    ret = -1
    rtcd = []
    while ret != 10:
      ret = self.cpu.resume()
      rtcd.append(ret)

    return "".join([chr(c) for c in rtcd[:-1]])

  def input_read_line(self, *cpu_in):
    ret = [self.cpu.resume(*cpu_in)]
    while ret[-1] != 10:
      ret.append(self.cpu.resume())

    return "".join([chr(c) for c in ret[:-1]])

  def _check_alignment(self, i, j):
    return (
        self.area_map[j - 1][i] == "#" and
        self.area_map[j][i - 1] == "#" and
        self.area_map[j][i + 1] == "#" and
        self.area_map[j + 1][i] == "#")

  def get_alignment(self):
    ret = 0
    for j, row in enumerate(self.area_map[1:-1]):
      for i, v in enumerate(row[1:-1]):
        if v == "#" and self._check_alignment(j + 1, i + 1):
          ret += (i + 1) * (j + 1)

    return ret

  def program(self, main, f_a, f_b, f_c, display_camera=True):

    print(self.read_line())
    main_int = [ord(c) for c in main]
    f_a_int = [ord(c) for c in f_a]
    f_b_int = [ord(c) for c in f_b]
    f_c_int = [ord(c) for c in f_c]

    print(self.input_read_line(*main_int, ord("\n")))
    print(self.input_read_line(*f_a_int, ord("\n")))
    print(self.input_read_line(*f_b_int, ord("\n")))
    print(self.input_read_line(*f_c_int, ord("\n")))
    print(self.input_read_line(
        ord('y') if display_camera else ord('n'), ord("\n")))

    if display_camera:
      while self.cpu.halt_fg:
        self.update_feed()
        print(self)
    else:
      for _ in range(40):
        print(self.read_line())
      print(self.cpu.resume())

  def __repr__(self):
    return "\n".join([
        "".join(c for c in line)
        for line in self.area_map])
