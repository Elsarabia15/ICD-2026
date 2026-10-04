# Procesamiento de datasets: Síndrome de Ovario Poliquístico (PCOS)

Práctica 2 de Introducción a la Ciencia de Datos (Posgrado en Ciencias de la Computación, CICESE).
Continúa el trabajo de la Práctica 1 sobre PCOS, pero con un dataset distinto, e incluye
detección y corrección de problemas de calidad, EDA sobre los datos limpios y reducción de
dimensionalidad (PCA y t-SNE).

## Descripción del dataset

- **Dataset:** PCOS Clinical Dataset
- **Autor:** Michael Mendiola Sy
- **Fuente:** [Kaggle](https://www.kaggle.com/datasets/michaelmendiolasy/pcos-clinical-dataset)
- **Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Fecha de acceso:** 29 de septiembre de 2026
- **Procedencia:** datos de ensayos y estudios clínicos realizados en Filipinas, sin nombres
  de pacientes, publicados con fines educativos y de investigación.
- **Qué mide:** datos generales y antropométricos (edad, peso, altura, IMC, cintura, cadera),
  signos vitales, perfil hormonal y de laboratorio (FSH, LH, AMH, PRL, TSH, PRG, Vit D3, RBS,
  entre otras), hallazgos ecográficos (número y tamaño de folículos por ovario, endometrio),
  características del ciclo menstrual y síntomas o hábitos (aumento de peso, crecimiento de
  vello, oscurecimiento de piel, acné, caída de cabello, comida rápida, ejercicio).
- **Unidad de observación:** cada fila representa **una paciente**.
- **Tamaño:** 541 filas × 43 columnas. Variable objetivo: `PCOS (Y/N)` (0 = sin PCOS, 1 = con PCOS),
  con 364 pacientes sin PCOS (67.3%) y 177 con PCOS (32.7%), un desbalance leve.
- **Archivo esperado:** `data without infertility _final.csv`

## Estructura del repositorio

```
.
├── Practica-II.ipynb       # notebook principal: limpieza, EDA y reducción de dimensionalidad
├── Images/                 # figuras generadas por el notebook (Figura 1 a 10, PNG)
├── requirements.txt        # dependencias de Python
└── README.md
```

El dataset (`data without infertility _final.csv`) está incluido en el repositorio, pero en una
carpeta fuera de la carpeta del proyecto: [Datos](../../Datos/). El notebook lo lee con la ruta
relativa `../../Datos/data without infertility _final.csv`, así que debe ejecutarse desde
`Practicas/Practica-2/`.

## Contenido del notebook

1. **Carga de datos y librerías.**
2. **EDA inicial:** estructura general, calidad de los datos (faltantes, duplicados, tipos,
   categorías inválidas, verificación de `BMI`, `Waist:Hip Ratio` y `FSH/LH`) y balance de la
   variable objetivo.
3. **Limpieza de datos:** eliminación de columnas sin aporte, corrección de tipos y valores
   inválidos, conversión de pulgadas a cm, tratamiento de outliers imposibles (FSH, LH, Vit D3),
   recálculo de variables compuestas e imputación de faltantes. El dataset queda en
   541 filas × 35 columnas, sin eliminar ninguna paciente.
4. **EDA sobre datos limpios:** análisis univariado, bivariado contra PCOS y correlaciones de
   Spearman (matriz completa, por bloques temáticos y con la variable objetivo).
5. **Reducción de dimensionalidad:** PCA y t-SNE sobre el perfil hormonal
   (transformación `log1p` + `StandardScaler`).
6. **Conclusiones y referencias** (APA 7).

## Requisitos de ejecución

- **Python** ≥ 3.9
- **Librerías necesarias** (ver `requirements.txt`): pandas, numpy, matplotlib, seaborn,
  scikit-learn y jupyter.

```bash
pip install -r requirements.txt
jupyter notebook Practica-II.ipynb
```

## Hallazgos principales

- El diagnóstico de PCOS se explica mejor por hallazgos **ecográficos y clínicos** que por el
  perfil hormonal: las variables más correlacionadas son el número de folículos
  (r = 0.63 y 0.58), el crecimiento de vello (r = 0.46) y la irregularidad del ciclo (r = 0.40),
  que corresponden a los criterios de Rotterdam.
- El oscurecimiento de piel (r = 0.48) y el aumento de peso (r = 0.44) destacan como señales
  visibles asociadas a resistencia a la insulina.
- La **AMH** es la única hormona con relación apreciable (r = 0.24), ya que funciona como
  indicador indirecto del número de folículos.
- **PCA y t-SNE** sobre las hormonas no separan a las pacientes con y sin PCOS: se necesitan
  6 de 7 componentes para explicar el 80% de la varianza y ambas clases aparecen mezcladas.
- **Limitación:** el dataset no incluye testosterona ni otros andrógenos, por lo que el análisis
  hormonal está incompleto respecto al criterio de hiperandrogenismo bioquímico.

El detalle de cada decisión de limpieza, las figuras y la discusión con referencias se
encuentran en el notebook.


