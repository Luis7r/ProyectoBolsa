"""
Informe de comparación de empresas.
"""
import tkinter as tk
from tkinter import ttk

from utilidades import obtener_ticker_obj
from graficos import crear_grafico_barras


def abrir_informe_comparacion(tickers: list):
    tickers = [t for t in tickers if t][:5]
    if not tickers:
        return

    datos = {}
    for ticker in tickers:
        info = obtener_ticker_obj(ticker).info
        datos[ticker] = {
            "Capitalización": info.get("marketCap", 0),
            "P/E": info.get("trailingPE", 0),
            "EPS": info.get("trailingEps", 0),
            "Dividend Yield": info.get("dividendYield", 0) or 0,
            "ROE": info.get("returnOnEquity", 0) or 0,
            "Precio": info.get("currentPrice", 0),
        }

    ventana = tk.Toplevel()
    ventana.title("Comparación de Empresas")
    ventana.geometry("900x700")

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True)

    metricas = ["Capitalización", "P/E", "EPS", "Dividend Yield", "ROE", "Precio"]
    for metrica in metricas:
        tab = ttk.Frame(pestanas)
        pestanas.add(tab, text=metrica)
        valores = [datos[t][metrica] for t in tickers]
        crear_grafico_barras(tab, tickers, valores, titulo=metrica)
