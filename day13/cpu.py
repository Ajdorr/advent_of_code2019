class Intcode:

  def __init__(self, code, verbose=False, halt_on_output=False):
    self._code = code
    self._code.extend([0] * len(code) * 8)
    self.verbose = verbose
    self.halt_fg = False
    self.halt_on_output = halt_on_output
    self.input = []

  def exec(self, *input_values):
    self.ep = 0
    self.rel_base = 0
    self.code = self._code.copy()
    return self.resume(*input_values)

  def resume(self, *input_values):
    self.halt_fg = False
    self.input.extend(input_values)

    while self.code[self.ep] != 99:
      op, self.parm_cds = self._slice_op(str(self.code[self.ep]))

      instr = self.instr_set[op]
      instr["f"](self, *self._get_args(instr["sz"] - 1))

      if instr["inc_ep"]:
        self.ep += instr["sz"]

      if self.halt_fg:
        break

    return self.output

  def _slice_op(self, code_str):
    code_str = code_str.zfill(5)
    return int(code_str[-2:]), [int(x) for x in code_str[-3::-1]]

  def _get_args(self, arg_cnt):
    return self.code[self.ep + 1:self.ep + arg_cnt + 1]

  def _resolve_args(self, *args):
    args = list(args)
    for i, arg in enumerate(args):
      if self.parm_cds[i] == 0:
        args[i] = self.code[arg]
      elif self.parm_cds[i] == 2:
        args[i] = self.code[self.rel_base + arg]

    return args

  def _resolve_store(self, addr, parm_ndx, val):
    if self.parm_cds[parm_ndx] == 0:
      self.code[addr] = val
    elif self.parm_cds[parm_ndx] == 2:
      self.code[self.rel_base + addr] = val
    else:
      raise Exception("Invalid parm code")

  def _instr1(self, a, b, y):
    a, b = self._resolve_args(a, b)
    self._resolve_store(y, 2, a + b)

  def _instr2(self, a, b, y):
    a, b = self._resolve_args(a, b)
    self._resolve_store(y, 2, a * b)

  def _instr3(self, x):
    self._resolve_store(x, 0, self.input.pop(0))

  def _instr4(self, x):
    x = self._resolve_args(x)[0]

    if self.verbose:
      print(f"Output: {x}")

    self.halt_fg = self.halt_on_output
    self.output = x

  def _instr5(self, a, b):
    a, b = self._resolve_args(a, b)

    if a != 0:
      self.ep = b
    else:
      self.ep += 3

  def _instr6(self, a, b):
    a, b = self._resolve_args(a, b)

    if a == 0:
      self.ep = b
    else:
      self.ep += 3

  def _instr7(self, a, b, y):
    a, b = self._resolve_args(a, b)
    self._resolve_store(y, 2, 1 if a < b else 0)

  def _instr8(self, a, b, y):
    a, b = self._resolve_args(a, b)
    self._resolve_store(y, 2, 1 if a == b else 0)

  def _instr9(self, x):
    self.rel_base = self.rel_base + self._resolve_args(x)[0]

  instr_set = [
      None,
      {"sz": 4, "f": _instr1, "inc_ep": True},
      {"sz": 4, "f": _instr2, "inc_ep": True},
      {"sz": 2, "f": _instr3, "inc_ep": True},
      {"sz": 2, "f": _instr4, "inc_ep": True},
      {"sz": 3, "f": _instr5, "inc_ep": False},
      {"sz": 3, "f": _instr6, "inc_ep": False},
      {"sz": 4, "f": _instr7, "inc_ep": True},
      {"sz": 4, "f": _instr8, "inc_ep": True},
      {"sz": 2, "f": _instr9, "inc_ep": True},
  ]
