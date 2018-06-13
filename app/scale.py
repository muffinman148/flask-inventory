"""
Reads from hx711 amplifier and pair loadcell to provide a number of weight
values. These weight values are compiled to a list where an average is
cultivated for external processes.
"""

import RPi.GPIO as GPIO
import time
import sys
from numpy import mean
from hx711py.hx711 import HX711

def cleanAndExit():
    """Legacy function used for safely quiting scale read process."""

    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def requestScaleData(weight_list):
    """Requests data from scale and produces a list.

    Args:
        weight_list (list): List of all float weight values.

    Returns:
        list: Float value list.
    """

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

    while len(weight_list) < 5:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        weight_list.append(int(val))

        hx.power_down()
        hx.power_up()
    return weight_list

def runScale(mode, weight):
    """Runs the scale to return a weight.

    Args:
        mode (str): Mode of the operation.
        weight (float): Weight of item on scale.

    Returns:
        float: Overall weight of the item.
    """

    if mode == "getWeight":
        weight_list = []
        requestScaleData(weight_list)
        weight = mean(weight_list)
    elif mode == "getTare":
        weight_list = []
        requestScaleData(weight_list)
        weight = mean(weight_list)
    # TODO Have this return a JSON. ex: {weight : 10.4}
    return weight

# Use this to run individually
# if __name__ == "__runSacle__":
#     runScale("getWeight", 0)
