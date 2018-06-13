import serial
import pprint

# serialUSB = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'

# Opens Serial Port
ser = serial.Serial("/dev/ttyUSB0", 9600)  # 115200 baudrate ; open first serial port
print("Connected to port: " + ser.portstr)       # check which port was really used

# Clear Buffers
ser.reset_input_buffer()
ser.reset_output_buffer() 

# DEBUG Displays serial settings
# print(ser.get_settings())

# Retrieves Scale Data
while True:
    try:
        data = []
        value = None
        while not value:
            for x in range(0, 8):
                value = ser.readline()
                data.append(value)

        # Prints Readable Console Data
        pp = pprint.PrettyPrinter()
        pp.pprint(data)
        print("==============================")

        # Example Print
        # ['  0.0896 lb GR\r\n',
        # '  0.0066 lb TA\r\n',
        # '  0.0830 lb NT\r\n',
        # '       0 PCS\r\n',
        # '       0 lb PW\r\n',
        # '       0 ACC#\r\n',
        # '  0.0000 lb NT ACC\r\n',
        # '       0 PCS ACC\r\n']
        
        # Logging
        # Total Weight = data[0]
        # Tare Weight = data[1]
        # Item Weight = data[2]

        # value = ser.read()
        # print value

    except:
        print("Keyboard Interrupt")
        break

