import pcf8574
import time
from wordsclockEnum import ButtonStatus, GPIOList

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def get_status():
    '''
    Function that returns button status:
         NoClick
    .    ShortClick: toogle eco_manual
    _    LongClick:  reset leds
    '''
    if pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True:
        super_long_click_flag = False
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True:
            time.sleep(0.01)
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False:
            if time.time() - start_time >= 1.0:  
                print('LongClick')
                return ButtonStatus.LongClick.value           # LongClick threshold 
            time.sleep(0.01) 
        print('ShortClick')
        return ButtonStatus.ShortClick.value                  # ShortClick threshold   
    # workarround to set button pin working again after reset
    print('workarround')
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "OUTPUT")
    pcf8574.s3.write(GPIOList.S3_1_BUTTON.value, "HIGH")
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "INPUT")
    time.sleep(0.1)         
    return ButtonStatus.NoClick.value