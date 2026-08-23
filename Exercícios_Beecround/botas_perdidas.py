import sys

def resolver():
    while True:
        try:
            linha = input().strip()
            if not linha:
                break
            n = int(linha)

            direitos = [0] * 61
            esquerdos = [0] * 61

            for _ in range(n):
                tamanho_str, pe = input().split()
                m = int(tamanho_str)

                if pe == 'D':
                    direitos[m] += 1
                else:
                    esquerdos[m] += 1

            total_pares = 0
            for m in range(30, 61):
                total_pares += min(direitos[m], esquerdos[m])

            print(total_pares)

        except EOFError:
            break

if __name__ == '__main__':
    resolver()