# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
import time
import calendar
import copy

CalendarEntries=8

def findEnd(line,line_pos_start):
    colon=line.find(';', line_pos_start)
    if colon==-1:
        colon=999
    n=line.find('\n', line_pos_start)
    if n==-1:
        n=999
    r=line.find('\r', line_pos_start)
    if r==-1:
        r=99
    return min(colon,n,r)

    

def Get_CalendarData():
                
    start_time = time.time()

    today=datetime.now()

    API_Query_Calendar='https://calendar.google.com/calendar/ical/nicopieper%40googlemail.com/private-8d3e42de6e84efb3a88b35783f6a6ad0/basic.ics'
    RawCalendar = requests.get(API_Query_Calendar)
    CalendarData=RawCalendar.text

    MoreTimeZones=True

    TimeZones={}
    pos_start=CalendarData.rfind('BEGIN:VTIMEZONE',1,10000)
    n=1
    while MoreTimeZones==True and n<5:        
        pos_start=CalendarData.find('TZNAME:',pos_start+50,10000)        
        if pos_start!=-1:
            TimeZones[n]={}
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))        
            TimeZones[n]['name']=CalendarData[pos_start+7:pos_end]
            pos_start=CalendarData.rfind('BEGIN:', 1, pos_start)+6
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            TimeZones[n]['type']=CalendarData[pos_start:pos_end]
            pos_start=CalendarData.find('TZOFFSETTO:', pos_end)+11
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            TimeZones[n]['offset']=timedelta(0, int(CalendarData[pos_start:pos_start+1] + '1') * (int(CalendarData[pos_start+1:pos_start+3])*60*60+ int(CalendarData[pos_start+3:pos_start+5])*60))
            pos_start=CalendarData.find('FREQ=', pos_end)+5
            pos_end=CalendarData.find(';', pos_start)
            Freq=CalendarData[pos_start:pos_end]
            pos_start=CalendarData.find('BYMONTH=', pos_end)+8
            pos_end=pos_end=CalendarData.find(';', pos_start)
            Bymonth=CalendarData[pos_start:pos_end]
            pos_start=CalendarData.find('BYDAY=', pos_end)+6
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            Byday=CalendarData[pos_start:pos_end]            
            if Byday=='-1SU':
                last_sunday = max(week[-1] for week in calendar.monthcalendar(today.year, int(Bymonth)))
            TimeZones[n]['start_date']=datetime(today.year, int(Bymonth), last_sunday, 2, 0, 0)
            
            
            n=n+1
        else:
            MoreTimeZones=False
            

    if today>TimeZones[1]['start_date'] and today<TimeZones[2]['start_date']:
        TimeZone=TimeZones[1]['offset']
    else:
        TimeZone=TimeZones[2]['offset']

 
