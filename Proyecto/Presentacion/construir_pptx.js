// Arma Presentacion-Proyecto-CMAPSS.pptx (portada + 8 diapositivas) con el estilo de la propuesta.
// Las gráficas son las del notebook Proyecto-CMAPSS-v2.ipynb, guardadas otra vez con letra más grande por
// figuras/reexportar_figuras_notebook.py en figuras_notebook/ (las de Images/ se usan si falta alguna).
//
// Uso (desde la carpeta Proyecto, con pptxgenjs instalado en NODE_PATH):
//   node Presentacion/construir_pptx.js [ruta de apply_theme.js]
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const AQUI = __dirname;
const IMAGES = path.join(AQUI, "..", "Images");
const REEXPORTADAS = path.join(AQUI, "figuras_notebook");
const IMG = (n) => path.join(AQUI, "img", n);
const SALIDA = process.env.PPTX_SALIDA || path.join(AQUI, "Presentacion-Proyecto-CMAPSS.pptx");

// "Figura 05" -> la figura del notebook en Images/; "algo.png" -> Presentacion/img/.
function FIG(nombre) {
  if (nombre.endsWith(".png")) return IMG(nombre);
  for (const dir of [REEXPORTADAS, IMAGES]) {
    const f = fs.existsSync(dir) && fs.readdirSync(dir).find((x) => x.startsWith(nombre + " "));
    if (f) return path.join(dir, f);
  }
  throw new Error(`No está ${nombre} en ${REEXPORTADAS} ni en ${IMAGES}`);
}

// Proporción alto / ancho de un PNG, leída de su encabezado IHDR.
function proporcion(nombre) {
  const b = fs.readFileSync(FIG(nombre));
  return b.readUInt32BE(20) / b.readUInt32BE(16);
}

const THEME = {
  name: "Propuesta C-MAPSS",
  headFontFace: "Source Serif 4",
  bodyFontFace: "IBM Plex Sans",
  colors: {
    dk1: "3A4657", lt1: "FFFFFF", dk2: "1E3F6B", lt2: "F6F7F4",
    accent1: "1E3F6B", accent2: "1B7A8C", accent3: "B2531B", accent4: "E3EEF0",
    accent5: "5A6575", accent6: "D5DBDF", hlink: "1B7A8C", folHlink: "5A6575",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";                                   // 13.333 x 7.5 in, como la propuesta
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Pronóstico de vida útil remanente de motores turbofán";
pres.author = "Carlos Campos Sarabia";
pres.subject = "Proyecto final C-MAPSS, Introducción a ciencia de datos, CICESE";

const C = pres.SchemeColor;
const NAVY = C.text2, TEXTO = C.text1, FONDO = C.background2, BLANCO = C.background1;
const TEAL = C.accent2, NARANJA = C.accent3, CAJA = C.accent4, SUAVE = C.accent5, BORDE = C.accent6;
const X0 = 0.885, ANCHO = 11.563, Y0 = 1.52;                  // margen y área útil (igual que el PDF)

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: NAVY },
  objects: [
    { image: { path: IMG("onda.png"), x: 0, y: 0, w: 13.333, h: 4.46, sizing: { type: "cover", w: 13.333, h: 4.46 }, transparency: 68 } },
    { image: { path: IMG("logo_cicese.png"), x: 9.72, y: 0.67, w: 2.45, h: 1.213 } },
    { line: { x: X0, y: 6.44, w: ANCHO, h: 0, line: { color: "4F6E96", width: 0.75 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: X0, y: 3.82, w: 10, h: 0.36, fontSize: 14, bold: true, color: "9FD6DE", margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 4.36, w: 11.4, h: 1.55, fontFace: THEME.headFontFace, fontSize: 42, bold: true, color: "F7F8F5", margin: 0, valign: "top", align: "left", lineSpacingMultiple: 0.95 }, text: "" } },
    { placeholder: { options: { name: "subtitulo", type: "body", x: X0, y: 5.92, w: ANCHO, h: 0.42, fontSize: 17, color: "DCE6EF", margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "meta", type: "body", x: X0, y: 6.56, w: ANCHO, h: 0.68, fontSize: 12, color: "C9D6E3", margin: 0, valign: "top", lineSpacingMultiple: 1.15 }, text: "" } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: FONDO },
  margin: [0.5, 0.885, 0.8, 0.885],
  objects: [
    { rect: { x: 0, y: 6.81, w: 13.333, h: 0.69, fill: { color: NAVY }, line: { color: NAVY } } },
    { placeholder: { options: { name: "kicker", type: "body", x: X0, y: 0.56, w: ANCHO, h: 0.3, fontSize: 12, bold: true, color: TEAL, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.84, w: ANCHO, h: 0.58, fontFace: THEME.headFontFace, fontSize: 26, bold: true, color: NAVY, margin: 0, valign: "top", align: "left" }, text: "" } },
    { placeholder: { options: { name: "pie", type: "body", x: X0, y: 6.81, w: 10.9, h: 0.69, fontSize: 9.5, color: "DCE6EF", margin: 0, valign: "middle" }, text: "" } },
  ],
  slideNumber: { x: 12.05, y: 6.96, w: 0.4, h: 0.38, fontFace: THEME.bodyFontFace, fontSize: 12, color: "FFFFFF", align: "right" },
});

