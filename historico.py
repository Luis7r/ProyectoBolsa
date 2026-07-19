"""
Informe 3: Histórico de cotizaciones.
"""
import tkinter as tk
from tkinter import ttk
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utilidades import obtener_ticker_obj


def abrir_informe_historico(ticker: str, periodo: str):
    empresa = obtener_ticker_obj(ticker)
    df_raw = empresa.history(period=periodo)
    df = df_raw.reset_index()
    df["MM20"] = df["Close"].rolling(20).mean()
    df["MM50"] = df["Close"].rolling(50).mean()

    ventana = tk.Toplevel()
    ventana.title(f"Histórico - {ticker}")
    ventana.geometry("950x750")

    columnas = ["Fecha", "Open", "High", "Low", "Close", "Volume"]
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(fill="x", padx=10, pady=(10, 4))

    for _, fila in df.tail(100).iterrows():
        tabla.insert("", "end", values=[
            fila["Date"].strftime("%Y-%m-%d"),
            round(fila["Open"], 2),
            round(fila["High"], 2),
            round(fila["Low"], 2),
            round(fila["Close"], 2),
            int(fila["Volume"]),
        ])

    grafico_frame = ttk.Frame(ventana)
    grafico_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

    if not df_raw.empty:
        styles = mpf.make_mpf_style(base_mpf_style="charles", rc={"figure.facecolor": "#0f172a", "axes.facecolor": "#0f172a"})
        fig, axes = mpf.plot(
            df_raw,
            type="candle",
            volume=True,
            mav=(20, 50),
            style=styles,
            figsize=(10, 5),
            returnfig=True,
            tight_layout=True,
        )
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
