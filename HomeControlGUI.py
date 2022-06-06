# for rdp
# sudo chown root:rdp /dev/gpiomem
# sudo chmod g+rw /dev/gpiomem

#Overrun of label in calendar section avoidance
#Upper right corner 



DevMode=False

from tkinter import * #in python 3.x: tkinter wird kleingeschrieben
import tkinter.font
from PIL import Image, ImageTk
from time import *
import thingspeak
from GetCalendarData import *
import re
import os
import sys
import subprocess
from GetTimeDateWeekday import *
from GetInternetWeatherData import *
import threading

def thread_second():
    subprocess.call(["python3", os.path.abspath(os.path.dirname(__file__)) + "/ControlDisplay.py"])

if not DevMode:
    import RPi.GPIO as GPIO
    from MeasurePressure import *
    from MeasureTemperatureHumidity import *

    processThread = threading.Thread(target=thread_second)
    processThread.start()



    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')


Temp_Update_Interval=1
Weather_Update_Interval=1
Calendar_Update_Interval=15
Weather_Update_Failures=3
Calendar_Update_Failures=3

ts_channel_id=767213
ts_write_key="Q0YQPPTL6AZUB261"
ts_read_key="GWR487L13HJIK2FU"
thingspeakURL = 'https://api.thingspeak.com'
channel=thingspeak.Channel(id,api_key=ts_write_key,fmt='json',timeout=None,server_url=thingspeakURL)

if DevMode==False:
    WeatherIconsPath="/home/pi/HomeControl/WeatherIcons/"
else:
    WeatherIconsPath="C:/Users/nicop/HomeControl/WeatherIcons/"


weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

latitude=50.93937372944934
longitude=6.878069606047314

DHTPowerPin=20
DHTDataPin=14

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
analogChannel = 0
LCDLightPin = 18
LCDLightThreshold = 65
LCDLightChangeThreshold = 2
LCDLightDiff = 0
LCDLightStatus = 1
LCDLightSwitchOnPin=26
LCDLightSwitchOffPin=19


if DevMode==False:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DHTPowerPin, GPIO.OUT)
    GPIO.output(DHTPowerPin,1)

    DHTSensor=Python_DHT.DHT22


degree = chr(176)
humidity_list=[1,1,1]
temperature_list=[1,1,1]
ErrorOccuredDHT=[False,False,False]
temp_humidity=0
temperature=100
counter=15
BreakChars=[' ', '-', '/']


root = Tk()
root.wm_attributes('-type', 'splash')
root.title("Weather Station")
root.geometry('1024x600')
#root.geometry("+%d+%d" % (-2, -30))
root.geometry("+%d+%d" % (-2, -30))
#canvas = Canvas(root, height=600, width=1024)
#canvas.pack()
print(root.winfo_y())
print(root.winfo_x())


Font10 = tkinter.font.Font(family = 'Times', size = 10, weight = 'bold')
Font11 = tkinter.font.Font(family = 'Times', size = 11, weight = 'bold')
Font12 = tkinter.font.Font(family = 'Times', size = 12, weight = 'bold')
Font13 = tkinter.font.Font(family = 'Times', size = 13, weight = 'bold')
Font14 = tkinter.font.Font(family = 'Times', size = 14, weight = 'bold')
Font15 = tkinter.font.Font(family = 'Times', size = 15, weight = 'bold')
Font16 = tkinter.font.Font(family = 'Times', size = 16, weight = 'bold')
Font17 = tkinter.font.Font(family = 'Times', size = 17, weight = 'bold')
Font18 = tkinter.font.Font(family = 'Times', size = 18, weight = 'bold')
Font19 = tkinter.font.Font(family = 'Times', size = 19, weight = 'bold')
Font20 = tkinter.font.Font(family = 'Times', size = 20, weight = 'bold')
Font21 = tkinter.font.Font(family = 'Times', size = 21, weight = 'bold')
Font22 = tkinter.font.Font(family = 'Times', size = 22, weight = 'bold')
Font23 = tkinter.font.Font(family = 'Times', size = 23, weight = 'bold')
Font24 = tkinter.font.Font(family = 'Times', size = 24, weight = 'bold')
Font25 = tkinter.font.Font(family = 'Times', size = 25, weight = 'bold')
Font26 = tkinter.font.Font(family = 'Times', size = 26, weight = 'bold')
Font27 = tkinter.font.Font(family = 'Times', size = 27, weight = 'bold')
Font28 = tkinter.font.Font(family = 'Times', size = 28, weight = 'bold')
Font29 = tkinter.font.Font(family = 'Times', size = 29, weight = 'bold')
Font30 = tkinter.font.Font(family = 'Times', size = 30, weight = 'bold')
Font31 = tkinter.font.Font(family = 'Times', size = 31, weight = 'bold')
Font32 = tkinter.font.Font(family = 'Times', size = 32, weight = 'bold')
Font33 = tkinter.font.Font(family = 'Times', size = 33, weight = 'bold')
Font34 = tkinter.font.Font(family = 'Times', size = 34, weight = 'bold')
Font35 = tkinter.font.Font(family = 'Times', size = 35, weight = 'bold')
Font36 = tkinter.font.Font(family = 'Times', size = 36, weight = 'bold')
Font37 = tkinter.font.Font(family = 'Times', size = 37, weight = 'bold')
Font38 = tkinter.font.Font(family = 'Times', size = 38, weight = 'bold')
Font39 = tkinter.font.Font(family = 'Times', size = 39, weight = 'bold')
Font40 = tkinter.font.Font(family = 'Times', size = 40, weight = 'bold')

