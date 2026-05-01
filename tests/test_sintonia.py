import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.models.sintonia import sintonizar_chr, sintonizar_cc, validar_estabilidade, sintonizar_manual

K_REF = 2.0
TAU_REF = 10.0
THETA_REF = 3.0

def test_sintonizar_chr():
    chr_result = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    assert abs(chr_result['Kp'] - 1.0) < 0.05, "Kp de CHR fora do esperado"
    assert chr_result['Ti'] == 10.0, "Ti de CHR fora do esperado"
    assert chr_result['Td'] == 1.5, "Td de CHR fora do esperado"

def test_sintonizar_cc():
    cc_result = sintonizar_cc(K_REF, TAU_REF, THETA_REF)
    # Valores de referência baseados na execução correta
    assert abs(cc_result['Kp'] - 2.3472) < 0.01, "Kp de Cohen-Coon fora do esperado"
    assert abs(cc_result['Ti'] - 6.5844) < 0.01, "Ti de Cohen-Coon fora do esperado"
    assert abs(cc_result['Td'] - 1.0345) < 0.01, "Td de Cohen-Coon fora do esperado"

def test_validar_estabilidade_sistema_estavel():
    chr_result = sintonizar_chr(K_REF, TAU_REF, THETA_REF)
    estavel, msg = validar_estabilidade(K_REF, TAU_REF, THETA_REF, chr_result['Kp'], chr_result['Ti'], chr_result['Td'])
    assert estavel is True, "O sistema CHR deveria ser estável"

def test_validar_estabilidade_sistema_instavel():
    estavel, msg = validar_estabilidade(K_REF, TAU_REF, THETA_REF, 100.0, 0.01, 50.0)
    assert estavel is False, "O sistema com Kp extremo deveria ser instável"

def test_sintonizar_manual():
    manual = sintonizar_manual(1.5, 8.0, 0.5)
    assert manual['Kp'] == 1.5
    assert manual['Ti'] == 8.0
    assert manual['Td'] == 0.5
