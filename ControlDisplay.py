from Lightsensor import *
import RPi.GPIO as GPIO
import subprocess
import time

usb_power_command = "sudo uhubctl -l 1-1 -a "

spiclk = 11
spimiso = 9
spimosi = 10
spics = 8
analog_channel = 0
lcd_power_threshold = 65
lcd_power_change_threshold = 2
lcd_power_status = 1
lcd_power_switch_on_pin = 26
lcd_power_switch_off_pin = 19


def ControlDisplay(analog_channel, spiclk, spimiso, spimosi, spics, lcd_power_switch_on_pin, lcd_power_switch_off_pin, lcd_power_status, lcd_power_threshold, lcd_power_change_threshold):

    LightSwitch = 0

    lightintensity = (1023-readadc(analog_channel, spiclk, spimosi, spimiso, spics))*100/1023

    print("lightintensity: " + str(lightintensity) + " and lcd_power_threshold:" + str(lcd_power_threshold))
    print("on_pin: " + str(GPIO.input(lcd_power_switch_on_pin)))
    print("off_pin: " + str(GPIO.input(lcd_power_switch_off_pin)))

    if GPIO.input(lcd_power_switch_on_pin) == 1 and LightSwitch:
        lcd_power_status = 1
    elif GPIO.input(lcd_power_switch_off_pin) == 1 and LightSwitch:
        lcd_power_status = 0
    else:
        if lightintensity > (lcd_power_threshold + lcd_power_change_threshold):
            lcd_power_status = 1

        elif lightintensity < (lcd_power_threshold + lcd_power_change_threshold):
            lcd_power_status = 0

        process = subprocess.Popen((usb_power_command + str(lcd_power_status)).split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        subprocess.call(['sudo', 'sh', '/home/pi/HomeControl/set_usb_rights.sh'])


    return lcd_power_status


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lcd_power_switch_on_pin, GPIO.IN)
GPIO.setup(lcd_power_switch_off_pin, GPIO.IN)

Setup_Lightsensor(spimosi, spimiso, spiclk, spics)

while 1:
    ControlDisplay(analog_channel, spiclk, spimiso, spimosi, spics, lcd_power_switch_on_pin, lcd_power_switch_off_pin, lcd_power_status, lcd_power_threshold, lcd_power_change_threshold)
    time.sleep(5)