button = Button(root,text="OK",command=root.destroy)
button.pack(side="bottom")

Space=4
Elements=[4,5,5,3]
rows=4
ElementPositions=[]
Elementheight=(600-2*Space)/rows
VertFontSpace=13
HorFontSpace=30
TileColor='#6f80ac'                        #'#101c3e'
FontColor='white'
BackgroundColor='#404e73'                                 #'#0a1227'

canvasHintergrund = Canvas(master=root)
canvasHintergrund.place(x=-1, y=-1, width=1030, height=610)


#imageHintergrund = PhotoImage(file='BlackBackground.gif')    
#canvasHintergrund.create_image(0, 0, image=imageHintergrund, anchor='nw')
canvasHintergrund.create_rectangle(0, -2, 1030, 610, fill=BackgroundColor)

for row in range (0,rows):
    Elementwidth=(1024-2*Space)/Elements[row]
    for col in range(0,Elements[row]):
        canvasHintergrund.create_rectangle(Elementwidth*col+Space*2, Elementheight*row+Space*2, Elementwidth*(col+1), Elementheight*(row+1), fill=TileColor)
        ElementPositions.append([Elementwidth*col+Space*2, Elementheight*row+Space*2, Elementwidth*(col+1), Elementheight*(row+1)])


#SVPressure = StringVar()
#SVPressure.set('')
#lPressure = Label(root, font = Font20, textvariable = SVPressure, bg=TileColor, fg=FontColor)
#lPressure.place(x=100,y=90)

#SVAltitude = StringVar()
#SVAltitude.set('')
#lAltitude = Label(root, font = Font20, textvariable = SVAltitude, bg=TileColor, fg=FontColor)
#lAltitude.place(x=100,y=120)

#SVBMPTemp = StringVar()
#SVBMPTemp.set('')
#lBMPTemp = Label(root, font = Font20, textvariable = SVBMPTemp, bg=TileColor, fg=FontColor)
#lBMPTemp.place(x=100,y=150)

#SVLightInt = StringVar()
#SVLightInt.set('')
#lLightInt = Label(root, font = Font20, textvariable = SVLightInt, bg=TileColor, fg=FontColor)
#lLightInt.place(x=100,y=180)
        
        
#print(ElementPositions)

SVTime = StringVar()
SVTime.set('')
lTime = Label(root, font = Font35, textvariable = SVTime, bg=TileColor, fg=FontColor)
lTime.place(x=ElementPositions[0][0]+HorFontSpace,y=ElementPositions[0][1]+VertFontSpace)

SVDate = StringVar()
SVDate.set('')
lDate = Label(root, font = Font20, textvariable = SVDate, bg=TileColor, fg=FontColor)
lDate.place(x=ElementPositions[0][0]+HorFontSpace,y=ElementPositions[0][1]+VertFontSpace+60)

SVWeekday = StringVar()
SVWeekday.set('')
lWeekday = Label(root, font = Font20, textvariable = SVWeekday, bg=TileColor, fg=FontColor)
lWeekday.place(x=ElementPositions[0][0]+HorFontSpace,y=ElementPositions[0][1]+VertFontSpace+60+30)


