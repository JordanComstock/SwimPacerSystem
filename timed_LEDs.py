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
SCALER = 4.5
PACE1 = 20 - SCALER
PACE2 = 15 - SCALER
PACE3 = 15 - SCALER
PACE4 = 10 - SCALER
LAPS = 4

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

def pool_slope_calculations(strip, numLaps, lapTimes):
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
    for i in range(len(diagonal_length)):
        led_in_section.append(LED_COUNT * diagonal_length[i]/total_diagonal_length)
    
    for n in range(numLaps):
        start = time.time()
        total_led_num = 0    
        for i in range(len(horizontal_length)):
            time_in_section = (lapTimes[n] - SCALER) * horizontal_length[i]/total_horizontal_length

            if n % 2 == 0:
                for j in range(0, int(led_in_section[i]), 2):
                    strip.setPixelColor(total_led_num+2, Color(0,255,0))
                    strip.show()
                    time.sleep(2*(float(time_in_section)/led_in_section[i]))
                    strip.setPixelColor(total_led_num, Color(0,0,0))
                    total_led_num += 2
            else:
                for j in range(int(led_in_section[i]), 0, -2):
                    strip.setPixelColor(total_led_num-2, Color(0,255,0))
                    strip.show()
                    time.sleep(2*(float(time_in_section)/ledCount))
                    strip.setPixelColor(total_led_num, Color(0,0,0))
                    total_led_num += 2

        end = time.time()
        print(end-start)
        print(lapTimes[n])

'''
Odd laps 
first = 0 
last = numPixels
'''
def follow_odd(strip, pace, ledCount):
    strip.setPixelColor(0, Color(0,255,0))
    for i in range(0, int(ledCount)-2, 2):
        strip.setPixelColor(i+2, Color(0,255,0))
        strip.show()
        time.sleep(2*(float(pace)/ledCount))
        strip.setPixelColor(i, Color(0,0,0))

'''
Even laps
first = numPixels 
last = 0
'''
def follow_even(strip, pace, ledCount):
    #strip.setPixelColor(strip.numPixels()-2, Color(0,255,0))
    for i in range(int(ledCount), 0, -2):
        strip.setPixelColor(i-2, Color(0,255,0))
        strip.show()
        time.sleep(2*(float(pace)/ledCount))
        strip.setPixelColor(i, Color(0,0,0))

# Main program 
if __name__ == '__main__':
    opt_parse()

    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    
    strip.begin()
    
    pool_slope_calculations(strip, 2, [15, 20])

    #start = time.time()
    #follow_odd(strip,PACE1, strip.numPixels())
    #end = time.time()
    #print(end-start)
    #print(PACE1)

    #start = time.time()
    #follow_even(strip, PACE2, strip.numPixels())
    #end = time.time()
    #print(end-start)
    #print(PACE2)
