"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

from math import log10
import pyaudio
import wave
import signal
import sys

CHUNK = 1024
FORMAT = pyaudio.paUInt8
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

def get_db(data):
    min = 128
    max = 128
    for i in xrange(len(data)):
        c = ord(data[i])
        if (c < min):
            min = c
        if (c > max):
            max = c
    try:
        db = int(20.0 * log10(abs(max - min)))
    except:
        print "aie aie aie"
        db = 0
        pass
    return db

if (True):
    print("* get_device_count(): %d" % p.get_device_count())
    for i in xrange(p.get_device_count()):
        print("* %d: %s" % (i, p.get_device_info_by_index(i)['name']));

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* listening")

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        stream.stop_stream()
        stream.close()
        p.terminate()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while True:
    data = stream.read(CHUNK)
    #print "#" * get_db(str(data))
    db = get_db(str(data))
    print "%03d %s" % (db, "#" * db)

