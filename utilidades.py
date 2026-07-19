"""
Funciones auxiliares reutilizables en todo el proyecto.
"""
import yfinance as yf


def obtener_ticker_obj(ticker: str):
    """Devuelve el objeto Ticker de yfinance."""
    return yf.Ticker(ticker)


def formatear_numero_grande(numero):
    """Convierte números grandes a formato legible (K, M, B, T)."""
    if numero is None:
        return "N/D"
    abs_num = abs(numero)
    if abs_num >= 1e12:
        return f"{numero / 1e12:.2f}T"
    if abs_num >= 1e9:
        return f"{numero / 1e9:.2f}B"
    if abs_num >= 1e6:
        return f"{numero / 1e6:.2f}M"
    if abs_num >= 1e3:
        return f"{numero / 1e3:.2f}K"
    return str(numero)


def formatear_porcentaje(valor):
    if valor is None:
        return "N/D"
    return f"{valor * 100:.2f}%"
