import datetime

weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

def Get_Time():
    now=datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    hour=now.hour
    minute=now.minute
    second=now.second


    if minute>=10:
        minutestr=str(minute)
    else:
        minutestr="0" + str(minute)
    if hour>=10:
        hourstr=str(hour)
    else:
        hourstr="0" + str(hour)
        
    timestr=hourstr + ":" + minutestr
        
    
    if day>=10:
        daystr=str(day)
    else:
        daystr="0" + str(day)
    if month>=10:
        monthstr=str(month)
    else:
        monthstr="0" + str(month)
        
    datestr=daystr + "." + monthstr + "." + str(year)
    
    datetime.datetime.today()   
    weekdaystr=weekDays[datetime.datetime.today().weekday()]
        
    return timestr, datestr, weekdaystr
    
