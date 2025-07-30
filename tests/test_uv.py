from ufcf_zero.uv_check import uv_degree

def test_two_loop_convergent():
    # gamma = 0.35 için iki‑döngü diyagram yakınsak mı?
    assert uv_degree(2, 0.35) < 0
