"""Vuelve a guardar las figuras del notebook Proyecto-CMAPSS-v2.ipynb con letra más grande para la presentación.

Cada bloque copia el código de graficado de su celda del notebook (mismos datos, colores y títulos) y solo
cambia el tamaño de la figura y de la letra para que se lea en una diapositiva. Los datos salen de los
CSV que guardó el notebook (CMAPSSData/CMAPSS-v2) y de las tablas que imprimió (P1, P2 y P3).
Las figuras originales de Images/ no se tocan; las nuevas quedan en Presentacion/figuras_notebook/.

Uso (desde la carpeta Proyecto):  py Presentacion/figuras/reexportar_figuras_notebook.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]                  # carpeta Proyecto
V2 = RAIZ / "CMAPSSData" / "CMAPSS-v2"
SALIDA = RAIZ / "Presentacion" / "figuras_notebook"
SALIDA.mkdir(exist_ok=True)

Subsets = ["FD001", "FD002", "FD003", "FD004"]
SENSORES = ["T2", "T24", "T30", "T50", "P2", "P15", "P30", "Nf", "Nc", "epr", "Ps30", "phi",
            "NRf", "NRc", "BPR", "farB", "htBleed", "Nf_dmd", "PCNfR_dmd", "W31", "W32"]

# Igual que el notebook, con la letra más grande
plt.rcParams.update({
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 10.5,
})


def guardar_figura(nombre):
    """Como guardar_figura del notebook, pero en Presentacion/figuras_notebook y a 200 dpi."""
    plt.savefig(SALIDA / f"{nombre}.png", dpi=200, bbox_inches="tight")
    plt.close("all")
    print("ok", nombre)


def normalizar_por_condicion(tr):
    """Secciones 4.1-4.3: sensores útiles y z-score por condición con estadísticas de train."""
    desv_min = tr.groupby("condicion")[SENSORES].std().min()
    utiles = [s for s in SENSORES if desv_min[s] > 1e-3]
    est = tr.groupby("condicion")[utiles].agg(["mean", "std"])
    z = tr.copy()
    for s in utiles:
        media = tr["condicion"].map(est[(s, "mean")])
        desv = tr["condicion"].map(est[(s, "std")]).replace(0, np.nan)
        z[s] = ((tr[s] - media) / desv).fillna(0)
    return z


train = pd.read_csv(V2 / "train_todos.csv")
test = pd.read_csv(V2 / "test_todos.csv")
train_n = pd.concat([normalizar_por_condicion(train[train["subset"] == fd]) for fd in Subsets])

# ---------- Figura 02 (sección 3.2) ----------
vida = train.groupby(["subset", "engine_id"])["cycle"].max()
observados = test.groupby(["subset", "engine_id"])["cycle"].max()
bordes = np.arange(0, vida.max() + 20, 20)
descripcion = {"FD001": "1 condición · 1 falla", "FD002": "6 condiciones · 1 falla",
               "FD003": "1 condición · 2 fallas", "FD004": "6 condiciones · 2 fallas"}
fig, ejes = plt.subplots(2, 2, figsize=(9.2, 5.3), sharex=True)
for ax, fd in zip(ejes.flat, Subsets):
    v = vida[fd]
    ax.hist(v, bins=bordes, color="purple", alpha=0.75, edgecolor="white", label="Vida en train")
    ax.hist(observados[fd], bins=bordes, histtype="step", color="darkorange", lw=2,
            label="Ciclos observados en test")
    ax.axvline(v.median(), color="black", ls="--", lw=1.5, label="Mediana de train")
    ax.set_title(f"{fd} ({descripcion[fd]}) · {len(v)} motores", fontsize=11.5)
for ax in ejes[1]:
    ax.set_xlabel("Ciclos")
for ax in ejes[:, 0]:
    ax.set_ylabel("Motores")
ejes[0, 1].legend(loc="upper right", fontsize=10)
plt.tight_layout()
guardar_figura("Figura 02 - Vida de los motores en train y ciclos observados en test")

# ---------- Figura 04 (sección 4.5) ----------
fd = "FD001"
datos_fd = train_n[(train_n["subset"] == fd) & (train_n["RUL"] <= 300)]
perfil = datos_fd.groupby("RUL")[["Ps30", "T50", "htBleed"]].mean()
fig, ax = plt.subplots(figsize=(10, 3.9))
for s in perfil.columns:
    ax.plot(perfil.index, perfil[s].rolling(5, center=True, min_periods=1).mean(), lw=2.2, label=s)
ax.axvline(130, color="gray", ls="--", label="Recorte (130)")
ax.axvspan(300, 130, color="green", alpha=0.06, label="Zona sana")
ax.set(xlabel="RUL", ylabel="Valor normalizado\npromedio (z)", title=f"{fd}: promedio de los motores según su RUL")
ax.invert_xaxis()
ax.legend(loc="upper left", ncol=1)
plt.tight_layout()
guardar_figura("Figura 04 - Perfil de los sensores según el RUL en FD001")

# ---------- Figura 05 (sección 4.6) ----------
motor = train[train["engine_id"] == "FD002_1"]
motor_n = train_n[train_n["engine_id"] == "FD002_1"]
sensores_grafica = ["Ps30", "T50", "BPR", "htBleed"]
# En horizontal para la diapositiva: arriba sin normalizar, abajo normalizado; una columna por sensor
fig, ejes = plt.subplots(2, len(sensores_grafica), figsize=(13, 4.5), sharex=True)
for col, s in enumerate(sensores_grafica):
    ax1, ax2 = ejes[0, col], ejes[1, col]
    for cond, grupo in motor.groupby("condicion"):
        ax1.scatter(grupo["cycle"], grupo[s], s=10, label=cond)
    ax1.set_title(f"{s} sin normalizar", fontsize=12.5)
    ax2.scatter(motor_n["cycle"], motor_n[s], s=10, color="gray", alpha=0.6)
    ax2.plot(motor_n["cycle"], motor_n[s].rolling(20, min_periods=1).mean(), color="purple", lw=2.2)
    ax2.set_title(f"{s} normalizado", fontsize=12.5)
    ax2.set_xlabel("Ciclo")
ejes[0, 0].set_ylabel("Valor del sensor")
ejes[1, 0].set_ylabel("z")
fig.legend(*ejes[0, 0].get_legend_handles_labels(), title="Condición de vuelo (altitud_Mach_acelerador)",
           loc="upper center", bbox_to_anchor=(0.5, 1.09), ncol=6, fontsize=10.5, title_fontsize=10.5,
           frameon=False, markerscale=1.6)
plt.tight_layout()
guardar_figura("Figura 05 - Motor FD002_1 antes y después de normalizar")

# ---------- Figura 09 (sección 7.3) ----------
ven = pd.read_csv(V2 / "comparacion_ventanas.csv")
tabla = ven.groupby(["ventana", "subset"])["RMSE"].mean().unstack()
ventana_elegida = 70
fig, ax = plt.subplots(figsize=(6.6, 3.8))
for fd in Subsets:
    ax.plot(tabla.index, tabla[fd], marker="o", lw=2, label=fd)
    rmse_elegida = tabla.loc[ventana_elegida, fd]
    abajo = fd in ("FD001", "FD002")                # FD001 y FD003 casi coinciden en 70: una arriba y otra abajo
    ax.annotate(f"{rmse_elegida:.1f}", (ventana_elegida, rmse_elegida),
                textcoords="offset points", xytext=(6, -14 if abajo else 6), fontsize=10.5)
ax.axvline(ventana_elegida, color="crimson", ls=":", lw=1.5, label=f"Ventana elegida: {ventana_elegida}")
ax.set(xlabel="Ventana (ciclos)", ylabel="RMSE de validación (ciclos)",
       title="Error de validación según la ventana")
ax.set_xticks(tabla.index)
ax.legend(loc="center", bbox_to_anchor=(0.6, 0.47), fontsize=10, ncol=3, columnspacing=1.0)
plt.tight_layout()
guardar_figura("Figura 09 - Error de validación según la ventana")

# ---------- Figura 10 (sección 8.3) ----------
res = pd.read_csv(V2 / "comparacion_modelos.csv")
orden = list(dict.fromkeys(res["modelo"]))
tabla_rmse = res.pivot(index="modelo", columns="subset", values="RMSE").loc[orden]
ax = tabla_rmse.drop(index="Promedio").plot.bar(figsize=(7.4, 3.8), rot=0, width=0.8)
ax.set(xlabel="", ylabel="RMSE de validación (ciclos)", title="Error de validación por modelo y subconjunto")
ax.set_xticklabels(["Ridge", "kNN", "SVR", "Random\nForest", "XGBoost", "LightGBM"])
ax.legend(title="subset", ncol=4, loc="upper right", fontsize=10, title_fontsize=10)
ax.set_ylim(0, 40)
plt.tight_layout()
guardar_figura("Figura 10 - Error de validación por modelo")

# ---------- Figura 11 (sección 9.3) ----------
historial = pd.read_csv(V2 / "optuna_lightgbm.csv")[["number", "value"]]
fig, ax = plt.subplots(figsize=(7.6, 3.5))
ax.plot(historial["number"], historial["value"], "o", alpha=0.6, label="RMSE de cada intento")
ax.plot(historial["number"], historial["value"].cummin(), color="crimson", lw=2.2, label="Mejor hasta ese intento")
ax.set(xlabel="Intento de Optuna", ylabel="RMSE promedio de\nvalidación (ciclos)",
       title="Búsqueda de hiperparámetros de LightGBM con Optuna")
ax.legend()
plt.tight_layout()
guardar_figura("Figura 11 - Búsqueda de hiperparámetros con Optuna")

# ---------- Figura 9.2 b) (sección 9.2 b) ----------
d1 = train_n[train_n["subset"] == "FD001"].sort_values(["engine_id", "cycle"])
m = d1[d1["engine_id"] == "FD001_1"]
y_m = m["RUL"]
valor = m["Ps30"]
media_70 = valor.rolling(70, min_periods=1).mean()
media_10 = valor.rolling(10, min_periods=1).mean()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.3))
ax1.plot(y_m, valor, color="gray", alpha=0.5, label="Valor del ciclo")
ax1.plot(y_m, media_70, color="purple", lw=2.2, label="Media de 70 ciclos")
ax1.plot(y_m, media_10, color="darkorange", lw=2.2, label="Media de 10 ciclos")
ax1.set(xlabel="RUL", ylabel="Ps30 (z)", title="FD001_1 · Ps30: ventana de 10 contra 70")
ax1.invert_xaxis()
ax1.legend(fontsize=10)
ax2.plot(y_m, media_10 - media_70, color="crimson", lw=2.2)
ax2.axhline(0, color="gray", lw=1)
ax2.set(xlabel="RUL", ylabel="media_10 − media_70 (z)", title="Diferencia entre las dos medias")
ax2.invert_xaxis()
plt.tight_layout()
guardar_figura("Figura 9.2b - Ventana de 10 contra 70 en Ps30")
print(f"  RUL 0: media_70 = {media_70.iloc[-1]:.2f}, media_10 = {media_10.iloc[-1]:.2f}")

# ---------- Figura 12 (sección 9.7) ----------
pred = pd.read_csv(RAIZ / "Predicciones" / "predicciones_test_v2.csv")
RUL_TOPE = 130
fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.6), sharex=True, sharey=True)
for ax, (fd, df_p) in zip(axes.ravel(), pred.groupby("subset")):
    rmse_fd = np.sqrt(np.mean((df_p["RUL_predicho"] - df_p["RUL_real"]) ** 2))
    ax.scatter(df_p["RUL_real"], df_p["RUL_predicho"], s=15, alpha=0.6)
    ax.plot([0, 200], [0, 200], color="gray", ls="--", label="Predicción perfecta")
    ax.axhline(RUL_TOPE, color="crimson", ls=":", label=f"Recorte ({RUL_TOPE})")
    ax.set_title(f"{fd} · RMSE {rmse_fd:.1f}")
# El motor de test FD001_1 (31 ciclos observados), el ejemplo de la presentación
ej = pred[pred["engine_id"] == "FD001_1"].iloc[0]
axes[0, 0].scatter([ej["RUL_real"]], [ej["RUL_predicho"]], s=70, facecolor="none", edgecolor="black", lw=1.5)
axes[0, 0].annotate("FD001_1: 31 ciclos,\nreal 112, predicho 127.5", (ej["RUL_real"], ej["RUL_predicho"]),
                    xytext=(5, 168), fontsize=10, arrowprops={"arrowstyle": "-", "color": "black", "lw": 0.8})
for ax in axes[1]:
    ax.set_xlabel("RUL real (ciclos)")
for ax in axes[:, 0]:
    ax.set_ylabel("RUL predicho (ciclos)")
axes[1, 1].legend(loc="lower right", fontsize=10)
plt.tight_layout()
guardar_figura("Figura 12 - RUL predicho contra RUL real en test")

# ---------- Figura 15 (sección 10.1), con la tabla tabla_p1 que imprimió el notebook ----------
tabla_p1 = pd.DataFrame({
    "Random Forest, 1 ciclo (Kaggle [2])": {"FD001": 17.96},
    "LSTM, 30 ciclos (Kaggle [4])": {"FD001": 15.30},
    "Chronos-2 + LightGBM (Kaggle, fleet-readiness [5])": {"FD001": 11.79, "FD002": 23.38, "FD003": 11.13, "FD004": 23.86},
    "LightGBM 10 + 70, Optuna (este proyecto)": {"FD001": 13.10, "FD002": 21.55, "FD003": 11.91, "FD004": 23.12},
    "LightGBM 10 + 70, Optuna + Chronos-2 (este proyecto)": {"FD001": 12.66, "FD002": 21.51, "FD003": 11.90, "FD004": 22.79},
}).T[Subsets]
ax = tabla_p1[Subsets].T.plot.bar(figsize=(9.0, 4.6), rot=0, width=0.8)
ax.set(xlabel="", ylabel="RMSE de test contra\nel RUL real (ciclos)",
       title="P1: este proyecto contra los notebooks de Kaggle (protocolo oficial)")
ax.legend(fontsize=9.5, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)
plt.tight_layout()
guardar_figura("Figura 15 - P1 comparación con los notebooks de Kaggle")

# ---------- Figura 16 (sección 10.2), con la tabla tabla_p2 que imprimió el notebook ----------
tabla_p2 = pd.DataFrame({
    "sensor": ["Ps30", "cycle", "T50", "Nc", "NRc", "BPR", "phi", "htBleed", "T30", "NRf", "T24", "P30", "Nf", "W32", "W31", "P15", "epr"],
    "Promedio": [6.40, 5.03, 2.62, 1.88, 1.51, 1.30, 1.19, 1.08, 1.01, 0.60, 0.58, 0.42, 0.36, 0.28, 0.23, 0.07, 0.01],
    "± entre pliegues": [2.68, 1.54, 0.80, 1.14, 0.92, 1.03, 0.93, 0.48, 0.62, 0.32, 0.30, 0.29, 0.27, 0.25, 0.39, 0.10, 0.04],
}).set_index("sensor")
fig, ax = plt.subplots(figsize=(6.4, 4.2))
orden_p2 = tabla_p2.index[::-1]
ax.barh(orden_p2, tabla_p2.loc[orden_p2, "Promedio"], xerr=tabla_p2.loc[orden_p2, "± entre pliegues"],
        color="purple", alpha=0.8, capsize=3)
ax.set(xlabel="Aumento del RMSE al revolver el sensor (ciclos)", ylabel="",
       title="P2: importancia por permutación (5 pliegues × 4 subconjuntos)")
ax.title.set_fontsize(11.5)
ax.tick_params(axis="y", labelsize=10)
plt.tight_layout()
guardar_figura("Figura 16 - P2 importancia por permutación")

# ---------- Figura 17 (sección 10.3), con la tabla tabla_p3 que imprimió el notebook ----------
tabla_p3 = pd.DataFrame({
    "Validación (FD002 y FD004)": [30.54, 30.54, 25.20],
    "Test (FD002 y FD004)": [26.96, 26.96, 22.34],
}, index=["Sin normalizar\npor condición", "Sin normalizar + condición\ncomo columna", "Normalizado por condición\n(este proyecto)"])
fig, ax = plt.subplots(figsize=(7.8, 3.3))
tabla_p3.plot.barh(ax=ax, color=["steelblue", "darkorange"])
ax.set(xlabel="RMSE contra el RUL real (ciclos)", ylabel="",
       title="P3: el mismo LightGBM con y sin normalización por condición")
ax.title.set_fontsize(12)
ax.invert_yaxis()
ax.set_xlim(0, 40)
ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.22), fontsize=10, ncol=2, frameon=False)
plt.tight_layout()
guardar_figura("Figura 17 - P3 con y sin normalización por condición")
