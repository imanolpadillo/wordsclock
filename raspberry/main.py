# *************************************************************************************************** 
# **************************************** WORDSCLOCK (MAIN) ****************************************
# *************************************************************************************************** 
import datetime
import pytz
import threading
import button
import leds
from wordsclockEnum import ButtonStatus, EcoModeSchedule

# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
eco_auto_flag = False       # deactivates display in eco time slot
eco_manual_flag = False     # deactivates display when long click unt short click
force_display = False       # displays time instantaneously

# *************************************************************************************************** 
# FUNCTIONS
# ***************************************************************************************************

def thread_check_time():
    """
    At every new hour checks if eco_mode must be activated.
    At minute%5 updates time.
    Force_display flag updates time always.
    """
    global eco_auto_flag,eco_manual_flag,force_display
    madrid_tz = pytz.timezone('Europe/Madrid')
    current_time = datetime.datetime.now(madrid_tz)
    if (current_time.minute == 0 and current_time.second == 0):
        set_eco_auto_flag(current_time)
    if force_display == True or (eco_auto_flag == False and eco_manual_flag == False and (current_time.minute % 5 == 0 and current_time.second == 0)):
        force_display = False
        leds.set_time(current_time)
    # Schedule the function to be called again after 1 second
    threading.Timer(1, thread_check_time).start()

def thread_check_button():
    """
    Checks button status:
    - LongClick: Enables eco_manual mode
    - ShortClick: Disables eco_manual/eco_auto mode
    """
    global eco_auto_flag, eco_manual_flag, force_display
    button_status = button.get_status()
    if button_status == ButtonStatus.LongClick.value:
        eco_manual_flag = True
    elif button_status == ButtonStatus.ShortClick.value:
        eco_manual_flag = False
        eco_auto_flag = False
        force_display = True
    elif button_status == ButtonStatus.SuperLongClick.value:
        leds.reset(True)  # reset all leds (activating all first)
        eco_manual_flag = False
        eco_auto_flag = False
        force_display = True
    # Schedule the function to be called again after 0.1 second
    threading.Timer(0.1, thread_check_button).start()

def set_eco_auto_flag(current_time):
    """
    Enables/disables eco_auto_flag depending on current time.
    """
    global eco_auto_flag, force_display
    # Set eco_auto_flag at init_hour
    if int(current_time.strftime("%H")) == EcoModeSchedule.InitHour.value and int(current_time.strftime("%M")) == 0 and \
        int(current_time.strftime("%S")) == 0 and eco_auto_flag == False:
        leds.reset(False)  # reset all leds
        eco_auto_flag = True
    # Reset eco_auto_flag at end_hour
    if int(current_time.strftime("%H")) == EcoModeSchedule.EndHour.value and int(current_time.strftime("%M")) == 0 and \
        int(current_time.strftime("%S")) == 0 and eco_auto_flag == True:
        eco_auto_flag = False

# *************************************************************************************************** 
# MAIN
# ***************************************************************************************************
if __name__ == "__main__":
    leds.reset(True)  # reset all leds (activating all first)
    thread_check_time()
    thread_check_button()
