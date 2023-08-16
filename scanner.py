import xmlrpc.client
import time
import io
import numpy as np
from datetime import datetime

# Connect to the flrig server on localhost port 12345
server_url = "http://localhost:12346"
flrig = xmlrpc.client.ServerProxy(server_url)
version = flrig.main.get_version
print("Connected to flrig {server_url}version:",version())
current_freq = flrig.rig.get_vfo()
print("Current frequency:", current_freq)
smeter = flrig.rig.get_smeter()
print("Current S Meter:",smeter)

# Set scanning config
step_size = 12500
sensitivity = 10
delay = 0.02

def sprint(*args, end='', **kwargs):
    sio = io.StringIO()
    print(*args, **kwargs, end=end, file=sio)
    return sio.getvalue()

# read teh band information from teh cs - use header and this format:
# band,low,high,mode,bw,sq
bands = np.genfromtxt('scan1.csv', delimiter=',',dtype=[('band','U5'),
                ('startFreq','i8'),('stopFreq','i8'),('mode','U5'),('ssize','i8'),('sens','i8')])

#display bands
for i in range(len(bands)-1):
    i = i + 1
    band = bands[i][0]
    startFreq = bands[i][1]
    stopFreq = bands[i][2]
    mode = bands[i][3]
    sss = bands[i][4]
    sens = bands[i][5]
    print(f"{band} : {startFreq} --> {stopFreq} size {sss} sq {sens} mode {mode}")

# Ask user to set the band manually or use the current frequency
band_choice = input(f"Current freq: {current_freq}. Enter to scan this band, or enter a band from list above: ")

# Determine which band we are in based on user input or current frequency
if band_choice == "":
    for i in range(len(bands)-1):
        i = i + 1
        band = bands[i][0]
        startFreq = int(bands[i][1])
        stopFreq = int(bands[i][2])
        if float(current_freq) >= float(startFreq) and float(current_freq) <= float(stopFreq):
            start_freq = startFreq
            end_freq =  stopFreq 
            mode =  str(bands[i][3])
            step_size = int(bands[i][4])
            sensitivity = int(bands[i][5])
            print(f"set mode {mode} start {start_freq} to {end_freq}")
            break;
    else:
        # We are not in a supported band
        print("Current frequency is not in a supported band.")
        exit()
else:
    # see which band was selected
    for i in range(len(bands)):
        band = bands[i][0]
        startFreq = int(bands[i][1])
        stopFreq = int(bands[i][2])
        if band_choice == str(band):
            start_freq = startFreq
            end_freq =  stopFreq 
            mode =  str(bands[i][3])
            step_size = int(bands[i][4])
            sensitivity = int(bands[i][5])
            print(f"set mode {mode} start {start_freq} to {end_freq} size {step_size}")
            break;
    else:
        # Invalid band selection
        print("Invalid band selection.")
        exit()

# Scan from current frequency to the end of the band
flrig.rig.set_mode(mode)

while True:
    for freq in range(int(start_freq), int(end_freq), step_size):
        flrig.rig.set_vfo(float(freq))

        time.sleep(delay)

        # check the sensitity
        smeter = flrig.rig.get_smeter()
        if int(smeter) >= sensitivity:
            tstart = time.time()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            sStr = sprint(f"Signal {smeter} > {sensitivity} dB. Scan stopped ({dt_string}). Frequency ({band}) is {float( freq)/1000000.0}MHz")
            while ( int(smeter) >= sensitivity ):
                time.sleep(0.5)
                smeter = flrig.rig.get_smeter()
            #time.sleep(5)
            tend = time.time()
            if (tend - tstart) > 1.1:
                elapsedStr = "{:.2f}".format((tend - tstart))
                print(sStr)
                print(f"Signal {smeter} < {sensitivity} dB. Scaning restarted ({dt_string}) after {elapsedStr}S")
      
        freq = freq + step_size # was before above in oriinal code !
    #    continue
    # break out of the infinite loop when a signal is detected
    #break