// ---------- Ayudas ----------
const txt = (s, texto, o) => s.addText(texto, { isTextBox: true, margin: 0, valign: "top", fontSize: 12.5, color: TEXTO, ...o });
const h2 = (s, texto, x, y, w) => txt(s, texto, { x, y, w, h: 0.32, fontFace: THEME.headFontFace, fontSize: 15.5, bold: true, color: NAVY, objectName: `Subtítulo: ${texto}` });
const pequeno = (s, texto, o) => txt(s, texto, { fontSize: 10.8, color: SUAVE, ...o });
const tarjeta = (s, x, y, w, h, o = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.07, fill: { color: BLANCO }, line: { color: BORDE, width: 0.75 }, ...o });
const caja = (s, x, y, w, h, color = CAJA, nombre = "Caja") => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.07, fill: { color }, line: { color }, objectName: nombre });
// Coloca una figura con ancho w (o menos, si así no cabe en hMax) y devuelve dónde termina.
function figura(s, nombre, x, y, w, hMax = 99) {
  const p = proporcion(nombre);
  if (w * p > hMax) w = hMax / p;
  const h = w * p;
  s.addImage({ path: FIG(nombre), x, y, w, h, altText: `Gráfica del notebook: ${path.basename(FIG(nombre), ".png")}` });
  return y + h;
}
const b = (text, o = {}) => ({ text, options: { bold: true, color: NAVY, ...o } });
const n = (text, o = {}) => ({ text, options: { ...o } });
const tabla = { fontFace: THEME.bodyFontFace, fontSize: 10.8, color: TEXTO, border: { type: "solid", pt: 0.75, color: "D5DBDF" }, fill: { color: "FFFFFF" }, margin: [0.03, 0.08, 0.03, 0.08], valign: "middle" };
const enc = (text, align = "right") => ({ text, options: { bold: true, color: "FFFFFF", fill: { color: "1E3F6B" }, align } });
const celda = (text, align = "right", o = {}) => ({ text, options: { align, ...o } });

function contenido(seccion, kicker, titulo, pie) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: seccion });
  s.addText(kicker, { placeholder: "kicker" });
  s.addText(titulo, { placeholder: "title", align: "left", bold: true });
  s.addText(pie, { placeholder: "pie" });
  return s;
}

// ---------- 1. Portada ----------
pres.addSection({ title: "Portada" });
{
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Portada" });
  s.addText("PROYECTO FINAL · CIENCIA DE DATOS", { placeholder: "kicker" });
  s.addText("Pronóstico de vida útil remanente de motores turbofán", { placeholder: "title", align: "left", bold: true });
  s.addText("Normalización por condición, ventanas deslizantes y LightGBM sobre C-MAPSS de NASA", { placeholder: "subtitulo" });
  s.addText([
    n("Materia: Introducción a ciencia de datos · Profesores: Dr. Hussein López / M.C. Joan Raygoza", { breakLine: true }),
    n("Alumno: Carlos Campos Sarabia · CICESE · noviembre de 2026"),
  ], { placeholder: "meta" });
  s.addNotes("0:00. Presentarse en una frase y pasar de inmediato al contexto.");
}

