n = int(input())

listaPares = []
listaImpares = []

for i in range(n):
    num = int(input())
    if num % 2 == 0:
        listaPares.append(num)
    else:
        listaImpares.append(num)
listaPares.sort()
listaImpares.sort(reverse=True)
lista = listaPares + listaImpares
for i in range(len(lista)):
    print(lista[i])
