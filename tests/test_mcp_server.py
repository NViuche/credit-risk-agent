"""
Prueba el servidor MCP `credit-risk` como lo haría Claude Code: lo arranca por stdio,
lista sus herramientas y las llama. Ejecutar: python tests/test_mcp_server.py
"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RAIZ = Path(__file__).resolve().parents[1]


def _contenido(resultado) -> object:
    return json.loads(resultado.content[0].text)


async def main():
    parametros = StdioServerParameters(command=sys.executable, args=[str(RAIZ / "backend" / "mcp_server.py")], cwd=str(RAIZ))
    async with stdio_client(parametros) as (lectura, escritura):
        async with ClientSession(lectura, escritura) as sesion:
            await sesion.initialize()

            herramientas = sorted(t.name for t in (await sesion.list_tools()).tools)
            assert herramientas == ["analizar_cartera", "puntuar_prestamo", "resumen_cartera"], herramientas
            print("OK  list_tools:", ", ".join(herramientas))

            r = _contenido(await sesion.call_tool("puntuar_prestamo", {
                "loan_percent_income": 0.4, "loan_int_rate": 15.2, "cb_person_default_on_file": "Y", "loan_grade": "D"}))
            assert r["score_riesgo"] == 76.17 and r["requiere_autorizacion_humana"] is True, r
            print("OK  puntuar_prestamo:", r["score_riesgo"], r["categoria"])

            r = _contenido(await sesion.call_tool("analizar_cartera", {"limite": 20, "orden": "importe"}))
            assert r["kpis"]["prestamos"] == 20 and r["kpis"]["pendientes_autorizacion"] == 2, r["kpis"]
            print("OK  analizar_cartera: 20 préstamos,", r["kpis"]["pendientes_autorizacion"], "pendientes de autorización")

            r = _contenido(await sesion.call_tool("analizar_cartera", {"loan_grade": "Z"}))
            assert r["errores"], r
            print("OK  analizar_cartera con grado inválido:", r["errores"][0])

            r = await sesion.call_tool("resumen_cartera", {})
            filas = r.structured_content["result"] if r.structured_content else [json.loads(c.text) for c in r.content]
            assert sum(f["prestamos"] for f in filas) == 32_581
            print("OK  resumen_cartera: 32.581 préstamos")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
    print("Servidor MCP verificado")
