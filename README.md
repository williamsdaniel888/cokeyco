# cokeyco
Embedded Systems Project 1

##How to Get Up and Running with the Development Board

1. Follow Ed Stott's instructions on installing Python 3, Ampy and PuTTY
1. Connect the board to your PC via USB, then open Command / Powershell and run the following command:
> wmic path Win32_SerialPort > dump.txt
Check which serial port is listed (e.g. COM4).
1. In PuTTY, in the Session menu, select Serial with Serial Line: COM4 and Speed: 115200. Click Open to start the serial communication terminal.
1. To copy a new script to the board, open Command / Powershell in the directory containing the script, then type the following:
> ampy --port COM12 put script.py
1. To run the existing code on the board, press the reset button (main.py will run by default). To run a different script, type the following, where ____ is the name of the Python script minus the .py file extension:
> import _____


#Summary of Revisions

30-Jan-18: Serial communication established between board and sensor

