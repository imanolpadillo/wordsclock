# *************************************************************************************************** 
# ****************************************** WORDSCLOCKENUM *****************************************
# *************************************************************************************************** 
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
class ButtonStatus(Enum):
    NoClick = 0
    ShortClick = 1
    LongClick = 2
    SuperLongClick = 3

class EcoModeSchedule(Enum):
    InitHour = 22  # 'eco mode' init hour
    EndHour = 6    # 'eco mode' end hour 

class GPIOList(Enum):
    S0_0_E = "p0"
    S0_1_S = "p1"
    S0_2_ON = "p2"
    S0_3_LA = "p3"
    S0_4_S_2 = "p4"
    S0_5_UNA = "p5"
    S0_6_DOS = "p6"
    S0_7_TRES = "p7"
    S1_0_CUATRO = "p0"
    S1_1_CINCO = "p1"
    S1_2_SEIS = "p2"
    S1_3_SIETE = "p3"
    S1_4_OCHO = "p4"
    S1_5_NUEVE = "p5"
    S1_6_DIEZ = "p6"
    S1_7_ONCE = "p7"
    S2_0_DOCE = "p0"
    S2_1_Y = "p1"
    S2_2_MENOS = "p2"
    S2_3_VEINTE = "p3"
    S2_4_DIEZ_2 = "p4"
    S2_5_VEINTI = "p5"
    S2_6_CINCO_2 = "p6"
    S2_7_MEDIA = "p7"
    S3_0_CUARTO = "p0"
    S3_1_BUTTON = "p1"