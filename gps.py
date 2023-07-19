
import serial
import time
import string
import pynmea2

class GPSModule:
    def __init__(self):
        self.gps = [0, 0]
        self.port = '/dev/ttyS0'
        self.ser = serial.Serial(self.port, baudrate=9600, timeout=0.1)
        self.dataout = pynmea2.NMEAStreamReader()

    def read_gps_data(self):
        newdata = self.ser.readline().decode("unicode_escape")

        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude
            self.gps[0] = lat
            self.gps[1] = lng
            #self.gps = (lat, lng)

        return self.gps

def main():
    data_read = gps_module.read_gps_data()
    print(data_read)

# Usage in the main program
if __name__ == '__main__':
    gps_module = GPSModule()
    while True:
        main()
