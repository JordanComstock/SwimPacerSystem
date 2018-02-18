# Set off LED strip one by one in a certain amount of time

from neopixel import *

import argparse
import math
import signal
#import sys
import time


def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# Time Constant
PACE1 = 5.0
PACE2 = 2.0
PACE3 = 7.0
PACE4 = 0.25
LAPS = 4

# LED Strip Config - Object params
LED_COUNT       = 60
LED_PIN         = 18                    # GPIO18 actually pin 12!!!!!
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
    
    for i in range(strip.numPixels()-2):
        strip.setPixelColor(i, Color(0,255,0))
        strip.setPixelColor(i+1, Color(0,255,0))
        strip.setPixelColor(i+2, Color(0,255,0))
        strip.show()
        time.sleep(pace/60.0)
        strip.setPixelColor(i, Color(0,0,0))
        #strip.setPixelColor(i+1, Color(0,0,0))
        #strip.setPixelColor(i+2, Color(0,0,0))
        strip.show()
def follow_even(strip, pace):

    for i in range(strip.numPixels(), 2, -1):
        strip.setPixelColor(i, Color(0,255,0))
        strip.setPixelColor(i-1, Color(0,255,0))
        strip.setPixelColor(i-2, Color(0,255,0))
        strip.show()
        time.sleep(pace/60.0)
        strip.setPixelColor(i, Color(0,0,0))
        #strip.setPixelColor(i-1, Color(0,0,0))
        #strip.setPixelColor(i-2, Color(0,0,0))
        strip.show()
        
        


# Main program 
if __name__ == '__main__':
    opt_parse()

    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    
    strip.begin()
    

    print('Start')



    follow_odd(strip,PACE1)
    follow_even(strip, PACE2)
    follow_odd(strip, PACE3)
    follow_even(strip,PACE4)



