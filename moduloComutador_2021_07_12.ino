//-------------------------------------------------------------------------//
//                Universidade do Estado de Santa Catarina                 //
//            Programa de Pós-Graduação em Engenharia Elétrica             //
//                    Doutorado em Engenharia Elétrica                     //
//                                                                         //
//   Programador:                                                          //
//       Marcos Eduardo Treter                                             //
//                                                                         //
//   Versão: 1.1 - Data: 23/11/2020                                        //
//=========================================================================//
//                         Descrição do Programa                           //
//=========================================================================//
//  Módulo comutador: Conexão/desconexão com inversor FV e traçador I-V.   //
//                                                                         //
//  v1.1 - Protótipo para instalação na usina.                             //
//-------------------------------------------------------------------------//

//-------------------------------------------------------------------------//
// Inclusão de bibliotecas                                                 //
//-------------------------------------------------------------------------//
#include <Modbus.h>           // Biblioteca Modbus
#include <ModbusSerial.h>     // Biblioteca Modbus
#include <Thermistor.h>       // Biblioteca sensor temperatura

//-------------------------------------------------------------------------//
// Definições de constantes                                                //
//-------------------------------------------------------------------------//
#define R               1       // Define a variável R para ser usada como Red nas configurações dos LED
#define G               0       // Define a variável G para ser usada como Green nas configurações dos LED
#define I               0       // Define a variável I para ser usada como Inversor na comunicação Modbus
#define T               1       // Define a variável I para ser usada como Traçador na comunicação Modbus
#define C               2       // Define a variável I para ser usada como Cooler na comunicação Modbus

//-------------------------------------------------------------------------//
// Pinos do microcontrolador                                               //
//-------------------------------------------------------------------------//
#define LEDclock        3       // Saída - Controle do CI 74HC595 para comando dos LED's
#define LEDlatch        4       // Saída - Controle do CI 74HC595 para comando dos LED's
#define LEDdata         5       // Saída - Controle do CI 74HC595 para comando dos LED's
#define receiveCooler   8       // Saída - Sinal de funcionamento do cooler
#define switchTracer    9       // Saída - Comando do transistor para conexão com o traçador de curvas I-V
#define switchCooler    10      // Saída - Comando do transistor para acionamento do cooler
#define switchInverter  13      // Saída - Comando do transistor para conexão com o inversor fotovoltaico
#define DS1             A1;     // Entrada - Chave DIP Switch para configurar o endereço Modbus
#define DS2             A2;     // Entrada - Chave DIP Switch para configurar o endereço Modbus
#define DS3             A3;     // Entrada - Chave DIP Switch para configurar o endereço Modbus
#define DS4             A4;     // Entrada - Chave DIP Switch para configurar o endereço Modbus
#define DS5             A5;     // Entrada - Chave DIP Switch para configurar o endereço Modbus

//-------------------------------------------------------------------------//
// Configuração Modbus                                                     //
//-------------------------------------------------------------------------//
ModbusSerial mb;                // Cria o objeto ModbusSerial

//-------------------------------------------------------------------------//
// Variáveis Globais                                                       //
//-------------------------------------------------------------------------//
byte LEDstatus = B00000000;                                       // Variável que indica os LED's que estão ligados/desligados
static const uint8_t dipSwitch_pins[] = {A1, A2, A3, A4, A5};     // Vetor para armazenar a leitura da chave DIP Switch
static const uint8_t LEDstart[] = {0, 1};                         // Variável que armazena o endereço dos LED's que identificam a conexão com o inversor fotovoltaico
static const uint8_t LEDinverter[] = {2, 3};                      // Variável que armazena o endereço dos LED's que identificam a conexão com o inversor fotovoltaico
static const uint8_t LEDtracer[] = {4, 5};                        // Variável que armazena o endereço dos LED's que identificam a conexão com o traçador de curvas I-V
static const uint8_t LEDtemperature[] = {6, 7};                   // Variável que armazena o endereço dos LED's que identificam o estado da temperatura
Thermistor sensorTemp(0);                                         // Cria o objeto para o sensor de temperatura

