import control
import numpy as np


def sintonizar_chr(k, tau, theta):
    Kp = 0.6 * tau / (k * theta)
    Ti = tau
    Td = 0.5 * theta
    return {
        "Kp": round(float(Kp), 4),
        "Ti": round(float(Ti), 4),
        "Td": round(float(Td), 4),
    }
