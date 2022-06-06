try:
    import Adafruit_DHT as Python_DHT
except:
    import Python_DHT

def Get_TempHum(sensor, DataPin):
    humidity=-1
    temperature=-273
    try:
        humidity, temperature= Python_DHT.read_retry(sensor, DataPin)
        ErrorOccured=False
    except:
        ErrorOccured=True
        
    return humidity, temperature, ErrorOccured