#IMHomeTemp = Image.open("HomeTemp.png")
#IMTKHomeTemp = ImageTk.PhotoImage(IMHomeTemp)
#LAHomeTemp = Label(root, image=IMTKHomeTemp)
#LAHomeTemp.image = IMTKHomeTemp
#LAHomeTemp.place(x=281+10, y=30)

SVTemp = StringVar()
SVTemp.set('')
lTemp = Label(root, font = Font35, textvariable = SVTemp, bg=TileColor, fg=FontColor)
lTemp.place(x=ElementPositions[1][0]+HorFontSpace,y=ElementPositions[1][1]+VertFontSpace)

SVHum = StringVar()
SVHum.set('')
lHum = Label(root, font = Font20, textvariable = SVHum, bg=TileColor, fg=FontColor)
lHum.place(x=ElementPositions[1][0]+HorFontSpace,y=ElementPositions[1][1]+VertFontSpace+60)

SVSunrise = StringVar()
SVSunrise.set('')
lSunrise = Label(root, font = Font20, textvariable = SVSunrise, bg=TileColor, fg=FontColor)
lSunrise.place(x=ElementPositions[1][0]+HorFontSpace,y=ElementPositions[1][1]+VertFontSpace+60+30)

SVSunset = StringVar()
SVSunset.set('')
lSunset = Label(root, font = Font20, textvariable = SVSunset, bg=TileColor, fg=FontColor)
lSunset.place(x=ElementPositions[1][0]+HorFontSpace+100,y=ElementPositions[1][1]+VertFontSpace+60+30)


#SVMinTemp = StringVar()
#SVMinTemp.set('')
#lMinTemp = Label(root, font = FontNormal, textvariable = SVMinTemp, bg=TileColor, fg=FontColor)
#lMinTemp.place(x=100,y=330)

#SVMaxTemp = StringVar()
#SVMaxTemp.set('')
#lMaxTemp = Label(root, font = FontNormal, textvariable = SVMaxTemp, bg=TileColor, fg=FontColor)
#lMaxTemp.place(x=100,y=360)

SVIntTemp = StringVar()
SVIntTemp.set('')
lIntTemp = Label(root, font = Font35, textvariable = SVIntTemp, bg=TileColor, fg=FontColor)
lIntTemp.place(x=ElementPositions[2][0]+HorFontSpace,y=ElementPositions[2][1]+VertFontSpace)
        

SVIntHum = StringVar()
SVIntHum.set('')
lIntHum = Label(root, font = Font20, textvariable = SVIntHum, bg=TileColor, fg=FontColor)
lIntHum.place(x=ElementPositions[2][0]+HorFontSpace,y=ElementPositions[2][1]+VertFontSpace+60)

SVWindSpeed = StringVar()
SVWindSpeed.set('')
lWindSpeed = Label(root, font = Font20, textvariable = SVWindSpeed, bg=TileColor, fg=FontColor)
lWindSpeed.place(x=ElementPositions[2][0]+HorFontSpace,y=ElementPositions[2][1]+VertFontSpace+60+30)

SVTodayTempTime=[]
lTodayTempTime=[]
for i in range(0,5):
    SVTodayTempTime.append(StringVar())
    SVTodayTempTime[i].set('')
    lTodayTempTime.append(Label(root, font = Font15, textvariable = SVTodayTempTime[i], bg=TileColor, fg=FontColor, justify='left', anchor='w'))
    lTodayTempTime[i].place(x=ElementPositions[i+4][0]+HorFontSpace,y=ElementPositions[i+4][1]+10)
    
SVTodayTemp=[]
lTodayTemp=[]
for i in range(0,5):
    SVTodayTemp.append(StringVar())
    SVTodayTemp[i].set('')
    lTodayTemp.append(Label(root, font = Font25, textvariable = SVTodayTemp[i], bg=TileColor, fg=FontColor, justify='right', anchor="e"))
    lTodayTemp[i].place(x=ElementPositions[i+4][0]+HorFontSpace,y=int((ElementPositions[i+4][1]+ElementPositions[i+4][3])/2))


SVForecastTempDate=[]
lForecastTempDate=[]
for i in range(0,5):
    SVForecastTempDate.append(StringVar())
    SVForecastTempDate[i].set('')
    lForecastTempDate.append(Label(root, font = Font15, textvariable = SVForecastTempDate[i], bg=TileColor, fg=FontColor, justify='left', anchor='w'))
    lForecastTempDate[i].place(x=ElementPositions[i+9][0]+HorFontSpace,y=ElementPositions[i+9][1]+10)
    
