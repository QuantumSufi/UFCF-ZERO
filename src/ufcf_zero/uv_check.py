import sympy as sp

def uv_degree(L: int, gamma: float) -> float:
    """
    Basit UFCF modeli:
        D = 4 - gamma - 2L
    L : döngü sayısı
    gamma : fraktal boyut parametresi (0 < gamma < 1)
    """
    return 4 - gamma - 2*L
