"""
Skill: Credit Risk & Default Calculator
Calcula de forma determinista el Score de Riesgo de Impago (0 - 100) y la severidad
a partir de las columnas reales de la tabla `public.credit_risk` de Supabase.

Uso desde terminal (lee un objeto JSON o una lista de objetos por stdin):
    echo '{"loan_percent_income": 0.4, "loan_int_rate": 15.2,
           "cb_person_default_on_file": "Y", "loan_grade": "D"}' | python skills/credit-risk/credit_risk.py
"""
import json
import sys

# Puntos por grado de préstamo (A = mejor, G = peor). Máximo 20.
PUNTOS_GRADO = {"A": 0.0, "B": 4.0, "C": 8.0, "D": 14.0, "E": 17.0, "F": 19.0, "G": 20.0}

# Rango de tipos de interés observado en credit_risk (5.42 % - 23.22 %).
TIPO_MIN = 5.0
TIPO_MAX = 23.0


def calculate_credit_risk(
    loan_percent_income: float,
    loan_int_rate: float | None,
    cb_person_default_on_file: str,
    loan_grade: str,
) -> dict:
    """
    Calcula el Score de Riesgo combinando 4 factores ponderados.

    `loan_status` NO es una entrada: es el resultado real (1 = impago) y solo se usa
    para validar el score, nunca para calcularlo.

    Retorna un diccionario con el Score, la Categoría de Riesgo y la Recomendación.
    """
    avisos = []

    # 1. Factor Esfuerzo Financiero (Peso 35%): cuota / ingresos. Satura en 0.50.
    factor_esfuerzo = min(max(float(loan_percent_income), 0.0) / 0.50, 1.0) * 35.0

    # 2. Factor Tipo de Interés (Peso 25%): el precio que el prestamista puso al riesgo.
    if loan_int_rate is None:
        # ~9,6 % de las filas no tienen tipo: se imputa el punto medio y se avisa.
        factor_interes = 12.5
        avisos.append("loan_int_rate nulo: factor imputado a 12,5 (punto medio).")
    else:
        proporcion = (float(loan_int_rate) - TIPO_MIN) / (TIPO_MAX - TIPO_MIN)
        factor_interes = min(max(proporcion, 0.0), 1.0) * 25.0

    # 3. Factor Impago Previo (Peso 20%): historial en buró.
    factor_historial = 20.0 if str(cb_person_default_on_file).upper() == "Y" else 0.0

    # 4. Factor Grado del Préstamo (Peso 20%).
    grado = str(loan_grade).upper()
    if grado not in PUNTOS_GRADO:
        raise ValueError(f"loan_grade debe ser A-G; recibido: {loan_grade!r}")
    factor_grado = PUNTOS_GRADO[grado]

    # Score Total (0 a 100)
    score_total = round(factor_esfuerzo + factor_interes + factor_historial + factor_grado, 2)
    score_total = min(max(score_total, 0.0), 100.0)

    # Matriz de Severidad
    if score_total < 30.0:
        categoria = "BAJO"
        accion = "Enviar recordatorio amigable de pago."
        requiere_aprobacion = False
    elif score_total <= 65.0:
        categoria = "MODERADO"
        accion = "Congelar ampliación de crédito y ofrecer plan de pago en 3 cuotas."
        requiere_aprobacion = False
    else:
        categoria = "CRÍTICO"
        accion = "Generar orden de suspensión temporal de servicio y borrador de reclamo legal."
        requiere_aprobacion = True

    return {
        "score_riesgo": score_total,
        "categoria": categoria,
        "desglose_factores": {
            "esfuerzo_financiero": round(factor_esfuerzo, 2),
            "tipo_interes": round(factor_interes, 2),
            "impago_previo": round(factor_historial, 2),
            "grado_prestamo": round(factor_grado, 2),
        },
        "accion_sugerida": accion,
        "requiere_autorizacion_humana": requiere_aprobacion,
        "avisos": avisos,
    }


def _evaluar(registro: dict) -> dict:
    resultado = calculate_credit_risk(
        loan_percent_income=registro["loan_percent_income"],
        loan_int_rate=registro.get("loan_int_rate"),
        cb_person_default_on_file=registro["cb_person_default_on_file"],
        loan_grade=registro["loan_grade"],
    )
    if "id" in registro:
        resultado = {"id": registro["id"], **resultado}
    return resultado


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # La consola de Windows no es UTF-8 por defecto.
    entrada = json.load(sys.stdin)
    if isinstance(entrada, list):
        salida = [_evaluar(r) for r in entrada]
    else:
        salida = _evaluar(entrada)
    print(json.dumps(salida, ensure_ascii=False, indent=2))