SVForecastTemp=[]
lForecastTemp=[]
for i in range(0,5):
    SVForecastTemp.append(StringVar())
    SVForecastTemp[i].set('')
    lForecastTemp.append(Label(root, font = Font20, textvariable = SVForecastTemp[i], bg=TileColor, fg=FontColor, justify='right', anchor="e"))
    lForecastTemp[i].place(x=ElementPositions[i+9][0]+HorFontSpace,y=int((ElementPositions[i+9][1]+ElementPositions[i+9][3])/2)-16)



#    SVTodayTemp1.set('')
#    lTodayTemp1 = Label(root, font = Font15, textvariable = SVTodayTemp1, bg=TileColor, fg=FontColor)
#    lTodayTemp1.place(x=int((ElementPositions[4][0]+ElementPositions[4][0])/2),y=ElementPositions[4][1]+20)
#    
#    SVTodayTemp1= StringVar()
#    SVTodayTemp1.set('')
#    lTodayTemp1 = Label(root, font = Font15, textvariable = SVTodayTemp1, bg=TileColor, fg=FontColor)
#    lTodayTemp1.place(x=int((ElementPositions[4][0]+ElementPositions[4][0])/2),y=ElementPositions[4][1]+20)
#    
#    SVTodayTemp1= StringVar()
#    SVTodayTemp1.set('')
#    lTodayTemp1 = Label(root, font = Font15, textvariable = SVTodayTemp1, bg=TileColor, fg=FontColor)
#    lTodayTemp1.place(x=int((ElementPositions[4][0]+ElementPositions[4][0])/2),y=ElementPositions[4][1]+20)
#    
#    SVTodayTemp1= StringVar()
#    SVTodayTemp1.set('')
#    lTodayTemp1 = Label(root, font = Font15, textvariable = SVTodayTemp1, bg=TileColor, fg=FontColor)
#    lTodayTemp1.place(x=int((ElementPositions[4][0]+ElementPositions[4][0])/2),y=ElementPositions[4][1]+20)

#SVWindDirection = StringVar()
#SVWindDirection.set('')
#lWindDirection = Label(root, font = Font20, textvariable = SVWindDirection, bg=TileColor, fg=FontColor)
#lWindDirection.place(x=940,y=140)


SVCalendar1=[]
SVCalendar2=[]
SVCalendar3=[]
lCalendar1=[]
lCalendar2=[]
lCalendar3=[]
for i in range(0,3):
    SVCalendar1.append(StringVar())
    SVCalendar1[i].set('')
    SVCalendar2.append(StringVar())
    SVCalendar2[i].set('')
    SVCalendar3.append(StringVar())
    SVCalendar3[i].set('')
    lCalendar1.append(Label(root, font = Font15, textvariable = SVCalendar1[i], bg=TileColor, fg=FontColor, anchor='w'))
    lCalendar1[i].place(x=ElementPositions[i+14][0]+HorFontSpace,y=ElementPositions[i+14][1]+VertFontSpace)
    lCalendar2.append(Label(root, font = Font15, textvariable = SVCalendar2[i], bg=TileColor, fg=FontColor, anchor='w'))
    lCalendar2[-1].config(width=27)
    lCalendar2[i].place(x=ElementPositions[i+14][0]+HorFontSpace,y=ElementPositions[i+14][1]+VertFontSpace+25)
    lCalendar3.append(Label(root, font = Font20, textvariable = SVCalendar3[i], bg=TileColor, fg=FontColor, anchor='w', justify='left', wraplength=ElementPositions[i+14][2]-HorFontSpace-(ElementPositions[i+14][0]+HorFontSpace)))
    lCalendar3[i].place(x=ElementPositions[i+14][0]+HorFontSpace,y=ElementPositions[i+14][1]+VertFontSpace+25+40)


