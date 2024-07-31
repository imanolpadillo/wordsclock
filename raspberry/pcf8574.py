# *************************************************************************************************** 
# ********************************************* PCF8574 *********************************************
# *************************************************************************************************** 
import pcf8574_io
from wordsclockEnum import GPIOList

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

s0 = pcf8574_io.PCF(0x20)
s1 = pcf8574_io.PCF(0x21)
s2 = pcf8574_io.PCF(0x22)
s3 = pcf8574_io.PCF(0x23)

# set pins as output
s0.pin_mode(GPIOList.S0_0_E.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_1_S.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_2_ON.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_3_LA.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_4_S_2.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_5_UNA.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_6_DOS.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_7_TRES.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_0_CUATRO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_1_CINCO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_2_SEIS.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_3_SIETE.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_4_OCHO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_5_NUEVE.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_6_DIEZ.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_7_ONCE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_0_DOCE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_1_Y.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_2_MENOS.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_3_VEINTE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_4_DIEZ_2.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_5_VEINTI.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_6_CINCO_2.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_7_MEDIA.value, "OUTPUT")
s3.pin_mode(GPIOList.S3_0_CUARTO.value, "OUTPUT")
s3.pin_mode(GPIOList.S3_1_BUTTON.value, "INPUT")