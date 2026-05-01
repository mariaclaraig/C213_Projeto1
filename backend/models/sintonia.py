import control
import numpy as np


def sintonizar_chr(k, tau, theta):
    """
    Sintonia PID pelo método CHR sem sobrevalor (problema servo).

    Critério: resposta mais rápida possível sem sobrevalor para mudança de SetPoint.
    Aplicável a sistemas FOPDT identificados pelos métodos de Smith ou Sundaresan.

    Parâmetros:
        k     (float): ganho estático do processo
        tau   (float): constante de tempo [s]
        theta (float): tempo morto [s]

    Retorna:
        dict com chaves 'Kp', 'Ti', 'Td' (float nativos - JSON-safe)
    """
    Kp = 0.6 * tau / (k * theta)
    Ti = tau
    Td = 0.5 * theta
    return {
        "Kp": round(float(Kp), 4),
        "Ti": round(float(Ti), 4),
        "Td": round(float(Td), 4),
    }


def sintonizar_cc(k, tau, theta):
    """
    Sintonia PID pelo método Cohen-Coon.

    Adequado para sistemas com razão theta/tau elevada, onde os métodos
    clássicos tendem a ser conservadores. Calcula r = theta/tau como
    razão de controlabilidade e a utiliza nas fórmulas tabeladas do método.

    Parâmetros:
        k     (float): ganho estático do processo
        tau   (float): constante de tempo [s]
        theta (float): tempo morto [s]

    Retorna:
        dict com chaves 'Kp', 'Ti', 'Td' (float nativos - JSON-safe)
    """
    r = theta / tau
    Kp = (1 / k) * (tau / theta) * (4 / 3 + r / 4)
    Ti = theta * (32 + 6 * r) / (13 + 8 * r)
    Td = 4 * theta / (11 + 2 * r)
    return {
        "Kp": round(float(Kp), 4),
        "Ti": round(float(Ti), 4),
        "Td": round(float(Td), 4),
    }


def validar_estabilidade(k, tau, theta, Kp, Ti, Td):
    """
    Verifica se os parâmetros PID manuais resultam em sistema em malha fechada estável.

    Constrói a malha fechada com a planta FOPDT (atraso aproximado por Padé ordem 20)
    e o controlador PID paralelo, depois analisa os polos do sistema resultante.
    Um sistema é considerado estável se todos os polos têm parte real estritamente negativa.

    Parâmetros:
        k     (float): ganho estático do processo
        tau   (float): constante de tempo [s]
        theta (float): tempo morto [s]
        Kp    (float): ganho proporcional do PID
        Ti    (float): tempo integral do PID [s]
        Td    (float): tempo derivativo do PID [s]

    Retorna:
        tuple (bool, str): (é_estável, mensagem_descritiva)
    """
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
    """
    Retorna os parâmetros PID manuais no formato padronizado do módulo.

    A validação de estabilidade deve ser chamada externamente (via validar_estabilidade)
    antes de aceitar e repassar estes valores à simulação.

    Parâmetros:
        Kp (float): ganho proporcional
        Ti (float): tempo integral [s]
        Td (float): tempo derivativo [s]

    Retorna:
        dict com chaves 'Kp', 'Ti', 'Td' (float nativos - JSON-safe)
    """
    return {"Kp": float(Kp), "Ti": float(Ti), "Td": float(Td)}