// ---------- 2. Contexto ----------
pres.addSection({ title: "Contexto" });
{
  const s = contenido("Contexto", "1 · CONTEXTO", "Las fallas de motor cuestan vidas y dinero",
    "Fotos: NTSB (AA191, UA328, dominio público); AAIB (Kegworth, OGL v1.0); ATSB (QF32, CC BY-SA 3.0 AU). Informes NTSB-AAR-79-17, AAIB 4/1990, ATSB AO-2010-089, NTSB DCA21FA085; Flying Magazine, “AOG: When an airplane can't fly”; Munguía (2023), El Financiero.");
  const casos = [
    ["aa191.jpg", "American 191 · 1979", "El motor y su pilón se desprenden al despegar, por daño de mantenimiento. 273 muertes."],
    ["kegworth.jpg", "Kegworth · 1989", "Un álabe del ventilador se fractura por fatiga y se apaga el motor sano. 47 muertes."],
    ["qf32.jpg", "Qantas 32 · 2010", "Grieta por fatiga en un tubo de aceite: falla no contenida. Sin víctimas."],
    ["ua328.jpg", "United 328 · 2021", "Álabe del ventilador agrietado por fatiga: falla del motor derecho. Sin víctimas."],
  ];
  const w = (ANCHO - 3 * 0.17) / 4;
  casos.forEach(([img, titulo, texto], i) => {
    const x = X0 + i * (w + 0.17);
    tarjeta(s, x, Y0, w, 2.66, { objectName: `Tarjeta ${titulo}` });
    s.addImage({ path: IMG(img), x: x + 0.01, y: Y0 + 0.01, w: w - 0.02, h: 1.55, sizing: { type: "cover", w: w - 0.02, h: 1.55 }, altText: `Foto: ${titulo}` });
    txt(s, [b(titulo, { fontSize: 12, breakLine: true }), n(texto, { fontSize: 11 })], { x: x + 0.13, y: Y0 + 1.66, w: w - 0.26, h: 0.95, lineSpacingMultiple: 1.05 });
  });
  const y2 = Y0 + 2.66 + 0.2;
  const wc = (5.63 - 0.13) / 2;
  [["10–20 mil USD", "por hora con un avión en tierra por mantenimiento no programado (AOG); hasta 100 mil."],
   ["39 MDD", "pérdida neta de Volaris en 2023, con 200 despidos, por problemas con motores."]].forEach(([g, t], i) => {
    const x = X0 + i * (wc + 0.13);
    caja(s, x, y2, wc, 1.22, CAJA, `Cifra ${g}`);
    txt(s, [b(g, { fontSize: 22, breakLine: true }), n(t, { fontSize: 11, color: SUAVE })], { x: x + 0.17, y: y2 + 0.1, w: wc - 0.3, h: 1.05 });
  });
  txt(s, [n("El "), b("mantenimiento por calendario"), n(" retira motores sanos antes de tiempo y no anticipa a los que se degradan rápido. Estimar la "), b("vida útil remanente (RUL)"), n(" con los sensores permite intervenir según el estado real de cada motor.")],
    { x: X0, y: y2 + 1.33, w: 5.63, h: 0.95, fontSize: 11.8 });
  const xp = X0 + 5.63 + 0.17, wp = ANCHO - 5.63 - 0.17;
  [["P1 · Desempeño.", " ¿Un modelo con ventanas deslizantes supera a los notebooks públicos de Kaggle en la prueba oficial de los 4 subconjuntos?"],
   ["P2 · Sensores.", " ¿Qué sensores anticipan la degradación de forma consistente y con sentido físico?"],
   ["P3 · Condiciones.", " ¿Tomar en cuenta la condición de vuelo al preprocesar mejora FD002 y FD004?"]].forEach(([p, t], i) => {
    const y = y2 + i * 0.8;
    tarjeta(s, xp, y, wp, 0.72, { objectName: `Pregunta ${p}` });
    txt(s, [b(p, { color: TEAL }), n(t)], { x: xp + 0.15, y: y + 0.1, w: wp - 0.3, h: 0.56, fontSize: 11.5 });
  });
  s.addNotes("0:00-1:00. Tres de los cuatro casos comparten un daño que crece con los ciclos (fatiga). Un avión en tierra cuesta 10-20 mil USD por hora. Por eso interesa estimar la RUL con sensores. Leer las tres preguntas: se responden en la última diapositiva.");
}

