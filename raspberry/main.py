# *************************************************************************************************** 
# **************************************** WORDSCLOCK (MAIN) ****************************************
# *************************************************************************************************** 
import datetime, time
import pytz
import threading
import button
import leds
from wordsclockEnum import ButtonStatus, EcoModeSchedule, FlashModeSchedule

# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
eco_auto_flag = False       # deactivates display in eco time slot
eco_manual_flag = False     # deactivates display when long click unt short click
flash_auto_flag = False     # activates display only for a few seconds
force_display = True        # displays time instantaneously

# *************************************************************************************************** 
# FUNCTIONS
# ***************************************************************************************************

def thread_check_button():
    """
    Checks button status:
    - LongClick: Reset leds
    - ShortClick: Toogle eco_manual
    """
    while True:
        global eco_auto_flag, eco_manual_flag, force_display
        button_status = button.get_status()
        if button_status == ButtonStatus.ShortClick.value:
            if eco_manual_flag == True:
                eco_manual_flag = False
                eco_auto_flag = False
                force_display = True
            else:
                leds.reset(False)  # reset all leds 
                eco_manual_flag = True           
        elif button_status == ButtonStatus.LongClick.value:
            leds.reset(True)  # reset all leds (activating all first)
            eco_manual_flag = False
            eco_auto_flag = False
            force_display = True
        # Schedule the function to be called again after 0.1 second
        time.sleep(0.1) 

def check_time (firstCheck = False):
    """
    At every new hour checks if eco_mode must be activated.
    At minute%5 updates time.
    Force_display flag updates time always.
    """
    global eco_auto_flag,eco_manual_flag,force_display
    madrid_tz = pytz.timezone('Europe/Madrid')
    current_time = datetime.datetime.now(madrid_tz)
    if ((current_time.minute == 0 and current_time.second == 0)) or firstCheck == True:
        set_eco_auto_flag()
    if ((current_time.minute == 0 and current_time.second == 0)) or firstCheck == True:
        set_flash_auto_flag()
    if (force_display == True or (eco_auto_flag == False and eco_manual_flag == False and (current_time.minute % 5 == 0 and current_time.second == 0))) or firstCheck == True:
        force_display = False
        leds.set_time(current_time)
        # switch off leds with delay time if flash_auto_flag is activated
        if flash_auto_flag == True:
            time.sleep(FlashModeSchedule.SecondsOn.value)
            leds.reset(False)  # reset all leds


def set_eco_auto_flag():
    """
    Enables/disables eco_auto_flag depending on current time.
    """
    global eco_auto_flag
    
    # Set/Reset eco_auto_flag
    if EcoModeSchedule.Enabled.value == True:
        # check if current time is between scheduled time
        is_time_between_flag = is_time_between(EcoModeSchedule.InitTime.value, EcoModeSchedule.EndTime.value)
        if eco_auto_flag == False and is_time_between_flag == True:
            print('ECO_MODE_ON')
            leds.reset(False)  # reset all leds
            eco_auto_flag = True
        elif eco_auto_flag == True and is_time_between_flag == False:
            print('ECO_MODE_OFF')
            eco_auto_flag = False

def set_flash_auto_flag():
    """
    Enables/disables flash_auto_flag depending on current time.
    """
    global flash_auto_flag
    
    # Set/Reset flash_auto_flag
    if FlashModeSchedule.Enabled.value == True:
        # check if current time is between scheduled time
        is_time_between_flag = is_time_between(FlashModeSchedule.InitTime.value, FlashModeSchedule.EndTime.value)
        if flash_auto_flag == False and is_time_between_flag == True:
            print('FLASH_MODE_ON')
            flash_auto_flag = True
        elif flash_auto_flag == True and is_time_between_flag == False:
            print('FLASH_MODE_OFF')
            flash_auto_flag = False


def is_time_between(start_time_str, end_time_str):
    """
    check if current time is between init and end times
    """
    # Parse the input time strings into datetime objects
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()
    
    # Get the current time
    current_time = datetime.datetime.now().time()
    
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
    check_time(True)
    while True:
        check_time()
        time.sleep(1)
