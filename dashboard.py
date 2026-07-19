"""Dashboard ejecutivo para una empresa seleccionada."""
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ta

from utilidades import obtener_ticker_obj, formatear_numero_grande


def _color_semaforo(valor, tipo="rsi"):
    if tipo == "rsi":
        if valor >= 70:
            return "#ef4444"
        elif valor <= 30:
            return "#22c55e"
        return "#f59e0b"
    return "#94a3b8"


def _texto_semaforo(rsi, ma50, ma200):
    senales = []
    if rsi >= 70:
        senales.append("RSI: Sobrecompra")
    elif rsi <= 30:
        senales.append("RSI: Sobreventa")

    if ma50 is not None and ma200 is not None and not np.isnan(ma50) and not np.isnan(ma200):
        if ma50 > ma200:
            senales.append("Golden Cross")
        else:
            senales.append("Death Cross")

    if not senales:
        senales.append("Neutral")

    return " | ".join(senales)


def _color_compra(rsi, ma50, ma200):
    if rsi <= 30:
        return "#22c55e"
    if rsi >= 70:
        return "#ef4444"
    if ma50 is not None and ma200 is not None and not np.isnan(ma50) and not np.isnan(ma200):
        if ma50 > ma200:
            return "#22c55e"
        return "#ef4444"
    return "#f59e0b"


def _texto_compra(rsi, ma50, ma200):
    if rsi <= 30:
        return "COMPRA"
    if rsi >= 70:
        return "VENTA"
    if ma50 is not None and ma200 is not None and not np.isnan(ma50) and not np.isnan(ma200):
        if ma50 > ma200:
            return "COMPRA"
        return "VENTA"
    return "NEUTRAL"


