import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

# Definições da curva a ser plotada
serieFV = 1
data = "2021_8_3_12_0_2"

# Variáveis globais
dbClima = "s"+str(serieFV)+"_clima"
dbCurva = "s"+str(serieFV)+"_curva"
tabName = "tab_"+data
id = []
tensao = []
corrente = []

# Inicializa a conexão com o banco de dados
db = mysql.connector.connect(host="192.168.1.107", user="mtreter", password="t18m17m4")
dbCursor = db.cursor()

# Seleciona os parâmetros climáticos no banco de dados
dbCursor.execute("SELECT * FROM " + dbClima + "." + tabName)
result = dbCursor.fetchall()
irrad = (result[0][2]-388)*0.942632
irrad = '{0:.4g}'.format(irrad)
temp = result[0][1]/100
temp = '{0:.3g}'.format(temp)

# Seleciona os parâmetros elétricos no banco de dados
dbCursor.execute("SELECT * FROM " + dbCurva + "." + tabName)
result = dbCursor.fetchall()

for k in range(3, len(result)):
    tensao.append((result[k][1]-18.5)*0.220188659)
    corrente.append((result[k][2]-10)*0.002139045)

# Plota os dados no terminal
print("Corrente (A): " + str(corrente))
print("Tensão (V): " + str(tensao))
print("Irradiância (W/m²): " + str(irrad))
print("Temperatura (ºC): " + str(temp))


# Plota a curva I-V
plt.plot(tensao, corrente, 'bo')
plt.title('Curva I-V')
plt.ylabel('Corrente (A)')
plt.xlabel('Tensão (V)')
plt.axis([0, 1000, 0, 8])
plt.text(220, 2.3, "$G = " + str(irrad) + " ~W/m^2$")
plt.text(220, 1.3, "$T = " + str(temp) + " ~^\circ C$")
plt.grid(True)
plt.show()
