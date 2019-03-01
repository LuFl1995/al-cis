import cis_config as conf
import numpy as np
import random
import scipy.constants as cons
import time


def feed(cell, time):
    """
        Give the cell food,
        depending on position and time.
    """

    #  get value from the food_function --> definition area: {-3, 3}
    food_value = food_function(cell.pos.x, cell.pos.y, cell.pos.z, time)

    # normalize food_value to {0, 1}
    food_value = normalize(food_value)

    # check if cell gets the fixed amount of food
    if food_value < conf.FOOD_THRESHOLD:
        cell.energy_level += conf.FOOD_ENERGY

    return cell


def normalize(num, definition_area_size=6):
    """
        Normalizes the defenition area of the num to {0, 1} .
    """
    ret = round(num) / definition_area_size + 0.5
    return ret


def get_food_function():
    """
        Creates the 4-dim food function and returns it.
    """
    f1 = get_wave_function()

    f2 = get_wave_function()

    f3 = get_wave_function()

    def f(x, y, z, t): return f1(x, t) + f2(y, t) + f3(z, t)

    return f


def get_wave_function(
        max_ampli=1,
        oscillation_period=1,
        init_deflec_factor=0):
    """
        Create and return a mechanical wave function.
    """

    def f(x, t):
        """
            Classical mechanical wave function.
        """

        time_relation = t / oscillation_period
        space_relation = x / (cons.speed_of_light * oscillation_period)
        init_deflec = init_deflec_factor * np.pi

        return max_ampli * np.sin(2 * np.pi *
                                  (time_relation - space_relation) +
                                  init_deflec)

    return f
