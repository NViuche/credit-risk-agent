"""
Servidor MCP propio `credit-risk`, construido adaptando el SDK oficial de Python
(github.com/modelcontextprotocol/python-sdk). Expone la skill y el backend como
herramientas que Claude Code puede llamar.

Arranque (lo hace Claude Code a partir de .mcp.json):
    python backend/mcp_server.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcp.server.mcpserver import MCPServer  # noqa: E402

from backend import servicio  # noqa: E402

mcp = MCPServer(
    "credit-risk",
    instructions=(
        "Herramientas de riesgo de impago sobre public.credit_risk (solo lectura). "
        "Las acciones CRÍTICAS son propuestas: requieren autorización humana."
    ),
)


@mcp.tool()
def puntuar_prestamo(
    loan_percent_income: float,
    loan_int_rate: float | None,
    cb_person_default_on_file: str,
    loan_grade: str,
) -> dict:
    """Calcula el Score de Riesgo (0-100), la categoría y la acción para un préstamo."""
    return servicio.calculate_credit_risk(loan_percent_income, loan_int_rate, cb_person_default_on_file, loan_grade)


@mcp.tool()
def analizar_cartera(
    limite: int = 20,
    loan_intent: str | None = None,
    loan_grade: str | None = None,
    orden: str = "importe",
) -> dict:
    """
    Consulta préstamos reales en Supabase, los puntúa con la skill y devuelve KPI y acciones.
    orden: importe | tipo_interes | esfuerzo | id. limite: 1-500.
    """
    return servicio.analizar_cartera(limite, loan_intent, loan_grade, orden)


@mcp.tool()
def resumen_cartera() -> list[dict]:
    """KPI globales de toda la cartera por loan_grade: préstamos, impagos, tasa de impago e importe."""
    return servicio.resumen_cartera()


if __name__ == "__main__":
    mcp.run()
