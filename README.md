# cokeyco
Embedded Systems Project 1

## Projected Timeframe

Let's try to finish the prototype by the 9th of February. Once we settle on which idea we're using, we can start to build the website in parallel with working on the prototype.

## How to Get Up and Running with the Development Board

1. Follow Ed Stott's instructions on installing Python 3, Ampy and PuTTY
1. Connect the board to your PC via USB, then open Command / Powershell and run the following command:
    > wmic path Win32_SerialPort > dump.txt
1. Check which serial port is listed in the text file (e.g. COM4) and make a note of this
1. In PuTTY, in the Session menu, select Serial with Serial Line: COM4 and Speed: 115200. Click Open to start the serial communication terminal.
1. To copy a new script to the board, open Command / Powershell in the directory containing the script, then type the following:
    > ampy --port COM12 put script.py
1. To run the existing code on the board, press the reset button (main.py will run by default). To run a different script, type the following, where ____ is the name of the Python script minus the .py file extension:
    > import _____


## Summary of Revisions

30-Jan-18: Serial communication established between board and sensor
01-Feb-18: Minor revisions to core direction-finding functionalty

## To Do

### Core
- [x] Establish serial communication between board and sensor
- [] Fix direction-finding to give output in degrees from True North
- [] Settle on prototype concept
- [] Build website to promote the product

### Optional
- [] Find API to pull latitude and calculate declination angle using a local IP address (for Key idea)