// ---------- 4. Normalización ----------
pres.addSection({ title: "Metodología" });
{
  const s = contenido("Metodología", "2 · PREPROCESAMIENTO", "La condición de vuelo esconde el desgaste del motor",
    "Gráfica: notebook, sección 4.6. P3: sección 10.3; RMSE de validación en ciclos, promedio de 3 semillas (ruido ≤ 0.05). La condición se identifica redondeando los 3 ajustes de operación.");
  // Figura 05 a lo ancho: arriba los sensores sin normalizar, abajo normalizados por condición
  const p5 = proporcion("Figura 05");
  const w5 = Math.min(ANCHO, 4.2 / p5);
  const yf = figura(s, "Figura 05", X0 + (ANCHO - w5) / 2, Y0 - 0.06, w5);
  const ys = yf + 0.1, hs = 6.62 - ys;
  caja(s, X0, ys, 4.15, hs, CAJA, "Fórmula del z");
  txt(s, [n("z = (x − μ"), n("cond", { subscript: true }), n(") / σ"), n("cond", { subscript: true })],
    { x: X0 + 0.17, y: ys + 0.06, w: 3.85, h: 0.42, fontFace: THEME.headFontFace, fontSize: 19, bold: true, color: NAVY });
  pequeno(s, [n("μ y σ de cada condición, calculadas "), b("solo con train"), n(".")], { x: X0 + 0.17, y: ys + 0.5, w: 3.85, h: 0.3 });
  txt(s, [n("Arriba, cada color es una condición: T50 marca ≈1400 °R a nivel del mar y ≈1050 °R a 25 000 pies. Abajo, el z mide cada vuelo contra lo normal "), b("para su condición"), n(" y aparece el desgaste.")],
    { x: X0 + 4.35, y: ys + 0.02, w: 3.75, h: hs - 0.04, fontSize: 11, valign: "middle" });
  caja(s, X0 + 8.3, ys, ANCHO - 8.3, hs, NAVY, "Resultado P3");
  txt(s, [
    b("P3 · mismo LightGBM, FD002 y FD004", { color: "9FD6DE", breakLine: true }),
    n("Validación 30.54 → ", { color: "EAF1F7" }), b("25.20", { color: "FFFFFF" }), n(" · prueba 26.96 → ", { color: "EAF1F7" }), b("22.34", { color: "FFFFFF" }),
  ], { x: X0 + 8.45, y: ys + 0.04, w: ANCHO - 8.6, h: hs - 0.08, fontSize: 11, valign: "middle" });
  s.addNotes("1:00-2:00. Arriba, los sensores del motor FD002_1 sin normalizar: cada color es una de las 6 condiciones de vuelo y cada una pone al sensor en otro nivel, así que el desgaste queda escondido entre franjas. Abajo, los mismos sensores normalizados con el z-score dentro de cada condición, con media y desviación solo de train: cada vuelo se mide contra lo normal para su condición y aparece la tendencia de desgaste (línea morada, media móvil de 20 ciclos). Evidencia de P3: el mismo LightGBM baja de 30.54 a 25.20 en validación y de 26.96 a 22.34 en prueba; poner la condición como columna no ayuda (30.54).");
}

// ---------- 5. Recorte ----------
{
  const s = contenido("Metodología", "2 · DATOS Y RECORTE", "Los sensores cambian poco hasta RUL ≈ 130: ahí se recorta",
    "Gráfica: notebook, sección 4.5. Datos: Saxena y Goebel (2008), NASA Ames. Objetivo lineal por tramos: Heimes (2008), PHM08.");
  const wl = 8.1;
  const yf = figura(s, "Figura 04", X0, Y0, wl);
  pequeno(s, "FD001: promedio de los 100 motores de cada sensor normalizado, según los ciclos que le quedan. La zona verde es la zona sana.",
    { x: X0, y: yf + 0.06, w: wl, h: 0.42 });
  caja(s, X0, yf + 0.6, wl, 1.0, CAJA, "Objetivo recortado");
  txt(s, [b("Objetivo = mín(RUL, 130).", { breakLine: true }), n("Un motor con 191 ciclos por delante se entrena como 130; uno con 100, como 100. El modelo aprende “130 o más” en la zona sana y se concentra en el desgaste.", { fontSize: 11.5 })],
    { x: X0 + 0.18, y: yf + 0.7, w: wl - 0.36, h: 0.85, fontSize: 12.5 });
  const xr = X0 + wl + 0.3, wr = ANCHO - wl - 0.3;
  txt(s, [n("Ps30 sube "), b("0.5 desviaciones"), n(" de RUL 300 a 130 y "), b("casi 3"), n(" de 130 a la falla.")],
    { x: xr, y: Y0, w: wr, h: 0.65, fontSize: 12 });
  txt(s, [b("Datos: "), n("709 motores de train vuelan hasta fallar (128 a 543 ciclos); 707 de test se cortan antes. RUL = último ciclo − ciclo actual.")],
    { x: xr, y: Y0 + 0.75, w: wr, h: 1.15, fontSize: 11.5 });
  caja(s, xr, Y0 + 1.98, wr, 0.95, CAJA, "Cifra 42 %");
  txt(s, [b("42 %", { fontSize: 22, breakLine: true }), n("de los ciclos de train está en la zona sana.", { fontSize: 11, color: SUAVE })],
    { x: xr + 0.17, y: Y0 + 2.06, w: wr - 0.3, h: 0.8 });
  pequeno(s, "La propuesta usaba 125. Se usó 130 porque ahí está el codo y ningún motor vive menos de 128 ciclos.",
    { x: xr, y: Y0 + 3.05, w: wr, h: 1.0 });
  s.addNotes("2:00-2:55. Datos: cada fila es un ciclo de vuelo de un motor, con 3 ajustes de operación y 21 sensores; en train los 709 motores vuelan hasta fallar y la RUL es último ciclo menos ciclo actual; en test se cortan antes y NASA da la RUL del último ciclo. La gráfica de la sección 4.5 es el promedio normalizado de Ps30, T50 y htBleed según la RUL. Mientras el motor está sano casi no cambian, y desde RUL 130 suben. Un motor con 300 ciclos y otro con 200 se ven iguales, así que se recorta el objetivo a 130: el modelo responde 130 o más en la zona sana. La propuesta decía 125; ningún motor vive menos de 128.");
}

