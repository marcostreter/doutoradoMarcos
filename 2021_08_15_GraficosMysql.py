import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Inicializa a conexão com o banco de dados
db = mysql.connector.connect(host="192.168.1.107", user="mtreter", password="t18m17m4")
dbCursor = db.cursor()

# Determina a quantidade e quais os gráficos que serão plotados
#qntd = int(input())
qntd = 2
tab = [4, "tab_2021_8_19_16_4_57", 4, "tab_2021_8_23_16_4_56"]

irrad = np.zeros((1, qntd))
temp = np.zeros((1, qntd))
tensao = np.zeros((497, qntd))
corrente = np.zeros((497, qntd))

# Busca os valores no banco de dados e armazena nas respectivas variáveis
for i in range(0, qntd):

    dbClima = "s" + str(tab[i*2]) + "_clima"
    dbCurva = "s" + str(tab[i*2]) + "_curva"
    tabName = tab[i*2+1]

    # Seleciona os parâmetros climáticos no banco de dados
    dbCursor.execute("SELECT * FROM " + dbClima + "." + tabName)
    result = dbCursor.fetchall()
    irrad[0,i] = (result[0][2]-388)*0.942632
    irrad[0,i] = '{0:.4g}'.format(irrad[0,i])
    temp[0,i] = result[0][1]/100
    temp[0,i] = '{0:.3g}'.format(temp[0,i])

    # Seleciona os parâmetros elétricos no banco de dados
    dbCursor.execute("SELECT * FROM " + dbCurva + "." + tabName)
    result = dbCursor.fetchall()

    for j in range(3, len(result)):
        tensao[j-3, i] = (result[j][1]-18.5)*0.220188659
        corrente[j-3, i] = (result[j][2]-10)*0.002139045

    # Plota os dados no terminal
    #print("Corrente da curva " + str(i+1) + " (A): " + str(corrente[:, i]))
    #print("Tensão da curva " + str(i+1) + " (V): " + str(tensao[:, i]))
    #print("Irradiância da curva " + str(i+1) + " (W/m²): " + str(irrad[0,i]))
    #print("Temperatura da curva " + str(i+1) + " (ºC): " + str(temp[0, i]))

    # Plota a curva I-V
    plt.plot(tensao[:, i], corrente[:, i], 'o', label="Série FV " + str(tab[i*2]) + ", " + str(tab[i*2+1]) + ", Irrad: " + str(irrad[0,i]) + " W/m², Temp: " + str(temp[0, i]) + " ºC")
    plt.legend(["A simple line " + str(i)])

# Plota a curva I-V
plt.title('Curva I-V')
plt.ylabel('Corrente (A)')
plt.xlabel('Tensão (V)')
plt.legend(loc="upper right")
plt.minorticks_on()
plt.axis([0, 1000, 0, 10])
plt.grid(True)
plt.show()
