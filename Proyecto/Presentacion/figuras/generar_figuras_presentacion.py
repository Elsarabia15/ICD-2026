"""Figuras de la presentación final del proyecto C-MAPSS (diapositivas de 13.33 x 7.5 pulgadas).

Usa la paleta de la presentación de la propuesta (azul marino, turquesa y naranja) y se guardan
como SVG con el texto como texto, para que la página HTML las muestre con IBM Plex Sans.

Uso (desde la carpeta Proyecto):  py Presentacion/figuras/generar_figuras_presentacion.py
"""
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]          # carpeta Proyecto
SALIDA = Path(__file__).resolve().parent
DATOS = RAIZ / "CMAPSSData"

NAVY, TEAL, ORANGE, SLATE = "#1E3F6B", "#1B8A9A", "#C4622D", "#8C97A5"
TEXTO, SUAVE, LINEA = "#3A4657", "#5A6575", "#D5DBDF"
CONDICIONES = [NAVY, TEAL, ORANGE, "#C9A227", "#7B5EA7", SLATE]
SUBSETS = {"FD001": NAVY, "FD002": TEAL, "FD003": ORANGE, "FD004": SLATE}

SENSORES = ["T2", "T24", "T30", "T50", "P2", "P15", "P30", "Nf", "Nc", "epr", "Ps30", "phi",
            "NRf", "NRc", "BPR", "farB", "htBleed", "Nf_dmd", "PCNfR_dmd", "W31", "W32"]

from matplotlib import font_manager

PLEX = RAIZ / "Presentacion" / "fuentes" / "IBMPlexSans[wdth,wght].ttf"
if PLEX.exists():
    font_manager.fontManager.addfont(str(PLEX))
plt.rcParams.update({
    "font.family": ["IBM Plex Sans", "DejaVu Sans"], "font.size": 12, "axes.titlesize": 12.5, "axes.labelsize": 12,
    "legend.fontsize": 11, "xtick.labelsize": 11, "ytick.labelsize": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": SUAVE,
    "axes.labelcolor": TEXTO, "xtick.color": SUAVE, "ytick.color": SUAVE, "text.color": TEXTO,
    "axes.titlecolor": NAVY, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "lines.linewidth": 2.2, "legend.frameon": False, "svg.fonttype": "none",
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
})