//-------------------------------------------------------------------------//
// Função para configuração dos LED's                                      //
//-------------------------------------------------------------------------//
void setLED(int LEDpos, int LEDstate) {             // LED = Posição do LED 1~4; State = Estado atual 0~1
  bitWrite(LEDstatus, LEDpos, LEDstate);            // Modifica a variável LEDstatus, de acordo a posição LEDpos (0~7) e o estado LEDstate (0~1)
  shiftOut(LEDdata, LEDclock, LSBFIRST, LEDstatus); // Operação necessária para gravar as informações no CI 74HC595
  digitalWrite(LEDlatch, HIGH);                     // Operação necessária para gravar as informações no CI 74HC595
  digitalWrite(LEDlatch, LOW);                      // Operação necessária para gravar as informações no CI 74HC595
}

//-------------------------------------------------------------------------//
// Função para definir o endereço do módulo comutador                      //
//-------------------------------------------------------------------------//
void setAdrress() {
  byte adressModbus = B00000;                                       // Variável para armazenar o endereço Modbus
  for (int i = 0; i < 5; i++)
    bitWrite(adressModbus, i, digitalRead(dipSwitch_pins[i]));      // Modifica a variável adressModbus de acordo com as posições da chave DIP Switch
  mb.setSlaveId(adressModbus);                                      // Define o endereço do módulo comutador
}

//-------------------------------------------------------------------------//
// Função para controlar o transistor que faz a conexão com o inversor     //
//-------------------------------------------------------------------------//
void setInverter(int statusInverter) {

  if (statusInverter == 1) {                    // Entra no if ao realizar a conexão com o inversor fotovoltaico
    digitalWrite(switchInverter,  HIGH);        // Efetiva a conexão com o inversor fotovoltaico
    setLED(LEDinverter[R], 0);                  // Apaga o LED vermelho da conexão com o inversor fotovoltaico
    setLED(LEDinverter[G], 1);                  // Acende o LED verde da conexão com o inversor fotovoltaico
  }

  else {
    digitalWrite(switchInverter,  LOW);         // Abre a conexão com o inversor fotovoltaico
    setLED(LEDinverter[G], 0);                  // Apaga o LED verde da conexão com o inversor fotovoltaico
    setLED(LEDinverter[R], 1);                  // Acende o LED vermelho da conexão com o inversor fotovoltaico
  }

}

//-------------------------------------------------------------------------//
// Função para controlar o transistor que faz a conexão com o traçador     //
//-------------------------------------------------------------------------//
void setTracer(int statusTracer) {

  if (statusTracer == 1) {                      // Entra no if ao realizar a conexão com o traçador de curvas I-V
    digitalWrite(switchTracer,  HIGH);          // Efetiva a conexão com o traçador de curvas I-V
    setLED(LEDtracer[R], 0);                    // Apaga o LED vermelho da conexão com o traçador de curvas I-V
    setLED(LEDtracer[G], 1);                    // Acende o LED verde da conexão com o traçador de curvas I-V
  }

  else {
    digitalWrite(switchTracer,  LOW);           // Abre a conexão com o traçador de curvas I-V
    setLED(LEDtracer[G], 0);                    // Apaga o LED verde da com o traçador de curvas I-V
    setLED(LEDtracer[R], 1);                    // Acende o LED vermelho da conexão com o traçador de curvas I-V
  }

}

//-------------------------------------------------------------------------//
// Função para controlar o transistor que faz o acionamento do Cooler      //
//-------------------------------------------------------------------------//
void setCooler(int statusCooler) {

  if (statusCooler == 1) {
    digitalWrite(switchCooler,  HIGH);         // Aciona o Cooler
    setLED(LEDtemperature[R], 0);              // Apaga o LED vermelho do Cooler
    setLED(LEDtemperature[G], 1);              // Acende o LED verde do Cooler
  }

  else {
    digitalWrite(switchCooler,  LOW);          // Desliga o Cooler
    setLED(LEDtemperature[R], 0);              // Apaga o LED vermelho do Cooler
    setLED(LEDtemperature[G], 0);              // Apaga o LED verde do Cooler
  }

}

