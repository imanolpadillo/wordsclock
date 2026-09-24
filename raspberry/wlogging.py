# *************************************************************************************************** 
# ******************************************** WLOGGING *********************************************
# *************************************************************************************************** 

import logging, os
import sys
import threading
import traceback
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
    CRITICAL = 3

class LogMessage(Enum):
    SWITCH_ON =     'Starting wordsclock!'
    TIME_CHG =      'TIME_CHG'
    ERR_WIFI_CONN = 'Unable to connect to WIFI'
    ECO_MODE =      'ECO MODE activated'
    FLASH_MODE =    'FLASH MODE activated'
    ALWAYSON_MODE = 'ALWAYSON MODE activated'
    ALWAYSOFF_MODE ='ALWAYSOFF MODE activated'
    FATAL_ERROR =   'FATAL ERROR'


current_path = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_path, 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'wordsclock.log'),
    level=logging.INFO,
    format='%(message)s'
)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def log(logType, logId, message = ''):
    madrid_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(madrid_tz)
    log_line = now.strftime("%Y-%m-%d %H:%M")
    if logType in (LogType.ERROR.value, LogType.CRITICAL.value): 
        logidlength = LOGID_MAX_LEN - 1
    else:
        logidlength = LOGID_MAX_LEN
    while len(logId) < logidlength:
        logId = ' ' + logId
    log_line += ' [' + logId + '] ' + str(message)
    if logType == LogType.INFO.value:
        logging.info(log_line)
    elif logType == LogType.CRITICAL.value:
        logging.critical(log_line)
    else:
        logging.error(log_line)
    print(log_line)

def log_exception(logId, message='', exc=None):
    """
    Logs an exception and its full stack trace to the log file.
    """
    if exc is None:
        exc_type, exc_val, exc_tb = sys.exc_info()
        tb_lines = traceback.format_exception(exc_type, exc_val, exc_tb)
    elif isinstance(exc, BaseException):
        tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    else:
        tb_lines = [str(exc)]
    
    tb_text = "".join(tb_lines).strip()
    full_message = f"{message}\n{tb_text}" if message else tb_text
    log(LogType.ERROR.value, logId, full_message)

def _uncaught_exception_handler(exc_type, exc_val, exc_tb):
    """
    Handler for uncaught exceptions in the main thread.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_val, exc_tb)
        return
    tb_lines = traceback.format_exception(exc_type, exc_val, exc_tb)
    tb_text = "".join(tb_lines).strip()
    log(LogType.CRITICAL.value, LogMessage.FATAL_ERROR.name, f"Uncaught exception terminating program:\n{tb_text}")

def _thread_exception_handler(args):
    """
    Handler for uncaught exceptions in background threads (Python 3.8+).
    """
    if issubclass(args.exc_type, KeyboardInterrupt):
        return
    tb_lines = traceback.format_exception(args.exc_type, args.exc_val, args.exc_tb)
    tb_text = "".join(tb_lines).strip()
    thread_name = args.thread.name if args.thread else "UnknownThread"
    log(LogType.CRITICAL.value, LogMessage.FATAL_ERROR.name, f"Uncaught exception in thread '{thread_name}':\n{tb_text}")

# Install global exception hooks
sys.excepthook = _uncaught_exception_handler
if hasattr(threading, 'excepthook'):
    threading.excepthook = _thread_exception_handler
