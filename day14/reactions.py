import re
import math


rep_compound = re.compile(r"(\d+) (\w+)")


def _lcm(a, b):
  return a * b // math.gcd(a, b)


class Reaction:

  def __init__(self, react_raw, prod_raw):
    m = rep_compound.search(prod_raw)
    self.product = (m.group(2), int(m.group(1)))
    self.reactants = dict([
        (m.group(2), int(m.group(1)))
        for m in rep_compound.finditer(react_raw)])
    self.runs = 0
    self.leftovers = 0

  def __repr__(self):
    return f"[{self.runs} r{self.leftovers}]: " + \
        ", ".join([f"{q} {r}" for r, q in self.reactants.items()]) + \
        f" => {self.product[1]} {self.product[0]}"


class Reaction_Table:

  def __init__(self, table_raw):
    split_reactions = [line.split(" => ") for line in table_raw.splitlines()]
    self.table = [Reaction(lh, prod_raw) for lh, prod_raw in split_reactions]

  def find_ore_path(self, compound):
    reaction = next(filter(
        lambda r: compound == r.product[0], self.table))

    if reaction is None:
      raise RuntimeError(f"Compound({compound}) not found in table")
    elif "ORE" in reaction.reactants.keys():
      return "ORE"
    else:
      return {
          reactant: self.find_ore_path(reactant)
          for reactant in reaction.reactants.keys()}

  def run_process(self, compound, quantity_req):
    self._process(compound, quantity_req)

    return sum(map(
        lambda r: r.reactants["ORE"] * r.runs,
        filter(lambda r: "ORE" in r.reactants.keys(), self.table)))

  def clear(self):
    for r in self.table:
      r.leftovers = 0
      r.runs = 0

  def _process(self, compound, quantity_req):
    reaction = next(filter(
        lambda r: compound == r.product[0], self.table))

    if reaction is None:
      raise RuntimeError(f"Compound({compound}) not found in table")
    elif reaction.leftovers >= quantity_req:
      reaction.leftovers -= quantity_req
    else:
      quantity_req -= reaction.leftovers
      runs_req = math.ceil(quantity_req / reaction.product[1])
      reaction.runs += runs_req
      reaction.leftovers = (runs_req * reaction.product[1]) - quantity_req

      for reactant, q_req in reaction.reactants.items():
        if reactant != "ORE":
          self._process(reactant, runs_req * q_req)

  def __repr__(self):
    return "\n".join(r.__repr__() for r in self.table)
