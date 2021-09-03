import scipy.io as sio
from scipy import interpolate
import numpy as np
import mysql.connector

# Inicializa a conexão com o banco de dados
db = mysql.connector.connect(host="192.168.1.107", user="mtreter", password="t18m17m4")
dbCursor = db.cursor()

# Determina a tabela que será convertida
serieFV = "1"
tabName = "tab_2021_8_27_13_0_1"
dbClima = "s" + str(serieFV) + "_clima"
dbCurva = "s" + str(serieFV) + "_curva"

# Inicialização das variáveis
irrad = 0
temp = 0
tensao = np.zeros(498)
corrente = np.zeros(498)

# Seleciona os parâmetros climáticos no banco de dados
dbCursor.execute("SELECT * FROM " + dbClima + "." + tabName)
result = dbCursor.fetchall()
irradFloat = '{0:.4g}'.format((result[0][2]-388)*0.942632)
tempFloat = '{0:.3g}'.format(result[0][1]/100)
irradInt = int((result[0][2]-388)*0.942632)
tempInt = int(result[0][1]/100)

# Seleciona os parâmetros elétricos no banco de dados
dbCursor.execute("SELECT * FROM " + dbCurva + "." + tabName)
result = dbCursor.fetchall()

for j in range(2, len(result)):
    tensao[j-2] = ((result[j][1]-18.5)*0.220188659)/24
    corrente[j-2] = (result[j][2]-10)*0.002139045

nomeArquivo = "G:\Meu Drive\Doutorado\Traçador de curvas I-V\Programação\Curvas I-V\curvasBrutas\IxV_S" + str(irradInt) + "_T" + str(tempInt) + ".mat"
print(nomeArquivo)
sio.savemat(nomeArquivo, {'irrad':irradFloat,'temp':tempFloat,'ten':tensao,'cor':corrente})