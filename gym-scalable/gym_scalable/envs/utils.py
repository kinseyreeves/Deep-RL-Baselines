import math
import numpy as np

def clamp_angle(angle):
    """
    Clamps angle between values
    :param angle:
    :return:
    """
    if(angle > 2*math.pi):
            angle = angle%2*math.pi
    if(angle < 0):
        angle = 2*math.pi + angle
    
    return angle

def normalize(x, minx, maxx):
    """
    Normalize val
    :param x:
    :param minx:
    :param maxx:
    :return:
    """
    return (x - minx)/(maxx - minx)

def convert_1hot_action(action, size):
    """
    Converts action from int to 1hot array
    :param action:
    :return:
    """
    z_arr = np.zeros(size)
    z_arr[action] = 1
    action = z_arr
    return action

