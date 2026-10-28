"""
Pruebas del backend: lógica de negocio, gestión de errores y validación BI contra Supabase.
Ejecutar: python tests/test_backend.py   (necesita DATABASE_URL en .env)
"""
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend import servicio  # noqa: E402
from backend.db import ErrorDatos  # noqa: E402


# --- Lógica sin base de datos ---------------------------------------------------
def test_fila_invalida_no_detiene_el_analisis():
    filas = [
        {"id": 1, "loan_percent_income": 0.4, "loan_int_rate": 15.0, "cb_person_default_on_file": "Y", "loan_grade": "D", "loan_amnt": 1000, "loan_status": 1},
        {"id": 2, "loan_percent_income": 0.1, "loan_int_rate": 9.0, "cb_person_default_on_file": "N", "loan_grade": "Z", "loan_amnt": 1000, "loan_status": 0},
    ]
    puntuados, errores = servicio.puntuar(filas)
    assert [p["id"] for p in puntuados] == [1]
    assert len(errores) == 1 and "Préstamo 2" in errores[0]


def test_filtro_no_valido_se_rechaza_sin_consultar():
    r = servicio.analizar_cartera(loan_intent="DROP TABLE")
    assert r["errores"] and not r["prestamos"]
    r = servicio.analizar_cartera(limite=10_000)
    assert r["errores"]
    r = servicio.analizar_cartera(orden="loan_amnt; DELETE")
    assert r["errores"]


def test_base_de_datos_caida_devuelve_error_legible():
    with mock.patch.object(servicio, "consultar", side_effect=ErrorDatos("Error al consultar Supabase: timeout")):
        r = servicio.analizar_cartera()
    assert r["errores"] == ["Error al consultar Supabase: timeout"]
    assert r["kpis"]["prestamos"] == 0


def test_sin_datos_avisa():
    with mock.patch.object(servicio, "consultar", return_value=[]):
        r = servicio.analizar_cartera()
    assert r["avisos"] and not r["errores"]


# --- Con Supabase ----------------------------------------------------------------
def test_top20_importe_coincide_con_prueba_mcp():
    r = servicio.analizar_cartera(limite=20, orden="importe")
    assert not r["errores"], r["errores"]
    cat = r["kpis"]["por_categoria"]
    assert (cat["CRÍTICO"]["prestamos"], cat["MODERADO"]["prestamos"], cat["BAJO"]["prestamos"]) == (2, 10, 8)
    assert r["kpis"]["importe_total"] == 700_000
    assert r["kpis"]["pendientes_autorizacion"] == 2


def test_validacion_bi_resumen_global():
    filas = servicio.resumen_cartera()
    assert sum(f["prestamos"] for f in filas) == 32_581
    assert sum(f["impagos"] for f in filas) == 7_108
    assert {f["loan_grade"]: f["tasa_impago_pct"] for f in filas}["G"] == 98.44


def test_sesion_de_solo_lectura():
    try:
        servicio.consultar("CREATE TEMP TABLE prueba_escritura (x int)")
    except ErrorDatos as e:
        assert "read-only" in str(e) or "ReadOnly" in str(e), e
        return
    raise AssertionError("La sesión permitió escribir")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pruebas = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print(f"{len(pruebas)} pruebas superadas")
