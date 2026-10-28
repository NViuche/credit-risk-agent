"""Pruebas unitarias de la skill credit-risk. Ejecutar: python tests/test_credit_risk.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "credit-risk"))

from credit_risk import calculate_credit_risk  # noqa: E402


def test_perfil_bajo():
    r = calculate_credit_risk(0.05, 7.0, "N", "A")
    assert r["categoria"] == "BAJO"
    assert r["requiere_autorizacion_humana"] is False


def test_perfil_moderado():
    r = calculate_credit_risk(0.25, 14.0, "N", "C")
    assert r["categoria"] == "MODERADO", r


def test_perfil_critico_requiere_autorizacion():
    r = calculate_credit_risk(0.45, 20.0, "Y", "F")
    assert r["categoria"] == "CRÍTICO"
    assert r["requiere_autorizacion_humana"] is True


def test_score_acotado_0_100():
    assert calculate_credit_risk(0.0, 1.0, "N", "A")["score_riesgo"] == 0.0
    assert calculate_credit_risk(0.9, 30.0, "Y", "G")["score_riesgo"] == 100.0


def test_tipo_nulo_se_imputa_y_avisa():
    r = calculate_credit_risk(0.1, None, "N", "B")
    assert r["desglose_factores"]["tipo_interes"] == 12.5
    assert r["avisos"]


def test_grado_invalido_falla():
    try:
        calculate_credit_risk(0.1, 10.0, "N", "Z")
    except ValueError:
        return
    raise AssertionError("Se esperaba ValueError para loan_grade='Z'")


def test_determinista():
    assert calculate_credit_risk(0.3, 12.0, "Y", "C") == calculate_credit_risk(0.3, 12.0, "Y", "C")


if __name__ == "__main__":
    pruebas = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print(f"{len(pruebas)} pruebas superadas")
