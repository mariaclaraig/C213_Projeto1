import numpy as np
import control
from scipy.interpolate import interp1d


def identificar_sistemas(t, y, u):
    y0 = y[0]
    yf = y[-1]
    delta_y = yf - y0
    delta_u = u[-1] - u[0]
    k = delta_y / delta_u

    f_interp = interp1d(y, t, kind='linear')

    t1_smith = float(f_interp(y0 + 0.283 * delta_y))
    t2_smith = float(f_interp(y0 + 0.632 * delta_y))
    tau_smith = 1.5 * (t2_smith - t1_smith)
    theta_smith = t2_smith - tau_smith

    res_smith = {
        'k': float(k),
        'tau': float(tau_smith),
        'theta': float(theta_smith),
    }

    t1_sund = float(f_interp(y0 + 0.353 * delta_y))
    t2_sund = float(f_interp(y0 + 0.853 * delta_y))
    tau_sund = 0.67 * (t2_sund - t1_sund)
    theta_sund = 1.3 * t1_sund - 0.29 * t2_sund

    res_sund = {
        'k': float(k),
        'tau': float(tau_sund),
        'theta': float(theta_sund),
    }

    return {
        'smith': res_smith,
        'sundaresan': res_sund,
    }


def simular_fopdt(t, k, tau, theta, delta_u, y0):
    num_p, den_p = control.pade(max(theta, 1e-6), 20)
    G_delay = control.tf(num_p, den_p)
    G_planta = control.tf([k], [tau, 1])
    G = control.series(G_planta, G_delay)

    t_sim, y_sim = control.step_response(G, T=t)
    y_sim = y0 + y_sim * delta_u

    return t_sim, y_sim
