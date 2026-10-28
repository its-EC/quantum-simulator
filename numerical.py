import numpy as np

def simpson(y, x, points):
    if x is not None and y is not None:
        step = x[1]-x[0]
        integral = 0
        for i in range(0, points):
            if i == 0 or i == points-1:
                coefficient = 1
            elif i%2 == 0 and i!=(points-1):
                coefficient = 2
            elif i%2 == 1 and i!=(points-1):
                coefficient = 4
            integral += step/3 * (coefficient*y[i])

        return integral
    else:
        return 0