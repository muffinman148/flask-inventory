import RPi.GPIO as GPIO
import time
import sys
from hx711py.hx711 import HX711

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

def requestScaleData():
    hx = HX711(5, 6)

    hx.set_reading_format("LSB", "MSB")

    # HOW TO CALCULATE THE REFFERENCE UNIT
    # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
    # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
    # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
    # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
    #hx.set_reference_unit(113)
    hx.set_reference_unit(92)

    hx.reset()
    hx.tare()

    while len(weight_list) < 100:
        try:
            # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
            #np_arr8_string = hx.get_np_arr8_string()
            #binary_string = hx.get_binary_string()
            #print binary_string + " " + np_arr8_string
            
            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val = hx.get_weight(5)
            weight_list.append(val)

            hx.power_down()
            hx.power_up()
            time.sleep(0.01)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
    return weight_list

def average(a):
    # TODO Replace with Kevin's Average Function
    average = a / 100;

def main(mode, weight):
    while True:
        try:
            if mode == "getWeight":
                requestScaleData(weight_list = [])
                weight = average(weight_list)
                print weight
            elif mode == "getTare":
                val = 0
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

if __name__ == "__main__":
    main("getWeight", 0)
