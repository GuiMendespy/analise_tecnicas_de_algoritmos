def mover_linha_esquerda(linha):
    sem_zeros = [x for x in linha if x != 0]
    fundidos = []
    i = 0
    
    # Funde blocos adjacentes iguais
    while i < len(sem_zeros):
        if i + 1 < len(sem_zeros) and sem_zeros[i] == sem_zeros[i + 1]:
            fundidos.append(sem_zeros[i] * 2)
            i += 2
        else:
            fundidos.append(sem_zeros[i])
            i += 1
            
    # Completa com zeros ate o tamanho 4
    fundidos += [0] * (4 - len(fundidos))
    
    # Retorna True se a linha mudou de estado
    return fundidos != linha

def transpor(matriz):
    return [[matriz[r][c] for r in range(4)] for c in range(4)]

def resolver():
    t = int(input())
    
    for _ in range(t):
        matriz = []
        tem_2048 = False
        
        for _ in range(4):
            linha = list(map(int, input().split()))
            if 2048 in linha:
                tem_2048 = True
            matriz.append(linha)
            
        # Se 2048 já esta na matriz, nenhuma jogada é valida
        if tem_2048:
            print("NONE")
            continue
            
        jogadas = []

        # 1. DOWN (Baixo): Transpõe a matriz e inverte as linhas
        matriz_down = [linha[::-1] for linha in transpor(matriz)]
        if any(mover_linha_esquerda(linha) for linha in matriz_down):
            jogadas.append("DOWN")

        # 2. LEFT (Esquerda): Aplica diretamente nas linhas
        if any(mover_linha_esquerda(linha) for linha in matriz):
            jogadas.append("LEFT")

        # 3. RIGHT (Direita): Inverte as linhas
        matriz_right = [linha[::-1] for linha in matriz]
        if any(mover_linha_esquerda(linha) for linha in matriz_right):
            jogadas.append("RIGHT")

        # 4. UP (Cima): Transpõe a matriz
        if any(mover_linha_esquerda(linha) for linha in transpor(matriz)):
            jogadas.append("UP")

        # Saida dos resultados
        if jogadas:
            print(" ".join(jogadas))
        else:
            print("NONE")

if __name__ == '__main__':
    resolver()