// ---------- 6. Ventanas ----------
{
  const s = contenido("Metodología", "3 · VENTANAS DESLIZANTES", "70 ciclos estabilizan la señal; 10 ciclos corrigen el atraso",
    "Gráficas: notebook, secciones 7.3 y 9.2 b). Validar por motor evita un error optimista: mezclando filas, Random Forest estima 2.52 en FD001; separando motores, 10.67; el error real fue 13.74.");
  txt(s, "Por cada sensor se resumen los últimos ciclos del motor:", { x: X0, y: Y0 - 0.02, w: 4.4, h: 0.3, fontSize: 12 });
  const chips = ["valor actual", "media", "desviación", "mínimo", "máximo", "pendiente"];
  const anchos = [1.12, 0.72, 1.0, 0.86, 0.86, 0.98];
  let x = X0 + 4.4;
  chips.forEach((c, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: Y0 - 0.04, w: anchos[i], h: 0.32, rectRadius: 0.16, fill: { color: BLANCO }, line: { color: BORDE, width: 0.75 }, objectName: `Estadística ${c}` });
    txt(s, c, { x, y: Y0 - 0.04, w: anchos[i], h: 0.32, fontSize: 11, align: "center", valign: "middle" });
    x += anchos[i] + 0.08;
  });
  txt(s, "→ 91 columnas con 70 ciclos; 181 con 10 + 70.", { x: X0, y: Y0 + 0.36, w: ANCHO, h: 0.3, fontSize: 12 });
  const wl = 4.85, xr = X0 + wl + 0.3, wr = ANCHO - wl - 0.3;
  h2(s, "¿Cuántos ciclos? Random Forest", X0, Y0 + 0.78, wl);
  let yf = figura(s, "Figura 09", X0, Y0 + 1.14, wl);
  pequeno(s, [n("GroupKFold por motor, 3 semillas (ruido ≤ 0.09). Baja de 25.69 a "), b("20.16"), n(" y se estabiliza: 70 queda a menos de 1 % de 100 y deja menos motores de test con la ventana incompleta.")],
    { x: X0, y: yf + 0.06, w: wl, h: 0.85 });
  h2(s, "El atraso de la media de 70 (Ps30, FD001_1)", xr, Y0 + 0.78, wr);
  yf = figura(s, "Figura 9.2b", xr, Y0 + 1.14, wr);
  pequeno(s, [n("Izquierda: al fallar, la media de 70 vale "), b("0.90"), n(" y la de 10 vale "), b("2.25"), n(": la de 70 sigue promediando ciclos de cuando el motor estaba sano. Derecha: la diferencia entre las dos medias es ≈0 mientras el motor está sano y crece hasta 1.35 al fallar; el modelo usa el nivel de la de 10 y la tendencia de la de 70.")],
    { x: xr, y: yf + 0.06, w: wr, h: 1.0 });
  s.addNotes("2:55-3:55. Un solo ciclo tiene ruido de más o menos 1 desviación; la ventana resume los últimos ciclos en 6 estadísticas. Izquierda (sección 7.3): con Random Forest y validación por motor, el error baja de 25.69 a 20.16 y se estabiliza en 70. Derecha (sección 9.2 b): cerca de la falla la media de 70 se atrasa, vale 0.90 cuando la de 10 vale 2.25; por eso se agrega una ventana de 10. La línea roja es la diferencia entre las dos medias: cero mientras el motor está sano y crece cuando el desgaste se acelera.");
}

