"""
Informe 2: Estados Financieros (Resultados, Balance, Flujo de Caja).
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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


def _agregar_grafico_barras_financiero(pestanas, df_financials):
    tab = ttk.Frame(pestanas)
    pestanas.add(tab, text="Gráfico Financiero")

    if df_financials.empty:
        ttk.Label(tab, text="No hay datos financieros disponibles.").pack(expand=True)
        return

    periodos = [str(c)[:7] for c in df_financials.columns]

    def _extraer_fila(nombre):
        return df_financials.loc[nombre] if nombre in df_financials.index else None

    ingresos = _extraer_fila("Total Revenue")
    beneficio = _extraer_fila("Net Income")
    ebitda = _extraer_fila("EBITDA")

    if ingresos is None and beneficio is None and ebitda is None:
        ttk.Label(tab, text="No se encontraron las filas esperadas en los estados financieros.").pack(expand=True)
        return

    fig, ax = plt.subplots(figsize=(9, 4), dpi=120)
    x = range(len(periodos))
    width = 0.25

    if ingresos is not None:
        ax.bar([i - width for i in x], ingresos.values / 1e9, width,
               label="Ingresos", color="#38bdf8")
    if beneficio is not None:
        ax.bar(x, beneficio.values / 1e9, width,
               label="Beneficio Neto", color="#22c55e")
    if ebitda is not None:
        ax.bar([i + width for i in x], ebitda.values / 1e9, width,
               label="EBITDA", color="#f59e0b")

    ax.set_xticks(x)
    ax.set_xticklabels(periodos, rotation=45, ha="right")
    ax.set_ylabel("Miles de millones (USD)")
    ax.set_title("Ingresos, Beneficio Neto y EBITDA por periodo", fontsize=11)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


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

    _agregar_grafico_barras_financiero(pestanas, empresa.financials)
