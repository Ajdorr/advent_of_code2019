from area_map import Area_Map
fp = "day18/ex5.txt"
vault = Area_Map(open(fp).read())


def part1():
  routes = vault.find_routes()
  routes.sort(key=lambda r: r[0])
  for r in routes[:20]:
    print(r)
  print(f"Shortest route {routes[0][0]} keys {routes[0][1]}")


part1()
