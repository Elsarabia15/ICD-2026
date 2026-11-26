"""Figuras compactas (ancho de columna IEEE) para el reporte del proyecto C-MAPSS v2.

Reproduce el preprocesamiento del notebook (secciones 2.4, 4.1-4.3 y 5.2) sobre
CMAPSSData/CMAPSS-v2/train_todos.csv y genera:
  - fig_normalizacion.pdf: T50 del motor FD002_1 antes y después de normalizar por condición.
  - fig_ventanas.pdf: Ps30 del motor FD001_1 con las medias de 10 y 70 ciclos y su diferencia.

Uso (desde la carpeta Proyecto):  py Reporte/figuras/generar_figuras.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]          # carpeta Proyecto
SALIDA = Path(__file__).resolve().parent
SENSORES = ["T2", "T24", "T30", "T50", "P2", "P15", "P30", "Nf", "Nc", "epr", "Ps30", "phi",
            "NRf", "NRc", "BPR", "farB", "htBleed", "Nf_dmd", "PCNfR_dmd", "W31", "W32"]
ANCHO = 3.5  # pulgadas, una columna IEEE

plt.rcParams.update({
    "font.family": "serif", "font.size": 7.5, "axes.titlesize": 7.5, "axes.labelsize": 7.5,
    "legend.fontsize": 6.2, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.2,
})

train = pd.read_csv(RAIZ / "CMAPSSData" / "CMAPSS-v2" / "train_todos.csv")


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


# --- Figura: antes y después de normalizar (FD002_1, T50) ---
fd2 = train[train["subset"] == "FD002"]
z2 = normalizar_subset(fd2)
motor = fd2[fd2["engine_id"] == "FD002_1"]
motor_z = z2[z2["engine_id"] == "FD002_1"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(ANCHO, 1.55))
for cond, g in motor.groupby("condicion"):
    ax1.scatter(g["cycle"], g["T50"], s=3)
ax1.set(xlabel="Ciclo", ylabel="T50 (°R)", title="Sin normalizar")
ax2.scatter(motor_z["cycle"], motor_z["T50"], s=3, color="0.65")
ax2.plot(motor_z["cycle"], motor_z["T50"].rolling(20, min_periods=1).mean(), color="purple")
ax2.axhline(0, color="black", lw=0.5, ls=":")
ax2.set(xlabel="Ciclo", ylabel="T50 (z)", title="Normalizado")
fig.tight_layout(pad=0.3, w_pad=0.8)
fig.savefig(SALIDA / "fig_normalizacion.pdf")
plt.close(fig)

# --- Figura: medias de 10 y 70 ciclos (FD001_1, Ps30) ---
fd1 = train[train["subset"] == "FD001"]
z1 = normalizar_subset(fd1).sort_values(["engine_id", "cycle"])
m = z1[z1["engine_id"] == "FD001_1"].copy()
m["media_70"] = m["Ps30"].rolling(70, min_periods=1).mean()
m["media_10"] = m["Ps30"].rolling(10, min_periods=1).mean()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(ANCHO, 1.55), gridspec_kw={"width_ratios": [1.35, 1]})
ax1.plot(m["RUL"], m["Ps30"], color="0.7", lw=0.7, label="Valor del ciclo")
ax1.plot(m["RUL"], m["media_70"], color="purple", label="Media 70")
ax1.plot(m["RUL"], m["media_10"], color="darkorange", label="Media 10")
ax1.set(xlabel="RUL (ciclos)", ylabel="Ps30 (z)")
ax1.invert_xaxis()
ax1.legend(loc="upper left", frameon=False)
ax2.plot(m["RUL"], m["media_10"] - m["media_70"], color="crimson")
ax2.axhline(0, color="0.5", lw=0.6)
ax2.set(xlabel="RUL (ciclos)", ylabel="media 10 − media 70")
ax2.invert_xaxis()
fig.tight_layout(pad=0.3, w_pad=0.8)
fig.savefig(SALIDA / "fig_ventanas.pdf")
plt.close(fig)

# --- Figura: RUL predicho contra real en test (sección 9.7) ---
pred = pd.read_csv(RAIZ / "Predicciones" / "predicciones_test_v2.csv")
fig, ejes = plt.subplots(2, 2, figsize=(ANCHO, 3.0), sharex=True, sharey=True)
for ax, (fd, g) in zip(ejes.flat, pred.groupby("subset")):
    rmse = np.sqrt(np.mean((g["RUL_predicho"] - g["RUL_real"]) ** 2))
    ax.scatter(g["RUL_real"], g["RUL_predicho"], s=4, alpha=0.6)
    ax.plot([0, 200], [0, 200], color="0.4", ls="--", lw=0.8)
    ax.axhline(130, color="crimson", ls=":", lw=0.8)
    ax.set_title(f"{fd} · RMSE {rmse:.1f}")
for ax in ejes[1]:
    ax.set_xlabel("RUL real (ciclos)")
for ax in ejes[:, 0]:
    ax.set_ylabel("RUL predicho")
fig.tight_layout(pad=0.3, h_pad=0.6, w_pad=0.6)
fig.savefig(SALIDA / "fig_dispersion.pdf")
plt.close(fig)

# --- Figura: importancia por permutación (sección 10.2) ---
# Aumento medio del RMSE al revolver cada sensor y su desviación entre los 20 pliegues
# (5 pliegues x 4 subconjuntos), copiados de la salida de la tabla tabla_p2 del notebook.
p2 = pd.DataFrame({
    "sensor": ["Ps30", "cycle", "T50", "Nc", "NRc", "BPR", "phi", "htBleed", "T30", "NRf"],
    "media": [6.40, 5.03, 2.62, 1.88, 1.51, 1.30, 1.19, 1.08, 1.01, 0.60],
    "desv": [2.68, 1.54, 0.80, 1.14, 0.92, 1.03, 0.93, 0.48, 0.62, 0.32],
    "top5": [20, 20, 19, 12, 11, 8, 4, 1, 3, 1],
}).iloc[::-1]
fig, ax = plt.subplots(figsize=(ANCHO, 1.9))
ax.barh(p2["sensor"], p2["media"], xerr=p2["desv"], color="purple", alpha=0.8,
        error_kw={"elinewidth": 0.7, "capsize": 1.5})
for y, (m_, d_, t) in enumerate(zip(p2["media"], p2["desv"], p2["top5"])):
    ax.text(m_ + d_ + 0.2, y, f"{t}/20", fontsize=5.8, va="center", color="0.25")
ax.set_xlim(0, 10.2)
ax.set_xlabel("Aumento del RMSE al revolver el sensor (ciclos)")
fig.tight_layout(pad=0.3)
fig.savefig(SALIDA / "fig_permutacion.pdf")
plt.close(fig)

# Comprobación contra la tabla de la sección 9.2 b)
for r in [130, 75, 50, 25, 10, 0]:
    fila = m[m["RUL"] == r].iloc[0]
    print(f"RUL {r:>3}: media_70 = {fila['media_70']:.2f}, media_10 = {fila['media_10']:.2f}")
