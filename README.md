# Serial-Monitor
A Serial Monitor based on python. Only command-line.

![preview](screenshot.png)

You can see incoming data. On pressing 'i' you are able to write data to an USB Device.\
I created this small script because arduino-cli has no built-in serial monitor.

## Installation
clone the repo to your local machine:
```bash
git clone https://github.com/PBahner/Serial-Monitor.git
```
If you have installed _python_ you can get the ___keyboard___ and ___serial___ library with:
```bash
pip install keyboard
pip install pyserial
```
## Launch
you can start the serial monitor with:
```bash
python monitor.py
```