"""
Prueba el frontend sin navegador con el simulador oficial de Streamlit.
Ejecutar: python tests/test_frontend.py   (necesita DATABASE_URL en .env)
"""
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "frontend" / "app.py")


def test_pantalla_inicial():
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception
    assert "Analizar cartera" in at.info[0].value


def test_analisis_y_autorizacion():
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.sidebar.button[0].click().run()
    assert not at.exception, at.exception
    assert [m.value for m in at.metric][:2] == ["20", "700.000 $"]
    assert at.metric[3].value == "2"

    autorizar = [b for b in at.button if b.label == "Autorizar propuesta"]
    assert len(autorizar) == 2
    autorizar[0].click().run()
    assert any("Autorizado por el analista" in s.value for s in at.success)


def test_filtro_sin_resultados_no_rompe():
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.sidebar.selectbox[1].select("VENTURE")
    at.sidebar.selectbox[2].select("G")
    at.sidebar.button[0].click().run()
    assert not at.exception, at.exception


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    pruebas = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print(f"{len(pruebas)} pruebas superadas")
