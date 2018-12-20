from functools import reduce

s = input('')
print(reduce(lambda acc, (c, e): acc + int(x[0]) * x[1], zip(s[::2], s[1::2]), ''))