while True:
#    print(time.time()%60)
    
   # if DevMode==False:
   #     LCDLightDiff, lightintensity=ControlDisplay(analogChannel, SPICLK, SPIMOSI, SPIMISO, SPICS, LCDLightSwitchOnPin, LCDLightSwitchOffPin, LCDLightStatus, LCDLightThreshold, LCDLightChangeThreshold, LCDLightPin, LCDLightDiff)

    timestr, datestr, weekdaystr = Get_Time()
    
    SVTime.set(timestr)
    SVDate.set(datestr)
    SVWeekday.set(weekdaystr)
    root.update_idletasks()
    
    
    if counter % Weather_Update_Interval == 0:
        try:
            Location_Name, Sunset, Sunrise, Weather_Description, Pressure, Pressure_Sea_Level, Min_Temp, Max_Temp, Internet_Temp, Internet_Humidity, Wind_Speed, Wind_Direction, Cardinal_Wind_Direction, forecast_time, Clouds, Icon, DateStamp, TimeZone, max_temp_forecast, min_temp_forecast, icon_forecast, weekday_forecast = Get_InternetWeatherData(latitude, longitude)
            Weather_Update_Failures=0
            SVSunrise.set(Sunrise)
            SVSunset.set(Sunset)                
            SVIntTemp.set(Internet_Temp[0] + " " + degree +  "C")
            SVIntHum.set(Internet_Humidity[0] + " " + "%")
            SVWindSpeed.set(Wind_Speed[0] + " m/s " + str(Cardinal_Wind_Direction[0]))                        
                
            
            for i in range(0,5):
                SVTodayTempTime[i].set((DateStamp[i+1]+TimeZone[0]).strftime("%H:%M"))
                SVTodayTemp[i].set(str(round(float(Max_Temp[i+1]))) + "°")
                
            for i in range(0,5):
                SVForecastTempDate[i].set(weekdays[weekday_forecast[i]])
                SVForecastTemp[i].set(str(round(float(max_temp_forecast[i]))) + "°" + "\n" + str(round(float(min_temp_forecast[i]))) + "°")
          
        except:
            Weather_Update_Failures=Weather_Update_Failures+1
            print("Could not load weather data")
            if Weather_Update_Failures >= 4:
                SVSunrise.set("--:--")
                SVSunset.set("--:--")                
                SVIntTemp.set("--.-" + " " + degree +  "C")
                SVIntHum.set("--.-" + " " + "%")
                SVWindSpeed.set("--.-" + " m/s " + str(Cardinal_Wind_Direction[0]))
                for i in range(0,5):
                    SVTodayTempTime[i].set("--:--")
                    SVTodayTemp[i].set("--" + "°")
               
                for i in range(0,5):
                    SVForecastTempDate[i].set("")
                    SVForecastTemp[i].set("--" + "°" + "\n" + "--" + "°")
   
   
    if counter%Temp_Update_Interval==0:
    
        if DevMode==False:
        
            for i in range(0,3):        #DHT11
                humidity_list[i], temperature_list[i], ErrorOccuredDHT[i] = Get_TempHum(DHTSensor, DHTDataPin)
                
            if True in ErrorOccuredDHT:
                print("Could not sense temperature and humidity")
            else:
                # single element in temperature_list cann be 'None'. So better check that before calc sum
                
                
                humidity=round(sum(humidity_list) / len(humidity_list),0)
                if humidity<=100:
                    temp_humidity=humidity
                    temperature=round(sum(temperature_list) / len(temperature_list), 1)
                else:
                    humidity=temp_humidity

        else:

            temperature=23
            humidity=50
            
        SVTemp.set(str(temperature) + " " + degree +  "C")
        SVHum.set(str(humidity) + " %")
        