def abrir_informe_dashboard(ticker: str, periodo: str):
    obj = obtener_ticker_obj(ticker)
    info = obj.info
    df = obj.history(period=periodo)

    # Calcular indicadores
    if not df.empty:
        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
        macd = ta.trend.MACD(df["Close"])
        df["MACD"] = macd.macd()
        df["MACD_signal"] = macd.macd_signal()
        df["MACD_diff"] = df["MACD"] - df["MACD_signal"]

        precio_actual = df["Close"].iloc[-1]
        precio_anterior = df["Close"].iloc[-2] if len(df) > 1 else precio_actual
        cambio_pct = ((precio_actual - precio_anterior) / precio_anterior) * 100
        volumen = df["Volume"].iloc[-1]
        rsi = df["RSI"].iloc[-1]
        macd_val = df["MACD"].iloc[-1]
        ma50 = df["MA50"].iloc[-1]
        ma200 = df["MA200"].iloc[-1]
    else:
        precio_actual = info.get("currentPrice", 0)
        cambio_pct = 0
        volumen = 0
        rsi = 50
        macd_val = 0
        ma50 = None
        ma200 = None

    ventana = tk.Toplevel()
    ventana.title(f"Dashboard Ejecutivo - {ticker}")
    ventana.geometry("1100x780")
    ventana.configure(bg="#0f172a")

    # --- Header ---
    header = ttk.Frame(ventana, padding=(16, 12, 16, 4))
    header.pack(fill="x")
    ttk.Label(header, text=f"Dashboard Ejecutivo", style="Title.TLabel").pack(anchor="w")
    ttk.Label(header, text=f"{info.get('longName', ticker)}  ·  {periodo}", foreground="#94a3b8").pack(anchor="w")

    # --- KPI Cards ---
    cards_frame = ttk.Frame(ventana, padding=(16, 8, 16, 4))
    cards_frame.pack(fill="x")

    direction = "▲" if cambio_pct >= 0 else "▼"
    cambio_color = "#22c55e" if cambio_pct >= 0 else "#ef4444"

    semaforo_color = _color_compra(rsi, ma50, ma200)
    semaforo_texto = _texto_compra(rsi, ma50, ma200)

    kpis = [
        ("Precio Actual", f"${precio_actual:.2f}", "#38bdf8"),
        ("Cambio %", f"{direction} {abs(cambio_pct):.2f}%", cambio_color),
        ("Capitalización", f"${info.get('marketCap', 0):,}", "#a78bfa"),
        ("Volumen", formatear_numero_grande(volumen), "#f472b6"),
        ("RSI", f"{rsi:.1f}", _color_semaforo(rsi, "rsi")),
        ("MACD", f"{macd_val:.2f}", "#22d3ee"),
        ("Media 50", f"${ma50:.2f}" if ma50 is not None and not np.isnan(ma50) else "N/D", "#fbbf24"),
        ("Media 200", f"${ma200:.2f}" if ma200 is not None and not np.isnan(ma200) else "N/D", "#f97316"),
    ]

    for idx, (label, value, color) in enumerate(kpis):
        card = tk.Frame(cards_frame, bg="#1e293b", highlightbackground="#334155", highlightthickness=1)
        card.grid(row=0, column=idx, padx=4, pady=4, sticky="nsew")
        cards_frame.grid_columnconfigure(idx, weight=1)
        tk.Label(card, text=label, bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 8)).pack(anchor="w", padx=8, pady=(8, 0))
        tk.Label(card, text=str(value), bg="#1e293b", fg=color, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=8, pady=(0, 8))

    # --- Semáforo (card aparte más grande) ---
    sem_card = tk.Frame(cards_frame, bg=semaforo_color, highlightbackground=semaforo_color, highlightthickness=1)
    sem_card.grid(row=0, column=len(kpis), padx=4, pady=4, sticky="nsew")
    cards_frame.grid_columnconfigure(len(kpis), weight=1)
    tk.Label(sem_card, text="SEÑAL", bg=semaforo_color, fg="#0f172a", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(8, 0))
    tk.Label(sem_card, text=semaforo_texto, bg=semaforo_color, fg="#0f172a", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=8, pady=(0, 8))
    tk.Label(sem_card, text=_texto_semaforo(rsi, ma50, ma200), bg=semaforo_color, fg="#0f172a", font=("Segoe UI", 7)).pack(anchor="w", padx=8, pady=(0, 6))

    # --- 4 Charts (2x2) ---
    charts_frame = ttk.Frame(ventana, padding=(16, 4, 16, 12))
    charts_frame.pack(fill="both", expand=True)

    charts_frame.grid_rowconfigure(0, weight=1)
    charts_frame.grid_rowconfigure(1, weight=1)
    charts_frame.grid_columnconfigure(0, weight=1)
    charts_frame.grid_columnconfigure(1, weight=1)

    if not df.empty and len(df) > 5:
        plt.style.use("seaborn-v0_8-darkgrid")

        # Chart 1: Price + MA50 + MA200
        fig1, ax1 = plt.subplots(figsize=(5, 2.8), dpi=110)
        ax1.plot(df.index, df["Close"], color="#38bdf8", linewidth=1.5, label="Close")
        if not df["MA50"].isna().all():
            ax1.plot(df.index, df["MA50"], color="#fbbf24", linewidth=1, label="MA50")
        if not df["MA200"].isna().all():
            ax1.plot(df.index, df["MA200"], color="#f97316", linewidth=1, label="MA200")
        ax1.set_title(f"Precio + Medias ({ticker})", fontsize=9, color="#334155")
        ax1.legend(fontsize=6, loc="upper left")
        ax1.grid(True, alpha=0.2)
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        # Chart 2: Volume
        fig2, ax2 = plt.subplots(figsize=(5, 2.8), dpi=110)
        ax2.bar(df.index, df["Volume"], color="#22c55e", alpha=0.7, width=0.8)
        ax2.set_title(f"Volumen ({ticker})", fontsize=9, color="#334155")
        ax2.grid(axis="y", alpha=0.2)
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        # Chart 3: RSI
        fig3, ax3 = plt.subplots(figsize=(5, 2.8), dpi=110)
        ax3.plot(df.index, df["RSI"], color="#a78bfa", linewidth=1.5)
        ax3.axhline(y=70, color="#ef4444", linestyle="--", linewidth=0.8, alpha=0.5)
        ax3.axhline(y=30, color="#22c55e", linestyle="--", linewidth=0.8, alpha=0.5)
        ax3.fill_between(df.index, 30, 70, alpha=0.05, color="#94a3b8")
        ax3.set_ylim(0, 100)
        ax3.set_title(f"RSI ({ticker})", fontsize=9, color="#334155")
        ax3.grid(True, alpha=0.2)
        fig3.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=charts_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

        # Chart 4: MACD
        fig4, ax4 = plt.subplots(figsize=(5, 2.8), dpi=110)
        ax4.plot(df.index, df["MACD"], color="#22d3ee", linewidth=1.5, label="MACD")
        ax4.plot(df.index, df["MACD_signal"], color="#f59e0b", linewidth=1, label="Signal")
        # Histogram for MACD difference
        colors_macd = ["#22c55e" if v >= 0 else "#ef4444" for v in df["MACD_diff"]]
        ax4.bar(df.index, df["MACD_diff"], color=colors_macd, alpha=0.4, width=0.8)
        ax4.axhline(y=0, color="#94a3b8", linewidth=0.5)
        ax4.set_title(f"MACD ({ticker})", fontsize=9, color="#334155")
        ax4.legend(fontsize=6, loc="upper left")
        ax4.grid(True, alpha=0.2)
        fig4.tight_layout()
        canvas4 = FigureCanvasTkAgg(fig4, master=charts_frame)
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, padx=4, pady=4, sticky="nsew")
