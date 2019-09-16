import math

def clamp_angle(angle):
    if(angle > 2*math.pi):
            angle = angle%2*math.pi
    if(angle < 0):
        angle = 2*math.pi + angle
    
    return angle

def normalize(x, minx, maxx):
    return (x - minx)/(maxx - minx)