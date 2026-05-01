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


def sintonizar_cc(k, tau, theta):
    r = theta / tau
    Kp = (1 / k) * (tau / theta) * (4/3 + r/4)
    Ti = theta * (32 + 6*r) / (13 + 8*r)
    Td = 4 * theta / (11 + 2*r)
    return {
        "Kp": round(float(Kp), 4),
        "Ti": round(float(Ti), 4),
        "Td": round(float(Td), 4),
    }
