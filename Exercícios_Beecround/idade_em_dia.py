valor = int(input())


a = valor // 365
valor = valor % 365

b = valor // 30
valor = valor % 30

c = valor


print("{} ano(s)". format(a))
print("{} mes(es)". format(b))
print("{} dia(s)". format(c))