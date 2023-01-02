from Lightsensor import *
import RPi.GPIO as GPIO
import subprocess
import time
from screeninfo import get_monitors
from datetime import datetime

usb_power_command = "sudo uhubctl -l 1-1 -a "

spiclk = 11
spimiso = 9
spimosi = 10
spics = 8
analog_channel = 0
lcd_power_threshold = 23
lcd_power_change_threshold = 5
lcd_power_status = -1
lcd_power_switch_on_pin = 26
lcd_power_switch_off_pin = 19


def ControlDisplay(analog_channel, spiclk, spimiso, spimosi, spics, lcd_power_switch_on_pin, lcd_power_switch_off_pin, lcd_power_status, lcd_power_threshold, lcd_power_change_threshold):

    LightSwitch = 0
    light_measures = []

    for n in range(0, 3):
        light_measures.append((1023-readadc(analog_channel, spiclk, spimosi, spimiso, spics))*100/1023)
        time.sleep(0.2)

    light_measures.sort()
    lightintensity = light_measures[1]


    print("lightintensity: " + str(lightintensity) + " and lcd_power_threshold:" + str(lcd_power_threshold))
    print("on_pin: " + str(GPIO.input(lcd_power_switch_on_pin)))
    print("off_pin: " + str(GPIO.input(lcd_power_switch_off_pin)))

    if GPIO.input(lcd_power_switch_on_pin) == 1 and LightSwitch:
        lcd_power_status_new = 1
    elif GPIO.input(lcd_power_switch_off_pin) == 1 and LightSwitch:
        lcd_power_status_new = 0
    else:
        if lightintensity > (lcd_power_threshold + lcd_power_change_threshold):
            lcd_power_status_new = 1

        elif lightintensity < (lcd_power_threshold - lcd_power_change_threshold):
            lcd_power_status_new = 0
        else:
            lcd_power_status_new = lcd_power_status

    with open("/sys/bus/usb/devices/1-1/authorized") as f:
        authorized_file = f.read()

    if ((get_monitors()[0].width >= 1920) or (len(get_monitors()) > 1)) and (authorized_file[0] != "0"):
        subprocess.call(['sudo', 'sh', '/home/pi/HomeControl/usb_rights_enable.sh'])

    elif lcd_power_status != lcd_power_status_new:

        with open("/sys/bus/usb/devices/1-1/authorized") as f:
            authorized_file = f.read()

        if authorized_file[0] != "0":

            subprocess.call(['sudo', 'sh', '/home/pi/HomeControl/usb_rights_disable.sh'])
            process = subprocess.Popen((usb_power_command + str(lcd_power_status_new)).split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

        time.sleep(2)

        process = subprocess.Popen((usb_power_command + str(lcd_power_status_new)).split(), stdout=subprocess.PIPE)
        output, error = process.communicate()



    return lcd_power_status


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lcd_power_switch_on_pin, GPIO.IN)
GPIO.setup(lcd_power_switch_off_pin, GPIO.IN)

Setup_Lightsensor(spimosi, spimiso, spiclk, spics)

while 1:
    lcd_power_status = ControlDisplay(analog_channel, spiclk, spimiso, spimosi, spics, lcd_power_switch_on_pin, lcd_power_switch_off_pin, lcd_power_status, lcd_power_threshold, lcd_power_change_threshold)
    time.sleep(5)

