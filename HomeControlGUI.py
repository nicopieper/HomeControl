# for rdp
# sudo chown root:rdp /dev/gpiomem
# sudo chmod g+rw /dev/gpiomem

#Overrun of label in calendar section avoidance
#Upper right corner 


DevMode = False

from tkinter import * #in python 3.x: tkinter wird kleingeschrieben
import tkinter.font
from PIL import Image, ImageTk
from time import *
import thingspeak
from GetCalendarData import *
import os
import subprocess
from GetTimeDateWeekday import *
from GetInternetWeatherData import *
import threading
from Keys import ts_channel_id, ts_write_key, ts_read_key
from Configuration import Config, Disp
from datetime import datetime
from screeninfo import get_monitors

with open("/sys/bus/usb/devices/1-1/authorized") as f:
    authorized_file = f.read()

with open("tmp.txt", "a") as f:
    f.write("Main: " + str(datetime.now()) + "\n" + str(get_monitors()[0].width) + "\n" + authorized_file[0] + "\n")

confi = Config()


def thread_second():
    subprocess.call(["python3", os.path.abspath(os.path.dirname(__file__)) + "/ControlDisplay.py"])


if not DevMode:
    import RPi.GPIO as GPIO
    from MeasureTemperatureHumidity import *

    processThread = threading.Thread(target=thread_second)
    processThread.start()

    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')


humidity_list = [1, 1, 1]
temperature_list = [1, 1, 1]
ErrorOccuredDHT = [False, False, False]
temp_humidity = 0
temperature = 100
counter = 15

channel = thingspeak.Channel(id, api_key=ts_write_key, fmt='json', timeout=None,server_url=confi.thingspeak_url)

if not DevMode:
    WeatherIconsPath = "/home/pi/HomeControl/WeatherIcons/"
else:
    WeatherIconsPath = "C:/Users/nicop/HomeControl/WeatherIcons/"


if not DevMode:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(confi.dht_power_pin, GPIO.OUT)
    GPIO.output(confi.dht_power_pin, 1)

    DHTSensor = Python_DHT.DHT22


disp = Disp()