// ---------- 7. Modelos ----------
pres.addSection({ title: "Resultados" });
{
  const s = contenido("Resultados", "4 · MODELOS", "LightGBM fue el mejor modelo; Optuna lo ajusta un poco más",
    "Gráficas: notebook, secciones 8.3 y 9.3. Ke et al. (2017), LightGBM · Chen y Guestrin (2016), XGBoost · Pedregosa et al. (2011), scikit-learn · Akiba et al. (2019), Optuna · Bergstra et al. (2011), TPE.");
  const wl = 5.3;
  h2(s, "RMSE de validación con ventana de 70", X0, Y0, wl);
  const yf = figura(s, "Figura 10", X0, Y0 + 0.4, wl);
  pequeno(s, "Promedio de los 4 subconjuntos: Ridge 26.22 · kNN 25.61 · SVR 21.20 · Random Forest 20.15 · XGBoost 19.58 · LightGBM 19.17. Línea base (predecir el promedio): 48.36.",
    { x: X0, y: yf + 0.06, w: wl, h: 0.62 });
  txt(s, [b("¿Por qué LightGBM?"), n(" Suma árboles en secuencia, cada uno corrige el error de los anteriores; capta relaciones no lineales entre las 91 columnas y gana en los 4 subconjuntos.")],
    { x: X0, y: yf + 0.72, w: wl, h: 0.85, fontSize: 11.8 });
  const xr = X0 + wl + 0.3, wr = ANCHO - wl - 0.3;
  const wt = (wr - 0.24) / 3;
  [["LightGBM, 70", "19.17", ""], ["+ ventana de 10", "18.95", ""], ["+ Optuna", "18.78", "± 0.01 (3 semillas)"]].forEach(([e, v, nota], i) => {
    const x = xr + i * (wt + 0.12), final = i === 2;
    tarjeta(s, x, Y0, wt, 1.1, { line: { color: final ? NARANJA : BORDE, width: final ? 1.25 : 0.75 }, objectName: `Paso ${e}` });
    txt(s, [n(e, { fontSize: 11, color: SUAVE, breakLine: true }), b(v, { fontSize: 22, color: final ? NARANJA : NAVY, breakLine: !!nota }), ...(nota ? [n(nota, { fontSize: 10.5, color: SUAVE })] : [])],
      { x: x + 0.17, y: Y0 + 0.08, w: wt - 0.3, h: 0.95 });
  });
  h2(s, "Optuna: 30 intentos con TPE", xr, Y0 + 1.25, wr);
  const yo = figura(s, "Figura 11", xr, Y0 + 1.62, wr, 2.75);
  pequeno(s, "Parte de la configuración de fleet-readiness (500 árboles, tasa 0.03, 31 hojas). La mejor: 900 árboles, tasa 0.0105, 41 hojas. La mejora (0.16) es 16 veces el ruido entre semillas.",
    { x: xr, y: yo + 0.06, w: wr, h: 0.5 });
  s.addNotes("3:55-4:45. Con la ventana de 70 se compararon 7 modelos; los de árboles ganan y LightGBM es el mejor en los 4 subconjuntos (19.17 en promedio). Agregar la ventana de 10 baja a 18.95 y Optuna, con 30 intentos, a 18.78, con ruido de 0.01 entre semillas. En la gráfica de Optuna, cada punto es un intento y la línea roja el mejor hasta ese momento. Son mejoras pequeñas comparadas con normalizar y usar ventanas.");
}