def guardar(fig, nombre):
    """Guarda en SVG (texto editable, para el PDF) y en PNG de 250 dpi (para PowerPoint y Google Slides)."""
    ruta = SALIDA / f"{nombre}.svg"
    fig.savefig(ruta, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(SALIDA / f"{nombre}.png", bbox_inches="tight", pad_inches=0.04, dpi=250)
    plt.close(fig)
    svg = ruta.read_text(encoding="utf-8")
    svg = re.sub(r"font-family:\s*'?DejaVu Sans'?", "font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif", svg)
    ruta.write_text(svg, encoding="utf-8")
    print("ok", ruta.name)


def normalizar_subset(tr):
    """Sensores útiles y z-score por condición con estadísticas del propio train (secciones 4.1-4.3)."""
    desv_min = tr.groupby("condicion")[SENSORES].std().min()
    utiles = [s for s in SENSORES if desv_min[s] > 1e-3]
    est = tr.groupby("condicion")[utiles].agg(["mean", "std"])
    z = tr.copy()
    for s in utiles:
        media = tr["condicion"].map(est[(s, "mean")])
        desv = tr["condicion"].map(est[(s, "std")]).replace(0, np.nan)
        z[s] = ((tr[s] - media) / desv).fillna(0)
    return z


train = pd.read_csv(DATOS / "CMAPSS-v2" / "train_todos.csv")
fd1 = train[train["subset"] == "FD001"]
fd2 = train[train["subset"] == "FD002"]
z1 = normalizar_subset(fd1).sort_values(["engine_id", "cycle"])
z2 = normalizar_subset(fd2).sort_values(["engine_id", "cycle"])

# --- Diapositiva 2: qué es la RUL (motor de train y motor de test) ---
vida = int(fd1[fd1["engine_id"] == "FD001_1"]["cycle"].max())          # 192
obs_test, rul_test = 31, 112                                           # test_FD001 motor 1 y RUL_FD001
fig, ax = plt.subplots(figsize=(5.6, 3.0))
c = np.arange(1, vida + 1)
ax.plot(c, vida - c, color=NAVY, label="Train: vuela hasta fallar")
ct = np.arange(1, obs_test + 1)
ax.plot(ct, obs_test + rul_test - ct, color=ORANGE, label="Test: se corta antes")
ax.plot([obs_test, obs_test + rul_test], [rul_test, 0], color=ORANGE, ls=":", lw=1.6)
ax.scatter([obs_test], [rul_test], color=ORANGE, zorder=3, s=36)
ax.annotate("RUL real = 112\n(la da NASA)", (obs_test, rul_test), xytext=(8, 45),
            fontsize=11, color=ORANGE, arrowprops={"arrowstyle": "-", "color": ORANGE, "lw": 1})
ax.annotate("falla", (vida, 0), xytext=(vida - 30, 38), fontsize=11, color=NAVY,
            arrowprops={"arrowstyle": "-", "color": NAVY, "lw": 1})
ax.set(xlabel="Ciclo de vuelo", ylabel="RUL (ciclos)", ylim=(-5, 200), xlim=(0, 200))
ax.legend(loc="upper right")
guardar(fig, "fig_rul")

# --- Diapositiva 3: antes y después de normalizar (FD002_1) ---
motor = fd2[fd2["engine_id"] == "FD002_1"]
motor_z = z2[z2["engine_id"] == "FD002_1"]
fig, ejes = plt.subplots(2, 2, figsize=(7.6, 4.3), sharex=True)
for fila, (s, unidad) in enumerate([("T50", "°R"), ("Ps30", "psia")]):
    a, b = ejes[fila]
    for k, (cond, g) in enumerate(motor.groupby("condicion")):
        a.scatter(g["cycle"], g[s], s=9, color=CONDICIONES[k])
    a.set_ylabel(f"{s} ({unidad})")
    b.scatter(motor_z["cycle"], motor_z[s], s=9, color="#B8C0C9")
    b.plot(motor_z["cycle"], motor_z[s].rolling(20, min_periods=1).mean(), color=ORANGE)
    b.axhline(0, color=SUAVE, lw=0.8, ls=":")
    b.set_ylabel(f"{s} (z)")
ejes[0, 0].set_title("Sin normalizar: 6 condiciones de vuelo")
ejes[0, 1].set_title("Normalizado por condición")
for ax in ejes[1]:
    ax.set_xlabel("Ciclo")
fig.tight_layout(h_pad=0.8, w_pad=1.6)
guardar(fig, "fig_normalizacion")

# --- Diapositiva 4: perfil de los sensores normalizados según el RUL y recorte a 130 ---
perfil = z1[z1["RUL"] <= 300].groupby("RUL")[["Ps30", "T50", "htBleed"]].mean()
perfil = perfil.rolling(5, center=True, min_periods=1).mean()          # suaviza el ruido de pocos motores
fig, ax = plt.subplots(figsize=(7.4, 4.2))
ax.axvspan(300, 130, color=TEAL, alpha=0.08, lw=0)
for s, col in zip(perfil.columns, [NAVY, ORANGE, TEAL]):
    ax.plot(perfil.index, perfil[s], color=col, label=s)
ax.axvline(130, color=TEXTO, ls="--", lw=1.4)
ax.text(126, 2.2, "Recorte: RUL = 130", fontsize=11.5, ha="left", color=TEXTO, fontweight="bold")
ax.text(126, 1.75, "Zona de desgaste", fontsize=11.5, ha="left", color=ORANGE)
ax.text(292, 1.0, "Zona sana: los sensores\ncasi no cambian", fontsize=11.5, color=TEAL)
ax.invert_xaxis()
ax.set(xlabel="RUL (ciclos que le quedan)", ylabel="Promedio normalizado (z)")
ax.legend(loc="lower right")
guardar(fig, "fig_recorte")

m1 = fd1[fd1["engine_id"] == "FD001_1"]
fig, ax = plt.subplots(figsize=(3.4, 2.5))
ax.plot(m1["cycle"], m1["RUL"], color=SLATE, lw=1.6, ls="--", label="RUL real")
ax.plot(m1["cycle"], m1["RUL"].clip(upper=130), color=NAVY, label="Objetivo")
ax.set(xlabel="Ciclo", ylabel="RUL", yticks=[0, 65, 130, 191])
ax.legend(loc="upper right", fontsize=10.5)
guardar(fig, "fig_objetivo")

# --- Diapositiva 5: error de validación según la ventana (Random Forest, 3 semillas) ---
ven = pd.read_csv(DATOS / "CMAPSS-v2" / "comparacion_ventanas.csv")
tabla = ven.groupby(["ventana", "subset"])["RMSE"].mean().unstack()
fig, ax = plt.subplots(figsize=(5.2, 3.3))
for s, col in SUBSETS.items():
    ax.plot(tabla.index, tabla[s], marker="o", ms=5, color=col, label=s)
ax.axvline(70, color=ORANGE, ls=":", lw=1.6)
ax.text(71.5, 31.2, "70", color=ORANGE, fontsize=11.5, fontweight="bold")
ax.set(xlabel="Ventana (ciclos hacia atrás)", ylabel="RMSE de validación (ciclos)", xticks=list(tabla.index))
ax.legend(ncol=2, loc="center right", fontsize=10.5, bbox_to_anchor=(1.0, 0.47))
guardar(fig, "fig_ventanas_rf")

# --- Diapositiva 5: atraso de la media de 70 ciclos y ventana de 10 (FD001_1, Ps30) ---
m = z1[z1["engine_id"] == "FD001_1"].copy()
m["media_70"] = m["Ps30"].rolling(70, min_periods=1).mean()
m["media_10"] = m["Ps30"].rolling(10, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(5.8, 3.3))
ax.plot(m["RUL"], m["Ps30"], color="#B8C0C9", lw=1.1, label="Lectura de cada ciclo")
ax.plot(m["RUL"], m["media_70"], color=NAVY, label="Media de 70 ciclos")
ax.plot(m["RUL"], m["media_10"], color=ORANGE, label="Media de 10 ciclos")
fin = m.iloc[-1]
ax.annotate("", xy=(-3, fin["media_70"]), xytext=(-3, fin["media_10"]),
            arrowprops={"arrowstyle": "<->", "color": TEXTO, "lw": 1.2})
ax.text(-6, (fin["media_70"] + fin["media_10"]) / 2, "atraso", fontsize=11, va="center", color=TEXTO)
ax.set_xlim(195, -22)
ax.set(xlabel="RUL (ciclos que le quedan)", ylabel="Ps30 normalizado (z)")
ax.legend(loc="upper left", fontsize=10.5)
guardar(fig, "fig_atraso")
print(f"  RUL 0: media_70 = {fin['media_70']:.2f}, media_10 = {fin['media_10']:.2f}")

# --- Diapositiva 6: RMSE de validación por modelo (ventana de 70) ---
mod = pd.read_csv(DATOS / "CMAPSS-v2" / "comparacion_modelos.csv")
prom = mod.groupby("modelo")["RMSE"].mean()
orden = ["Ridge", "kNN", "SVR", "Random Forest", "XGBoost", "LightGBM"]
prom = prom.reindex(orden)
fig, ax = plt.subplots(figsize=(5.0, 3.2))
colores = [ORANGE if n == "LightGBM" else SLATE for n in orden]
ax.barh(orden, prom.values, color=colores, height=0.62)
for y, v in enumerate(prom.values):
    ax.text(v + 0.3, y, f"{v:.2f}", va="center", fontsize=11.5,
            color=ORANGE if orden[y] == "LightGBM" else TEXTO,
            fontweight="bold" if orden[y] == "LightGBM" else "normal")
ax.invert_yaxis()
ax.set_xlim(0, 30)
ax.set_xlabel("RMSE de validación promedio (ciclos)")
guardar(fig, "fig_modelos")
print("  promedios:", prom.round(2).to_dict())

# --- Diapositiva 6: búsqueda de Optuna ---
opt = pd.read_csv(DATOS / "CMAPSS-v2" / "optuna_lightgbm.csv")
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.scatter(opt["number"], opt["value"], s=26, color=SLATE, alpha=0.8, label="Cada intento")
ax.plot(opt["number"], opt["value"].cummin(), color=ORANGE, drawstyle="steps-post", label="Mejor hasta ese intento")
ax.scatter([0], [opt["value"].iloc[0]], s=46, color=NAVY, zorder=3)
ax.annotate("base (18.95)", (0, opt["value"].iloc[0]), xytext=(1.2, 19.55), fontsize=11, color=NAVY,
            arrowprops={"arrowstyle": "-", "color": NAVY, "lw": 1})
best = opt["value"].idxmin()
ax.annotate(f"mejor ({opt['value'].min():.2f})", (opt.loc[best, "number"], opt["value"].min()),
            xytext=(17, 19.45), fontsize=11, color=ORANGE,
            arrowprops={"arrowstyle": "-", "color": ORANGE, "lw": 1})
ax.set(xlabel="Intento de Optuna", ylabel="RMSE promedio", ylim=(18.6, 20.1))
ax.legend(loc="upper right", fontsize=10.5)
guardar(fig, "fig_optuna")

# --- Diapositiva 7: prueba oficial contra trabajos públicos ---
comp = pd.DataFrame({
    "GRU + atención": [14.21, 27.99, 14.64, 26.78],
    "fleet-readiness (Chronos-2 + LightGBM)": [11.79, 23.38, 11.13, 23.86],
    "Este trabajo: LightGBM 10 + 70": [13.10, 21.55, 11.91, 23.12],
    "Este trabajo + Chronos-2": [12.66, 21.51, 11.90, 22.79],
}, index=["FD001", "FD002", "FD003", "FD004"])
cols = ["#C9CFD6", TEAL, NAVY, ORANGE]
promedios = [20.91, 17.54, 17.42, 17.22]          # promedios de la tabla del reporte (sin redondear antes)
fig, ax = plt.subplots(figsize=(6.6, 4.3))
x = np.arange(4)
w = 0.2
for k, (nombre, col) in enumerate(zip(comp.columns, cols)):
    barras = ax.bar(x + (k - 1.5) * w, comp[nombre], w * 0.95, color=col,
                    label=f"{nombre}  ·  prom. {promedios[k]:.2f}")
    if k >= 1:
        for b in barras:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4, f"{b.get_height():.1f}",
                    ha="center", fontsize=8.6, color=TEXTO, rotation=90)
