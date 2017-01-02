import RPi.GPIO as GPIO
import time
import os
import glob
import time

Rele = 13 # pin11

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def setup(pin):
    global RelePin
    RelePin = pin
    GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
    GPIO.setup(RelePin, GPIO.OUT)
    #GPIO.output(RelePin, GPIO.HIGH)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

def on():
    GPIO.output(RelePin, GPIO.LOW)

def off():
    GPIO.output(RelePin, GPIO.HIGH)

#def beep(x):
#    on()
#    time.sleep(x)
#    off()
#    time.sleep(x)

def readRecipe():
    print("reading recipe... TODO")

def loop():
    while True:
        beep(1)

def heat():
    while True:
        GPIO.output(RelePin, GPIO.HIGH)

def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f

def destroy():
    GPIO.output(RelePin, GPIO.LOW)
    GPIO.cleanup() # Release resource

if __name__ == '__main__': # Program start from here
    setup(Rele)
    #TODO
    # mettere tra un try catch la lettura del file della ricetta
    #read recipe from file...
    readRecipe()
    try:       
        temp=read_temp()
        heat()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()
