origem, destino = input().split()

dx = abs(ord(origem[0]) - ord(destino[0]))

dy = abs(int(origem[1]) - int(destino[1]))

if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
    print("VALIDO")
else:
    print("INVALIDO")