"""
Informe 1: Información General de la empresa.
"""
import tkinter as tk
from tkinter import ttk
from utilidades import obtener_ticker_obj, formatear_numero_grande, formatear_porcentaje
from graficos import crear_grafico_linea


def abrir_informe_general(ticker: str, periodo: str):
    empresa = obtener_ticker_obj(ticker)
    info = empresa.info

    ventana = tk.Toplevel()
    ventana.title(f"Información General - {ticker}")
    ventana.geometry("800x600")

    datos_frame = ttk.Frame(ventana)
    datos_frame.pack(side="top", fill="x", padx=10, pady=10)

    campos = [
        ("Nombre", info.get("longName", "N/D")),
        ("Sector", info.get("sector", "N/D")),
        ("Industria", info.get("industry", "N/D")),
        ("CEO", info.get("companyOfficers", [{}])[0].get("name", "N/D") if info.get("companyOfficers") else "N/D"),
        ("País", info.get("country", "N/D")),
        ("Página Web", info.get("website", "N/D")),
        ("Capitalización bursátil", formatear_numero_grande(info.get("marketCap"))),
        ("Beta", info.get("beta", "N/D")),
        ("EPS", info.get("trailingEps", "N/D")),
        ("P/E", info.get("trailingPE", "N/D")),
        ("Dividend Yield", formatear_porcentaje(info.get("dividendYield"))),
        ("Máximo 52 semanas", info.get("fiftyTwoWeekHigh", "N/D")),
        ("Mínimo 52 semanas", info.get("fiftyTwoWeekLow", "N/D")),
        ("Número de empleados", info.get("fullTimeEmployees", "N/D")),
    ]

    for i, (etiqueta, valor) in enumerate(campos):
        ttk.Label(datos_frame, text=f"{etiqueta}:", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
        ttk.Label(datos_frame, text=str(valor)).grid(row=i, column=1, sticky="w", padx=10, pady=2)

    grafico_frame = ttk.Frame(ventana)
    grafico_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    historico = empresa.history(period=periodo)
    if not historico.empty:
        crear_grafico_linea(
            grafico_frame,
            historico.index,
            historico["Close"],
            titulo=f"Evolución del precio - {ticker}",
            xlabel="Fecha",
            ylabel="Precio (USD)",
        )
