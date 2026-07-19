"""
Funciones reutilizables para generar gráficos con matplotlib,
embebidos en ventanas de Tkinter.
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def crear_grafico_linea(frame_padre, x, y, titulo="", xlabel="", ylabel=""):
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(6.3, 3.8), dpi=120)
    ax.plot(x, y, color="#38bdf8", linewidth=2)
    ax.set_title(titulo, fontsize=10, color="#0f172a")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_padre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas


def crear_grafico_barras(frame_padre, categorias, valores, titulo="", ylabel=""):
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(6.3, 3.8), dpi=120)
    ax.bar(categorias, valores, color="#22c55e", alpha=0.9)
    ax.set_title(titulo, fontsize=10, color="#0f172a")
    ax.set_ylabel(ylabel, fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_padre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
