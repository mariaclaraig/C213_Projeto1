import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.identificacao import identificar_sistemas

K_REF   = 2.0
TAU_REF = 10.0
THETA_REF = 3.0
TOLERANCE = 0.05

@pytest.fixture
def simulacao_fopdt():
    t = np.linspace(0, 80, 500)
    y = K_REF * (1 - np.exp(-(t - THETA_REF) / TAU_REF)) * (t >= THETA_REF)
    u = np.ones_like(t)
    u[0] = 0.0
    return t, y, u

def test_identificacao_smith(simulacao_fopdt):
    t, y, u = simulacao_fopdt
    resultado = identificar_sistemas(t, y, u)
    s = resultado['smith']
    
    assert abs(s['k'] - K_REF) / K_REF < TOLERANCE, "Smith: k fora da tolerância"
    assert abs(s['tau'] - TAU_REF) / TAU_REF < TOLERANCE, "Smith: tau fora da tolerância"
    assert abs(s['theta'] - THETA_REF) / THETA_REF < TOLERANCE, "Smith: theta fora da tolerância"

def test_identificacao_sundaresan(simulacao_fopdt):
    t, y, u = simulacao_fopdt
    resultado = identificar_sistemas(t, y, u)
    sund = resultado['sundaresan']
    
    assert abs(sund['k'] - K_REF) / K_REF < TOLERANCE, "Sundaresan: k fora da tolerância"
    assert abs(sund['tau'] - TAU_REF) / TAU_REF < TOLERANCE, "Sundaresan: tau fora da tolerância"
    assert abs(sund['theta'] - THETA_REF) / THETA_REF < TOLERANCE, "Sundaresan: theta fora da tolerância"

def test_recomendacao(simulacao_fopdt):
    t, y, u = simulacao_fopdt
    resultado = identificar_sistemas(t, y, u)
    assert resultado['recomendado'] in ['smith', 'sundaresan'], "Recomendado deve ser smith ou sundaresan"
