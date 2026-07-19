"""
Módulo de configuración general del proyecto.
Contiene constantes, listas de tickers y parámetros por defecto.
"""

TICKERS_DISPONIBLES = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Nvidia": "NVDA",
    "Tesla": "TSLA",
    "Netflix": "NFLX",
    "AMD": "AMD",
    "Intel": "INTC",
}

PERIODOS_DISPONIBLES = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"]

TIPOS_DE_INFORME = [
    "Información General",
    "Estados Financieros",
    "Histórico de Cotizaciones",
    "Dividendos",
    "Splits",
    "Noticias",
    "Indicadores Técnicos",
    "Comparación de Empresas",
    "Predicción con IA",
    "Dashboard Ejecutivo",
]

COLOR_FONDO = "#1e1e2f"
COLOR_TEXTO = "#ffffff"
COLOR_ACENTO = "#00c896"
