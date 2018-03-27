# Set off LED strip one by one in a certain amount of time

from neopixel import *

import argparse
import math
import signal
import sys
import time


def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# Time Constant
PACE1 = 20
PACE2 = 15
PACE3 = 15
PACE4 = 10
LAPS = 4
SCALER = 4.5

# LED Strip Config - Object params
LED_COUNT       = 742
LED_PIN         = 18                    # GPIO18 is actually pin 12
LED_FREQ        = 800000
LED_DMA         = 5
LED_BRIGHTNESS  = 127  
LED_INVERT      = False
LED_CHANNEL     = 0
LED_STRIP       = ws.WS2812_STRIP       # Specific LED strip we have

POOL_X_VALUES = [0, 16.5, 21, 75]
POOL_Y_VALUES = [4, 5, 6.5, 8]

def pool_slope_calculations(time):
    horizontal_length = []
    diagonal_length = []
    total_horizontal_length = 0
    total_diagonal_length = 0
    for i in range(len(POOL_X_VALUES)-1):
        x_diff = POOL_X_VALUES[i+1] - POOL_X_VALUES[i]
        y_diff = POOL_Y_VALUES[i+1] - POOL_Y_VALUES[i]
        horizontal_length.append(x_diff)
        diagonal_length.append(math.sqrt(x_diff ** 2 + y_diff ** 2))
        total_horizontal_length += x_diff
        total_diagonal_length += math.sqrt(x_diff ** 2 + y_diff ** 2)
    led_in_section = []
    time_in_section = []
    for i in range(len(horizontal_length)):
        led_in_section.append(LED_COUNT * diagonal_length[i]/total_diagonal_length)
        time_in_section.append(time * horizontal_length[i]/total_horizontal_length)

'''
odd laps first = 0 last = num pix = num pixels
even laps first = num pixels last =0
'''
def follow_odd(strip, pace):
    pace = pace - SCALER
    strip.setPixelColor(0, Color(0,255,0))
    for i in range(0, strip.numPixels()-2, 2):
        strip.setPixelColor(i+2, Color(0,255,0))
        strip.show()
        time.sleep(2*(float(pace)/LED_COUNT))
        strip.setPixelColor(i, Color(0,0,0))

def follow_even(strip, pace):
    pace = pace - SCALER
    strip.setPixelColor(LED_COUNT-2, Color(0,255,0))
    for i in range(strip.numPixels(), 0, -2):
        strip.setPixelColor(i-2, Color(0,255,0))
        strip.show()
        time.sleep(2*(float(pace)/LED_COUNT))
        strip.setPixelColor(i, Color(0,0,0))

# Main program 
if __name__ == '__main__':
    opt_parse()

    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    
    strip.begin()

    start = time.time()
    follow_odd(strip,PACE1)
    end = time.time()
    print(end-start)
    print(PACE1)

    start = time.time()
    follow_even(strip, PACE2)
    end = time.time()
    print(end-start)
    print(PACE2)
