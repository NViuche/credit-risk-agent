"""
Lógica de negocio: consulta la cartera, la puntúa con la skill credit-risk
y calcula los KPI de BI. La usan el frontend, el servidor MCP y las pruebas.
"""
import sys
from decimal import Decimal

from config import settings
from backend.db import ErrorDatos, consultar

sys.path.insert(0, str(settings.CARPETA_SKILL))
from credit_risk import calculate_credit_risk  # noqa: E402

FINALIDADES = ("DEBTCONSOLIDATION", "EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE")
GRADOS = ("A", "B", "C", "D", "E", "F", "G")
CATEGORIAS = ("CRÍTICO", "MODERADO", "BAJO")

# Lista blanca de ordenaciones: el usuario elige una clave, nunca escribe SQL.
ORDENES = {
    "importe": "loan_amnt DESC, id",
    "tipo_interes": "loan_int_rate DESC NULLS LAST, id",
    "esfuerzo": "loan_percent_income DESC, id",
    "id": "id",
}


def _num(valor):
    return float(valor) if isinstance(valor, Decimal) else valor


def cargar_prestamos(
    limite: int = 20,
    loan_intent: str | None = None,
    loan_grade: str | None = None,
    orden: str = "importe",
) -> list[dict]:
    """Lee préstamos reales de public.credit_risk con filtros validados."""
    if not 1 <= limite <= settings.MAX_FILAS:
        raise ValueError(f"El límite debe estar entre 1 y {settings.MAX_FILAS}.")
    if orden not in ORDENES:
        raise ValueError(f"Orden no válido: {orden!r}. Opciones: {', '.join(ORDENES)}.")
    if loan_intent and loan_intent not in FINALIDADES:
        raise ValueError(f"Finalidad no válida: {loan_intent!r}.")
    if loan_grade and loan_grade not in GRADOS:
        raise ValueError(f"Grado no válido: {loan_grade!r}.")

    condiciones, parametros = [], []
    if loan_intent:
        condiciones.append("loan_intent = %s")
        parametros.append(loan_intent)
    if loan_grade:
        condiciones.append("loan_grade = %s")
        parametros.append(loan_grade)
    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    sql = f"""
        SELECT id, loan_amnt, loan_intent, loan_grade, loan_int_rate,
               loan_percent_income, cb_person_default_on_file, loan_status
        FROM public.credit_risk {where}
        ORDER BY {ORDENES[orden]}
        LIMIT %s
    """
    filas = consultar(sql, (*parametros, limite))
    return [{k: _num(v) for k, v in fila.items()} for fila in filas]


def puntuar(prestamos: list[dict]) -> tuple[list[dict], list[str]]:
    """Aplica la skill a cada préstamo. Las filas inválidas se apartan y se informan, no detienen el análisis."""
    puntuados, errores = [], []
    for p in prestamos:
        try:
            r = calculate_credit_risk(
                loan_percent_income=p["loan_percent_income"],
                loan_int_rate=p["loan_int_rate"],
                cb_person_default_on_file=p["cb_person_default_on_file"],
                loan_grade=p["loan_grade"],
            )
        except (KeyError, TypeError, ValueError) as e:
            errores.append(f"Préstamo {p.get('id', '?')}: {e}")
            continue
        puntuados.append({**p, **r})
    puntuados.sort(key=lambda x: x["score_riesgo"], reverse=True)
    return puntuados, errores


def kpis(puntuados: list[dict]) -> dict:
    """KPI por categoría: nº de préstamos, importe expuesto e impago real observado."""
    por_categoria = {}
    for cat in CATEGORIAS:
        grupo = [p for p in puntuados if p["categoria"] == cat]
        impagos = sum(p["loan_status"] for p in grupo)
        por_categoria[cat] = {
            "prestamos": len(grupo),
            "importe": sum(p["loan_amnt"] for p in grupo),
            "impagos_reales": impagos,
            "tasa_impago_pct": round(100 * impagos / len(grupo), 1) if grupo else None,
        }
    return {
        "prestamos": len(puntuados),
        "importe_total": sum(p["loan_amnt"] for p in puntuados),
        "score_medio": round(sum(p["score_riesgo"] for p in puntuados) / len(puntuados), 2) if puntuados else None,
        "pendientes_autorizacion": sum(p["requiere_autorizacion_humana"] for p in puntuados),
        "por_categoria": por_categoria,
    }


def analizar_cartera(
    limite: int = 20,
    loan_intent: str | None = None,
    loan_grade: str | None = None,
    orden: str = "importe",
) -> dict:
    """Flujo completo: datos -> skill -> KPI -> acciones. Nunca lanza: devuelve los errores en el resultado."""
    resultado = {"filtros": {"limite": limite, "loan_intent": loan_intent, "loan_grade": loan_grade, "orden": orden},
                 "prestamos": [], "kpis": kpis([]), "errores": [], "avisos": []}
    try:
        prestamos = cargar_prestamos(limite, loan_intent, loan_grade, orden)
    except (ValueError, ErrorDatos) as e:
        resultado["errores"].append(str(e))
        return resultado

    if not prestamos:
        resultado["avisos"].append("La consulta no devolvió préstamos con esos filtros: datos insuficientes para analizar.")
        return resultado

    puntuados, errores = puntuar(prestamos)
    resultado.update(prestamos=puntuados, kpis=kpis(puntuados), errores=errores)
    resultado["avisos"] = [f"Préstamo {p['id']}: {a}" for p in puntuados for a in p["avisos"]]
    return resultado


def resumen_cartera() -> list[dict]:
    """KPI globales de toda la tabla por grado (validación contra el dato original)."""
    filas = consultar("""
        SELECT loan_grade, count(*) AS prestamos, sum(loan_status) AS impagos,
               round(avg(loan_status) * 100, 2) AS tasa_impago_pct, sum(loan_amnt) AS importe
        FROM public.credit_risk GROUP BY loan_grade ORDER BY loan_grade
    """)
    return [{k: _num(v) for k, v in f.items()} for f in filas]


if __name__ == "__main__":
    import json

    sys.stdout.reconfigure(encoding="utf-8")
    informe = analizar_cartera(limite=20)
    print(json.dumps(informe["kpis"], ensure_ascii=False, indent=2))
    for e in informe["errores"] + informe["avisos"]:
        print("·", e)
