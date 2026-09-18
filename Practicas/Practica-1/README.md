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
- **Archivo esperado:** `PCOS_extended_dataset.csv` (ver ubicaciones válidas en
  "Estructura del repositorio")

## Estructura del repositorio

```
.
├── Practica-I.ipynb        # notebook principal con el EDA completo
├── Images/                 # figuras generadas por el notebook (Figura 1 a 8, PNG)
├── requirements.txt        # dependencias de Python
└── README.md
```

El dataset (`PCOS_extended_dataset.csv`) no está incluido en el repositorio. El
notebook lo busca automáticamente en su propia carpeta, en una subcarpeta `Datos/`,
o en las mismas ubicaciones dentro de cualquier carpeta superior — alcanza con
colocar el CSV en `Practicas/Practica-1/` o en `Practicas/Practica-1/Datos/`.

## Requisitos de ejecución

- **Python** ≥ 3.9
- **Librerías necesarias** (ver `requirements.txt`):

```bash
pip install -r requirements.txt
```

## Hallazgos principales

El notebook cierra con una comparativa entre los valores de referencia clínica
estándar (AMH, duración del ciclo, hirsutismo, acantosis nigricans, acné/alopecia)
y los resultados obtenidos en la cohorte del dataset, junto con las guías y
consensos citados (APA 7). Un resumen detallado de hallazgos, preguntas abiertas
y problemas de calidad de datos corregidos durante el análisis se encuentra en la
sección de conclusión del notebook.
