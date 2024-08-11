import pcf8574
import time
from wordsclockEnum import ButtonStatus, GPIOList
# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
# When button is pressed>1second, this flag is activated.
super_long_click_flag = False

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def get_status():
    '''
    Function that returns button status:
         NoClick
    .    ShortClick
    _    LongClick
    __   SuperLongClick
    '''
    global super_long_click_flag
    if pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True and super_long_click_flag == False:
        super_long_click_flag = False
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True:
            time.sleep(0.01)
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False:
            if time.time() - start_time >= 1.0:  
                super_long_click_flag = True
                print('LongClick')
                return ButtonStatus.LongClick.value           # LongClick threshold 
            time.sleep(0.01) 
        print('ShortClick')
        return ButtonStatus.ShortClick.value                  # ShortClick threshold 
    elif super_long_click_flag == True:
        super_long_click_flag = False
        # long click remains
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False:
            if time.time() - start_time >= 4.0:  
                print('SuperLongClick')
                return ButtonStatus.SuperLongClick.value      # SuperLongClick threshold 
            time.sleep(0.01)
        return ButtonStatus.NoClick.value   
    # workarround to set button pin working again after reset
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "OUTPUT")
    pcf8574.s3.write(GPIOList.S3_1_BUTTON.value, "HIGH")
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "INPUT")
    time.sleep(0.1)             
    return ButtonStatus.NoClick.value