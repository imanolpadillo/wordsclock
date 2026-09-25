# *************************************************************************************************** 
# ********************************************* PCF8574 *********************************************
# *************************************************************************************************** 
import threading
import time
import pcf8574_io
from wordsclockEnum import GPIOList

# *************************************************************************************************** 
# I2C THREAD SAFETY AND RETRY WRAPPER
# *************************************************************************************************** 

i2c_lock = threading.RLock()

class ThreadSafePCF:
    """
    Thread-safe wrapper around pcf8574_io.PCF with automatic retries for transient I2C errors.
    """
    def __init__(self, address):
        self.address = address
        self._pcf = pcf8574_io.PCF(address)

    def _retry_call(self, func, *args, max_retries=3, delay=0.01, **kwargs):
        with i2c_lock:
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (OSError, IOError):
                    if attempt == max_retries:
                        raise
                    time.sleep(delay * attempt)

    def pin_mode(self, pin_name, mode):
        return self._retry_call(self._pcf.pin_mode, pin_name, mode)

    def write(self, pin_name, val):
        return self._retry_call(self._pcf.write, pin_name, val)

    def read(self, pin_name):
        return self._retry_call(self._pcf.read, pin_name)

    def __getattr__(self, item):
        attr = getattr(self._pcf, item)
        if callable(attr):
            def wrapper(*args, **kwargs):
                return self._retry_call(attr, *args, **kwargs)
            return wrapper
        return attr

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

s0 = ThreadSafePCF(0x20)
s1 = ThreadSafePCF(0x21)
s2 = ThreadSafePCF(0x22)
s3 = ThreadSafePCF(0x23)

# set pins as output
s0.pin_mode(GPIOList.S0_0_E.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_1_S.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_2_ON.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_3_LA.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_4_S_2.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_5_UNA.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_6_DOS.value, "OUTPUT")
s0.pin_mode(GPIOList.S0_7_TRES.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_0_CUATRO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_1_CINCO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_2_SEIS.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_3_SIETE.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_4_OCHO.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_5_NUEVE.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_6_DIEZ.value, "OUTPUT")
s1.pin_mode(GPIOList.S1_7_ONCE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_0_DOCE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_1_Y.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_2_MENOS.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_3_VEINTE.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_4_DIEZ_2.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_5_VEINTI.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_6_CINCO_2.value, "OUTPUT")
s2.pin_mode(GPIOList.S2_7_MEDIA.value, "OUTPUT")
s3.pin_mode(GPIOList.S3_0_CUARTO.value, "OUTPUT")
s3.pin_mode(GPIOList.S3_1_BUTTON.value, "INPUT")