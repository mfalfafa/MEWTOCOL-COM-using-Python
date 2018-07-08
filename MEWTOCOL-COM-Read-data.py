#Program for reading data from specific address in FPSigma Panasonic PLC
#using MEWTOCOL-COM Protocol RS232
#Created by MF ALFAFA
#8 July 2018
#miftahf77@gmail.com

# Note :
# Set timeout parameter to zero (small enough).
# If not, the PLC will not send the response
# timeout and write_timeout parameter must be zero in value

# How to use :
# Just add the data register address or contact number to array addr_all_xx below
# and PLC will return the value of choosen register address.
# If you want to read data not from Data or Contact just change data_code or
# contact_code

import serial

## Variables for serial data response
connected = False
ser = 0
x=0
resp=''
_delay=0

## FPSigma commands initialization
dev_no='01'                                 #for device no. 01
data_code='D'                               #for data register
rd_cmd='%' + dev_no + '#RD' + data_code     #Read Data
contact_code='R'                            #for internal relay
rc_cmd='%' + dev_no + '#RCS' + contact_code #Read contact as single
BCC='**'                                    #Block Check Code
CR='\r'                                     #Carriage Return
resp_len='%01$RD'                           #same length as %01$RC

## Addresses to be read from PLC
## Data addresses :
#addr_counter=['32740', '32740']             #start and end address
#addr_size=['32764', '32764']
#addr_speed=['32762', '32762']
addr_all_dt=[['32740', '32740'], ['32764', '32764'], ['32762', '32762'],
             ['32743', '32743']]

## Contact addresses :
#addr_pb1=['0000']
#addr_pb2=['0001']
#addr_pb3=['0002']
addr_all_ct=[['0000'],['0001'],['0002']]

## Variable Values to be displayed from PLC
data_dt=[0]*len(addr_all_dt)
data_ct=[0]*len(addr_all_ct)

## Establish connection to COM Port
locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','COM8']
## COM Port settings
for device in locations:
    try:
        print "Trying...",device
        ## Serial Initialization
        ser = serial.Serial(device,             #port
                            19200,              #baudrate
                            serial.EIGHTBITS,   #bytesize
                            serial.PARITY_ODD,  #parity
                            serial.STOPBITS_ONE,#stop bit
                            0,                  #timeout
                            False,              #xonxoff
                            False,              #rtscts
                            0,                  #write_timeout
                            False,              #dsrdtr
                            None,               #inter byte timeout
                            None                #exclusive
                            )
        break
    except:
        print "Failed to connect on ", device

## loop until the device tells us it is ready
while not connected:
    serin = ser.read()
    connected = True
print "Connected to ",device

## open text file to store the current
## write it to the text file 'serial_data.txt'
text_file = open("serial_data.txt", 'a+')

while 1:
    _delay=_delay+1
    if _delay >= 5000000:
        _delay=0
        #Read all data register values
        for i in range(0,len(addr_all_dt)):
            # sending MEWTOCOL Command
            ser.write(rd_cmd + addr_all_dt[i][0] + addr_all_dt[i][1] + BCC + CR)
            # waiting for incoming serial data from PLC
            while 1:
                if ser.inWaiting():
                    x=ser.read()
                    resp=resp + x
                    if x=='\r':
                        #print resp
                        #Parsing data register
                        dt_with_bcc=resp[len(resp_len):]
                        l=len(dt_with_bcc)
                        dt=dt_with_bcc[0:l-3]   #3 means BCC + RC length
                        #swap the value
                        l=len(dt)/2
                        dt_sw=dt[l:]+dt[0:l]
                        dt_dec=int(dt_sw, 16)
                        #print dt
                        #print dt_sw
                        #print dt_dec
                        data_dt[i]=dt_dec
                        resp=''
                        break
        print data_dt
        #Read all contact values
        for i in range(0, len(addr_all_ct)):
            # sending MEWTOCOL Command
            ser.write(rc_cmd + addr_all_ct[i][0] + BCC + CR)
            while 1 :
                if ser.inWaiting():
                    x=ser.read()
                    resp=resp + x
                    if x=='\r':
                        #print resp
                        #Parsing data register
                        dt_with_bcc=resp[len(resp_len):]
                        l=len(dt_with_bcc)
                        dt=dt_with_bcc[0:l-3]   #3 means BCC + RC length
                        data_ct[i]=int(dt)
                        resp=''
                        break
        print data_ct
        print '-----------------'

## close the serial connection and text file
print "Connection is closed!"
text_file.close()
ser.close()
