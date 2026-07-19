"""Ventana de noticias para la empresa seleccionada."""
import tkinter as tk
from tkinter import ttk

from utilidades import obtener_ticker_obj


def abrir_informe_noticias(ticker: str):
    obj = obtener_ticker_obj(ticker)
    ventana = tk.Toplevel()
    ventana.title(f"Noticias - {ticker}")
    ventana.geometry("720x520")
    ventana.configure(bg="#0f172a")

    header = ttk.Frame(ventana, padding=16)
    header.pack(fill="x")
    ttk.Label(header, text=f"Noticias recientes de {ticker}", style="Title.TLabel").pack(anchor="w")
    ttk.Label(header, text="Sección de ejemplo con información contextual del ticker.", foreground="#94a3b8").pack(anchor="w")

    contenido = ttk.Frame(ventana, padding=(16, 0, 16, 16))
    contenido.pack(fill="both", expand=True)

    noticias = [
        f"{ticker}: evolución reciente en el mercado y sentimiento del inversor.",
        f"{ticker}: próximos eventos y resultados esperados del trimestre.",
        f"{ticker}: noticias macroeconómicas que pueden afectar su valoración.",
    ]

    for idx, texto in enumerate(noticias):
        card = ttk.Frame(contenido, padding=10)
        card.pack(fill="x", pady=(0, 8))
        ttk.Label(card, text=f"• {texto}", wraplength=650, justify="left", foreground="#e2e8f0").pack(anchor="w")
