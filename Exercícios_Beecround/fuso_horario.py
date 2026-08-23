n = map(int, input().split())

a = sum(n)

if a == 24:
    print(0)
elif a > 24:
    print(a - 24)
elif a < 0:
    print(a + 24)
else:
    print(a)