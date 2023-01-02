from tkinter import * #in python 3.x: tkinter wird kleingeschrieben
import tkinter.font
from PIL import Image, ImageTk


class Config:

    def __init__(self):

        self.temp_update_interval = 1
        self.weather_update_interval = 1
        self.calendar_update_interval = 15
        self.weather_update_failures = 3
        self.calendar_update_failures = 3

        self.thingspeak_url = 'https://api.thingspeak.com'

        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        self.dht_power_pin = 20
        self.dht_data_pin = 14

        self.spiclk = 11
        self.spimiso = 9
        self.spimosi = 10
        self.spics = 8
        self.analog_channel = 0
        self.lcd_power_pin = 18
        self.lcd_power_threshold = 65
        self.lcd_power_change_threshold = 2
        self.lcd_power_status = 1
        self.lcd_power_switch_on_pin = 26
        self.lcd_power_switch_off_pin = 19

        self.degree = chr(176)
        self.humidity_list = [1, 1, 1]
        self.temperature_list = [1, 1, 1]
        self.ErrorOccuredDHT = [False, False, False]
        self.temp_humidity = 0
        self.temperature = 100
        self.counter = 15


class Disp(object):

    def __init__(self):
        self.space = 4
        self.elements_per_row = [4, 5, 5, 3]

        self.rows = 4
        self.element_positions = []
        self.element_height = (600 - 2 * self.space) / self.rows
        self.vert_font_space = 13
        self.hor_font_space = 30
        self.tile_color = '#6f80ac'  # '#101c3e'
        self.font_color = 'white'
        self.background_color = '#404e73'

        self.root = Tk()
        self.root.wm_attributes('-type', 'splash')
        self.root.title("Weather Station")
        self.root.geometry('1024x600')
        self.root.geometry("+%d+%d" % (-2, -30))

        self.font = [tkinter.font.Font(family='Times', size=size, weight='bold') for size in range(1, 41)]

        self.canvas_background = Canvas(master=self.root)
        self.canvas_background.place(x=-1, y=-1, width=1030, height=610)
        self.canvas_background.create_rectangle(0, -2, 1030, 610, fill=self.background_color)

        for row in range(0, self.rows):
            self.elements_width = (1024 - 2 * self.space) / self.elements_per_row[row]
            for col in range(0, self.elements_per_row[row]):
                self.canvas_background.create_rectangle(self.elements_width * col + self.space * 2,
                                                        self.element_height * row + self.space * 2,
                                                        self.elements_width * (col + 1),
                                                        self.element_height * (row + 1), fill=self.tile_color)
                self.element_positions.append(
                    [self.elements_width * col + self.space * 2, self.element_height * row + self.space * 2,
                     self.elements_width * (col + 1), self.element_height * (row + 1)])

        self.SVTime = StringVar()
        self.SVTime.set('')
        self.lTime = Label(self.root, font=self.font[35], textvariable=self.SVTime, bg=self.tile_color,
                           fg=self.font_color)
        self.lTime.place(x=self.element_positions[0][0] + self.hor_font_space,
                         y=self.element_positions[0][1] + self.vert_font_space)

        self.SVDate = StringVar()
        self.SVDate.set('')
        self.lDate = Label(self.root, font=self.font[20], textvariable=self.SVDate, bg=self.tile_color,
                           fg=self.font_color)
        self.lDate.place(x=self.element_positions[0][0] + self.hor_font_space,
                         y=self.element_positions[0][1] + self.vert_font_space + 60)

        self.SVWeekday = StringVar()
        self.SVWeekday.set('')
        self.lWeekday = Label(self.root, font=self.font[20], textvariable=self.SVWeekday, bg=self.tile_color,
                              fg=self.font_color)
        self.lWeekday.place(x=self.element_positions[0][0] + self.hor_font_space,
                            y=self.element_positions[0][1] + self.vert_font_space + 60 + 30)

        self.SVTemp = StringVar()
        self.SVTemp.set('')
        self.lTemp = Label(self.root, font=self.font[35], textvariable=self.SVTemp, bg=self.tile_color,
                           fg=self.font_color)
        self.lTemp.place(x=self.element_positions[1][0] + self.hor_font_space,
                         y=self.element_positions[1][1] + self.vert_font_space)

        self.SVHum = StringVar()
        self.SVHum.set('')
        self.lHum = Label(self.root, font=self.font[20], textvariable=self.SVHum, bg=self.tile_color,
                          fg=self.font_color)
        self.lHum.place(x=self.element_positions[1][0] + self.hor_font_space,
                        y=self.element_positions[1][1] + self.vert_font_space + 60)

        self.SVSunrise = StringVar()
        self.SVSunrise.set('')
        self.lSunrise = Label(self.root, font=self.font[20], textvariable=self.SVSunrise, bg=self.tile_color,
                              fg=self.font_color)
        self.lSunrise.place(x=self.element_positions[1][0] + self.hor_font_space,
                            y=self.element_positions[1][1] + self.vert_font_space + 60 + 30)

        self.SVSunset = StringVar()
        self.SVSunset.set('')
        self.lSunset = Label(self.root, font=self.font[20], textvariable=self.SVSunset, bg=self.tile_color,
                             fg=self.font_color)
        self.lSunset.place(x=self.element_positions[1][0] + self.hor_font_space + 100,
                           y=self.element_positions[1][1] + self.vert_font_space + 60 + 30)

        self.SVIntTemp = StringVar()
        self.SVIntTemp.set('')
        self.lIntTemp = Label(self.root, font=self.font[35], textvariable=self.SVIntTemp, bg=self.tile_color,
                              fg=self.font_color)
        self.lIntTemp.place(x=self.element_positions[2][0] + self.hor_font_space,
                            y=self.element_positions[2][1] + self.vert_font_space)

        self.SVIntHum = StringVar()
        self.SVIntHum.set('')
        self.lIntHum = Label(self.root, font=self.font[20], textvariable=self.SVIntHum, bg=self.tile_color,
                             fg=self.font_color)
        self.lIntHum.place(x=self.element_positions[2][0] + self.hor_font_space,
                           y=self.element_positions[2][1] + self.vert_font_space + 60)

        self.SVWindSpeed = StringVar()
        self.SVWindSpeed.set('')
        self.lWindSpeed = Label(self.root, font=self.font[20], textvariable=self.SVWindSpeed, bg=self.tile_color,
                                fg=self.font_color)
        self.lWindSpeed.place(x=self.element_positions[2][0] + self.hor_font_space,
                              y=self.element_positions[2][1] + self.vert_font_space + 60 + 30)

        self.SVTodayTempTime = []
        self.lTodayTempTime = []
        for i in range(0, 5):
            self.SVTodayTempTime.append(StringVar())
            self.SVTodayTempTime[i].set('')
            self.lTodayTempTime.append(
                Label(self.root, font=self.font[15], textvariable=self.SVTodayTempTime[i], bg=self.tile_color,
                      fg=self.font_color, justify='left', anchor='w'))
            self.lTodayTempTime[i].place(x=self.element_positions[i + 4][0] + self.hor_font_space,
                                         y=self.element_positions[i + 4][1] + 10)

        self.SVTodayTemp = []
        self.lTodayTemp = []
        for i in range(0, 5):
            self.SVTodayTemp.append(StringVar())
            self.SVTodayTemp[i].set('')
            self.lTodayTemp.append(
                Label(self.root, font=self.font[25], textvariable=self.SVTodayTemp[i], bg=self.tile_color,
                      fg=self.font_color, justify='right', anchor="e"))
            self.lTodayTemp[i].place(x=self.element_positions[i + 4][0] + self.hor_font_space,
                                     y=int((self.element_positions[i + 4][1] + self.element_positions[i + 4][3]) / 2))

        self.SVForecastTempDate = []
        self.lForecastTempDate = []
        for i in range(0, 5):
            self.SVForecastTempDate.append(StringVar())
            self.SVForecastTempDate[i].set('')
            self.lForecastTempDate.append(
                Label(self.root, font=self.font[15], textvariable=self.SVForecastTempDate[i], bg=self.tile_color,
                      fg=self.font_color, justify='left', anchor='w'))
            self.lForecastTempDate[i].place(x=self.element_positions[i + 9][0] + self.hor_font_space,
                                            y=self.element_positions[i + 9][1] + 10)

        self.SVForecastTemp = []
        self.lForecastTemp = []
        for i in range(0, 5):
            self.SVForecastTemp.append(StringVar())
            self.SVForecastTemp[i].set('')
            self.lForecastTemp.append(
                Label(self.root, font=self.font[20], textvariable=self.SVForecastTemp[i], bg=self.tile_color,
                      fg=self.font_color, justify='right', anchor="e"))
            self.lForecastTemp[i].place(x=self.element_positions[i + 9][0] + self.hor_font_space, y=int(
                (self.element_positions[i + 9][1] + self.element_positions[i + 9][3]) / 2) - 16)

        self.SVCalendar1 = []
        self.SVCalendar2 = []
        self.SVCalendar3 = []
        self.lCalendar1 = []
        self.lCalendar2 = []
        self.lCalendar3 = []
        for i in range(0, 3):
            self.SVCalendar1.append(StringVar())
            self.SVCalendar1[i].set('')
            self.SVCalendar2.append(StringVar())
            self.SVCalendar2[i].set('')
            self.SVCalendar3.append(StringVar())
            self.SVCalendar3[i].set('')
            self.lCalendar1.append(
                Label(self.root, font=self.font[15], textvariable=self.SVCalendar1[i], bg=self.tile_color,
                      fg=self.font_color, anchor='w'))
            self.lCalendar1[i].place(x=self.element_positions[i + 14][0] + self.hor_font_space,
                                     y=self.element_positions[i + 14][1] + self.vert_font_space)
            self.lCalendar2.append(
                Label(self.root, font=self.font[15], textvariable=self.SVCalendar2[i], bg=self.tile_color,
                      fg=self.font_color, anchor='w'))
            self.lCalendar2[-1].config(width=27)
            self.lCalendar2[i].place(x=self.element_positions[i + 14][0] + self.hor_font_space,
                                     y=self.element_positions[i + 14][1] + self.vert_font_space + 25)
            self.lCalendar3.append(
                Label(self.root, font=self.font[20], textvariable=self.SVCalendar3[i], bg=self.tile_color,
                      fg=self.font_color, anchor='w', justify='left',
                      wraplength=self.element_positions[i + 14][2] - self.hor_font_space - (
                                  self.element_positions[i + 14][0] + self.hor_font_space)))
            self.lCalendar3[i].place(x=self.element_positions[i + 14][0] + self.hor_font_space,
                                     y=self.element_positions[i + 14][1] + self.vert_font_space + 25 + 40)
        
