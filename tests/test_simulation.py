import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.models.sintonia import sintonizar_chr
from backend.utils.simulation import simular_malha_fechada

K_REF = 2.0
TAU_REF = 10.0
THETA_REF = 3.0


def test_simular_malha_fechada_retorna_chaves_esperadas():
    params = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    resultado = simular_malha_fechada(
        K_REF, TAU_REF, THETA_REF,
        params['Kp'], params['Ti'], params['Td'],
        setpoint=1.0,
    )
    assert 't' in resultado
    assert 'y' in resultado
    assert 'tr' in resultado
    assert 'ts' in resultado
    assert 'Mp' in resultado
    assert 'ess' in resultado


def test_simular_malha_fechada_tipos_json_safe():
    params = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    resultado = simular_malha_fechada(
        K_REF, TAU_REF, THETA_REF,
        params['Kp'], params['Ti'], params['Td'],
    )
    assert isinstance(resultado['t'], list)
    assert isinstance(resultado['y'], list)
    assert isinstance(resultado['tr'], float)
    assert isinstance(resultado['ts'], float)
    assert isinstance(resultado['Mp'], float)
    assert isinstance(resultado['ess'], float)


def test_chr_sem_sobrevalor():
    params = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    resultado = simular_malha_fechada(
        K_REF, TAU_REF, THETA_REF,
        params['Kp'], params['Ti'], params['Td'],
        setpoint=1.0,
    )
    assert resultado['Mp'] < 5.0, f"CHR servo sem sobrevalor: Mp esperado ≈ 0%, obtido {resultado['Mp']:.2f}%"


def test_erro_regime_permanente_proximo_de_zero():
    params = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    resultado = simular_malha_fechada(
        K_REF, TAU_REF, THETA_REF,
        params['Kp'], params['Ti'], params['Td'],
        setpoint=1.0,
    )
    assert resultado['ess'] < 0.05, f"Erro em regime permanente alto: {resultado['ess']:.6f}"


def test_tempo_subida_finito():
    params = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    resultado = simular_malha_fechada(
        K_REF, TAU_REF, THETA_REF,
        params['Kp'], params['Ti'], params['Td'],
        setpoint=1.0,
    )
    assert resultado['tr'] < float('inf'), "Tempo de subida deveria ser finito"
    assert resultado['tr'] > 0, "Tempo de subida deveria ser positivo"
