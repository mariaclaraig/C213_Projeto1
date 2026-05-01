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


def validar_estabilidade(k, tau, theta, Kp, Ti, Td):
    try:
        num_p, den_p = control.pade(max(theta, 1e-6), 20)
        G = control.series(control.tf([k], [tau, 1]), control.tf(num_p, den_p))
        C = control.tf([Kp * Td, Kp, Kp / Ti], [1, 0])
        T = control.feedback(control.series(C, G), 1)
        polos = control.poles(T)
        estavel = all(p.real < 0 for p in polos)
        if estavel:
            return True, "Sistema estável."
        return False, "Sistema instável: polos com parte real positiva."
    except Exception as e:
        return False, f"Erro na verificação: {str(e)}"


def sintonizar_manual(Kp, Ti, Td):
    return {"Kp": float(Kp), "Ti": float(Ti), "Td": float(Td)}
