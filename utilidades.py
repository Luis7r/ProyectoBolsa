"""
Funciones auxiliares reutilizables en todo el proyecto.
"""
import yfinance as yf


def obtener_ticker_obj(ticker: str):
    """Devuelve el objeto Ticker de yfinance."""
    try:
        return yf.Ticker(ticker)
    except Exception as exc:
        raise RuntimeError(f"No se pudo cargar la información para {ticker}") from exc


def formatear_numero_grande(numero):
    """Convierte números grandes a formato legible (K, M, B, T)."""
    if numero is None:
        return "N/D"
    if not isinstance(numero, (int, float)):
        return str(numero)

    abs_num = abs(numero)
    if abs_num >= 1e12:
        return f"{numero / 1e12:.2f}T"
    if abs_num >= 1e9:
        return f"{numero / 1e9:.2f}B"
    if abs_num >= 1e6:
        return f"{numero / 1e6:.2f}M"
    if abs_num >= 1e3:
        return f"{numero / 1e3:.2f}K"
    return f"{numero:.2f}"


def formatear_porcentaje(valor):
    if valor is None:
        return "N/D"
    if not isinstance(valor, (int, float)):
        return str(valor)
    return f"{valor * 100:.2f}%"


def formatear_moneda(valor):
    if valor is None:
        return "N/D"
    if not isinstance(valor, (int, float)):
        return str(valor)
    return f"${valor:,.2f}"
