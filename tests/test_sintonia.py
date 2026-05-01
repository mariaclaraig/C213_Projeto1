import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.models.sintonia import sintonizar_chr, sintonizar_cc, validar_estabilidade, sintonizar_manual

k, tau, theta = 2.0, 10.0, 3.0

chr_result = sintonizar_chr(k, tau, theta)
cc_result = sintonizar_cc(k, tau, theta)

print("=== CHR (problema servo, sem sobrevalor) ===")
print(f"Kp={chr_result['Kp']}  (esperado ~= 1.0)")
print(f"Ti={chr_result['Ti']}  (esperado = 10.0)")
print(f"Td={chr_result['Td']}  (esperado = 1.5)")

print("\n=== Cohen-Coon ===")
print(f"Kp={cc_result['Kp']}")
print(f"Ti={cc_result['Ti']}")
print(f"Td={cc_result['Td']}")

print("\n=== Validação de Estabilidade (parâmetros CHR) ===")
estavel, msg = validar_estabilidade(k, tau, theta, chr_result['Kp'], chr_result['Ti'], chr_result['Td'])
print(f"Estável: {estavel} — {msg}")

print("\n=== Validação de Estabilidade (PID instável) ===")
estavel_inst, msg_inst = validar_estabilidade(k, tau, theta, 100.0, 0.01, 50.0)
print(f"Estável: {estavel_inst} — {msg_inst}")

print("\n=== sintonizar_manual ===")
manual = sintonizar_manual(1.5, 8.0, 0.5)
print(f"Kp={manual['Kp']}, Ti={manual['Ti']}, Td={manual['Td']}")
