"""
Informe 7: Indicadores Técnicos (SMA, EMA, RSI, MACD, Bollinger, Estocástico).
Requiere la librería `ta`.
"""
import tkinter as tk
from tkinter import ttk
from utilidades import obtener_ticker_obj
from graficos import crear_grafico_linea
import ta


def calcular_indicadores(df):
    df["SMA20"] = ta.trend.sma_indicator(df["Close"], window=20)
    df["SMA50"] = ta.trend.sma_indicator(df["Close"], window=50)
    df["SMA200"] = ta.trend.sma_indicator(df["Close"], window=200)
    df["EMA"] = ta.trend.ema_indicator(df["Close"], window=20)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    bollinger = ta.volatility.BollingerBands(df["Close"])
    df["BB_high"] = bollinger.bollinger_hband()
    df["BB_low"] = bollinger.bollinger_lband()
    estocastico = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"])
    df["Stoch"] = estocastico.stoch()
    return df


def abrir_informe_indicadores(ticker: str, periodo: str):
    empresa = obtener_ticker_obj(ticker)
    df = empresa.history(period=periodo)
    df = calcular_indicadores(df)

    ventana = tk.Toplevel()
    ventana.title(f"Indicadores Técnicos - {ticker}")
    ventana.geometry("900x700")

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True)

    indicadores_a_graficar = {
        "SMA 20/50/200": ["SMA20", "SMA50", "SMA200"],
        "RSI": ["RSI"],
        "MACD": ["MACD", "MACD_signal"],
        "Bollinger": ["BB_high", "BB_low"],
        "Estocástico": ["Stoch"],
    }

    for nombre, columnas in indicadores_a_graficar.items():
        tab = ttk.Frame(pestanas)
        pestanas.add(tab, text=nombre)
        for col in columnas:
            crear_grafico_linea(tab, df.index, df[col], titulo=col)
