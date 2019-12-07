import numpy as np
from itertools import permutations
from functools import reduce
from cpu import Intcode

# fp = "day7/example5.txt"
fp = "day7/input.txt"
with open(fp) as fd:
  text = fd.read()
  fd.close()
  code = [int(c) for c in text.split(",")]


def amplifier_sequencer(amplifiers, phase_seq, amp_in=0):
  for amp, seq in zip(amplifiers, phase_seq):
    if amp.halt_fg:
      amp_in = amp.resume([amp_in])
    else:
      amp_in = amp.exec([seq, amp_in])

  return amp_in


def amplifier_feedback(amplifiers, phase_seq):
  amp_in = amplifier_sequencer(amplifiers, phase_seq, 0)

  while reduce(lambda a, b: a and b, map(lambda amp: amp.halt_fg, amplifiers)):
    amp_in = amplifier_sequencer(amplifiers, phase_seq, amp_in)

  return amp_in


def part1():
  amplifiers = [Intcode(code) for _ in range(5)]

  amp_out = np.array([
      (amplifier_sequencer(amplifiers, phase_seq), phase_seq)
      for phase_seq in permutations(range(0, 5), 5)])

  max_ndx = np.argmax(amp_out[:, 0])
  print(amp_out[max_ndx])


def part2():
  amplifiers = [Intcode(code, halt_on_output=True) for _ in range(5)]

  amp_out = np.array([
      (amplifier_feedback(amplifiers, phase_seq), phase_seq)
      for phase_seq in permutations(range(5, 10), 5)])

  max_ndx = np.argmax(amp_out[:, 0])
  print(amp_out[max_ndx])


part2()
# print(amplifier_sequencer((3, 1, 4, 2, 0)))