// ---------- 8. Prueba y Kaggle ----------
{
  const s = contenido("Resultados", "5 · RESULTADOS EN PRUEBA", "En prueba, al nivel del mejor notebook público de Kaggle",
    "Gráfica: notebook, sección 10.1. Elsamahy (2026), “Fleet readiness: Engine RUL on NASA C-MAPSS”, Kaggle · Ansari et al. (2025), Chronos-2, Amazon Web Services.");
  const wl = 6.8;
  const yf = figura(s, "Figura 15", X0, Y0, wl, 4.55);
  pequeno(s, "RMSE de prueba contra el RUL real, una predicción por motor (707 motores).", { x: X0, y: yf + 0.06, w: wl, h: 0.3 });
  const xr = X0 + wl + 0.27, wr = ANCHO - wl - 0.27;
  s.addTable([
    [enc("Promedio FD001–FD004", "left"), enc("RMSE")],
    [celda("fleet-readiness (Chronos-2 + LightGBM)", "left"), celda("17.54")],
    [celda("Este trabajo: LightGBM 10 + 70", "left", { bold: true, color: "1E3F6B" }), celda("17.42", "right", { bold: true, color: "1E3F6B" })],
    [celda("Este trabajo + Chronos-2", "left"), celda("17.22")],
  ], { ...tabla, x: xr, y: Y0, w: wr, colW: [wr - 0.85, 0.85], rowH: 0.3 });
  pequeno(s, "Gano en FD002 y FD004 y pierdo en FD001 y FD003. La diferencia es menor que los ±2 ciclos de incertidumbre que reporta fleet-readiness, y ellos califican contra el RUL recortado a 125.",
    { x: xr, y: Y0 + 1.3, w: wr, h: 0.95 });
  caja(s, xr, Y0 + 2.35, wr, 1.95, CAJA, "Chronos-2");
  h2(s, "Chronos-2", xr + 0.18, Y0 + 2.47, wr - 0.36);
  txt(s, [
    n("Modelo de series de tiempo preentrenado (Amazon, 2025), usado congelado. Recibe los últimos 64 ciclos normalizados y devuelve un resumen de 1 054 valores; PCA lo reduce a 32 que se suman a las ventanas.", { breakLine: true }),
    n("Prueba "), b("17.42 → 17.22"), n(": 0.2 ciclos, a cambio de una GPU y 28 M de parámetros."),
  ], { x: xr + 0.18, y: Y0 + 2.83, w: wr - 0.36, h: 1.8, fontSize: 11, paraSpaceAfter: 5 });
  s.addNotes("4:45-5:45. Gráfica de la sección 10.1: en la prueba oficial el promedio es 17.42 contra 17.54 del mejor notebook (fleet-readiness): gano en FD002 y FD004 y pierdo en FD001 y FD003; la diferencia es menor que su incertidumbre. Ellos usan Chronos-2, por eso lo probé: un modelo preentrenado de series de tiempo usado como extractor; mejora solo 0.2 ciclos.");
}

// ---------- 8. RUL predicho contra real (sección 9.7) ----------
{
  const s = contenido("Resultados", "5 · RESULTADOS EN PRUEBA", "Cerca de la falla acierta; a un motor sano le dice ≈130",
    "Gráfica: notebook, sección 9.7; error por zona: sección 9.8. Con más de 130 ciclos restantes hay 8, 55, 11 y 60 motores en FD001–FD004. Sesgo = predicho − real.");
  const yf = figura(s, "Figura 12", X0, Y0 - 0.06, 7, 5.05);
  const wl = (yf - Y0 + 0.06) / proporcion("Figura 12");
  const xr = X0 + wl + 0.3, wr = ANCHO - wl - 0.3;
  h2(s, "Cómo leer la gráfica", xr, Y0, wr);
  const puntos = [
    ["Cada punto es un motor de test.", " Sobre la diagonal gris, la predicción sería perfecta."],
    ["RUL real < 50:", " los puntos siguen la diagonal. Ahí se decide sacar el motor."],
    ["RUL real > 130:", " los puntos forman una meseta en ≈130. El motor se ve sano y el modelo dice “130 o más”."],
    ["FD001_1 (círculo):", " con 31 ciclos se ve sano y se predijo en 127.5; le quedaban 112."],
  ];
  const runs = [];
  puntos.forEach(([t1, t2], i) => {
    runs.push(b(t1, { bullet: true }));
    runs.push(n(t2, { breakLine: i < puntos.length - 1 }));
  });
  txt(s, runs, { x: xr, y: Y0 + 0.4, w: wr, h: 2.75, fontSize: 11.5, paraSpaceAfter: 5 });
  s.addTable([
    [enc("RUL real", "left"), enc("RMSE"), enc("Sesgo"), enc("Lectura", "left")],
    [celda("< 50", "left"), celda("3.5–5.8", "right", { bold: true, color: "1E3F6B" }), celda("+0.2 a +2.4"), celda("donde se decide", "left")],
    [celda("50–130", "left"), celda("14–17"), celda("+3 a +5"), celda("desgaste", "left")],
    [celda("> 130", "left"), celda("14–41"), celda("−13 a −37"), celda("dice ≈130", "left")],
  ], { ...tabla, x: xr, y: Y0 + 2.75, w: wr, colW: [0.85, 0.95, 1.12, wr - 2.92], rowH: 0.31 });
  s.addNotes("5:45-6:50. Gráfica de la sección 9.7: cada punto es un motor de test, el eje horizontal es lo que realmente le quedaba y el vertical lo que predijo el modelo. Cerca de la falla los puntos siguen la diagonal: con menos de 50 ciclos el error es de 3.5 a 5.8 ciclos, justo donde se decide sacar un motor. Arriba de 130 hay una meseta: el motor todavía no muestra desgaste en sus sensores y el modelo responde 130, que significa 130 o más. Es el efecto del recorte, y el error es del lado seguro: avisa antes. Ejemplo, el círculo: el motor 1 de FD001 se observó 31 ciclos, se veía sano, el modelo dijo 127.5 y le quedaban 112. FD002 y FD004 tienen más error total porque tienen 55 y 60 motores sanos en test, no porque el modelo funcione peor.");
}

