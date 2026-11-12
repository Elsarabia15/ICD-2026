# Ensambles de clasificadores

Práctica 4 de Introducción a la Ciencia de Datos (Posgrado en Ciencias de la Computación, CICESE).
Mide cuánto ganan los ensambles sobre los cinco clasificadores base de la Práctica 3 (árbol de
decisión, Naive Bayes, kNN, SVM y regresión logística) cuando estos ya están bien ajustados, y
busca el mejor modelo para otro conjunto de datos: Bank Marketing.

## Descripción de los datasets

**Deserción estudiantil** (Predict Students' Dropout and Academic Success)

- **Autores:** V. Realinho, M. Vieira Martins, J. Machado y L. Baptista
- **Fuente:** [UCI Machine Learning Repository](https://doi.org/10.24432/C5MC89)
- **Tamaño:** 3539 estudiantes con `Target` y 30 atributos conocidos al cierre del 1er semestre
  (49.9 % *graduate*, 32.1 % *dropout* y 17.9 % *enrolled*).

**Bank Marketing** (`bank-additional-full.csv`)

- **Autores:** S. Moro, P. Cortez y P. Rita
- **Procedencia:** llamadas de telemarketing de un banco portugués, de mayo de 2008 a noviembre de 2010.
- **Tamaño:** 41 188 llamadas y 19 atributos, sin `duration`, que solo se conoce al terminar la
  llamada (88.7 % *no* y 11.3 % *yes*).

## Estructura del repositorio

```
.
├── Practica-IV.ipynb            # notebook principal
├── Carlos-Campos_modelo.joblib  # mejor modelo de Bank Marketing, entrenado con todos los datos
├── Images/                      # figuras generadas por el notebook (PNG)
├── requirements.txt             # dependencias de Python
└── README.md
```

Los datos están en el repositorio, fuera de la carpeta del proyecto, en [Datos](../../Datos/). El
notebook los lee con la ruta relativa `../../Datos/`, así que debe ejecutarse desde
`Practicas/Practica-4/`.

## Contenido del notebook

1. **Configuración y carga de datos:** librerías, estilo, pliegues y los cinco clasificadores base,
   con la comprobación de que reproducen el F1 de la Práctica 3.
2. **Varianza:** árbol sin límite y bagging, con su curva hasta 400 árboles y una medición directa
   del desacuerdo entre réplicas.
3. **Sesgo:** tocón y AdaBoost, con su curva hasta 400 rondas.
4. **Combinar los cinco base:** votación dura, votación suave, stacking y correlación de los errores.
5. **Bagging optimizado:** Random Forest y Extra-Trees.
6. **Boosting optimizado:** XGBoost y LightGBM.
7. **Comparación de todos los modelos:** tabla, ganancia por pares y matriz de confusión.
8. **Bank Marketing:** modelo transferido, preprocesamiento, balanceo, modelos base, optimización,
   combinaciones, tabla, matriz de confusión, verificación con la llamada del enunciado, modelo
   guardado y comparación con deserción.
9. **Conclusiones.**
10. **Referencias** (APA 7).
11. **Declaración de uso de IA.**

## Requisitos de ejecución

- **Python** ≥ 3.11 (probado con Python 3.14).
- **Librerías necesarias** (ver `requirements.txt`): pandas, numpy, scipy, matplotlib, seaborn,
  scikit-learn ≥ 1.8, xgboost, lightgbm, imbalanced-learn, joblib y jupyter.

```bash
pip install -r requirements.txt
jupyter notebook Practica-IV.ipynb
```

La ejecución completa tardó unos 25 minutos en una computadora de 16 núcleos, casi todo en Bank
Marketing. Los F1 son reproducibles: las semillas (`SEED = 67` y `SEED_BANCO = 2026`) fijan los
pliegues, las búsquedas y los modelos. Los tiempos dependen de la carga de la computadora. Al
ejecutarse, el notebook guarda cada gráfica en `Images/`, con un nombre que empieza con el número
de la sección donde se genera.

## Uso del modelo guardado

`Carlos-Campos_modelo.joblib` es el pipeline completo (preprocesamiento y LightGBM con peso 1:3),
entrenado con las 41 188 llamadas. Recibe las columnas del CSV sin `duration` ni `y`, y predice
1 (`yes`) o 0 (`no`). Solo depende de scikit-learn y LightGBM:

```python
import joblib
import pandas as pd

modelo = joblib.load("Carlos-Campos_modelo.joblib")
X = pd.read_csv("../../Datos/Bank Marketing/bank-additional-full.csv", sep=";").drop(columns=["duration", "y"])
prediccion = modelo.predict(X)             # 1 = yes, 0 = no
probabilidad = modelo.predict_proba(X)[:, 1]
```

El notebook lo vuelve a generar en la sección 8.8. Todo lo que se ajusta con datos va dentro del
pipeline, y su F1 macro se verifica con
`cross_validate(modelo, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=2026), scoring="f1_macro")`.

## Resultados principales

**Deserción estudiantil** (los cinco mejores de 18 modelos)

| Modelo | F1 macro | Sensibilidad *enrolled* |
|---|---|---|
| **XGBoost** | **0.6991 ± 0.0234** | 0.498 |
| LightGBM | 0.6891 ± 0.0134 | 0.583 |
| Stacking (meta con `balanced`) | 0.6872 ± 0.0167 | 0.594 |
| Regresión logística (base) | 0.6854 ± 0.0185 | 0.581 |
| Random Forest | 0.6835 ± 0.0144 | 0.535 |

**Bank Marketing** (los cinco mejores de 34 modelos)

| Modelo | F1 macro | Sensibilidad *yes* |
|---|---|---|
| **LightGBM (peso 1:3)** | **0.7200 ± 0.0061** | 0.537 |
| Random Forest (peso 1:3) | 0.7198 ± 0.0053 | 0.536 |
| Votación suave RF + XGBoost + LightGBM con umbral | 0.7196 ± 0.0068 | 0.536 |
| Random Forest (500 árboles) | 0.7195 ± 0.0054 | 0.536 |
| LightGBM + umbral | 0.7193 ± 0.0066 | 0.546 |

- **Los ensambles ganan poco sobre modelos bien ajustados:** +0.014 ± 0.012 de F1 macro en deserción
  (un máximo aislado entre 60 configuraciones) y +0.012 en el banco, contra la logística con umbral.
- **Bagging reduce la varianza:** el desacuerdo entre réplicas baja de 33.7 % a 9.6 %.
- **Boosting reduce el sesgo:** los tocones pasan de 0.492 a 0.631 en validación y de 0.492 a 0.657
  en entrenamiento.
- **Combinar casi no ayuda:** los errores de los cinco modelos tienen una correlación media de 0.54,
  y los cinco fallan juntos en el 12 % de los estudiantes.
- **Calibrar el SVM deshace buena parte de `class_weight`:** su sensibilidad de *enrolled* baja de
  0.581 a 0.307.
- **En Bank Marketing, lo que más importó fue la decisión:** un umbral o un peso moderado (1:3) le
  ganan a `balanced`, y SMOTE no ayudó. Los mejores modelos quedan empatados en ≈ 0.720.

El detalle de cada decisión, las figuras y las limitaciones se encuentran en el notebook.
