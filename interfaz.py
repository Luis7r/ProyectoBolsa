"""
Ventana principal de la aplicación.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from configuracion import TICKERS_DISPONIBLES, PERIODOS_DISPONIBLES, TIPOS_DE_INFORME
from empresa import abrir_informe_general
from finanzas import abrir_informe_financiero
from historico import abrir_informe_historico
from dividendos import abrir_informe_dividendos, abrir_informe_splits
from indicadores import abrir_informe_indicadores
from comparacion import abrir_informe_comparacion
from prediccion import abrir_informe_prediccion, MODELOS
from dashboard import abrir_informe_dashboard
from noticias import abrir_informe_noticias


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YFinance Analyst")
        self.geometry("580x760")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure("TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#38bdf8")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#94a3b8")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Accent.TButton", background="#38bdf8", foreground="#0f172a")
        style.map("Accent.TButton", background=[("active", "#0ea5e9")], foreground=[("active", "#f8fafc")])
        style.configure("TRadiobutton", background="#0f172a", foreground="#e2e8f0")
        # Combobox estilo más contrastado para que la opción seleccionada sea visible
        style.configure("TCombobox", fieldbackground="#07263a", background="#07263a", foreground="#e2e8f0")
        style.map("TCombobox",
              fieldbackground=[('readonly', '#07263a')],
              foreground=[('readonly', '#e2e8f0')])
        style.configure("Custom.TCombobox", fieldbackground="#07263a", background="#07263a", foreground="#e2e8f0")

        header = ttk.Frame(self, padding=18)
        header.pack(fill="x")

        ttk.Label(header, text="Panel de análisis bursátil", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Explora empresas, métricas financieras y tendencias con una experiencia más visual.",
            style="Subtitle.TLabel",
            wraplength=500,
        ).pack(anchor="w", pady=(6, 0))

        body = ttk.Frame(self, padding=(18, 0, 18, 18))
        body.pack(fill="both", expand=True)

        ttk.Label(body, text="Selecciona una empresa", foreground="#38bdf8").pack(anchor="w")
        self.combo_ticker = ttk.Combobox(body, values=list(TICKERS_DISPONIBLES.keys()), state="readonly", width=35, style="Custom.TCombobox")
        self.combo_ticker.set("Apple")
        self.combo_ticker.pack(fill="x", pady=(4, 10))

        ttk.Label(body, text="Periodo", foreground="#38bdf8").pack(anchor="w")
        self.combo_periodo = ttk.Combobox(body, values=PERIODOS_DISPONIBLES, state="readonly", width=35, style="Custom.TCombobox")
        self.combo_periodo.set("1y")
        self.combo_periodo.pack(fill="x", pady=(4, 10))

        ttk.Label(body, text="Tipo de informe", foreground="#38bdf8").pack(anchor="w")
        self.tipo_informe = tk.StringVar(value="Información General")

        informes_frame = ttk.Frame(body)
        informes_frame.pack(fill="x", pady=(4, 10))

        for idx, tipo in enumerate(TIPOS_DE_INFORME):
            ttk.Radiobutton(
                informes_frame,
                text=tipo,
                variable=self.tipo_informe,
                value=tipo,
            ).grid(row=idx // 2, column=idx % 2, sticky="w", padx=(0, 12), pady=3)

        ttk.Label(body, text="Comparación rápida", foreground="#38bdf8").pack(anchor="w", pady=(8, 4))
        # Listbox con colores de selección más visibles
        self.lista_empresas = tk.Listbox(
            body,
            height=5,
            selectmode="multiple",
            exportselection=False,
            bg="#071124",
            fg="#e2e8f0",
            bd=0,
            highlightthickness=1,
            selectbackground="#38bdf8",
            selectforeground="#0f172a",
            activestyle='dotbox',
        )
        for nombre in TICKERS_DISPONIBLES.keys():
            self.lista_empresas.insert("end", nombre)
        self.lista_empresas.pack(fill="x", pady=(0, 10))

        actions = ttk.Frame(body)
        actions.pack(fill="x", pady=(8, 10))

        ttk.Button(actions, text="Generar informe", command=self.generar_informe, style="Accent.TButton").pack(side="left")
        ttk.Button(actions, text="Dashboard", command=self.abrir_dashboard).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Noticias", command=self.abrir_noticias).pack(side="left", padx=(8, 0))

        self.status_var = tk.StringVar(value="Listo para analizar...")
        ttk.Label(body, textvariable=self.status_var, wraplength=500, foreground="#94a3b8").pack(anchor="w", pady=(8, 0))

        # Resumen de selección para mayor claridad
        self.seleccion_var = tk.StringVar(value="Empresas seleccionadas: ninguna")
        ttk.Label(body, textvariable=self.seleccion_var, foreground="#94a3b8").pack(anchor="w", pady=(6, 0))

        # Bind para actualizar el resumen cuando cambie la selección
        self.lista_empresas.bind('<<ListboxSelect>>', self._on_listbox_select)

    def generar_informe(self):
        empresa = self.combo_ticker.get()
        ticker = TICKERS_DISPONIBLES[empresa]
        periodo = self.combo_periodo.get()
        tipo = self.tipo_informe.get()

        self.status_var.set(f"Generando {tipo} para {empresa}...")

        try:
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
            elif tipo == "Noticias":
                abrir_informe_noticias(ticker)
            elif tipo == "Indicadores Técnicos":
                abrir_informe_indicadores(ticker, periodo)
            elif tipo == "Comparación de Empresas":
                seleccionadas = [self.lista_empresas.get(i) for i in self.lista_empresas.curselection()]
                tickers = [TICKERS_DISPONIBLES[nombre] for nombre in seleccionadas] if seleccionadas else [ticker]
                abrir_informe_comparacion(tickers)
            elif tipo == "Predicción con IA":
                abrir_informe_prediccion(ticker, periodo, next(iter(MODELOS.keys())))
            elif tipo == "Dashboard Ejecutivo":
                abrir_informe_dashboard(ticker, periodo)
            else:
                messagebox.showinfo("Próximamente", f"El informe '{tipo}' aún no está implementado.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo generar el informe.\n\n{exc}")
        else:
            self.status_var.set(f"{tipo} generado correctamente.")

    def abrir_dashboard(self):
        empresa = self.combo_ticker.get()
        ticker = TICKERS_DISPONIBLES[empresa]
        periodo = self.combo_periodo.get()
        abrir_informe_dashboard(ticker, periodo)

    def abrir_noticias(self):
        empresa = self.combo_ticker.get()
        ticker = TICKERS_DISPONIBLES[empresa]
        abrir_informe_noticias(ticker)

    def _on_listbox_select(self, event=None):
        seleccionadas = [self.lista_empresas.get(i) for i in self.lista_empresas.curselection()]
        if seleccionadas:
            texto = f"Empresas seleccionadas: {', '.join(seleccionadas)}"
        else:
            texto = "Empresas seleccionadas: ninguna"
        self.seleccion_var.set(texto)
