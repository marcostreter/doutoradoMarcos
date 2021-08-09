#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import mysql.connector
import datetime
from pymodbus.client.sync import ModbusSerialClient as ModbusClient  # initialize a serial RTU client instance

# Inicializa as variáveis globais
numSeriesFV = 4

for x in range(numSeriesFV):

    # Inicializa as variáveis locais
    #dadosADS1256_1 = []
    #dadosADS1256_2 = []
    serieAtual = str(x + 1)

    print("----------------- Série FV " + serieAtual + " -----------------")

    # Inicializa a comunicação Modbus
    client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=1, strict=False)
    client.connect()

    # Inicializa a conexão com o banco de dados local
    #dbLocal = mysql.connector.connect(host="localhost", user="root", password="t18m17m4")
    #cursorLocal = dbLocal.cursor()

    # Define o nome das bases de dados
    #dbNameClima = "s" + serieAtual + "_clima"
    #dbNameCurva = "s" + serieAtual + "_curva"

    # Define o nome da tabela conforme o dia e o horário da aquisição. Ex: Ano_Mês_Dia_Hora_Minuto_Segundo
    #dataAtual = datetime.datetime.now()
    #tabName = "tab_" + str(dataAtual.year) + "_" + str(dataAtual.month) + "_" + str(dataAtual.day) + "_" + str(dataAtual.hour) + "_" + str(dataAtual.minute) + "_" + str(dataAtual.second)

    # Aquisição dos parâmetros climáticos
    #print("Adquirindo dos parâmetros climáticos")
    #register = client.read_holding_registers(0, 2, unit=101)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    #time.sleep(1)  # Aguarda 1 segundos por questões de estabilidade
    #tempCelula = register.registers[0]
    #irrad = register.registers[1]

    #register = client.read_holding_registers(0, 1, unit=102)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    #time.sleep(1)  # Aguarda 1 segundos por questões de estabilidade
    #tempModulo = register.registers[0]

    # Cria a tabela no banco de dados
    #stmt = "CREATE TABLE " + dbNameClima + "." + tabName + " (id INT NOT NULL AUTO_INCREMENT, tempModulo INT, irrad INT, tempCelula INT, PRIMARY KEY (id));"
    #cursorLocal.execute(stmt)

    # Armazena os parâmetros climáticos no banco de dados
    #print("Armazenando os parâmetros climáticos")
    #stmt = "INSERT INTO " + dbNameClima + "." + tabName + " (id, tempModulo, irrad, tempCelula) VALUES (NULL, " + str(tempModulo) + ", " + str(irrad) + ", " + str(tempCelula) + ")"
    #cursorLocal.execute(stmt)
    #dbLocal.commit()

    # Desconecta a série FV do inversor
    print("Desconectando a série FV do inversor")
    client.write_coils(0, [False], unit=x+1)  # Endereço do registrador, valor escrito, endereço do escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

    # Conecta a série FV no traçador
    print("Conectando a série FV no traçador")
    client.write_coils(1, [True], unit=x+1)  # Endereço do registrador, valor escrito, endereço do escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

    time.sleep(3)

    # Aquisição dos parâmetros elétricos
    #print("Adquirindo os parâmetros elétricos")
    #client.write_coils(0, [True], unit=100)  # Endereço do registrador, valor escrito, endereço do escravo
    #time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

    #while True:  # Aguarda o pino de disponbilidade ficar em alto
    #    estadoModulo = client.read_coils(1, 1, unit=100) # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    #    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade
    #    if estadoModulo.bits[0] == 1:
    #        break

    # Desconecta a série FV do traçador
    print("Desconectando a série FV do traçador")
    client.write_coils(1, [False], unit=x+1)  # Endereço, valor escrito, endereço escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

    # Conecta a série FV no inversor
    print("Conectando a série FV no inversor")
    client.write_coils(0, [True], unit=x+1)  # Endereço, valor escrito, endereço escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

    # Leitura dos parâmetros do módulo ADS1256_1 via Modbus (leitura em pacotes de 100 registradores - 0 até 499)
    #print("Lendo os parâmetros elétricos via Modbus")
    #for y in range(5):
    #    temps = client.read_holding_registers(y*100, 100, unit=100)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    #    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade
    #    dadosADS1256_1 = dadosADS1256_1 + temps.registers  # Adiciona os novos parâmetros no vetor dadosADS1256_1

    #    temps = client.read_holding_registers(y * 100 + 500, 100, unit=100)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    #    time.sleep(1)  # Aguarda 1 segundos por questões de estabilidade
    #    dadosADS1256_2 = dadosADS1256_2 + temps.registers  # Adiciona os novos parâmetros no vetor dadosADS1256_2

    # Cria a tabela no banco de dados
    #stmt = "CREATE TABLE " + dbNameCurva + "." + tabName + " (id INT NOT NULL AUTO_INCREMENT, tensao INT, corrente INT, PRIMARY KEY (id));"
    #cursorLocal.execute(stmt)

    # Armazena os parâmetros elétricos no banco de dados
    #print("Armazenando os parâmetros elétricos")
    #for y in range(500):
    #    stmt = "INSERT INTO " + dbNameCurva + "." + tabName + " (id, tensao, corrente) VALUES (NULL, " + str(dadosADS1256_1[y]) + ", " + str(dadosADS1256_2[y]) + ")"
    #    cursorLocal.execute(stmt)
    #    dbLocal.commit()

    # Imprime os dados na tela
    #mediaTensao = sum(dadosADS1256_1) / len(dadosADS1256_1)
    #mediaCorrente = sum(dadosADS1256_2) / len(dadosADS1256_2)

    #print("A média da tensão é: " + str(mediaTensao))
    #print("A média da corrente é: " + str(mediaCorrente))

    client.close()
    #dbLocal.close()

    time.sleep(5)  # Aguarda 5 segundos antes da próxima série FV
