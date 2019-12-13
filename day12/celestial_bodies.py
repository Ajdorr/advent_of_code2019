from functools import reduce
from itertools import combinations
import numpy as np


class Planet:

  def __init__(self, position, velocity=[0, 0, 0]):
    self.pos = np.array(position)
    self.vel = np.array(velocity)

  def apply_gravity(self, planet):
    for i in range(len(self.pos)):
      if self.pos[i] < planet.pos[i]:
        self.vel[i] += 1
        planet.vel[i] -= 1
      elif self.pos[i] > planet.pos[i]:
        self.vel[i] -= 1
        planet.vel[i] += 1

  def apply_velocity(self):
    self.pos = self.pos + self.vel

  def calc_energy(self):
    return abs(self.pos).sum() * abs(self.vel).sum()

  def get_linear_vector(self):
    return [*self.pos, *self.vel]

  def __repr__(self):
    return f"<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, " \
           f"<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>"


class Bodies:

  def __init__(self, planets_raw, velocity_raw=None):
    if velocity_raw is not None:
      self.planets = [
          Planet(p, v)
          for p, v in zip(planets_raw, velocity_raw)]
    else:
      self.planets = [Planet(p) for p in planets_raw]

  def apply_gravity(self):
    for i, j in combinations(range(0, len(self.planets)), 2):
      self.planets[i].apply_gravity(self.planets[j])

  def apply_velocity(self):
    for p in self.planets:
      p.apply_velocity()

  def apply_motion(self):
    self.apply_gravity()
    self.apply_velocity()

  def calc_total_energy(self):
    return reduce(
        lambda a, b: a + b,
        map(lambda p: p.calc_energy(), self.planets))

  def get_planet_vectors(self):
    return [
        [(p.pos[i], p.vel[i]) for p in self.planets]
        for i in range(3)]

  def get_linear_vector(self):
    ret = []
    for p in self.planets:
      ret.extend(p.get_linear_vector())
    return ret

  def __repr__(self):
    return "\n".join([p.__repr__() for p in self.planets])


class Spatial_Map:
  root = {}

  def __getitem__(self, key):
    ret = self.root
    for k in key:
      if k in ret:
        ret = ret[k]
      else:
        return None
    return ret

  def __setitem__(self, key, value):
    m = self.root
    for k in key[:-1]:
      if k not in m:
        m[k] = {}
      m = m[k]
    m[key[-1]] = value
