# Set off LEd strip one by one in a certain amount of time

import time

from neopixel import *

import argparse
import signal
import sys


def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# Time Constant
PACE1 = 5 
PACE2 = 20
PACE3 = 5 
PACE4 = 10
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

'''
odd laps first = 0 last = num pix = num pixels
even laps first = num pixels last =0
'''
def follow_odd(strip, pace):
    strip.setPixelColor(0, Color(0,255,0))
    strip.setPixelColor(1, Color(0,255,0))
    for i in range(strip.numPixels()-2):
        strip.setPixelColor(i+2, Color(0,255,0))
        strip.show()
        time.sleep(float(pace)/LED_COUNT)
        strip.setPixelColor(i, Color(0,0,0))
        '''strip.setPixelColor(i+1, Color(0,0,0))
        strip.setPixelColor(i+2, Color(0,0,0))
        strip.show()'''
def follow_even(strip, pace):

    for i in range(strip.numPixels(), 2, -1):
        strip.setPixelColor(i, Color(0,255,0))
        strip.setPixelColor(i-1, Color(0,255,0))
        strip.setPixelColor(i-2, Color(0,255,0))
        strip.show()
        time.sleep(float(pace)/LED_COUNT)
        strip.setPixelColor(i, Color(0,0,0))
        '''strip.setPixelColor(i-1, Color(0,0,0))
        strip.setPixelColor(i-2, Color(0,0,0))'''
        strip.show()
        
        


# Main program 
if __name__ == '__main__':
    opt_parse()

    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    
    strip.begin()
    

    print('Start')


    follow_odd(strip,PACE1)
    '''follow_even(strip, PACE2)
    follow_odd(strip, PACE3)
    follow_even(strip,PACE4)'''



