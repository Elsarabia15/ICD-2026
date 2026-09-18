# Análisis Exploratorio de Datos: Síndrome de Ovario Poliquístico (PCOS)

## Descripción del dataset

Este proyecto realiza un análisis exploratorio de datos (EDA) sobre un dataset clínico
relacionado con el Síndrome de Ovario Poliquístico (PCOS), un trastorno endocrino-metabólico
que afecta a mujeres en edad reproductiva.

- **Qué mide:** variables antropométricas (edad, peso, altura, IMC), signos vitales,
  perfil hormonal (FSH, LH, AMH, TSH, PRL, entre otras), hallazgos ecográficos
  (conteo folicular por ovario), características del ciclo menstrual, y síntomas
  clínicos asociados (crecimiento de vello, oscurecimiento de piel, acné, caída de
  cabello, hábitos de estilo de vida).
- **Unidad de observación:** cada fila representa **una paciente** evaluada
  clínicamente, identificada por `Sl. No` y `Patient File No.`.
- **Procedencia:** dataset público de origen clínico/hospitalario (variante extendida
  del dataset "PCOS Dataset" ampliamente utilizado en estudios de investigación y
  disponible en repositorios como Kaggle). No se cuenta con documentación oficial
  detallada sobre la institución recolectora ni el año exacto de recolección — este
  es un punto señalado como limitación en el análisis (ver sección de calidad de datos
  en el notebook).
- **Archivo esperado:** `Datos/PCOS_extended_dataset.csv`


## Estructura del repositorio

```
.
├── Datos/
│   └── PCOS_extended_dataset.csv     # dataset (no incluido en el repo, ver Requisitos)
├── notebooks/
│   └── analisis_pcos.ipynb           # notebook principal con el EDA completo
├── src/                              # scripts auxiliares por sección de análisis
│   ├── univariado.py
│   ├── antropometricas.py
│   ├── cycle_length.py
│   ├── hormonal.py
│   ├── amh_vs_pcos.py
│   └── multivariado.py
└── README.md
```

## Requisitos de ejecución

- **Python** ≥ 3.9
- **Librerías necesarias:**

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Hallazgos principales

Un resumen detallado de hallazgos, preguntas abiertas y problemas de calidad de datos
que requieren corrección se encuentra en la sección de cierre del notebook principal.
