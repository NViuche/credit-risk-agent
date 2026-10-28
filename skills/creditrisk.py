"""
Skill: Credit Risk & Default Calculator
Calcula de forma determinista el Score de Riesgo de Impago (0 - 100) y la severidad.
"""

def calculate_credit_risk(
    dso_historico: int,
    porcentaje_credito_usado: float,
    dias_vencido: int,
    incidentes_pago_6m: int
) -> dict:
    """
    Calcula el Score de Riesgo combinando 4 factores ponderados.
    
    Retorna un diccionario con el Score, la Categoría de Riesgo y la Recomendación.
    """
    # 1. Factor Vencimiento Actual (Peso 40%)
    factor_vencimiento = min(dias_vencido * 1.5, 40.0)
    
    # 2. Factor Uso de Crédito (Peso 20%)
    factor_credito = 20.0 if porcentaje_credito_usado > 80.0 else (porcentaje_credito_usado * 0.25)
    
    # 3. Factor Incidentes Previos (Peso 20%)
    factor_incidentes = min(incidentes_pago_6m * 10.0, 20.0)
    
    # 4. Factor DSO Histórico (Peso 20%)
    factor_dso = 20.0 if dso_historico > 45 else (dso_historico * 0.44)
    
    # Score Total (0 a 100)
    score_total = round(factor_vencimiento + factor_credito + factor_incidentes + factor_dso, 2)
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
            "vencimiento": round(factor_vencimiento, 2),
            "credito_usado": round(factor_credito, 2),
            "incidentes": round(factor_incidentes, 2),
            "dso_historico": round(factor_dso, 2)
        },
        "accion_sugerida": accion,
        "requiere_autorizacion_humana": requiere_aprobacion
    }