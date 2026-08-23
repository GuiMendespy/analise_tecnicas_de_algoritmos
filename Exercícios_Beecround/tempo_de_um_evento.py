dia1 = []
h1 = []
dia2 = []
h2 = []

dia1 = input()

h1 = input()

dia2 = input()

h2 = input()

if len(dia1) >=6:
    
    a = dia1[4:6]
else:
    a = dia1[4]

if len(dia2) >=6:
    
    c = dia2[4:6]
else:
    c = dia2[4]

hora1 = h1[0:2]
hora2 = h2[0:2]
minuto1 = h1[5:7]
minuto2 = h2[5:7]
seg1 = h1[10:12]
seg2 = h2[10:12]

segundoTotal1 = int(hora1) * 3600 + int(minuto1) * 60 + int(seg1)
segundoTotal2 = int(hora2) * 3600 + int(minuto2) * 60 + int(seg2)

diatotal = 24 * 3600

diasinicial = diatotal - segundoTotal1
i = (int(c) - int(a)) - 1
diasfinal = diasinicial + i * 86400 + segundoTotal2 

diasTotais = diasfinal // 86400
diasfinal = diasfinal % 86400

horaFinal = diasfinal // 3600
minutoInicial = diasfinal % 3600

minutoFinal = minutoInicial // 60
segInicial = minutoInicial % 60

segFinal = segInicial

print("{} dia(s)".format(diasTotais))
print("{} hora(s)".format(horaFinal))
print("{} minuto(s)".format(minutoFinal))
print("{} segundo(s)".format(segFinal))



