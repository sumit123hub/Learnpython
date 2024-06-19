import serial
import serial.tools.list_ports
import csv
import re

def findingport():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'usbmodem' in port.device:
            return port.device
    return none

arduino_port = findingport()

if arduino_port:
    print('Arduino found')

    try:
        ser = serial.Serial(arduino_port,baudrate = 9600,timeout= 1)
    except serial.SerialException as e:
        print("Error opening port")
        exit()

    try:
        with open('example.csv','w') as file:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)
                    
                    # Regular expression to extract the values
                    pattern = r"Acceleration X: ([\-\d.]+) Y: ([\-\d.]+) Z: ([\-\d.]+)"
                     
                    match = re.match(pattern, line)

                    # Check if the pattern matches and extract values
                    if match:
                        x_val = match.group(1)
                        y_val = match.group(2)
                        z_val = match.group(3)
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(['Reading',x_val, y_val, z_val])

                
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    finally:
        ser.close()
        print("Serial port closed.")
else:
    print("Arduino not found. Please check the connection.")


