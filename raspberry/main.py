# *************************************************************************************************** 
# **************************************** WORDSCLOCK (MAIN) ****************************************
# *************************************************************************************************** 
import datetime, time
import pytz
import threading
import button
import leds
from wordsclockEnum import ButtonStatus, EcoModeSchedule, FLASH_SECONDS_ON

# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
change_in_mode = False      # defines if a mode has been changed
eco_mode = True             # mixes scheduled alwayson + alwaysoff + flash
flash_mode = False          # leds are only activated during a few seconds in time change
alwayson_mode = False       # leds are always activated
alwaysoff_mode = False      # leds are always deactivated

# *************************************************************************************************** 
# FUNCTIONS
# ***************************************************************************************************
def thread_check_button():
    """
    Checks button status:
    - Short1Click: eco_mode
    - Short2Click: alwayson_mode
    - Short3Click: flash_mode
    - LongClick: alwaysoff_mode
    """
    while True:
        global change_in_mode, eco_mode, flash_mode, alwayson_mode, alwaysoff_mode
        button_status = button.get_status()
        if button_status != ButtonStatus.NoClick.value:
            # Reset all status if new status is activated
            eco_mode = False
            alwayson_mode = False
            flash_mode = False
            alwaysoff_mode = False
            # Set new status
            if button_status == ButtonStatus.Short1Click.value:                # eco_mode
                print('ECO_MODE')
                eco_mode = True
            elif button_status == ButtonStatus.Short2Click.value:              # alwayson_mode
                print('ALWAYSON_MODE')
                alwayson_mode = True
            elif button_status == ButtonStatus.Short3Click.value:              # flash_mode
                print('FLASH_MODE')
                flash_mode = True
            elif button_status == ButtonStatus.LongClick.value:                # alwaysoff_mode
                print('ALWAYSOFF_MODE')
                leds.reset(True)  # reset all leds (activating all first)
                alwaysoff_mode = True
            # Notify that a new mode has been activated
            change_in_mode = True
        # Repeat the loop every 0.1    
        time.sleep(0.1) 

def check_time ():
    """
    At every minute%5 or mode change checks time display.
    """
    global change_in_mode, eco_mode, flash_mode, alwayson_mode, alwaysoff_mode
    madrid_tz = pytz.timezone('Europe/Madrid')
    current_time = datetime.datetime.now(madrid_tz)
    if (current_time.minute % 5 == 0 and current_time.second == 0) or change_in_mode == True:
        change_in_mode = False
        eco_flash = False         # in eco mode: flash flag
        eco_alwaysoff = False     # in eco mode: alwaysoff flag
        # Check current mode
        if eco_mode:                               # eco_mode: it is derived to alwaysoff, flash or alwayson
            eco_alwaysoff = get_eco_flag(EcoModeSchedule.alwaysoffEnabled.value, EcoModeSchedule.alwaysoffInitTime.value, EcoModeSchedule.alwaysoffEndTime.value)
            eco_flash = get_eco_flag(EcoModeSchedule.flashEnabled.value, EcoModeSchedule.flashInitTime.value, EcoModeSchedule.flashEndTime.value)
        if alwaysoff_mode or eco_alwaysoff:        # alwaysoff_mode
            leds.reset(False)     
        elif flash_mode or eco_flash:              # flash_mode
            leds.set_time(current_time)
            time.sleep(FLASH_SECONDS_ON)
            leds.reset(False)     
        else:                                      # alwayson_mode
            leds.set_time(current_time)

def get_eco_flag (enabled, start_time_str, end_time_str):
    """
    check if current time is between eco scheduled init and end times
    """
    if enabled == False:
        return False
    # Parse the input time strings into datetime objects
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()
    
    # Get the current time
    madrid_tz = pytz.timezone('Europe/Madrid')
    current_time = datetime.datetime.now(madrid_tz).time()
    
    # Check if the current time is between the start and end times
    if start_time < end_time:
        return start_time <= current_time <= end_time
    else:  # Over midnight case
        return current_time >= start_time or current_time <= end_time

# *************************************************************************************************** 
# MAIN
# ***************************************************************************************************
if __name__ == "__main__":
    leds.reset(True)  # reset all leds (activating all first)
    # Create a thread to check button status
    thread = threading.Thread(target=thread_check_button)
    thread.start()

    # check time first time avoiding waiting 5 minutes
    change_in_mode = True
    while True:
        check_time()
        time.sleep(1)
