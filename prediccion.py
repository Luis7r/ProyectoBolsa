"""
Informe 9: Predicción con IA (Regresión Lineal, Random Forest, Árboles).
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from utilidades import obtener_ticker_obj
from graficos import crear_grafico_linea

MODELOS = {
    "Regresión Lineal": LinearRegression,
    "Random Forest": RandomForestRegressor,
    "Árboles de Decisión": DecisionTreeRegressor,
}


def entrenar_y_predecir(df, nombre_modelo):
    df = df.reset_index()
    df["dias"] = np.arange(len(df))
    X = df[["dias"]]
    y = df["Close"]

    corte = int(len(df) * 0.8)
    X_train, X_test = X[:corte], X[corte:]
    y_train, y_test = y[:corte], y[corte:]

    modelo = MODELOS[nombre_modelo]()
    modelo.fit(X_train, y_train)
    predicciones = modelo.predict(X_test)

    rmse = mean_squared_error(y_test, predicciones, squared=False)
    mae = mean_absolute_error(y_test, predicciones)

    return y_test.values, predicciones, rmse, mae


def abrir_informe_prediccion(ticker: str, periodo: str, nombre_modelo: str):
    empresa = obtener_ticker_obj(ticker)
    df = empresa.history(period=periodo)

    real, predicho, rmse, mae = entrenar_y_predecir(df, nombre_modelo)

    ventana = tk.Toplevel()
    ventana.title(f"Predicción con IA - {ticker} ({nombre_modelo})")
    ventana.geometry("800x600")

    ttk.Label(ventana, text=f"RMSE: {rmse:.2f}   MAE: {mae:.2f}",
              font=("Arial", 11, "bold")).pack(pady=10)

    grafico_frame = ttk.Frame(ventana)
    grafico_frame.pack(fill="both", expand=True)

    x = list(range(len(real)))
    crear_grafico_linea(grafico_frame, x, real, titulo="Precio real vs predicho")
    crear_grafico_linea(grafico_frame, x, predicho, titulo="Precio predicho")
