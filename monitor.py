# Monitoring a serial port
import argparse
import os
import threading
import time

import serial
import serial.tools.list_ports
from getch import _Getch
getch = _Getch()


class ListenOnSerialPort(threading.Thread):
    # listens on serial communication

    def __init__(self, keyboard_thread, connection):
        super(ListenOnSerialPort, self).__init__()
        # threading.Thread.__init__(self)
        self.keyboard_thread = keyboard_thread
        self.connection = connection

    def run(self):
        while True:
            if not self.keyboard_thread.input_active:
                try:
                    ser_in = self.connection.readline().decode('utf-8').strip('\n')
                    print(ser_in)
                except UnicodeDecodeError:
                    print("Serial Error")


class ListenOnKeyboard(threading.Thread):
    # listens for keyboard presses
    input_active = False

    def __init__(self, connection):
        super(ListenOnKeyboard, self).__init__()
        # threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        while True:
            cmd_in = getch()
            if cmd_in == "i":  # if key 'i' is pressed
                self.input_active = True
                time.sleep(0.1)
                string = input(">> ")
                self.connection.write(string.encode())
                self.input_active = False
            elif cmd_in == "q":
                os._exit(1)


def main():
    # main of code

    # process any command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=str, required=False)
    parser.add_argument("--baudrate", "-b", type=int, required=False)
    args = parser.parse_args()

    print("")
    print("Press 'i' for sending data")
    print("Press 'q' to quit")

    port = None
    # assign port in the following order:
    # 1. if passed with the -p argument, use that
    # 2. if -p argument was not passed, present a list of detected ports
    #   to select from, allowing skipping to manual selection
    # 3. manually entered port
    if args.port is None:
        print("")
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list)>0:
            port_counter = int(0)
            print('Detected serial device ports:\n')
            for l_port in port_list:
                print(str(port_counter) + ' - ' + str(l_port))
                port_counter += 1
            port_selection = input("\nport (enter list number, s to skip): ")
            if port_selection == 's':
                port = input("port: ")
            else:
                try:
                    port = str(port_list[int(port_selection)]).split(' - ', maxsplit=1)[0]
                except IndexError as error:
                    print("You must choose a list item within the range")
                    print(error)
                except ValueError:
                    print("Port selection must be an integer. Try again.")
        else:
            print('No serial devices detected, you can enter a port manually')
    else:
        port = args.port

    # if port is still not set, present the input prompt
    if port is None:
        port = input("port: ")

    # if port is still not set, quit
    if port is None:
        os._exit(1)

    # assign baudrate in the following order:
    # 1. if passed with the -b argument, use that
    # 2. if -b argument was not passed hardcode to 9600
    # 3. manually entered port
    if args.baudrate is None:
        baud = 9600
    else:
        baud = args.baudrate

    print("")
    # start the monitor program
    try:
        conn = serial.Serial(port, baud)

        kb_listen = ListenOnKeyboard(conn)
        sp_listen = ListenOnSerialPort(kb_listen, conn)
        kb_listen.start()
        sp_listen.start()
    except serial.serialutil.SerialException as error:
        print("Could not start serial communication. Port chosen: " + port)
        print(error)


if __name__ == '__main__':
    main()
