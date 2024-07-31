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
    if pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == 0:
        super_long_click_flag = False
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == 0:
            time.sleep(0.01)
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == 1:
            if time.time() - start_time >= 1.0:  
                super_long_click_flag = True
                return ButtonStatus.LongClick           # LongClick threshold 
            time.sleep(0.01) 
        return ButtonStatus.ShortClick                  # ShortClick threshold 
    elif super_long_click_flag == True:
        # long click remains
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == 1:
            if time.time() - start_time >= 2.0:  
                super_long_click_flag = False
                return ButtonStatus.SuperLongClick      # SuperLongClick threshold 
            time.sleep(0.01)
        super_long_click_flag = False
        return ButtonStatus.NoClick                 
    return ButtonStatus.NoClick