//-------------------------------------------------------------------------//
// Função Setup - executada na energização do microcontrolador             //
//-------------------------------------------------------------------------//
void setup() {

  mb.config(&Serial, 9600, SERIAL_8N1, 2);       // Configuração do modbus (porta, velocidade, byte formato)
  setAdrress();                                  // Chama a função para definir o endereço do módulo

  mb.addCoil(I);     // Inicializa os registradores do tipo Coil da comunicação Modbus - Inversor
  mb.addCoil(T);     // Inicializa os registradores do tipo Coil da comunicação Modbus - Traçador
  mb.addCoil(C);     // Inicializa os registradores do tipo Coil da comunicação Modbus - Cooler
  mb.addIreg(0);                                 // Define o registrador do tipo Ireg para o envio da temperatura lida no módulo comutador

  pinMode(LEDclock,       OUTPUT);
  pinMode(LEDlatch,       OUTPUT);
  pinMode(LEDdata,        OUTPUT);
  pinMode(switchTracer,   OUTPUT);
  pinMode(switchCooler,   OUTPUT);
  pinMode(switchInverter, OUTPUT);
  pinMode(receiveCooler,   INPUT);

  mb.Coil(T, 0);                    // Inicializa com o traçador desconectado
  mb.Coil(I, 1);                    // Inicializa com o inversor conectado
  setCooler(0);                     // Inicializa com o cooler desligado

}

//-------------------------------------------------------------------------//
// Função Loop - executada a cada ciclo de varredura do microcontrolador   //
//-------------------------------------------------------------------------//
void loop() {

  mb.task();                                    // Função principal para fazer a atualização da comunicação Modbus

  // Liga os LEDs de start
  setLED(LEDstart[R], 0);
  setLED(LEDstart[G], 1);

  mb.Ireg(0, sensorTemp.getTemp());     // Armazena a temperatura atual no registador IREG 0

  if (sensorTemp.getTemp() > 45) setCooler(1);        // Se a temperatura atual for superior a 45 °C o Cooler é acionado independente da variável COIL_COL
  else if (mb.Coil(C) == 1) setCooler(1);      // Se a temperatura atual for inferior a 40 °C mas o registrador Coil 2 = 1, então o Cooler é acionado
  else if (sensorTemp.getTemp() < 40) setCooler(0);   // Se a temperatura atual for inferior a 40 °C e COIL_COL = 0, então o Cooler é desligado

  // Cooler não conectado ou temperatura acima de 80 °C
  if (((digitalRead(switchCooler) == 1) && (digitalRead(receiveCooler) == 1)) || (sensorTemp.getTemp() > 80) || ((digitalRead(switchCooler) == 0) && (digitalRead(receiveCooler) == 0))) {
    setLED(LEDtemperature[G], 0);                     // Apaga o LED verde do Cooler
    setLED(LEDtemperature[R], 1);                     // Acende o LED vermelho do Cooler
    mb.Coil(I, 0);
    mb.Coil(T, 0);
    setInverter(0);                                   // Abre a conexão com o inversor fotovoltaico
    setTracer(0);                                     // Abre a conexão com o traçador de curvas I-V
  }

  else {

    setLED(LEDtemperature[R], 0);                     // Apaga o LED vermelho do Cooler

    if (mb.Coil(I) == 1 && mb.Coil(T) == 0) setInverter(1);     // Ao receber a ordem via Modbus, estabelece a conexão com o inversor FV
    else setInverter(0);                            // Ao receber a ordem via Modbus, abre a conexão com o inversor FV
    if (mb.Coil(T) == 1 && mb.Coil(I) == 0) setTracer(1);       // Ao receber a ordem via Modbus, estabelece a conexão com o traçador de curvas I-V
    else setTracer(0);                              // Ao receber a ordem via Modbus, abre a conexão com o traçador de curvas I-V

  }

}
