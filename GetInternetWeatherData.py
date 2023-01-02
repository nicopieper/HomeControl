import requests
import json
import time
from datetime import datetime, timedelta
from Keys import Weather_Map_API_Key, latitude, longitude

Cardinal_Directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

number_forecasts = 40+1

forecast_time = list(range(0, number_forecasts))
Weather_Description = list(range(0, number_forecasts))
Weather_Description_ID = list(range(0, number_forecasts))
Icon = list(range(0, number_forecasts))
Clouds = list(range(0, number_forecasts))
Pressure = list(range(0, number_forecasts))
Pressure_Sea_Level = list(range(0, number_forecasts))
Min_Temp = list(range(0, number_forecasts))
Max_Temp = list(range(0, number_forecasts))
Temp = list(range(0, number_forecasts))
Humidity = list(range(0, number_forecasts))
Wind_Speed = list(range(0, number_forecasts))
Wind_Direction = list(range(0, number_forecasts))
Cardinal_Wind_Direction = list(range(0, number_forecasts))
DateStamp = list(range(0, number_forecasts))
TZ = list(range(0, 1))


API_Query_Now='http://api.openweathermap.org/data/2.5/weather?lat=' + str(latitude) + '&lon=' + str(longitude) + '&APPID=' + Weather_Map_API_Key
API_Query_Forecast='http://api.openweathermap.org/data/2.5/forecast?lat=' + str(latitude) + '&lon=' + str(longitude) + '&APPID=' + Weather_Map_API_Key