// ---------- 9. Conclusiones ----------
pres.addSection({ title: "Conclusiones" });
{
  const s = contenido("Conclusiones", "6 · CONCLUSIONES Y LIMITACIONES", "Respuestas: el preprocesamiento pesó más que el modelo",
    "Gráfica: notebook, sección 10.2. Código, resultados y predicciones: github.com/Elsarabia15/ICD-2026 (carpeta Proyecto) · Vollert y Theissler (2021), ETFA.");
  const wl = 6.0;
  tarjeta(s, X0, Y0, wl, 0.66, { objectName: "Respuesta P1" });
  txt(s, [b("P1 · En parte.", { color: TEAL }), n(" Mejor promedio (17.42) y mejor en FD002 y FD004; fleet-readiness gana en FD001 y FD003.")],
    { x: X0 + 0.17, y: Y0 + 0.08, w: wl - 0.34, h: 0.52, fontSize: 11.5 });
  const y2 = Y0 + 0.76;
  const wf = 4.25, hfig = wf * proporcion("Figura 16");
  tarjeta(s, X0, y2, wl, hfig + 0.82, { objectName: "Respuesta P2" });
  txt(s, [b("P2 · Sí.", { color: TEAL }), n(" Ps30 y T50 están entre los 5 más importantes en 20 y 19 de 20 pliegues, luego Nc y NRc: coherente con el desgaste del compresor de alta presión.")],
    { x: X0 + 0.17, y: y2 + 0.08, w: wl - 0.34, h: 0.6, fontSize: 11.5 });
  figura(s, "Figura 16", X0 + (wl - wf) / 2, y2 + 0.72, wf);
  const y3 = y2 + hfig + 0.92;
  tarjeta(s, X0, y3, wl, 0.56, { objectName: "Respuesta P3" });
  txt(s, [b("P3 · Sí.", { color: TEAL }), n(" Normalizar por condición baja el error 5.3 ciclos en validación y 4.6 en prueba.")],
    { x: X0 + 0.17, y: y3 + 0.08, w: wl - 0.34, h: 0.42, fontSize: 11.5 });
  const xr = X0 + wl + 0.3, wr = ANCHO - wl - 0.3;
  caja(s, xr, Y0, wr, 0.92, NAVY, "Hallazgo principal");
  txt(s, [b("Hallazgo:", { color: "9FD6DE" }), n(" normalizar (−5.3) y usar ventanas (−5.5) bajaron el error mucho más que cambiar a LightGBM (−1.0), Optuna (−0.16) o Chronos-2 (−0.19).", { color: "EAF1F7" })],
    { x: xr + 0.18, y: Y0 + 0.11, w: wr - 0.36, h: 0.75, fontSize: 11.5 });
  h2(s, "Limitaciones", xr, Y0 + 1.12, wr);
  const lim = [
    ["Datos simulados:", " C-MAPSS no modela grietas ni errores de montaje como los de los accidentes."],
    ["Sin intervalos de confianza", " en prueba; el ruido entre semillas subestima la variabilidad."],
    ["Recorte a 130", " elegido con el perfil de los sensores, no con validación."],
    ["Prueba usada dos veces:", " modelo final y Chronos-2."],
    ["Historias cortas:", " FD001_1 de test, con 31 ciclos, se predijo en 127.5 y le quedaban 112."],
  ];
  const runs = [];
  lim.forEach(([t, r], i) => {
    runs.push(b(t, { bullet: true }));
    runs.push(n(r, { breakLine: i < lim.length - 1 }));
  });
  txt(s, runs, { x: xr, y: Y0 + 1.52, w: wr, h: 3.3, fontSize: 11.5, paraSpaceAfter: 6 });
  s.addNotes("6:50-7:50. Checkpoint del minuto 7: aquí. P1 en parte, P2 sí (gráfica de la sección 10.2: Ps30 y T50, coherentes con el desgaste del compresor de alta presión), P3 sí. El hallazgo: el preprocesamiento pesó más que el modelo. Cerrar con las limitaciones: datos simulados, sin intervalos de confianza en prueba, recorte no validado.");
}

(async () => {
  await pres.writeFile({ fileName: SALIDA });
  const tema = process.argv[2];
  if (tema) {
    await require(tema).applyTheme(SALIDA, THEME);
  }
  console.log("PPTX:", SALIDA);
})();
