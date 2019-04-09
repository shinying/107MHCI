from __future__ import print_function
import time
import sys
import threading
import struct

# modules need to be installed
import pyaudio # pip install pyaudio
# from PyMata.pymata import PyMata # pip install PyMata
import serial
from audio_offset_finder.audio_offset_finder import find_offset # pip install audio-offset-finder

# files
import recorder as rc
from tempo import detect_beats


CHUNK = 1024
FORMAT = pyaudio.paInt16
MONO = 1
RATE = 44100
DURATION = 5.0
SAMPLE_FILE = "sample.wav"

# board config
LED_PIN1 = 8
LED_PIN2 = 13
BOARD = "/dev/cu.usbmodem14601"
ser = serial.Serial(BOARD, 9600)
# board = PyMata(BOARD, verbose=True)
# board.set_pin_mode(LED_PIN1, board.OUTPUT, board.DIGITAL)
# board.set_pin_mode(LED_PIN2, board. OUTPUT, board.DIGITAL)

# def light():
#     board.digital_write(LED_PIN1, 1)
#     board.digital_write(LED_PIN2, 1)
#     time.sleep(.1)
#     board.digital_write(LED_PIN1, 0)
#     board.digital_write(LED_PIN2, 0)

playing_status = True

def sync_beats(file):
    FULL_FILE = file
    beats = detect_beats(FULL_FILE)

    # record from device
    rec = rc.Recorder(channels=MONO)
    with rec.open(SAMPLE_FILE, 'wb') as recfile:
        print("Start recording...")
        recfile.record(duration=DURATION)
    t_start = time.time()

    # locate sample file with in original audio track
    print("Start locating...")
    offset, _ = find_offset(FULL_FILE, SAMPLE_FILE, 44100, 5*60)
    # print("Record starts at:", offset)

    t_end = time.time()

    cur_time = offset + DURATION + t_end - t_start + 0.1
    # print("Calculation ends at:", cur_time)
    start_point = 0
    for i in range(len(beats)):
        if beats[i] >= cur_time:
            start_point = i
            break

    if start_point == 0:
        print("Error: Locating fail!")
        print("> ", end="")
        sys.stdout.flush()
        sys.exit(1)

    # print("Next beats:", beats[start_point])
    print("Start tracking...")
    print("> ", end="") # to receive "stop"
    sys.stdout.flush()

    t_start = time.time()
    while playing_status and start_point < len(beats):
        if round(time.time()-t_start+cur_time, 2) == beats[start_point]:
            # t = threading.Thread(target=light)
            # t.start()
            ser.write(struct.pack('>B', 2))
            start_point += 1

    if not playing_status:
        print("> ", end="")
        sys.stdout.flush()

print("> ", end="")
sys.stdout.flush()
while True:
    try:
        cmd = raw_input() # "Panama.wav" or "rose.wav"
        if cmd == "stop":
            playing_status = False
            continue
        if (cmd == 'p'): file = "Panama.wav"
        elif (cmd == 'r'): file = "rose.wav"
        elif (cmd == 'g'): file = "goodboy.wav"
        elif (cmd == 't'): file = "threepigs.wav"
        elif (cmd == 'j'): file = "jj.wav"
        elif (cmd == 'u'): file = "ugly.wav"
        playing_status = True
        main = threading.Thread(target=sync_beats, args=[file])
        main.start()
    except:
        playing_status = False
        main.join()
        break

# board.close()
ser.close()