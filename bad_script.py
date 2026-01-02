import os
import time

def get_info():
    t = os.popen('vcgencmd measure_temp').readline()
    t = t.replace("temp=","").replace("'C\n","")
    return t

while True:
    print("Temp is: " + get_info())
    time.sleep(5)
    