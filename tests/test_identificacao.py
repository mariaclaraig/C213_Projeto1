import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.identificacao import identificar_sistemas

K_REF   = 2.0
TAU_REF = 10.0
THETA_REF = 3.0
TOLERANCE = 0.05

t = np.linspace(0, 80, 500)
y = K_REF * (1 - np.exp(-(t - THETA_REF) / TAU_REF)) * (t >= THETA_REF)
u = np.ones_like(t)
u[0] = 0.0

resultado = identificar_sistemas(t, y, u)

print("=== SMITH ===")
s = resultado['smith']
print(f"k={s['k']:.4f}, tau={s['tau']:.4f}, theta={s['theta']:.4f}, EQM={s['eqm']:.6f}")

print("\n=== SUNDARESAN ===")
sund = resultado['sundaresan']
print(f"k={sund['k']:.4f}, tau={sund['tau']:.4f}, theta={sund['theta']:.4f}, EQM={sund['eqm']:.6f}")

print(f"\nRecomendado (menor EQM): {resultado['recomendado'].upper()}")

for metodo, res in [('smith', s), ('sundaresan', sund)]:
    assert abs(res['k']     - K_REF)     / K_REF     < TOLERANCE, f"{metodo}: k fora da tolerância"
    assert abs(res['tau']   - TAU_REF)   / TAU_REF   < TOLERANCE, f"{metodo}: tau fora da tolerância"
    assert abs(res['theta'] - THETA_REF) / THETA_REF < TOLERANCE, f"{metodo}: theta fora da tolerância"

print("\n[OK] Todos os parametros dentro de 5% do valor de referencia.")
