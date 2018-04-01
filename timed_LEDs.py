# Set off LED strip one by one in a certain amount of time

from neopixel import *
import math
import time

# Time Constant
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

# Pool size data
POOL_X_VALUES = [0, 16.5, 21, 75]
POOL_Y_VALUES = [4, 5, 6.5, 8]

def start_LEDs(numLaps, lapTimeSec, lapTimeMs):
    print("start_LEDs")
    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()
    
    timing_array = []
    
    for _ in range(numLaps):
        timing_array << lapTimeSec
    
    led_timing(strip, numLaps, timing_array)

'''
Performs LED timing algorithm

strip: LED strip object
numLaps: Number of laps (lap is length of pool in one direction)
lapTimes: Array of lap times
'''
def led_timing(strip, numLaps, lapTimes, debug = False):
    # Check for invalid input
    if numLaps != len(lapTimes):
        print("Number of laps does not match lap time list")
        return

    # Calculate horizontal lengths and diagonal lengths for each section
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
        
    # Calculate number of LEDs in each section
    led_in_section = []
    for i in range(len(diagonal_length)):
        led_in_section.append(LED_COUNT * diagonal_length[i]/total_diagonal_length)
    
    # Execute laps
    for n in range(numLaps):
        start = time.time()
        
        # Set starting point in LED strip
        if n % 2 == 0:
            total_led_num = 0
        else:
            total_led_num = LED_COUNT

        for i in range(len(horizontal_length)):
            # Calculate time in each section
            time_in_section = (lapTimes[n] - SCALER) * horizontal_length[i]/total_horizontal_length

            # For even laps, turn on every other LED in ascending order
            if n % 2 == 0:
                for j in range(-2, int(led_in_section[i]), 2):
                    strip.setPixelColor(total_led_num+2, Color(0,255,0))
                    strip.show()
                    time.sleep(2*(float(time_in_section)/led_in_section[i]))
                    strip.setPixelColor(total_led_num, Color(0,0,0))
                    total_led_num += 2
            
            # For odd laps, turn on every other LED in descending order
            else:
                for j in range(int(led_in_section[i]), -2, -2):
                    strip.setPixelColor(total_led_num-2, Color(0,255,0))
                    strip.show()
                    time.sleep(2*(float(time_in_section)/led_in_section[i]))
                    strip.setPixelColor(total_led_num, Color(0,0,0))
                    total_led_num -= 2

        end = time.time()
        
        if debug:
            print(end - start)
            print(lapTimes[n])

# Main program 
if __name__ == '__main__':

    print("main")
    # Create Object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()
    
    led_timing(strip, 2, [15, 20], True)
