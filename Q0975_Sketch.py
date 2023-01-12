#     AUTOR:    BrincandoComIdeias
#     APRENDA:  https://cursodearduino.net/
#     SKETCH:   Robô Subindo Rampas e Inclinações (Com Pico)
#     DATA:     05/01/23

from machine import Pin
from machine import ADC
from machine import PWM
from utime import sleep_ms as delay

# Configurando pino dos sensores de linha
pinSensorE = Pin(2, Pin.IN)
pinSensorD = Pin(3, Pin.IN)

# Configurando pino Analogico
pinAcX = ADC(26)

# Configurando Pinos
pinIn1 = Pin(12, Pin.OUT)
pinIn2 = Pin(13, Pin.OUT)
pinIn3 = Pin(14, Pin.OUT)
pinIn4 = Pin(15, Pin.OUT)

# Configurando PWM
motorEsq1 = PWM(pinIn1)
motorEsq2 = PWM(pinIn2)
motorDir1 = PWM(pinIn3)
motorDir2 = PWM(pinIn4)

# Frequencia do PWM Arduino portas 3, 9, 10 e 11
motorEsq1.freq(490)
motorEsq2.freq(490)
motorDir1.freq(490)
motorDir2.freq(490)

# Equivalente a função map()
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Função para converter a velocidade de 0 a 100 em pulso PWM 16 bits
def pulsoMotor(potencia):
    return map(potencia, 0, 100, 0, 65534)

def parar():
    motorEsq1.duty_u16(0)
    motorEsq2.duty_u16(0)
    
    motorDir1.duty_u16(0)
    motorDir2.duty_u16(0)
    
# Delay de 2 segundos para começar o "loop"
delay(2000)

while True:    
    valSensorE = pinSensorE.value()
    valSensorD = pinSensorD.value()
    
    valAcX = pinAcX.read_u16()
    potencia = map( valAcX, 32000, 35500, 35, 100 )
    print(valAcX)
    
    if not valSensorD and valSensorE :
        motorEsq1.duty_u16(pulsoMotor(potencia))
        motorDir1.duty_u16(pulsoMotor(0))
        
    elif not valSensorE and valSensorD :
        motorDir1.duty_u16(pulsoMotor(potencia))
        motorEsq1.duty_u16(pulsoMotor(0))
        
    elif not valSensorE and not valSensorD :
        motorEsq1.duty_u16(pulsoMotor(potencia))
        motorDir1.duty_u16(pulsoMotor(potencia))
    
    else:
        parar()
        
    delay(250)
        