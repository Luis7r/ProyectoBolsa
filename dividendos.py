"""
Informe 4: Dividendos. Informe 5: Splits.
"""
import tkinter as tk
from tkinter import ttk
from utilidades import obtener_ticker_obj
from graficos import crear_grafico_barras


def abrir_informe_dividendos(ticker: str):
    empresa = obtener_ticker_obj(ticker)
    dividendos = empresa.dividends

    ventana = tk.Toplevel()
    ventana.title(f"Dividendos - {ticker}")
    ventana.geometry("700x600")

    tabla = ttk.Treeview(ventana, columns=("Fecha", "Monto"), show="headings", height=10)
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Monto", text="Monto")
    tabla.pack(fill="x", padx=10, pady=10)

    for fecha, monto in dividendos.items():
        tabla.insert("", "end", values=[fecha.strftime("%Y-%m-%d"), round(monto, 4)])

    if not dividendos.empty:
        por_anio = dividendos.groupby(dividendos.index.year).sum()
        grafico_frame = ttk.Frame(ventana)
        grafico_frame.pack(fill="both", expand=True, padx=10, pady=10)
        crear_grafico_barras(grafico_frame, por_anio.index.astype(str), por_anio.values,
                              titulo="Dividendos por año", ylabel="Monto")


def abrir_informe_splits(ticker: str):
    empresa = obtener_ticker_obj(ticker)
    splits = empresa.splits

    ventana = tk.Toplevel()
    ventana.title(f"Splits - {ticker}")
    ventana.geometry("500x400")

    tabla = ttk.Treeview(ventana, columns=("Fecha", "Split"), show="headings", height=15)
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Split", text="Split")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    for fecha, ratio in splits.items():
        tabla.insert("", "end", values=[fecha.strftime("%Y-%m-%d"), ratio])
