import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Determina a tabela MySQL que será plotada
serieFV = 1
tabName = "tab_2021_8_19_14_0_2"

# Importa o arquivo CSV e salva em uma variável do tipo pandas dataframe
df = pd.read_csv("C:/Users/marco/Downloads/Trace - 8-19-2021 01-43 PM.csv")
vl = df.values.tolist()

# Inicializa a conexão com o banco de dados
db = mysql.connector.connect(host="192.168.1.107", user="mtreter", password="t18m17m4")
dbCursor = db.cursor()

# Converte a variável dataframe em list
vlArray = np.array(vl)
irradSolmetric = '{0:.4g}'.format(float(vlArray[0, 1]))
tempSolmetric = '{0:.3g}'.format(float(vlArray[1, 1]))
tensaoSolmetric = [float(i) for i in vlArray[3:, 0]]
correnteSolmetric = [float(i) for i in vlArray[3:, 1]]

# Inicializa de variáveis
tensaoTracer = np.zeros(497)
correnteTracer = np.zeros(497)
dbClima = "s" + str(serieFV) + "_clima"
dbCurva = "s" + str(serieFV) + "_curva"

# Seleciona os parâmetros climáticos no banco de dados MySQL
dbCursor.execute("SELECT * FROM " + dbClima + "." + tabName)
result = dbCursor.fetchall()
irradTracer = (result[0][2]-388)*0.942632
irradTracer = '{0:.4g}'.format(irradTracer)
tempTracer = result[0][1]/100
tempTracer = '{0:.3g}'.format(tempTracer)

# Seleciona os parâmetros elétricos no banco de dados MySQL
dbCursor.execute("SELECT * FROM " + dbCurva + "." + tabName)
result = dbCursor.fetchall()

for j in range(3, len(result)):
    tensaoTracer[j-3] = (result[j][1] - 18.5) * 0.220188659
    correnteTracer[j-3] = (result[j][2] - 10) * 0.002139045

# Plota a curva I-V
plt.plot(tensaoTracer, correnteTracer, 'o', label="Traçador I-V Protótipo - Irrad: " + str(irradTracer) + " W/m², Temp: " + str(tempTracer) + " ºC")
plt.plot(tensaoSolmetric, correnteSolmetric, 'o', label="Traçador I-V Solmetric - Irrad: " + str(irradSolmetric) + " W/m², Temp: " + str(tempSolmetric) + " ºC")
plt.title('Curva I-V')
plt.ylabel('Corrente (A)')
plt.xlabel('Tensão (V)')
plt.legend(loc="upper right")
plt.minorticks_on()
plt.axis([0, 1000, 0, 10])
plt.grid(True)
plt.show()
