"""Dashboard ejecutivo para una empresa seleccionada."""
import tkinter as tk
from tkinter import ttk

from utilidades import obtener_ticker_obj, formatear_moneda, formatear_porcentaje


def abrir_informe_dashboard(ticker: str, periodo: str):
    obj = obtener_ticker_obj(ticker)
    info = obj.info

    ventana = tk.Toplevel()
    ventana.title(f"Dashboard ejecutivo - {ticker}")
    ventana.geometry("900x620")
    ventana.configure(bg="#0f172a")

    header = ttk.Frame(ventana, padding=16)
    header.pack(fill="x")
    ttk.Label(header, text=f"Resumen rápido {ticker}", style="Title.TLabel").pack(anchor="w")
    ttk.Label(header, text=info.get("longName", ticker), foreground="#94a3b8").pack(anchor="w")

    cards = ttk.Frame(ventana, padding=(16, 0, 16, 16))
    cards.pack(fill="x")

    metrics = [
        ("Precio actual", formatear_moneda(info.get("currentPrice"))),
        ("P/E", info.get("trailingPE") or "N/D"),
        ("Dividend Yield", formatear_porcentaje(info.get("dividendYield")) if info.get("dividendYield") is not None else "N/D"),
        ("Capitalización", f"{info.get('marketCap', 0):,}"),
    ]

    for idx, (label, value) in enumerate(metrics):
        card = ttk.Frame(cards, padding=12, style="Card.TFrame")
        card.grid(row=0, column=idx, padx=6, pady=6, sticky="nsew")
        ttk.Label(card, text=label, foreground="#38bdf8").pack(anchor="w")
        ttk.Label(card, text=str(value), font=("Segoe UI", 13, "bold"), foreground="#f8fafc").pack(anchor="w", pady=(4, 0))

    body = ttk.Frame(ventana, padding=(16, 0, 16, 16))
    body.pack(fill="both", expand=True)

    text = ttk.Frame(body)
    text.pack(fill="both", expand=True, side="left")
    ttk.Label(text, text="Contexto", foreground="#38bdf8").pack(anchor="w")
    resumen = (
        f"Sector: {info.get('sector', 'N/D')}\n"
        f"País: {info.get('country', 'N/D')}\n"
        f"Industria: {info.get('industry', 'N/D')}\n"
        f"Beta: {info.get('beta', 'N/D')}\n"
        f"Periodo: {periodo}"
    )
    ttk.Label(text, text=resumen, justify="left", wraplength=320, foreground="#e2e8f0").pack(anchor="w", pady=(8, 0))

    summary = ttk.Frame(body)
    summary.pack(fill="both", expand=True, side="left", padx=(16, 0))
    ttk.Label(summary, text="Indicadores clave", foreground="#38bdf8").pack(anchor="w")
    ttk.Label(summary, text="- Precio actual\n- Ratio P/E\n- Dividend Yield\n- Capitalización bursátil", justify="left", wraplength=280, foreground="#e2e8f0").pack(anchor="w", pady=(8, 0))
