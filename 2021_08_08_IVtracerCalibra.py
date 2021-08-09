import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient  # initialize a serial RTU client instance

# CÓDIGO PARA CALIBRAR O TRAÇADOR DE CURVAS I-V

# Inicializa as variáveis locais
dadosADS1256_1 = []
dadosADS1256_2 = []

# Inicializa a comunicação Modbus
client = ModbusClient(method="rtu", port="COM4", stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=1, strict=False)
client.connect()

# Aquisição dos parâmetros elétricos
print("Adquirindo os parâmetros elétricos")
client.write_coils(0, [True], unit=100)  # Endereço do registrador, valor escrito, endereço do escravo
time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade

while True:  # Aguarda o pino de disponbilidade ficar em alto
    estadoModulo = client.read_coils(1, 1, unit=100) # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade
    if estadoModulo.bits[0] == 1:
        break

# Leitura dos parâmetros elétricos via Modbus (leitura em pacotes de 100 registradores)
print("Lendo os parâmetros elétricos via Modbus")
for y in range(5):
    temps = client.read_holding_registers(y*100, 100, unit=100)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    time.sleep(1)  # Aguarda 1 segundo por questões de estabilidade
    dadosADS1256_1 = dadosADS1256_1 + temps.registers  # Adiciona os novos parâmetros no vetor dadosADS1256_1

    temps = client.read_holding_registers(y*100+500, 100, unit=100)  # Endereço do primeiro registrador, quantidade de registradores, endereço do escravo
    time.sleep(1)  # Aguarda 1 segundos por questões de estabilidade
    dadosADS1256_2 = dadosADS1256_2 + temps.registers  # Adiciona os novos parâmetros no vetor dadosADS1256_2

# Imprime os dados na tela
mediaTensao = sum(dadosADS1256_1) / len(dadosADS1256_1)
mediaCorrente = sum(dadosADS1256_2) / len(dadosADS1256_2)

print("A média da tensão é: " + str(mediaTensao))
print("A média da corrente é: " + str(mediaCorrente))

client.close()
