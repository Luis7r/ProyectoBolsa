"""
Informe 2: Estados Financieros (Resultados, Balance, Flujo de Caja).
"""
import tkinter as tk
from tkinter import ttk
from utilidades import obtener_ticker_obj


def _llenar_treeview(frame, dataframe):
    tabla = ttk.Treeview(frame, show="headings")
    if dataframe.empty:
        return tabla
    columnas = ["Concepto"] + [str(c) for c in dataframe.columns]
    tabla["columns"] = columnas
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=110)
    for idx, fila in dataframe.iterrows():
        tabla.insert("", "end", values=[idx] + list(fila.values))
    tabla.pack(fill="both", expand=True)
    return tabla


def abrir_informe_financiero(ticker: str):
    empresa = obtener_ticker_obj(ticker)

    ventana = tk.Toplevel()
    ventana.title(f"Estados Financieros - {ticker}")
    ventana.geometry("1000x600")

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True)

    tab_resultados = ttk.Frame(pestanas)
    tab_balance = ttk.Frame(pestanas)
    tab_flujo = ttk.Frame(pestanas)

    pestanas.add(tab_resultados, text="Estado de Resultados")
    pestanas.add(tab_balance, text="Balance General")
    pestanas.add(tab_flujo, text="Flujo de Caja")

    _llenar_treeview(tab_resultados, empresa.financials)
    _llenar_treeview(tab_balance, empresa.balance_sheet)
    _llenar_treeview(tab_flujo, empresa.cashflow)

    # TODO: agregar gráfico de barras con Ingresos, Beneficio Neto y EBITDA (usar graficos.py)
