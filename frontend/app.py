"""
Frontend de CreditGuard AI (Streamlit).
Arranque: streamlit run frontend/app.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from backend import servicio  # noqa: E402


def es(valor, decimales: int = 0) -> str:
    """Formato numérico español: punto de miles y coma decimal (22.000 · 93,14)."""
    if valor is None or pd.isna(valor):
        return "—"
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


st.set_page_config(page_title="CreditGuard AI", page_icon="📉", layout="wide")
st.title("CreditGuard AI · Riesgo de impago")
st.caption("Cartera real de 32.581 préstamos en Supabase (`public.credit_risk`). Lectura en modo solo lectura.")

# --- Petición del usuario -------------------------------------------------------
with st.sidebar:
    st.header("Petición de análisis")
    limite = st.number_input("Nº de préstamos", min_value=1, max_value=500, value=20)
    orden = st.selectbox("Ordenar por", list(servicio.ORDENES), format_func={
        "importe": "Mayor importe", "tipo_interes": "Mayor tipo de interés",
        "esfuerzo": "Mayor esfuerzo (cuota/ingresos)", "id": "Identificador"}.get)
    loan_intent = st.selectbox("Finalidad", ["Todas", *servicio.FINALIDADES])
    loan_grade = st.selectbox("Grado", ["Todos", *servicio.GRADOS])
    lanzar = st.button("Analizar cartera", type="primary", width="stretch")

if lanzar:
    st.session_state.informe = servicio.analizar_cartera(
        limite=int(limite),
        loan_intent=None if loan_intent == "Todas" else loan_intent,
        loan_grade=None if loan_grade == "Todos" else loan_grade,
        orden=orden,
    )
    st.session_state.autorizados = set()

informe = st.session_state.get("informe")
if not informe:
    st.info("Elige los filtros en el panel lateral y pulsa **Analizar cartera**.")
    st.stop()

# --- Errores y avisos (se muestran, no se ocultan) -----------------------------
for error in informe["errores"]:
    st.error(error)
for aviso in informe["avisos"]:
    st.warning(aviso)
if not informe["prestamos"]:
    st.stop()

# --- KPI ------------------------------------------------------------------------
k = informe["kpis"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Préstamos analizados", es(k["prestamos"]))
c2.metric("Importe expuesto", f"{es(k['importe_total'])} $")
c3.metric("Score medio", es(k["score_medio"], 2))
c4.metric("Pendientes de autorización", k["pendientes_autorizacion"])

st.subheader("KPI por categoría de riesgo")
tabla_kpi = pd.DataFrame(k["por_categoria"]).T.rename(columns={
    "prestamos": "Préstamos", "importe": "Importe ($)",
    "impagos_reales": "Impagos reales", "tasa_impago_pct": "Tasa de impago real (%)"})
izq, der = st.columns([3, 2])
izq.dataframe(tabla_kpi.style.format({
    "Préstamos": es, "Importe ($)": es, "Impagos reales": es,
    "Tasa de impago real (%)": lambda v: es(v, 1)}), width="stretch")
der.bar_chart(tabla_kpi["Préstamos"], horizontal=True)
st.caption("`loan_status` (impago real) solo se usa para validar el score, nunca para calcularlo.")

# --- Detalle y acciones ------------------------------------------------------
st.subheader("Préstamos priorizados por riesgo")
detalle = pd.DataFrame(informe["prestamos"])[[
    "id", "score_riesgo", "categoria", "loan_amnt", "loan_intent", "loan_grade",
    "loan_int_rate", "loan_percent_income", "cb_person_default_on_file", "accion_sugerida", "loan_status"]]
st.dataframe(detalle.style.format({
    "id": str, "score_riesgo": lambda v: es(v, 2), "loan_amnt": es,
    "loan_int_rate": lambda v: es(v, 2), "loan_percent_income": lambda v: es(v, 2)}),
    width="stretch", hide_index=True)

criticos = [p for p in informe["prestamos"] if p["requiere_autorizacion_humana"]]
st.subheader(f"Acciones que requieren autorización humana ({len(criticos)})")
if not criticos:
    st.success("Ningún préstamo supera el umbral crítico (score > 65).")
for p in criticos:
    autorizado = p["id"] in st.session_state.autorizados
    with st.container(border=True):
        st.markdown(f"**Préstamo {p['id']}** · score {es(p['score_riesgo'], 2)} · {es(p['loan_amnt'])} $ · {p['loan_intent']}")
        st.write(p["accion_sugerida"])
        if autorizado:
            st.success("Autorizado por el analista.")
        elif st.button("Autorizar propuesta", key=f"aut-{p['id']}"):
            st.session_state.autorizados.add(p["id"])
            st.rerun()
