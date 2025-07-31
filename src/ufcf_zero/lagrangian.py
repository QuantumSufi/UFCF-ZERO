"""
6‑Boyutlu (3T+3X) UFCF çekirdek eylemi ve Euler–Lagrange denklemi.
"""
import sympy as sp

# --- koordinatlar ---
t1, t2, t3, x, y, z = sp.symbols('t1 t2 t3 x y z')
coords = (t1, t2, t3, x, y, z)

# --- alan ve parametreler ---
A = sp.Function('A')(*coords)
m_A, lam = sp.symbols('m_A lambda', positive=True)

# --- metrik (diag(+,+,+,-,-,-)) ---
g = sp.diag(1, 1, 1, -1, -1, -1)
g_inv = g.inv()
sqrtg = sp.sqrt(abs(g.det()))  # = 1

# --- kinetik terim ---
kin = 0
for mu in range(6):
    dA = sp.diff(A, coords[mu])
    kin += g_inv[mu, mu] * dA * dA
kin = kin / 2

# --- potansiyel ---
V = m_A**2 * A**2 / 2 + lam * A**4 / 4

# --- Lagrangian yoğunluğu ---
L_density = sqrtg * (kin - V)

# --- Euler–Lagrange ---
def eom():
    term = 0
    for mu in range(6):
        dLdA = sp.diff(L_density, sp.diff(A, coords[mu]))
        term += sp.diff(dLdA, coords[mu])
    term -= sp.diff(L_density, A)
    return sp.simplify(term.expand())
