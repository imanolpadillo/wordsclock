# *************************************************************************************************** 
# **************************************** WORDSCLOCK (MAIN) ****************************************
# *************************************************************************************************** 
import datetime, time
import pytz
import holidays
import threading
import button
import leds
import wlogging
from wlogging import LogType, LogMessage
from wordsclockEnum import ButtonStatus, ClockMode, FLASH_SECONDS_ON, ECO_MODE_SCHEDULE, \
     ECO_MODE_HOLIDAYS, ECO_MODE_HOLIDAYS_SCHEDULE

# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
change_in_mode = False      # defines if a mode has been changed
eco_mode = False            # mixes scheduled alwayson + alwaysoff + flash
flash_mode = False          # leds are only activated during a few seconds in time change
alwayson_mode = False       # leds are always activated
alwaysoff_mode = False      # leds are always deactivated

# *************************************************************************************************** 
# FUNCTIONS
# ***************************************************************************************************
def thread_check_button():
    """
    Checks button status:
    - Short1Click: alwayson_mode
    - Short2Click: flash_mode
    - Short3Click: eco_mode
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
            if button_status == ButtonStatus.Short1Click.value:                # alwayson_mode
                wlogging.log(LogType.INFO.value,LogMessage.ALWAYSON_MODE.name,LogMessage.ALWAYSON_MODE.value)
                alwayson_mode = True
            elif button_status == ButtonStatus.Short2Click.value:              # flash_mode
                wlogging.log(LogType.INFO.value,LogMessage.FLASH_MODE.name,LogMessage.FLASH_MODE.value)
                flash_mode = True
            elif button_status == ButtonStatus.Short3Click.value:              # eco_mode
                wlogging.log(LogType.INFO.value,LogMessage.ECO_MODE.name,LogMessage.ECO_MODE.value)
                eco_mode = True
            elif button_status == ButtonStatus.LongClick.value:                # alwaysoff_mode
                wlogging.log(LogType.INFO.value,LogMessage.ALWAYSOFF_MODE.name,LogMessage.ALWAYSOFF_MODE.value)
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
    try:
        madrid_tz = pytz.timezone('Europe/Madrid')
        now = datetime.datetime.now(madrid_tz)
        current_time = now.replace(microsecond=0).time()
        current_day = now.weekday() # 0: Monday, 6: Sunday
    except:
        wlogging.log(LogType.INFO.value,LogMessage.ERR_WIFI_CONN.name,LogMessage.ERR_WIFI_CONN.value)
        return False
    if (current_time.minute % 5 == 0 and current_time.second == 0) or change_in_mode == True:
        change_in_mode = False
        eco_flash = False         # in eco mode: flash flag
        eco_alwaysoff = False     # in eco mode: alwaysoff flag
        log_suffix = ""
        # Check current mode
        if eco_mode:                               # eco_mode: it is derived to alwaysoff, flash or alwayson
            eco_flag = get_eco_flag(now.today(), current_day, current_time.hour)
            if eco_flag == ClockMode.ALWAYSOFF.value: 
                eco_alwaysoff = True
            elif eco_flag == ClockMode.FLASH.value: 
                eco_flash = True
        if flash_mode or eco_flash:                # flash_mode
            leds.set_time(current_time)
            time.sleep(FLASH_SECONDS_ON)
            leds.reset(False)     
            log_suffix = " (FLASH)"
        elif alwaysoff_mode or eco_alwaysoff:      # alwaysoff_mode
            leds.reset(False)     
            log_suffix = " (OFF)"
        else:                                      # alwayson_mode
            leds.set_time(current_time)
        # Log time change
        wlogging.log(LogType.INFO.value,LogMessage.TIME_CHG.value, current_time.strftime("%H:%M") + log_suffix)

def is_today_spanish_national_holiday():
    """
    Check if today is a Spanish national holiday
    """
    today = datetime.date.today()
    spanish_holidays = holidays.Spain()  # No 'year' argument

    # Filter for national holidays (not regional/local)
    national_holidays = {
        date for date, name in spanish_holidays.items()
        if "Nacional" in name or "national" in name.lower()
    }

    return today in national_holidays

def get_eco_flag (current_date, current_day, current_hour):
    """
    check if current date is holiday
    check if current time is between eco scheduled init and end times
    """
    try:
        today_tuple = (current_date.month, current_date.day)
        if today_tuple in ECO_MODE_HOLIDAYS or is_today_spanish_national_holiday():
            eco_flag = ECO_MODE_HOLIDAYS_SCHEDULE[current_hour]
        else:
            # No holiday
            today_schedule = ECO_MODE_SCHEDULE[current_day]
            eco_flag = today_schedule[current_hour]
        return eco_flag
    except:
        return ClockMode.ALWAYSON.value

# *************************************************************************************************** 
# MAIN
# ***************************************************************************************************
if __name__ == "__main__":
    wlogging.log(LogType.INFO.value,LogMessage.SWITCH_ON.name, LogMessage.SWITCH_ON.value)
    leds.reset(True)  # reset all leds (activating all first)
    # Create a thread to check button status
    thread = threading.Thread(target=thread_check_button)
    thread.start()

    # check time first time avoiding waiting 5 minutes
    eco_mode = True
    change_in_mode = True
    while True:
        check_time()
        time.sleep(1)