#        bmptemperature, pressure, altitude, ErrorOccuredBMP100 = func_MeasurePressure(float(Pressure_Sea_Level[1]))
#        bmptemperature=28
#        pressure=1030
#        altitude=8
#        ErrorOccuredBMP100=False
#        if ErrorOccuredBMP100==True:
#            print("Could not sense pressure, altitude and temperature")
#        else:
#            pressure=pressure/100
#           altitude=altitude
            #SVBMPTemp.set(str(bmptemperature) + " " + degree +  "C")
            #SVPressure.set(str(round(pressure,0)) + " hPa")    
            #SVAltitude.set(str(round(altitude,1)) + " m over 0")
    

  #  if DevMode==False:
  #      LCDLightDiff, lightintensity=ControlDisplay(analogChannel, SPICLK, SPIMOSI, SPIMISO, SPICS, LCDLightSwitchOnPin, LCDLightSwitchOffPin, LCDLightStatus, LCDLightThreshold, LCDLightChangeThreshold, LCDLightPin, LCDLightDiff)


    if counter%Calendar_Update_Interval==0:
    
        try:
            Calendar=Get_CalendarData()
            Calendar_Update_Failures=0
            WeekdayEvents=[]
            for i in range(0,3):
                WeekdayEvents.append(weekdays[Calendar[i]['start_date'].weekday()])
            
            #print(Calendar)
            
            for i in range (0,3):
                if Calendar[i]['start_date'].strftime("%H:%M")=="00:00" and Calendar[i]['end_date'].strftime("%H:%M") == "00:00":
                    SVCalendar1[i].set(str(WeekdayEvents[i]) + ", " + Calendar[i]['start_date'].strftime("%d.%m"))
                else:
                    SVCalendar1[i].set(str(WeekdayEvents[i]) + ", " + Calendar[i]['start_date'].strftime("%d.%m") + " - " + Calendar[i]['start_date'].strftime("%H:%M"))
                SVCalendar2[i].set(Calendar[i]['location'])
                if Calendar[i]['location']=='':
                    lCalendar3[i].place(x=ElementPositions[i+14][0]+HorFontSpace,y=ElementPositions[i+14][1]+VertFontSpace+25+9)
                else:
                    lCalendar3[i].place(x=ElementPositions[i+14][0]+HorFontSpace,y=ElementPositions[i+14][1]+VertFontSpace+25+40)
                SVCalendar3[i].set(Calendar[i]['event_name'])
        
        except:
            Calendar_Update_Failures=Calendar_Update_Failures+1
            print('Could not load Calendar')
            if Calendar_Update_Failures>=4:
                for i in range (0,3):
                    SVCalendar1[i].set("--" + ", " + "--.--" + " - " + "--:--")
                    SVCalendar2[i].set("--")
                    SVCalendar3[i].set("--")
                
        
    
    canvasHintergrund.create_rectangle(-2, -2, 1030, 610, fill=BackgroundColor)

    for row in range (0,rows):
        Elementwidth=(1024-2*Space)/Elements[row]
        for col in range(0,Elements[row]):
            canvasHintergrund.create_rectangle(Elementwidth*col+Space*2, Elementheight*row+Space*2, Elementwidth*(col+1), Elementheight*(row+1), fill=TileColor)    
   
    
    if Weather_Update_Failures<4:
        photoimage=[]
        AddSpace=0    
        for i in range (3, 14):
            if i<9:
                IconName=WeatherIconsPath + Icon[i-3]+".png"
            else:
                IconName=WeatherIconsPath + icon_forecast[i-9]+".png"
            
            if i>3:
                AddSpace=25
            photoimage.append(ImageTk.PhotoImage(file=IconName))
            #photoimage.append(ImageTk.PhotoImage(image=PIL.Image.fromarray(IconName)))
            #imgtk = ImageTk.PhotoImage(image=cv2image) with imgtk = ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image))
            canvasHintergrund.create_image(int((ElementPositions[i][0]+ElementPositions[i][2])/2+AddSpace+10), int((ElementPositions[i][1]+ElementPositions[i][3])/2+AddSpace), image=photoimage[i-3])
    
    root.update_idletasks()

        
    if DevMode==False:

        try:
            #response = channel.update({'field1': temperature, 'field2': humidity, 'field3': bmptemperature, 'field4': pressure, 'field5': altitude, 'field6': lightintensity})
            response = channel.update({'field1': temperature, 'field2': humidity, 'field6': lightintensity})
        except:
            print("An exception occurred during the data upload")
            pass

    
    if Weather_Update_Failures>=2 and Calendar_Update_Failures>=2:
        f = open("demofile2.txt", "r")
        LastBug=int(f.read())

        if not LastBug or int(time.time()) - LastBug > 60*60: # 1 hour
            f = open("Bugfile.txt", "w")
            f.write(int(time.time()))
            f.close()
        subprocess.call('sudo reboot', shell=True, stderr=subprocess.PIPE)
    else:
        f = open("Bugfile.txt", "w")
        f.write("")
        f.close()
        
    counter=counter+1

  #  if DevMode==False:
  #      LCDLightDiff, lightintensity=ControlDisplay(analogChannel, SPICLK, SPIMOSI, SPIMISO, SPICS, LCDLightSwitchOnPin, LCDLightSwitchOffPin, LCDLightStatus, LCDLightThreshold, LCDLightChangeThreshold, LCDLightPin, LCDLightDiff)
        
    sleep(60-time.time()%60)    


