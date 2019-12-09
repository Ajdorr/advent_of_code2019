def foo():
  return [3]

arr = [0, 5, 7, 82]
for i, x in enumerate(arr):
  if x > 3:
    arr[i] = x + 7

print(arr)
