# *************************************************************************************************** 
# ******************************************** WLOGGING *********************************************
# *************************************************************************************************** 

import logging, os
import pytz
from datetime import datetime
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

LOGID_MAX_LEN = 14

class LogType(Enum):
    INFO = 1
    ERROR = 2

class LogMessage(Enum):
    SWITCH_ON =     'Starting wordsclock!'
    TIME_CHG =      'TIME_CHG'
    ERR_WIFI_CONN = 'Unable to connect to WIFI'
    ECO_MODE =      'ECO MODE activated'
    FLASH_MODE =    'FLASH MODE activated'
    ALWAYSON_MODE = 'ALWAYSON MODE activated'
    ALWAYSOFF_MODE ='ALWAYSON MODE activated'


# logging.basicConfig(filename='/home/pi/Documents/weather4cast/logs/weather4cast.log', level=logging.INFO)
current_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=current_path+'/logs/wordsclock.log', level=logging.INFO)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def log(logType, logId, message = ''):
    madrid_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(madrid_tz)
    log = now.strftime("%Y-%m-%d %H:%M")
    if logType == LogType.ERROR.value: 
        logidlength = LOGID_MAX_LEN - 1
    else:
        logidlength = LOGID_MAX_LEN
    while len(logId) < logidlength:
        logId = ' ' + logId
    log += ' [' + logId + '] ' + message
    if logType == LogType.INFO.value:
        logging.info(log)
    else:
        logging.error(log)
    print(log)
