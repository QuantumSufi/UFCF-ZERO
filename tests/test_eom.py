from sympy import simplify
from ufcf_zero.lagrangian import eom, A

def test_euler_lagrange_flat6d():
    """
    EOM ifadesi A -> 0 ikamesi sonrası tam 0'a sadeleşmeli.
    """
    expr = eom()
    zero_expr = simplify(expr.subs({A: 0}).doit())
    assert zero_expr == 0
