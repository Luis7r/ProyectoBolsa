"""
Ventana principal de la aplicación.
"""
import tkinter as tk
from tkinter import ttk
from configuracion import TICKERS_DISPONIBLES, PERIODOS_DISPONIBLES, TIPOS_DE_INFORME
from empresa import abrir_informe_general
from finanzas import abrir_informe_financiero
from historico import abrir_informe_historico
from dividendos import abrir_informe_dividendos, abrir_informe_splits
from indicadores import abrir_informe_indicadores
from comparacion import abrir_informe_comparacion
from prediccion import abrir_informe_prediccion, MODELOS


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Análisis Financiero")
        self.geometry("400x600")

        ttk.Label(self, text="Ticker").pack(pady=(15, 0))
        self.combo_ticker = ttk.Combobox(self, values=list(TICKERS_DISPONIBLES.keys()), state="readonly")
        self.combo_ticker.set("Apple")
        self.combo_ticker.pack()

        ttk.Label(self, text="Periodo").pack(pady=(15, 0))
        self.combo_periodo = ttk.Combobox(self, values=PERIODOS_DISPONIBLES, state="readonly")
        self.combo_periodo.set("1y")
        self.combo_periodo.pack()

        ttk.Label(self, text="Tipo de Informe").pack(pady=(15, 0))
        self.tipo_informe = tk.StringVar(value=TIPOS_DE_INFORME[0])
        for tipo in TIPOS_DE_INFORME:
            ttk.Radiobutton(self, text=tipo, variable=self.tipo_informe, value=tipo).pack(anchor="w", padx=40)

        ttk.Button(self, text="GENERAR INFORME", command=self.generar_informe).pack(pady=20)

    def generar_informe(self):
        empresa = self.combo_ticker.get()
        ticker = TICKERS_DISPONIBLES[empresa]
        periodo = self.combo_periodo.get()
        tipo = self.tipo_informe.get()

        if tipo == "Información General":
            abrir_informe_general(ticker, periodo)
        elif tipo == "Estados Financieros":
            abrir_informe_financiero(ticker)
        elif tipo == "Histórico de Cotizaciones":
            abrir_informe_historico(ticker, periodo)
        elif tipo == "Dividendos":
            abrir_informe_dividendos(ticker)
        elif tipo == "Splits":
            abrir_informe_splits(ticker)
        elif tipo == "Indicadores Técnicos":
            abrir_informe_indicadores(ticker, periodo)
        elif tipo == "Comparación de Empresas":
            abrir_informe_comparacion([ticker])  # TODO: permitir selección múltiple
        elif tipo == "Predicción con IA":
            abrir_informe_prediccion(ticker, periodo, list(MODELOS.keys())[0])
        else:
            print(f"Informe '{tipo}' aún no implementado (Noticias / Dashboard Ejecutivo)")
