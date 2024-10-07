import pcf8574
import time
from wordsclockEnum import ButtonStatus, GPIOList

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def get_status():
    '''
    Function that returns button status:
    .     Short1Click
    . .   Short2Click
    . . . Short3Click
    __    LongClick
    '''
    if pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True: 
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True: 
            time.sleep(0.01)
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False: 
            if time.time() - start_time >= 1.0:  
                # print('LongClick')
                return ButtonStatus.LongClick.value       # LongClick threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True:
            if time.time() - start_time >= 0.5:  
                # print('short1Click')
                return ButtonStatus.Short1Click.value     # Short1Click threshold 
            time.sleep(0.01)  
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False:
            if time.time() - start_time >= 1.0:  
                # print('shortLongClick')
                return ButtonStatus.NoClick.value         # ShortLongClick threshold -> no function defined
            time.sleep(0.01) 
        start_time = time.time()
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == True:
            if time.time() - start_time >= 0.5:  
                # print('short2Click')
                return ButtonStatus.Short2Click.value     # Short2Click threshold 
            time.sleep(0.01) 
        while pcf8574.s3.read(GPIOList.S3_1_BUTTON.value) == False:
            if time.time() - start_time >= 1.0:  
                # print('shortShortLongClick')
                return ButtonStatus.NoClick.value         # ShortShortLongClick threshold -> no function defined
            time.sleep(0.01) 
        # print('short3Click')
        return ButtonStatus.Short3Click.value             # Short3Click threshold         
    # workarround to set button pin working again after reset
    #print('workarround')
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "OUTPUT")
    pcf8574.s3.write(GPIOList.S3_1_BUTTON.value, "HIGH")
    pcf8574.s3.pin_mode(GPIOList.S3_1_BUTTON.value, "INPUT")
    time.sleep(0.1)         
    return ButtonStatus.NoClick.value                     # NoClick -> no function defined
