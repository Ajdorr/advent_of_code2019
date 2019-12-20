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
    self.best_steps = 1e8

    ignore = [".", "#"]
    self.destinations = {start_char: self.start}
    for j, line in enumerate(self.mp):
      for i, c in enumerate(line):
        if c not in ignore and c.islower():
          self.destinations[c] = (i, j)
    self[self.start] = "."

    self.paths = {
        src: {
            dst: self.get_path_key_req(src, dst)
            for dst in self.destinations.values() if src != dst}
        for src in self.destinations.values()}

    keys = list(filter(lambda k: k != "@", self.destinations.keys()))
    keys.sort()
    self.free_keys = [
        key for key in keys
        if len(self.paths[self.start][self.destinations[key]].keys_req) == 0]

    self.closest_keys = {
        self._closest_key(key): key
        for key in keys if key not in self.free_keys}

    self.unlocked_keys = {
        key: [
            k for k in keys
            if k != key and key in self.paths[self.start][self.destinations[k]].keys_req]
        for key in keys}

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
    keys = list(filter(lambda k: k != "@", self.destinations.keys()))
    keys.sort()
    self.solutions = []

    self._find_routes_locked(
        self.start, self.free_keys,
        [key for key in keys if key not in self.free_keys], 0)
    # self._find_routes(self.start, keys, 0)

    routes = []
    for soln in self.solutions:
        route = [
            self.paths[self.destinations[src]][self.destinations[dst]]
            for src, dst, in zip(soln, soln[1:])
        ]
        total_steps = sum(map(lambda p: p.steps, route))
        # routes.append((total_steps, soln, route))
        routes.append((total_steps, soln))

    return routes

  def _closest_key(self, key):
    lowest_steps = 1e8
    dst_pos = self.destinations[key]
    for src_key, pos in self.destinations.items():
      if src_key == "@" or src_key == key:
        continue

      if self.paths[pos][dst_pos].steps < lowest_steps:
        cur_key = src_key
        lowest_steps = self.paths[pos][dst_pos].steps

    return cur_key

  def _find_routes(self, pos, req_keys, cur_steps, keys=[]):

    if len(req_keys) == 0 and cur_steps <= self.best_steps:
      self.best_steps = cur_steps
      self.solutions.append(("@", *keys))
      print(f"Solution {cur_steps} steps; keys: {keys}")

    for key in req_keys:
      dst = self.destinations[key]
      path = self.paths[pos][dst]

      if cur_steps + path.steps > self.best_steps:
        continue
      if not _issubset(keys, path.keys_req):
        continue
      # if len(list(filter(lambda k: k in free_keys, path.keys_enroute))) > 0:
        # continue

      self._find_routes(
          dst, list(filter(lambda k: k != key, req_keys)),
          cur_steps + path.steps, [*keys, key])

  def _find_routes_locked(self, pos, free_keys, locked_keys, cur_steps, keys=[]):

    if len(free_keys) == 0:
      if len(locked_keys) == 0:
        if cur_steps <= self.best_steps:
          self.best_steps = cur_steps
          self.solutions.append(("@", *keys))
          print(f"Solution {cur_steps} steps; keys: {keys}")
      elif len(locked_keys) > 0:
        self._find_routes(pos, locked_keys, cur_steps, keys)

    for key in free_keys:
      dst = self.destinations[key]
      path = self.paths[pos][dst]

      if cur_steps + path.steps > self.best_steps:
        continue
      # if len(list(filter(lambda k: k in free_keys, path.keys_enroute))) > 0:
        # continue

      cur_keys = [*keys, key]
      new_free_keys = list(filter(lambda k: k != key, free_keys))
      new_locked_keys = locked_keys.copy()
      c_key = self.closest_keys.get(key)
      steps = cur_steps + path.steps
      if c_key is not None and c_key in locked_keys:
        c_dst = self.destinations[c_key]
        if _issubset(cur_keys, self.paths[dst][c_dst].keys_req):
          steps += self.paths[dst][c_dst].steps
          dst = c_dst
          cur_keys.append(c_key)
          new_locked_keys.remove(c_key)

      for u_key in self.unlocked_keys[key]:
        unlocked_path = self.paths[dst][self.destinations[u_key]]
        if _issubset(cur_keys, unlocked_path.keys_req) and _issubset(cur_keys, unlocked_path.keys_enroute):
          self._find_routes_locked(
              self.destinations[u_key], new_free_keys,
              list(filter(lambda k: k != u_key, new_locked_keys)),
              steps + unlocked_path.steps, [*cur_keys, u_key])

      self._find_routes_locked(
          dst, new_free_keys, new_locked_keys, steps, cur_keys)

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
