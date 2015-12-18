#!/usr/bin/env python

"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

from Adafruit_PWM_Servo_Driver import PWM
import time
import os
import RPi.GPIO as GPIO
from math import log10, cos, radians
import pyaudio
import wave
import signal
import sys

NB_SERVO = 5

CHUNK = 1024
FORMAT = pyaudio.paUInt8
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

GPIO.setmode(GPIO.BCM)
DEBUG = 0
pwm = PWM(0x40)
servoMin = 150  # Min pulse length out of 4096
servoMax = 650  # Max pulse length out of 4096
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)



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

def get_angle(i):
    return (int((cos(radians(i)) * 90) + 90))

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
i = 0
last_angle = 0
tolerance = 2
while True:
    data = stream.read(CHUNK)
    #print "#" * get_db(str(data))
    db = get_db(str(data))
    print "%03d %s" % (db, "#" * db)
    angle = get_angle(i)
    print angle

    angle_changed = False
    angle_adjust = abs(angle - last_angle)
    if (angle_adjust > tolerance):
        angle_changed = True
    if (angle_changed):
        for j in range(NB_SERVO):
            pwm.setPWM(j, 0, servoMin + (((servoMax - servoMin)  * get_angle(i + (j * 70))) / 180))
        last_angle = angle

    i = i + 1 + (db / 4)
    if (i > 360):
        i = i % 360
