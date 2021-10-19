import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Arquivos a serem plotados
IVcomercial = "Trace - 10-5-2021 12-45 PM"
IVprototipo = "tab_2021_10_5_12_44"

# Importa os arquivos CSV
df_IVcomercial = pd.read_csv("G:/Meu Drive/Doutorado/Traçador de curvas I-V/Resultados sombreamento/Traçador comercial/" + IVcomercial + ".csv", header=None)
vl_IVcomercial = df_IVcomercial.values.tolist()

df_IVprototipoClima = pd.read_csv("G:/Meu Drive/Doutorado/Traçador de curvas I-V/Resultados sombreamento/Clima/" + IVprototipo + ".csv", header=None)
vl_IVprototipoClima = df_IVprototipoClima.values.tolist()

df_IVprototipoCurva = pd.read_csv("G:/Meu Drive/Doutorado/Traçador de curvas I-V/Resultados sombreamento/Curva/" + IVprototipo + ".csv", header=None)
vl_IVprototipoCurva = df_IVprototipoCurva.values.tolist()

# Ajusta os parâmetros do traçador de curvas I-V comercial
ar_IVcomercial = np.array(vl_IVcomercial)
irradIVcomercial = '{0:.4g}'.format(float(ar_IVcomercial[0, 1]))
tempIVcomercial = '{0:.3g}'.format(float(ar_IVcomercial[1, 1]))
tensaoIVcomercial = [float(i) for i in ar_IVcomercial[3:, 0]]
correnteIVcomercial = [float(i) for i in ar_IVcomercial[3:, 1]]
potenciaIVcomercial = [float(i) for i in ar_IVcomercial[3:, 2]]

for x in range(len(correnteIVcomercial)):
    tensaoIVcomercial[x] = tensaoIVcomercial[x] / 24
    potenciaIVcomercial[x] = potenciaIVcomercial[x] / 24

PmaxIVcomercial = max(potenciaIVcomercial)

# Ajusta os parâmetros do traçador de curvas I-V protótipo
ar_IVprototipoClima = np.array(vl_IVprototipoClima)
ar_IVprototipoCurva = np.array(vl_IVprototipoCurva)
irradIVprototipo = (ar_IVprototipoClima[0, 2] - 388) * 0.942632
tempprototipo = ar_IVprototipoClima[0, 1] / 100
tensaoIVprototipo = [float(i) for i in ((ar_IVprototipoCurva[3:, 1] - 18.5) * 0.220188659)/24]
correnteIVprototipo = [float(i) for i in (ar_IVprototipoCurva[3:, 2] - 10.0) * 0.002139045]

potenciaIVprototipo = []

for x in range(len(correnteIVprototipo)):
    potenciaIVprototipo.append(correnteIVprototipo[x] * tensaoIVprototipo[x])

PmaxIVprototipo = max(potenciaIVprototipo)

# Plota os gráficos da curva I-V
plt.plot(tensaoIVcomercial, correnteIVcomercial, 'o', label="Traçador de curvas I-V comercial. Pmax: " + str(int(PmaxIVcomercial)) + " W")
plt.plot(tensaoIVprototipo, correnteIVprototipo, 'o', label="Traçador de curvas I-V protótipo. Pmax: " + str(int(PmaxIVprototipo)) + " W")

# ConfiguraçÕes do gráfico
plt.title('Curva I-V')
plt.ylabel('Corrente (A)')
plt.xlabel('Tensão (V)')
plt.legend(loc="upper right")
plt.minorticks_on()
plt.axis([0, 40, 0, 10])
plt.grid(True)
plt.show()