def Get_InternetWeatherData(latitude, longitude):
    ErrorOccured = False
    n = 0
    try:
        r = requests.get(API_Query_Now)
        json_data = json.loads(r.text)
        
        Location_Name = str(json_data['name'])
        

        sys = json_data['sys']
        Sunset = str(time.strftime('%H:%M', time.localtime(sys['sunset'])))
        Sunrise = str(time.strftime('%H:%M', time.localtime(sys['sunrise'])))

        weather = json_data['weather']
        weather = weather[0]
        Weather_Description[n] = str(weather['description'])
        Weather_Description_ID[n] = weather['id']
        Icon[n] = str(weather['icon'])
        DateStamp[n] = datetime.fromtimestamp(json_data['dt'])
        TZ[n] = timedelta(seconds=json_data['timezone'])
        

        main = json_data['main']
        Pressure[n] = str(main['pressure'])
        Min_Temp[n] = main['temp_min']-273.15
        Max_Temp[n] = main['temp_max']-273.15
        Temp[n] = str(round(main['temp']-273.15, 1))
        Humidity[n] = str(main['humidity'])

        wind = json_data['wind']
        Wind_Speed[n] = str(wind['speed'])
        if 'deg' in wind:
            Wind_Direction[n] = (wind['deg'])
            Num_Wind_Direction = int((Wind_Direction[n] + 22.5)/45)
            Cardinal_Wind_Direction[n] = Cardinal_Directions[Num_Wind_Direction % 8]
        else:
            Wind_Direction[n] = ''
            Cardinal_Wind_Direction[n] = ''
        

    except:
        ErrorOccured = True
        print("Error: " + str(n))

                
    try:
        r = requests.get(API_Query_Forecast)
        json_data = json.loads(r.text)
        forecast_list = json_data['list']
        for n in range(1, number_forecasts):
            forecast = forecast_list[n-1]
            forecast_time[n] = forecast['dt_txt']
            
            clouds = forecast['clouds']
            Clouds[n] = str(clouds['all'])

            weather = forecast['weather']
            weather = weather[0]
            Weather_Description[n] = str(weather['description'])
            Weather_Description_ID[n] = weather['id']
            Icon[n] = str(weather['icon'])
            DateStamp[n] = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')

            main = forecast['main']
            Pressure[n] = str(main['pressure'])
            Pressure_Sea_Level[n] = str(main['sea_level'])
            Min_Temp[n] = main['temp_min']-273.15
            Max_Temp[n] = main['temp_max']-273.15
            Temp[n] = str(round(main['temp']-273.15, 1))
            Humidity[n] = str(main['humidity'])

            wind = forecast['wind']
            Wind_Speed[n] = str(wind['speed'])
            if 'deg' in wind:
                Wind_Direction[n] = wind['deg']
                Num_Wind_Direction = int((Wind_Direction[n] + 22.5)/45)
                Cardinal_Wind_Direction[n] = Cardinal_Directions[Num_Wind_Direction % 8]
            else:
                Wind_Direction[n] = ''
                Cardinal_Wind_Direction[n] = ''

            Num_Wind_Direction = int((Wind_Direction[n] + 22.5)/45)
            Cardinal_Wind_Direction[n] = Cardinal_Directions[Num_Wind_Direction % 8]
            
    except:
        ErrorOccured=True
        print("Error: " + str(n))
            
        
    max_temp_forecast = []
    min_temp_forecast = []
    icon_forecast = []
    weekday_forecast = []
    k = 1
    if DateStamp[k].hour > 14:
        while DateStamp[k].day == DateStamp[k+1].day:
            k = k+1
        k = k+1

    for i in range (0, 5):
        max_temp_day = -100
        min_temp_day = 100
        num_weather_types = [0, 0, 0, 0, 0, 0, 0, 0, 0]   # thunderstorm, drizzle, rain, snow, atmosphere, clear, few clouds, scattered clouds, dark clouds
        num_entries = 0
        if k < len(DateStamp):
            DateTemp = DateStamp[k]
        
        while k < len(DateStamp) and DateStamp[k].day == DateTemp.day:
            num_entries = num_entries+1
            if Max_Temp[k] > max_temp_day:
                max_temp_day = Max_Temp[k]
            if Min_Temp[k] < min_temp_day:
                min_temp_day = Min_Temp[k]
            if Weather_Description_ID[k] in range(200, 250):#thunderstorm
                num_weather_types[0] += 1
            if Weather_Description_ID[k] in range(300, 350):#drizzle
                num_weather_types[1] += 1
            if Weather_Description_ID[k] in range(500, 550):#rain
                num_weather_types[2] += 1
            if Weather_Description_ID[k] in range(600, 650):#snow
                num_weather_types[3] = num_weather_types[3]+1
            if Weather_Description_ID[k] in range(700, 790):#atmosphere
                num_weather_types[4] = num_weather_types[4]+1
            if Weather_Description_ID[k] == 800:#clear
                num_weather_types[5] = num_weather_types[5]+1
            if Weather_Description_ID[k] == 801:#few clouds
                num_weather_types[6] = num_weather_types[6]+1
            if Weather_Description_ID[k] == 802:#scattered clouds
                num_weather_types[7] = num_weather_types[7]+1
            if Weather_Description_ID[k] in range (803, 805):#heavy clouds
                num_weather_types[8] = num_weather_types[8]+1
            k = k+1
            

        weekday_forecast.append(DateTemp.weekday())
         
        max_temp_forecast.append(round(max_temp_day))
        min_temp_forecast.append(round(min_temp_day))
        
        #print(num_weather_types)
        rel_weather_types = [x/num_entries for x in num_weather_types]
        #print(rel_weather_types)
        
        if rel_weather_types[0] > 0:#thunderstorm
            icon = "11d"
        else:
            if rel_weather_types[3] > 0:#snow
                icon = "13d"
            else:
                if rel_weather_types[2] + rel_weather_types[1] > 0:#rain
                    if 2*rel_weather_types[5] + 1.5*rel_weather_types[6] + rel_weather_types[7] < 0.4:
                        icon = "09d"#rain dark clouds
                    else:
                        icon = "10d"#rain light clouds
                else:#no rain
                    if rel_weather_types[7] > 0.5:
                        icon = "50d"#atmosphere
                    else:
                        if 2*rel_weather_types[5] + 1.5*rel_weather_types[6] + rel_weather_types[7] < 0.4 and rel_weather_types[8] > 0.5:
                            icon = "04d"#dark clouds
                        else:
                            if rel_weather_types[5] > 0.6 and rel_weather_types[6] + 1.5*rel_weather_types[7] + 2*rel_weather_types[8] < 0.35:
                                icon = "01d"#clear
                            else:
                                if 2*rel_weather_types[5] + rel_weather_types[6] > rel_weather_types[7] + 2*rel_weather_types[8]:
                                    icon = "02d"#clouds and sun
                                else:
                                    icon = "03d"#scattered clouds
     
        icon_forecast.append(icon)
            

     
    return Location_Name, Sunset, Sunrise, Weather_Description, Pressure, Pressure_Sea_Level, Min_Temp, Max_Temp, Temp, Humidity, Wind_Speed, Wind_Direction, Cardinal_Wind_Direction, forecast_time, Clouds, Icon, DateStamp, TZ, max_temp_forecast, min_temp_forecast, icon_forecast, weekday_forecast

#Location_Name, Sunset, Sunrise, Weather_Description, Pressure, Pressure_Sea_Level, Min_Temp, Max_Temp, Internet_Temp, Internet_Humidity, Wind_Speed, Wind_Direction, Cardinal_Wind_Direction, forecast_time, Clouds, Icon, DateStamp, TimeZone, max_temp_forecast, min_temp_forecast, icon_forecast, weekday_forecast = Get_InternetWeatherData(latitude, longitude)
