while True:
    a, b = map(int, input().split())
    if a == 0 and b == 0:
        break
    conta = 0
    contb = 0
    cartas_a = set(input().split())
    cartas_b= set(input().split())

    apenas_a = len(cartas_a - cartas_b)
    apenas_b = len(cartas_b - cartas_a)

    print(min(apenas_a, apenas_b))