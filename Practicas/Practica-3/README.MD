# Predicción de deserción estudiantil

Práctica 3 de Introducción a la Ciencia de Datos (Posgrado en Ciencias de la Computación, CICESE).
Construye un clasificador que predice, **al cierre del primer semestre**, la situación de cada
estudiante al terminar la duración normal de su carrera: **graduado**, **desertor** o **todavía inscrito**. Compara cinco clasificadores (regresión logística, SVM, kNN, árbol de decisión y
Naive Bayes), cada uno con el preprocesamiento que requiere su modelo y con sus hiperparámetros
optimizados con validación cruzada estratificada.

## Descripción del dataset

- **Dataset:** Predict Students' Dropout and Academic Success
- **Autores:** V. Realinho, M. Vieira Martins, J. Machado y L. Baptista
- **Fuente:** [UCI Machine Learning Repository](https://doi.org/10.24432/C5MC89)
- **Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Procedencia:** Instituto Politécnico de Portalegre (Portugal), estudiantes de licenciatura que
  ingresaron entre 2008/09 y 2018/19.
- **Qué mide:** datos demográficos, socioeconómicos (escolaridad y ocupación de los padres, beca,
  deudas, colegiatura al día), de admisión (modo de ingreso, carrera, nota de admisión),
  rendimiento académico del 1er y 2º semestre (materias inscritas, evaluadas, aprobadas y nota) e
  indicadores macroeconómicos (desempleo, inflación y PIB).
- **Unidad de observación:** cada fila representa **un estudiante**.
- **Tamaño:** 4424 estudiantes, divididos por el curso en dos archivos:
  - `desercion-entrenamiento.csv`: 3539 estudiantes, 36 atributos y la variable objetivo `Target`
    (49.9 % *graduate*, 32.1 % *dropout* y 17.9 % *enrolled*).
  - `desercion-prueba.csv`: 885 estudiantes **sin** `Target` y solo con los 30 atributos que se
    conocen al cierre del 1er semestre.

## Estructura del repositorio

```
.
├── Practica-III.ipynb      # notebook principal
├── Images/                 # figuras generadas por el notebook (PNG)
├── Predicciones/
│   └── predicciones.csv    # predicciones del clasificador final para los 885 estudiantes de prueba
├── requirements.txt        # dependencias de Python
└── README.MD
```

Los datos están en el repositorio, fuera de la carpeta del proyecto:
[Datos/Students Dropout](../../Datos/Students%20Dropout/). El notebook los lee con la ruta relativa
`../../Datos/Students Dropout/`, así que debe ejecutarse desde `Practicas/Practica-3/`.

## Contenido del notebook

1. **Configuración y carga de datos:** librerías y versiones, estilo de las gráficas, semilla,
   información disponible al decidir (se excluyen las 6 columnas del 2º semestre) y tipo de cada
   atributo (9 nominales, 8 binarios, 1 ordinal y 12 numéricos).
2. **Descripción del problema y de los datos:** distribución de las clases, atributos más
   relacionados con la clase, falsas magnitudes en los nominales y escalas de los numéricos.
3. **Protocolo de evaluación:** validación cruzada estratificada de 5 pliegues, los mismos para
   los cinco modelos, con F1 macro como métrica.
4. **Preprocesamiento por clasificador:** un `Pipeline` con `ColumnTransformer` para cada modelo
   (one-hot, escalamiento o discretización según el caso), manejo de categorías no vistas y F1 de
   referencia con hiperparámetros por defecto.
5. **Optimización de hiperparámetros** con Optuna (muestreador TPE, 60–100 configuraciones por
   modelo). Cada subsección explica cómo funciona el modelo, por qué su preprocesamiento, el
   espacio de búsqueda y la lectura de los resultados.
6. **Comparación y elección del clasificador final**, con una comparación directa entre la
   regresión logística y el SVM.
7. **¿Conviene esperar al 2º semestre?** El mismo modelo, agregando las columnas del 2º semestre.
8. **Predicciones sobre el conjunto de prueba.**
9. **Conclusiones.**
10. **Referencias** (APA 7).
11. **Declaración de uso de IA.**

## Requisitos de ejecución

- **Python** ≥ 3.11 (probado con Python 3.14).
- **Librerías necesarias** (ver `requirements.txt`): pandas, numpy, matplotlib, seaborn,
  scikit-learn ≥ 1.8, optuna y jupyter. scikit-learn debe ser 1.8 o posterior: en versiones
  anteriores, `LogisticRegression` ignora `l1_ratio` y no se buscaría el tipo de regularización.

```bash
pip install -r requirements.txt
jupyter notebook Practica-III.ipynb
```

La ejecución completa tarda unos 5 minutos, casi todo en las búsquedas de Optuna de la regresión
logística y el SVM. Los resultados son reproducibles: la semilla (`SEED = 67`) fija los pliegues,
el muestreador de Optuna y los modelos.

Al ejecutarse, el notebook:

- guarda cada gráfica en `Images/`, con un nombre que empieza con el número de la sección donde se
  genera (por ejemplo, `2_9_escalas_numericos.png` o `5_meseta_svm_gamma_por_class_weight.png`);
- escribe `Predicciones/predicciones.csv`, con las columnas `id` y `Target`
  (`Dropout`, `Enrolled` o `Graduate`).

## Resultados principales

| Modelo | F1 macro (validación cruzada) |
|---|---|
| **SVM (RBF), elegido** | **0.6820 ± 0.0216** |
| Regresión logística | 0.6854 ± 0.0185 |
| Árbol de decisión | 0.6408 ± 0.0307 |
| Naive Bayes (categórico) | 0.6320 ± 0.0114 |
| kNN | 0.5733 ± 0.0153 |

- **Clasificador final: SVM con kernel RBF** (C ≈ 1.61, gamma ≈ 0.026, `class_weight="balanced"`).
  Empata con la regresión logística: la diferencia de F1 (0.003) es menos de un tercio de lo que
  varía entre pliegues (0.011), el SVM gana 3 de 5 pliegues y los dos tienen la misma estabilidad.
  Se eligió el SVM porque no supone una frontera lineal y da menos falsas alarmas de deserción,
  aceptando un recall de *dropout* algo menor (0.672 contra 0.699).
- **Compensar el desbalance fue más importante que el modelo:** `class_weight="balanced"` separó
  dos bandas de F1 en la regresión logística y el SVM. Los modelos que no pueden ponderar las clases
  (kNN y Naive Bayes) quedaron abajo.
- ***Enrolled* es la clase difícil** (F1 = 0.49): queda entre desertores y graduados, y el 80 % de
  los errores son confusiones con ella.
- **Utilidad práctica:** si la escuela contacta a todos los estudiantes que no se predicen como
  *graduate*, llega al 89 % de los desertores al cierre del 1er semestre.
- **Esperar al 2º semestre mejora poco** (+0.034 en F1 macro): conviene predecir al cierre del 1er
  semestre y actualizar la predicción al cierre del 2º.
- **Señales más fuertes:** materias aprobadas en el 1er semestre y tener la colegiatura al día.

El detalle de cada decisión, las figuras y la discusión con referencias se encuentran en el
notebook.
