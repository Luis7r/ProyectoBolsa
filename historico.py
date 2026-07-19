"""
Informe 3: Histórico de cotizaciones.
"""
import tkinter as tk
from tkinter import ttk
from utilidades import obtener_ticker_obj


def abrir_informe_historico(ticker: str, periodo: str):
    empresa = obtener_ticker_obj(ticker)
    df = empresa.history(period=periodo).reset_index()
    df["MM20"] = df["Close"].rolling(20).mean()
    df["MM50"] = df["Close"].rolling(50).mean()

    ventana = tk.Toplevel()
    ventana.title(f"Histórico - {ticker}")
    ventana.geometry("900x600")

    columnas = ["Fecha", "Open", "High", "Low", "Close", "Volume"]
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(fill="x", padx=10, pady=10)

    for _, fila in df.tail(100).iterrows():
        tabla.insert("", "end", values=[
            fila["Date"].strftime("%Y-%m-%d"),
            round(fila["Open"], 2),
            round(fila["High"], 2),
            round(fila["Low"], 2),
            round(fila["Close"], 2),
            int(fila["Volume"]),
        ])

    # TODO: agregar gráfico interactivo con precio, volumen y medias móviles (usar graficos.py o mplfinance)
