from ufcf_zero.lagrangian import eom, A

def test_euler_lagrange_flat6d():
    """
    Basit doğrulama: A -> 0 ikamesi sonrası EOM ifadesi sıfır olmalı.
    """
    expr = eom()
    assert expr.subs({A: 0}) == 0
