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

    return {
        't': list(t_sim),
        'y': list(y_sim),
    }
