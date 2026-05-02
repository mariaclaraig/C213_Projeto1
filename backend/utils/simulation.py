import numpy as np
import control


def simular_malha_fechada(k, tau, theta, Kp, Ti, Td, setpoint=1.0, t_final=None):
    if t_final is None:
        t_final = 10 * (tau + theta)

    t = np.linspace(0, t_final, 1000)

    num_p, den_p = control.pade(max(theta, 1e-6), 20)
    G_delay = control.tf(num_p, den_p)
    G_planta = control.tf([k], [tau, 1])
    G = control.series(G_planta, G_delay)

    C = control.tf([Kp * Td, Kp, Kp / Ti], [1, 0])

    T = control.feedback(control.series(C, G), 1)

    t_sim, y_sim = control.step_response(T * setpoint, T=t)

    metricas = calcular_metricas(t_sim, y_sim, setpoint)

    return {
        't': list(t_sim),
        'y': list(y_sim),
        **metricas,
    }


def calcular_metricas(t, y, setpoint):
    sp = setpoint

    idx_tr = np.where(y >= 0.9 * sp)[0]
    tr = float(t[idx_tr[0]]) if len(idx_tr) > 0 else float('inf')

    banda_superior = sp * 1.02
    banda_inferior = sp * 0.98
    fora_da_banda = np.where((y > banda_superior) | (y < banda_inferior))[0]
    ts = float(t[fora_da_banda[-1]]) if len(fora_da_banda) > 0 else 0.0

    y_max = np.max(y)
    Mp = float((y_max - sp) / sp * 100) if y_max > sp else 0.0

    ess = float(abs(sp - y[-1]))

    return {
        'tr': round(tr, 4),
        'ts': round(ts, 4),
        'Mp': round(Mp, 4),
        'ess': round(ess, 6),
    }