ax.set_xticks(x, comp.index)
ax.set_ylabel("RMSE en prueba (ciclos)")
ax.set_ylim(0, 31)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), fontsize=10.5, ncol=1)
guardar(fig, "fig_kaggle")

# --- Diapositiva 8: importancia por permutación (P2) ---
p2 = pd.DataFrame({
    "sensor": ["Ps30", "ciclo", "T50", "Nc", "NRc", "BPR"],
    "media": [6.40, 5.03, 2.62, 1.88, 1.51, 1.30],
    "desv": [2.68, 1.54, 0.80, 1.14, 0.92, 1.03],
    "top5": [20, 20, 19, 12, 11, 8],
}).iloc[::-1]
fig, ax = plt.subplots(figsize=(3.9, 2.5))
ax.barh(p2["sensor"], p2["media"], xerr=p2["desv"], color=NAVY,
        height=0.6, error_kw={"elinewidth": 1, "capsize": 2, "ecolor": SUAVE})
for y, (m_, d_, t) in enumerate(zip(p2["media"], p2["desv"], p2["top5"])):
    ax.text(m_ + d_ + 0.25, y, f"{t}/20", fontsize=10, va="center", color=SUAVE)
ax.set_xlim(0, 11)
ax.set_xlabel("Aumento del RMSE al revolverlo")
guardar(fig, "fig_permutacion")

# --- Diapositiva 8: cuánto redujo el error cada paso ---
pasos = pd.DataFrame({
    "paso": ["Normalizar por condición", "Ventana de 70 ciclos", "Random Forest a LightGBM",
             "Ventana extra de 10", "Chronos-2", "Optuna"],
    "mejora": [30.54 - 25.20, 25.69 - 20.16, 20.15 - 19.17, 19.17 - 18.95, 18.73 - 18.54, 18.94 - 18.78],
    "tipo": ["datos", "datos", "modelo", "datos", "modelo", "modelo"],
}).iloc[::-1]
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.barh(pasos["paso"], pasos["mejora"], color=[TEAL if t == "datos" else SLATE for t in pasos["tipo"]], height=0.62)
for y, v in enumerate(pasos["mejora"]):
    ax.text(v + 0.1, y, f"−{v:.2f}", va="center", fontsize=10.5, color=TEXTO)
ax.set_xlim(0, 6.6)
ax.set_xlabel("Reducción del RMSE de validación (ciclos)")
guardar(fig, "fig_aporte")
