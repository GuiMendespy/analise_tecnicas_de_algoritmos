valor = int(input())

print(valor)

a = valor // 100
valor = valor % 100

b = valor // 50
valor = valor % 50

c = valor // 20
valor = valor % 20

d = valor // 10
valor = valor % 10

e = valor // 5
valor = valor % 5

f = valor // 2
valor = valor % 2

g = valor // 1
valor = valor % 1

print("{} nota(s) de R$ 100,00". format(a))
print("{} nota(s) de R$ 50,00". format(b))
print("{} nota(s) de R$ 20,00". format(c))
print("{} nota(s) de R$ 10,00". format(d))
print("{} nota(s) de R$ 5,00". format(e))
print("{} nota(s) de R$ 2,00". format(f))
print("{} nota(s) de R$ 1,00". format(g))