#     pos_start=CalendarData.find('BEGIN:DAYLIGHT')
#     pos_start=CalendarData.find('TZOFFSETTO', pos_start)
#     pos_start=CalendarData.find(':', pos_start)+2
#     pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
#     TimeZone=timedelta(0,int(CalendarData[pos_start:pos_end][0:2])*60*60)

    n=0
    z=730    
    Events=[]
    EventsDic={}


    while z<len(RawCalendar.text):
        
        pos_start=CalendarData.find('DTSTART', z-1)
        
        if pos_start!=-1:
    #        n=n+1
    #        EventsDic[n]={}
            
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            line=CalendarData[pos_start:pos_end]
            if 'DATE' in line:
                len_line=len(line)
                event_date=line[len_line-8:len_line]
                event_time='000000'
            else:
                pos_T=line.rfind('T')
                event_date=line[pos_T-8:pos_T]
                event_time=line[pos_T+1:pos_T+7]                    

            date_time = datetime(int(event_date[0:4]), int(event_date[4:6]), int(event_date[6:8]), int(event_time[0:2]), int(event_time[2:4]), int(event_time[4:6]))
            
            #if date_time>today:
                
            n=n+1
            EventsDic[n]={}
        
            if line[len(line)-1]=='Z':
                EventsDic[n]['start_date']=date_time+TimeZone
            else:
                EventsDic[n]['start_date']=date_time

            pos_start=CalendarData.find('DTEND', pos_end)
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            line=CalendarData[pos_start:pos_end]    
            if 'DATE' in line:
                len_line=len(line)
                event_date=line[len_line-8:len_line]
                event_time='000000'            
            else:
                pos_T=line.rfind('T')
                event_date=line[pos_T-8:pos_T]
                event_time=line[pos_T+1:pos_T+7]
            date_time = datetime(int(event_date[0:4]), int(event_date[4:6]), int(event_date[6:8]), int(event_time[0:2]), int(event_time[2:4]), int(event_time[4:6]))
            if line[len(line)-1]=='Z':
                EventsDic[n]['end_date']=date_time+TimeZone
            else:
                EventsDic[n]['end_date']=date_time
                
            date_pos_end=pos_end
            
            pos_start=CalendarData.find('LOCATION', pos_end)
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            line=CalendarData[pos_start:pos_end]       
            pos_colon=line.find(':')
            EventsDic[n]['location']=line[pos_colon+1:len(line)]
            if EventsDic[n]['location']=='-' or EventsDic[n]['location']=='/' or EventsDic[n]['location']==' ':
                EventsDic[n]['location']=''

            pos_start=CalendarData.find('SUMMARY', pos_end)
            pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
            line=CalendarData[pos_start:pos_end]   
            pos_colon=line.find(':')
            EventsDic[n]['event_name']=line[pos_colon+1:len(line)]

            
            pos_end=date_pos_end
            start_Rule=CalendarData.find('RULE:', pos_end)-pos_end        
               
            if start_Rule <=40 and start_Rule>=0:
                pos_start=CalendarData.find('RULE:', pos_end)
                pos_end=min(CalendarData.find('\n', pos_start), CalendarData.find('\r', pos_start))
                line=CalendarData[pos_start:pos_end+60]
                #print(line)
                #Three repeting event options:
                    #1. Birthday: FREQ, INTERVAL; BYMONTHDAY
                    #2. Limited Event: FREQ, COUNT, BYDAY
                    #3. Unlimited EVENT: FREQ
             
                line_pos_start=line.find('FREQ=')+5
                line_pos_end=line.find(';')
                Freq=line[line_pos_start:line_pos_end]
                #print("Freq: " + Freq)
                
                if line.find('BYMONTHDAY=')!=-1:
                    line_pos_start=line.find('BYMONTHDAY=')+11
                    line_pos_end=findEnd(line,line_pos_start)
                    #print("start Bymonthday: " + str(line_pos_start))
                    #print("end Bymonthday: " + str(line_pos_end))
                    Bymonthday=line[line_pos_start:line_pos_end]
                else:
                    Bymonthday="-"
                if line.find('BYDAY=')!=-1:                                        
                    line_pos_start=line.find('BYDAY=')+6
                    line_pos_end=findEnd(line,line_pos_start)
                    #print("start Byday: " + str(line_pos_start))
                    #print("end Byday: " + str(line_pos_end))
                    Byday=line[line_pos_start:line_pos_end]
                else:
                    Byday="-"
                if line.find('COUNT=')!=-1:                                        
                    line_pos_start=line.find('COUNT=')+6
                    line_pos_end=findEnd(line,line_pos_start)
                    #print("start Count: " + str(line_pos_start))
                    #print("end Count: " + str(line_pos_end))
                    Count=int(line[line_pos_start:line_pos_end])
                else:
                    Count=9999
                if line.find('UNTIL=')!=-1:                                        
                    line_pos_start=line.find('UNTIL=')+6
                    line_pos_end=findEnd(line,line_pos_start)
                    Until=line[line_pos_start:line_pos_end]
                else:
                    Until="-"
                #print('Bymonthday: ' + str(Bymonthday))
                #print('Byday: ' + str(Byday))
                #print('Count: ' + str(Count))
                #print('Until: ' + str(Until))
                                
                
                e_start=EventsDic[n]['start_date']
                e_end=EventsDic[n]['end_date']
                if Freq=='YEARLY' and (Count==9999 or datetime(min(e_start.year+Count-1,e_start.year+5), e_start.month, e_start.day)>today):
                    #print("Yearly start date pre: " + str(EventsDic[n]['start_date']))
                    if EventsDic[n]['start_date'].strftime("%m%d")>today.strftime("%m%d"):
                        EventsDic[n]['start_date']=datetime(today.year, e_start.month, e_start.day)
                        EventsDic[n]['end_date']=datetime(today.year, e_start.month, e_start.day)+ timedelta(days=1)
                        #print(str(today.year) + " " + str(e_start.month) + " " + str(e_start.day))
                    else:
                        EventsDic[n]['start_date']=datetime(today.year+1, e_start.month, e_start.day)
                        EventsDic[n]['end_date']=datetime(today.year+1, e_end.month, e_end.day)
                        #print(str(today.year+1) + " " + str(e_start.month) + " " + str(e_start.day))
                    #print("Yearly start date: " + str(EventsDic[n]['start_date']))
                        
                if Freq=='MONTHLY' and (Count==9999 or e_start+timedelta(days=(Count-1)*31)>today):   # BIRTHDAY #CalendarData.find('BYMONTHDAY=', pos_end-2)-pos_end<40:
                    if Bymonthday!=-1:
                        if e_start.day>today.day:
                            EventsDic[n]['start_date']=datetime(today.year+int(today.month/12), today.month, e_start.day)
                            EventsDic[n]['end_date']=datetime(today.year+int(today.month/12), today.month,  e_end.day)     # Wrong for events overlapping a month
                        else:
                            EventsDic[n]['start_date']=datetime(today.year+int(today.month/12), (today.month+1)%12, e_start.day)
                            EventsDic[n]['end_date']=datetime(today.year+int(today.month/12), (today.month+1)%12,  e_end.day)
                    #print("Monthly start date: " + str(EventsDic[n]['start_date']))
                     
                
                if Freq=='WEEKLY' and (Count==9999 or e_start+timedelta(days=(Count-1)*7)>today):
                    k=1                
                    while k <=Count and e_start.year+int(k/365.25)<=today.year+1:
                        n=n+1
                        k=k+1
                        #print(n)
                        EventsDic[n]=copy.deepcopy(EventsDic[n-1])
                        #print(EventsDic[n])
                        
                        EventsDic[n]['start_date']=EventsDic[n]['start_date']+timedelta(days=7)
                        EventsDic[n]['end_date']=EventsDic[n]['end_date']+timedelta(days=7)
                        #print(EventsDic[n-1])
                        #print(EventsDic[n])
                        #print(n)
                        #print(EventsDic[n])
                        #print("\n")
                    #print(EventsDic[8])
                    #print(EventsDic[9])
                    #print(EventsDic[10])
                            
                if Freq=='DAILY' and (Count==9999 or e_start+timedelta(days=Count-1)>today):
                    k=1
                    while k <=Count and e_start.year+int(k/365.25)<=today.year+1:
                        n=n+1
                        k=k+1
                        EventsDic[n]=EventsDic[n-1]         
                            
                        EventsDic[n]['start_date']=EventsDic[n]['start_date']+timedelta(days=1)
                        EventsDic[n]['end_date']=EventsDic[n]['end_date']+timedelta(days=1)
                        #print(n)
                        #print(EventsDic[n])
                        #print("\n")
            
            #print("\n")
            z=pos_end
        else:
            z=len(CalendarData)


    #print(EventsDic)


    DicOrder=sorted(EventsDic, key=lambda x: EventsDic[x]['start_date'])

    #print(DicOrder)
    OrderedDic={}
    k=0
    z=0
    #for z in range (0,n-1):
    while k<=CalendarEntries:
        if EventsDic[DicOrder[z]]['end_date']>=today:
            OrderedDic[k]=EventsDic[DicOrder[z]]
            k=k+1
        z=z+1


    #print(time.time()-start_time)

    return OrderedDic
