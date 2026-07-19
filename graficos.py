"""
Funciones reutilizables para generar gráficos con matplotlib,
embebidos en ventanas de Tkinter.
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def crear_grafico_linea(frame_padre, x, y, titulo="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, color="#00c896")
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_padre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas


def crear_grafico_barras(frame_padre, categorias, valores, titulo="", ylabel=""):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categorias, valores, color="#00c896")
    ax.set_title(titulo)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_padre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
