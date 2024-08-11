# *************************************************************************************************** 
# *********************************************** LEDS **********************************************
# *************************************************************************************************** 

import pcf8574
import time
from wordsclockEnum import GPIOList

# *************************************************************************************************** 
# FUNCTIONS
# ***************************************************************************************************
def reset(activateAllFirst = False):
    """
    Resets all leds. If activateAllFirst is True, all leds are 
    previously activated.
    """
    if activateAllFirst == True:
        value = "LOW"
        counter = 2
    else:
        value = "HIGH"
        counter = 1
    while counter>0:
        pcf8574.s0.write(GPIOList.S0_0_E.value, value)
        pcf8574.s0.write(GPIOList.S0_1_S.value, value)
        pcf8574.s0.write(GPIOList.S0_2_ON.value, value)
        pcf8574.s0.write(GPIOList.S0_3_LA.value, value)
        pcf8574.s0.write(GPIOList.S0_4_S_2.value, value)
        pcf8574.s0.write(GPIOList.S0_5_UNA.value, value)
        pcf8574.s0.write(GPIOList.S0_6_DOS.value, value)
        pcf8574.s0.write(GPIOList.S0_7_TRES.value, value)
        pcf8574.s1.write(GPIOList.S1_0_CUATRO.value, value)
        pcf8574.s1.write(GPIOList.S1_1_CINCO.value, value)
        pcf8574.s1.write(GPIOList.S1_2_SEIS.value, value)
        pcf8574.s1.write(GPIOList.S1_3_SIETE.value, value)
        pcf8574.s1.write(GPIOList.S1_4_OCHO.value, value)
        pcf8574.s1.write(GPIOList.S1_5_NUEVE.value, value)
        pcf8574.s1.write(GPIOList.S1_6_DIEZ.value, value)
        pcf8574.s1.write(GPIOList.S1_7_ONCE.value, value)
        pcf8574.s2.write(GPIOList.S2_0_DOCE.value, value)
        pcf8574.s2.write(GPIOList.S2_1_Y.value, value)
        pcf8574.s2.write(GPIOList.S2_2_MENOS.value, value)
        pcf8574.s2.write(GPIOList.S2_3_VEINTE.value, value)
        pcf8574.s2.write(GPIOList.S2_4_DIEZ_2.value, value)
        pcf8574.s2.write(GPIOList.S2_5_VEINTI.value, value)
        pcf8574.s2.write(GPIOList.S2_6_CINCO_2.value, value)
        pcf8574.s2.write(GPIOList.S2_7_MEDIA.value, value)
        pcf8574.s3.write(GPIOList.S3_0_CUARTO.value, value)
        if activateAllFirst == True:
            value = "HIGH"
            time.sleep(2)
        counter-=1

def set_time(current_time):
    hour = int(current_time.strftime("%H"))
    minutes = int(current_time.strftime("%M"))
    #Minutes must be always rounded
    if minutes % 5 != 0:
        minutes = (minutes // 5 + 1) * 5
        if minutes >= 60:
            minutes = 0
            hour+=1
    print(str(hour) + ':' + str(minutes))
    #Switch off leds
    reset(False)
    # Adapt to "to" hours
    if minutes==35 or minutes==40 or minutes==45 or minutes==50 or minutes==55:
        hour+=1
    # Display 'ES LA' or 'SON LAS'
    if hour == 1 or hour == 13:
        pcf8574.s0.write(GPIOList.S0_0_E.value, "LOW")
        pcf8574.s0.write(GPIOList.S0_1_S.value, "LOW")
        pcf8574.s0.write(GPIOList.S0_3_LA.value, "LOW")
    else:
        pcf8574.s0.write(GPIOList.S0_1_S.value, "LOW")
        pcf8574.s0.write(GPIOList.S0_2_ON.value, "LOW")
        pcf8574.s0.write(GPIOList.S0_3_LA.value, "LOW")
        pcf8574.s0.write(GPIOList.S0_4_S_2.value, "LOW")
    # Display hour
    if hour==1 or hour==13:
        pcf8574.s0.write(GPIOList.S0_5_UNA.value, "LOW")
    elif hour==2 or hour==14:
        pcf8574.s0.write(GPIOList.S0_6_DOS.value, "LOW")
    elif hour==3 or hour==15:
        pcf8574.s0.write(GPIOList.S0_7_TRES.value, "LOW")
    elif hour==4 or hour==16:
        pcf8574.s1.write(GPIOList.S1_0_CUATRO.value, "LOW")
    elif hour==5 or hour==17:
        pcf8574.s1.write(GPIOList.S1_1_CINCO.value, "LOW")
    elif hour==6 or hour==18:
        pcf8574.s1.write(GPIOList.S1_2_SEIS.value, "LOW")
    elif hour==7 or hour==19:
        pcf8574.s1.write(GPIOList.S1_3_SIETE.value, "LOW")
    elif hour==8 or hour==20:
        pcf8574.s1.write(GPIOList.S1_4_OCHO.value, "LOW")
    elif hour==9 or hour==21:
        pcf8574.s1.write(GPIOList.S1_5_NUEVE.value, "LOW")
    elif hour==10 or hour==22:
        pcf8574.s1.write(GPIOList.S1_6_DIEZ.value, "LOW")
    elif hour==11 or hour==23:
        pcf8574.s1.write(GPIOList.S1_7_ONCE.value, "LOW")
    elif hour==0 or hour==12 or hour==24:
        pcf8574.s2.write(GPIOList.S2_0_DOCE.value, "LOW")
    # Display '-', 'Y' or 'MENOS'
    if minutes==5 or minutes==10 or minutes==15 or minutes==20 or minutes==25 or minutes==30:
        pcf8574.s2.write(GPIOList.S2_1_Y.value, "LOW")
    elif minutes==35 or minutes==40 or minutes==45 or minutes==50 or minutes==55:
        pcf8574.s2.write(GPIOList.S2_2_MENOS.value, "LOW")
    #Display minutes
    if minutes==5 or minutes==55:
        pcf8574.s2.write(GPIOList.S2_6_CINCO_2.value, "LOW")
    if minutes==10 or minutes==50:
        pcf8574.s2.write(GPIOList.S2_4_DIEZ_2.value, "LOW")
    if minutes==15 or minutes==45:
        pcf8574.s3.write(GPIOList.S3_0_CUARTO.value, "LOW")
    if minutes==20 or minutes==40:
        pcf8574.s2.write(GPIOList.S2_3_VEINTE.value, "LOW")
    if minutes==25 or minutes==35:
        pcf8574.s2.write(GPIOList.S2_5_VEINTI.value, "LOW")
        pcf8574.s2.write(GPIOList.S2_6_CINCO_2.value, "LOW")
    if minutes==30:
        pcf8574.s2.write(GPIOList.S2_7_MEDIA.value, "LOW")
    return False