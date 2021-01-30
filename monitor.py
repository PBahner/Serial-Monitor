import serial
import keyboard

print("Press 'i' for sending data")
port = input("port: ")
baud = 9600

ser = serial.Serial(port, baud)

while True:
    ch = ser.readline()
    print(ch)
    if keyboard.is_pressed('i'):  # if key 'i' is pressed
        string = input(">> ")
        ser.write(string.encode())