while True:

    timestr, datestr, confi.weekdaystr = Get_Time()
    
    disp.SVTime.set(timestr)
    disp.SVDate.set(datestr)
    disp.SVWeekday.set(confi.weekdaystr)
    disp.root.update_idletasks()

    if counter % confi.weather_update_interval == 0:
        try:
            Location_Name, Sunset, Sunrise, Weather_Description, Pressure, Pressure_Sea_Level, Min_Temp, Max_Temp, Internet_Temp, Internet_Humidity, Wind_Speed, Wind_Direction, Cardinal_Wind_Direction, forecast_time, Clouds, Icon, DateStamp, TimeZone, max_temp_forecast, min_temp_forecast, icon_forecast, weekday_forecast = Get_InternetWeatherData(latitude, longitude)
            confi.weather_update_failures=0
            disp.SVSunrise.set(Sunrise)
            disp.SVSunset.set(Sunset)                
            disp.SVIntTemp.set(Internet_Temp[0] + " " + confi.degree +  "C")
            disp.SVIntHum.set(Internet_Humidity[0] + " " + "%")
            disp.SVWindSpeed.set(Wind_Speed[0] + " m/s " + str(Cardinal_Wind_Direction[0]))                        

            for i in range(0,5):
                disp.SVTodayTempTime[i].set((DateStamp[i+1]+TimeZone[0]).strftime("%H:%M"))
                disp.SVTodayTemp[i].set(str(round(float(Max_Temp[i+1]))) + "°")
                
            for i in range(0,5):
                disp.SVForecastTempDate[i].set(confi.weekdays[weekday_forecast[i]])
                disp.SVForecastTemp[i].set(str(round(float(max_temp_forecast[i]))) + "°" + "\n" + str(round(float(min_temp_forecast[i]))) + "°")
          
        except:
            confi.weather_update_failures=confi.weather_update_failures+1
            print("Could not load weather data")
            if confi.weather_update_failures >= 4:
                disp.SVSunrise.set("--:--")
                disp.SVSunset.set("--:--")                
                disp.SVIntTemp.set("--.-" + " " + confi.degree +  "C")
                disp.SVIntHum.set("--.-" + " " + "%")
                disp.SVWindSpeed.set("--.-" + " m/s " + str(Cardinal_Wind_Direction[0]))
                for i in range(0,5):
                    disp.SVTodayTempTime[i].set("--:--")
                    disp.SVTodayTemp[i].set("--" + "°")
               
                for i in range(0,5):
                    disp.SVForecastTempDate[i].set("")
                    disp.SVForecastTemp[i].set("--" + "°" + "\n" + "--" + "°")
   
   
    if counter % confi.temp_update_interval == 0:
    
        if not DevMode:
        
            for i in range(0, 3):        #DHT11
                humidity_list[i], temperature_list[i], ErrorOccuredDHT[i] = Get_TempHum(DHTSensor, confi.dht_data_pin)
                
            if True in ErrorOccuredDHT:
                print("Could not sense temperature and humidity")
            else:
                # single element in temperature_list cann be 'None'. So better check that before calc sum
                
                
                humidity = round(sum(humidity_list) / len(humidity_list),0)
                if humidity <= 100:
                    temp_humidity = humidity
                    temperature = round(sum(temperature_list) / len(temperature_list), 1)
                else:
                    humidity = temp_humidity

        else:

            temperature = 23
            humidity = 50
            
        disp.SVTemp.set(str(temperature) + " " + confi.degree + "C")
        disp.SVHum.set(str(humidity) + " %")
        

    if counter % confi.calendar_update_interval == 0:
    
        try:
            Calendar = Get_CalendarData()
            confi.calendar_update_failures = 0
            WeekdayEvents = []
            for i in range(0, 3):
                WeekdayEvents.append(confi.weekdays[Calendar[i]['start_date'].weekday()])
            
            #print(Calendar)
            
            for i in range(0, 3):
                if Calendar[i]['start_date'].strftime("%H:%M") == "00:00" and Calendar[i]['end_date'].strftime("%H:%M") == "00:00":
                    disp.SVCalendar1[i].set(str(WeekdayEvents[i]) + ", " + Calendar[i]['start_date'].strftime("%d.%m"))
                else:
                    disp.SVCalendar1[i].set(str(WeekdayEvents[i]) + ", " + Calendar[i]['start_date'].strftime("%d.%m") + " - " + Calendar[i]['start_date'].strftime("%H:%M"))
                disp.SVCalendar2[i].set(Calendar[i]['location'])
                if Calendar[i]['location'] == '':
                    disp.lCalendar3[i].place(x=disp.element_positions[i+14][0]+disp.hor_font_space, y=disp.element_positions[i+14][1]+disp.vert_font_space+25+9)
                else:
                    disp.lCalendar3[i].place(x=disp.element_positions[i+14][0]+disp.hor_font_space, y=disp.element_positions[i+14][1]+disp.vert_font_space+25+40)
                disp.SVCalendar3[i].set(Calendar[i]['event_name'])
        
        except:
            confi.calendar_update_failures = confi.calendar_update_failures+1
            print('Could not load Calendar')
            if confi.calendar_update_failures >= 4:
                for i in range(0, 3):
                    disp.SVCalendar1[i].set("--" + ", " + "--.--" + " - " + "--:--")
                    disp.SVCalendar2[i].set("--")
                    disp.SVCalendar3[i].set("--")

    disp.canvas_background.create_rectangle(-2, -2, 1030, 610, fill=disp.background_color)

    for row in range(0, disp.rows):
        disp.elements_width = (1024-2*disp.space)/disp.elements_per_row[row]
        for col in range(0, disp.elements_per_row[row]):
            disp.canvas_background.create_rectangle(disp.elements_width*col+disp.space*2, disp.element_height*row+disp.space*2, disp.elements_width*(col+1), disp.element_height*(row+1), fill=disp.tile_color)    

    if confi.weather_update_failures < 4:
        photoimage = []
        add_space = 0
        for i in range(3, 14):
            if i < 9:
                IconName = WeatherIconsPath + Icon[i-3]+".png"
            else:
                IconName = WeatherIconsPath + icon_forecast[i-9]+".png"
            
            if i > 3:
                add_space = 25
            photoimage.append(ImageTk.PhotoImage(file=IconName))
            #photoimage.append(ImageTk.PhotoImage(image=PIL.Image.fromarray(IconName)))
            #imgtk = ImageTk.PhotoImage(image=cv2image) with imgtk = ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image))
            disp.canvas_background.create_image(int((disp.element_positions[i][0]+disp.element_positions[i][2])/2+add_space+10), int((disp.element_positions[i][1]+disp.element_positions[i][3])/2+add_space), image=photoimage[i-3])
    
    disp.root.update_idletasks()

        
    # if not DevMode:

        # try:
        #     #response = channel.update({'field1': temperature, 'field2': humidity, 'field3': bmptemperature, 'field4': pressure, 'field5': altitude, 'field6': lightintensity})
        #     response = channel.update({'field1': temperature, 'field2': humidity, 'field6': lightintensity})
        # except:
        #     print("An exception occurred during the data upload")
        #     pass

    
    if confi.weather_update_failures >= 2 and confi.calendar_update_failures >= 2:
        f = open("Bugfile.txt", "w")
        f.write(str(int(time.time())))
        f.close()
        subprocess.call('sudo reboot', shell=True, stderr=subprocess.PIPE)
    else:
        f = open("Bugfile.txt", "w")
        f.write("")
        f.close()
        
    counter = counter+1

    sleep(60-time.time() % 60)


