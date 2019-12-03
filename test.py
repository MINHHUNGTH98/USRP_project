import serial 
import time
#try:
ser = serial.Serial('/dev/ttyUSB0')
print "da ket noi"
while True:
    try:
        if(ser.inWaiting()>0):
            data_string = ser.readline()#
            #print data_string
            data = data_string.split(',');
            if data[0] == '$GPGGA':
                print data
                 
                if data[2] != '' and data[4] != '' and data[8] != '':
                    print 'lat = ', data[2], 'long = ', data[4], 'hdop = ',data[8]
                else:
                    print "song GPS yeu!!!"
                 
    except:
        print "thiet bi da ngat ket noi"
        break
#except:
#   print "chua co thiet bi ket noi"
