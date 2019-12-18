def _issubset(superset, subset):
  for a in subset:
    if a not in superset:
      return False
  return True


def _find_common(arr1, arr2):
  for e in arr1:
    if e in arr2:
      return e
  return None


class Path:
  def __init__(self, path, keys_req, keys_enroute):
    self.path = path
    self.steps = len(path)
    self.keys_req = keys_req
    self.keys_enroute = keys_enroute

  def __repr__(self):
    return self.path.__repr__()


class Area_Map:

  def __init__(self, map_raw, start_char="@"):
    self.mp = [
        [c for c in line]
        for line in map_raw.splitlines()]
    self.start = self.get_pos(start_char)
    self.best_steps = 6000

    ignore = [".", "#"]
    self.destinations = {start_char: self.start}
    for j, line in enumerate(self.mp):
      for i, c in enumerate(line):
        if c not in ignore and c.islower():
          self.destinations[c] = (i, j)
    self[self.start] = "."

  def __getitem__(self, pos):
    return self.mp[pos[1]][pos[0]]

  def __setitem__(self, pos, val):
    self.mp[pos[1]][pos[0]] = val

  def get_pos(self, char):
    for j, line in enumerate(self.mp):
      if char in line:
        return (line.index(char), j)

    raise ValueError(f"Unable to find {char}")

  def get_path(self, src, dst):

    # Lists are prepended
    src_paths = [self._flood(src)]
    dst_paths = [self._flood(dst)]
    if dst in src_paths[0]:
      return [dst]
    meet_point = _find_common(src_paths[0], dst_paths[0])
    if meet_point is not None:
      return [meet_point, dst]

    src_paths.insert(0, list(filter(
        lambda p: p != src, self._flood_list(src_paths[0]))))
    dst_paths.insert(0, list(filter(
        lambda p: p != dst, self._flood_list(dst_paths[0]))))
    if len(src_paths[0]) == 0 or len(dst_paths[0]) == 0:
      return None
    meet_point = _find_common(src_paths[0], dst_paths[0])
    if meet_point is None:
      meet_point = _find_common(src_paths[1], dst_paths[0])

    while meet_point is None:
      src_paths.insert(0, list(filter(
          lambda p: p not in src_paths[1],
          self._flood_list(src_paths[0]))))
      dst_paths.insert(0, list(filter(
          lambda p: p not in dst_paths[1],
          self._flood_list(dst_paths[0]))))

      if len(src_paths[0]) == 0 or len(dst_paths[0]) == 0:
        return None

      meet_point = _find_common(src_paths[0], dst_paths[0])
      if meet_point is None:
        meet_point = _find_common(src_paths[1], dst_paths[0])

    path = [meet_point]
    if meet_point in src_paths[0]:
      src_paths = src_paths[1:]
    else:
      src_paths = src_paths[2:]

    if meet_point in dst_paths[0]:
      dst_paths = dst_paths[1:]
    else:
      dst_paths = dst_paths[2:]

    for paths in src_paths:
      path.insert(0, _find_common(paths, self._flood(path[0])))
    for paths in dst_paths:
      path.append(_find_common(paths, self._flood(path[-1])))
    path.append(dst)

    return path

  def get_path_key_req(self, src, dst):
    path = self.get_path(src, dst)

    return Path(path, [
        self[p].lower() for p in path[:-1]
        if self[p] != "." and self[p].isupper()],
        [self[p] for p in path[:-1] if self[p] != "." and self[p].islower()])

  def find_routes(self):
    paths = {
        (src, dst): self.get_path_key_req(src, dst)
        for dst in self.destinations.values()
        for src in self.destinations.values() if src != dst}

    keys = list(filter(lambda k: k != "@", self.destinations.keys()))
    keys.sort()
    self.solutions = []
    self._find_routes(self.start, paths, keys, 0)

    routes = []
    for soln in self.solutions:
        route = [
            paths[(self.destinations[src], self.destinations[dst])]
            for src, dst, in zip(soln, soln[1:])
        ]
        total_steps = sum(map(lambda p: p.steps, route))
        # routes.append((total_steps, soln, route))
        routes.append((total_steps, soln))

    return routes

  def _find_routes(self, pos, paths, keys_req, cur_steps, keys=[]):

    if len(keys_req) == 0:
      self.best_steps = cur_steps
      self.solutions.append(("@", *keys))
      print(f"Best solution {cur_steps} steps; keys: {keys}")

    for key in keys_req:
      dst = self.destinations[key]
      path = paths[(pos, dst)]
      # Check key requirements
      if len(path.keys_req) > 0:
        if not _issubset(keys, path.keys_req):
          continue

      if cur_steps + path.steps >= self.best_steps:
        continue
      if len(list(filter(lambda k: k in keys_req, path.keys_enroute))) > 0:
        continue

      self._find_routes(
          dst, paths, list(filter(lambda k: k != key, keys_req)),
          cur_steps + path.steps, [*keys, key])

  def _flood_list(self, pos_list):
    ret = []
    for p in pos_list:
      ret.extend(self._flood(p))
    return ret

  def _flood(self, pos):
    return list(filter(
        lambda p: self.mp[p[1]][p[0]] != "#",
        [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
         (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]))
