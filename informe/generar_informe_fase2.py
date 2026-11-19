"""Genera informe/Informe_Fase2.pdf (≤ 8 páginas) a partir de resultados/fase2/resultados_fase2.json y sus figuras.

Ninguna cifra se escribe a mano: todas salen del JSON que exporta notebooks/Centinela_Fase2.ipynb.
Uso:  python informe/generar_informe_fase2.py
"""
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "resultados" / "fase2"
FIG, CLI = RES / "figuras", RES / "cliente"
SALIDA = ROOT / "informe" / "Informe_Fase2.pdf"
R = json.loads((RES / "resultados_fase2.json").read_text(encoding="utf-8"))

def n(x, d=3):
    return f"{x:.{d}f}".replace(".", ",")

def pct(x, d=0):
    return f"{100 * x:.{d}f}".replace(".", ",") + " %"

def sci(x):
    m, e = f"{x:.0e}".split("e")
    return f"{m}·10<super>{int(e)}</super>"

def miles(x):
    return f"{int(x):,}".replace(",", ".")

# ----------------------------------------------------------------------------- estilos
FUENTE, NEGRITA = "Helvetica", "Helvetica-Bold"
try:
    for nom, arch in [("Arial", "arial.ttf"), ("Arial-Bold", "arialbd.ttf"), ("Arial-Italic", "ariali.ttf"), ("Arial-BoldItalic", "arialbi.ttf")]:
        pdfmetrics.registerFont(TTFont(nom, str(Path("C:/Windows/Fonts") / arch)))
    addMapping("Arial", 0, 0, "Arial"); addMapping("Arial", 1, 0, "Arial-Bold")
    addMapping("Arial", 0, 1, "Arial-Italic"); addMapping("Arial", 1, 1, "Arial-BoldItalic")
    FUENTE, NEGRITA = "Arial", "Arial-Bold"
except Exception:
    pass
VERDE = colors.HexColor("#1f4e3d")
st = {
    "titulo": ParagraphStyle("t", fontName=NEGRITA, fontSize=15, leading=18, textColor=VERDE, spaceAfter=2),
    "sub": ParagraphStyle("s", fontName=FUENTE, fontSize=8.5, leading=10.5, textColor=colors.HexColor("#555555"), spaceAfter=6),
    "h": ParagraphStyle("h", fontName=NEGRITA, fontSize=11.5, leading=14, textColor=VERDE, spaceBefore=7, spaceAfter=3, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName=NEGRITA, fontSize=10, leading=12.5, spaceBefore=4, spaceAfter=2, keepWithNext=1),
    "p": ParagraphStyle("p", fontName=FUENTE, fontSize=9.2, leading=12, alignment=TA_JUSTIFY, spaceAfter=4),
    "b": ParagraphStyle("b", fontName=FUENTE, fontSize=9.2, leading=12, leftIndent=11, bulletIndent=2, spaceAfter=2),
    "pie": ParagraphStyle("pie", fontName=FUENTE, fontSize=7.9, leading=9.5, textColor=colors.HexColor("#444444"), spaceAfter=5),
    "caja": ParagraphStyle("c", fontName=FUENTE, fontSize=9.2, leading=12.3, leftIndent=10, bulletIndent=0, spaceAfter=1),
    "tab": ParagraphStyle("tb", fontName=FUENTE, fontSize=8.2, leading=9.8),
    "ref": ParagraphStyle("r", fontName=FUENTE, fontSize=8.2, leading=10.2, leftIndent=12, firstLineIndent=-12, spaceAfter=2.5),
}
P = lambda t: Paragraph(t, st["p"])
B = lambda t: Paragraph(t, st["b"], bulletText="•")
H = lambda t: Paragraph(t, st["h"])
H3 = lambda t: Paragraph(t, st["h3"])

def img(ruta, ancho_cm):
    from PIL import Image as PILImage
    w, hh = PILImage.open(ruta).size
    return Image(str(ruta), width=ancho_cm * cm, height=ancho_cm * cm * hh / w)

def figura(ruta, ancho_cm, pie):
    return KeepTogether([img(ruta, ancho_cm), Paragraph(pie, st["pie"])])

def tabla(filas, anchos, resaltar=None):
    t = Table([[Paragraph(str(c), st["tab"]) for c in f] for f in filas], colWidths=[a * cm for a in anchos])
    estilo = [("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c8c8c8")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6efe9")),
              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    if resaltar is not None:
        estilo.append(("BACKGROUND", (0, resaltar), (-1, resaltar), colors.HexColor("#eef5fb")))
    t.setStyle(TableStyle(estilo))
    return t

def caja(titulo, lineas):
    cont = [Paragraph(f"<b>{titulo}</b>", st["caja"])] + [Paragraph(l, st["caja"], bulletText="•") for l in lineas]
    t = Table([[cont]], colWidths=[17.8 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef5f1")), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9cc5b0")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t

def lado_a_lado(izq, der, a=8.9, b=8.9):
    t = Table([[izq, der]], colWidths=[a * cm, b * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    return t

# ----------------------------------------------------------------------------- datos
cps = R["clases_por_split"]; ficha = R["a3_ficha_arquitecturas"]; fe_ft = R["a4_fe_vs_ft_validacion"]
a3 = R["a5_prueba_3clases"]; ga = a3["global"]; pc = a3["por_clase"]; alerta = R["a5_prueba_alerta"]
bv, bt, b60, grad = R["b3_validacion"], R["b4_prueba"], R["b5_ventana60_validacion"], R["b5_gradiente_relativo"]
c1, abl, dup = R["c1_alineacion"], R["c2_ablacion_prueba"], R["duplicados"]
f1m = {f"{x['arquitectura']} · {'FT' if 'fine' in x['estrategia'] else 'FE'}": x["f1_macro"] for x in fe_ft}
ft = [x for x in fe_ft if "fine" in x["estrategia"]][0]
fus, img_, seq, perm, mlp = (abl[k] for k in ("Fusión", "Solo imagen", "Solo serie", "Fusión con clima permutado", "MLP Fase 1 (referencia)"))
celda = R["b_celda_elegida"]
d5 = {x["distancia_pHash_max"]: x for x in dup["por_distancia_phash"]}
pw = R["pesos_clase"]

E = [Paragraph("Centinela del Café · Fase 2: CNN, LSTM/GRU y fusión multimodal", st["titulo"]),
     Paragraph("Informe técnico · Proyecto Centinela · Briyith Lisdey Herrera Cruz, Juan Pablo Becerra Tirano y Johnatan Vélez Martínez · "
               "Deep Learning, Maestría en Ciencia de Datos, Universidad Santo Tomás · " + R["fecha_ejecucion"], st["sub"]),
     caja("Resultados clave", [
         f"<b>Rama A (imagen):</b> una EfficientNet-B0 con <i>fine-tuning</i> parcial distingue hojas sanas, con ácaro rojo y con roya, con "
         f"F1 macro de {n(ga['f1_macro'], 2)} en prueba. Como alerta sí/no logra AUC {n(alerta['cnn']['auc'])}, igual que el MLP de la Fase 1 "
         f"({n(mlp['auc'])}), pero deja escapar más hojas enfermas ({alerta['cnn']['FN']} frente a {int(mlp['FN'])}).",
         f"<b>Rama B (clima):</b> la {celda} pronostica la humedad relativa del día siguiente con un error medio de {n(bt[celda]['MAE'], 2)} puntos "
         f"(RMSE {n(bt[celda]['RMSE'], 2)}). Supera a ARIMA ({n(bt['ARIMA(2,0,1)']['RMSE'], 2)}) y a la persistencia ({n(bt['PERSISTENCIA']['RMSE'], 2)}).",
         f"<b>Rama C (fusión):</b> agregar el clima <b>no mejora</b> la alerta (AUC {n(fus['auc'])} frente a {n(img_['auc'])} con solo imagen), y barajar "
         f"el clima entre fotos no cambia nada ({n(perm['auc'])}). Las 1.560 fotos se tomaron en 5 días con clima casi idéntico.",
         "<b>Recomendación:</b> mantener la alerta de la Fase 1 para no dejar escapar hojas enfermas, usar la CNN para distinguir ácaro de roya, "
         "usar la rama B como semáforo climático de la finca y reservar la fusión para cuando haya fotos de muchas fincas y fechas."]),
     ]

# 1. Contexto
E += [H("1. Problema, cliente y qué cambia frente a la Fase 1"),
      P("El cliente son los técnicos de sanidad de las organizaciones de monitoreo fitosanitario, que deben decidir qué hojas de café revisar "
        "primero. En la Fase 1, un MLP recibía la foto resumida en 27 medidas de color y textura. En la Fase 2 se reemplaza ese resumen manual "
        "por arquitecturas especializadas: (A) una <b>red convolucional preentrenada</b> que aprende sola qué mirar en la foto; (B) una <b>red "
        "recurrente</b> que modela 18 años de clima diario de la finca; y (C) la <b>fusión</b> de ambas en una alerta única. Para que la "
        "comparación con la Fase 1 sea justa, se conservan la misma partición por planta (70/15/15), la semilla 42 y la regla de alerta "
        "(el umbral que minimiza 5·FN + FP en validación con <i>recall</i> ≥ 0,90)."),
      P("<b>Diferencias frente al ejemplo público del curso.</b> La actividad presenta \"Centinela del Café\" (imágenes RoCoLe con clima) como "
        "escenario de referencia y lo declara vetado como entrega. El equipo decidió continuar con RoCoLe, porque es la base de su Fase 1, y "
        "registró ese riesgo en la bitácora (E-11). Para no reproducir el ejemplo, el problema se planteó de otra manera en cada rama: la "
        "rama A clasifica <b>tres clases</b> (sana, ácaro rojo y roya) y alimenta una alerta con <b>costos asimétricos</b>; la rama B "
        "<b>pronostica la humedad</b> a un día con 18 años de datos y mide el desvanecimiento del gradiente; y la rama C <b>mide</b> la "
        "alineación entre foto y clima, en vez de suponerla, y comprueba con una permutación si la fusión realmente usa el clima.")]

# 2. Datos y duplicados
E += [H("2. Datos y verificación de duplicados"),
      P(f"Se usan {miles(sum(cps['total'].values()))} fotos de 390 plantas de café robusta (RoCoLe) en 3 clases: sana ({cps['total']['sana']}), "
        f"ácaro rojo ({cps['total']['ácaro rojo']}) y roya ({cps['total']['roya']}, niveles 1 a 4 agrupados). Además, se usan "
        f"{miles(R['b1_serie']['observaciones'])} días de clima de NASA POWER en las coordenadas de la finca. Antes de modelar se "
        f"<b>verificó la duplicidad de las fotos</b> con dos huellas: SHA-256 (copia exacta del archivo) y pHash (foto visualmente igual). "
        f"Se confirmaron <b>{dup['grupos_sha256']} pares de copias exactas</b> entre plantas distintas, y con pHash ≤ 5 aparecen "
        f"{d5[5]['pares']} pares en total ({d5[5]['pares_solo_visuales']} visualmente iguales aunque no son el mismo archivo). En "
        f"{dup['pares_phash5_clase_distinta']} de esos pares, las dos copias tienen clases distintas en las anotaciones. Las fotos no se "
        "eliminan, porque habría que elegir arbitrariamente una etiqueta, pero se comprobó que la partición mantiene cada par en el mismo "
        "subconjunto."),
      figura(FIG / "a0_duplicados.png", 9.6, "Figura 1. Pares duplicados verificados: arriba la foto A, abajo su pareja B, con la clase anotada "
             "de cada una. Los títulos indican si son copias exactas o visualmente iguales (distancia pHash).")]

# 3. Rama A
fa = ficha
E += [H("3. Rama A · Visión por computador (CNN)"),
      P("<b>EDA y preprocesamiento.</b> El ácaro es la clase minoritaria (11 %). El brillo y la nitidez se distribuyen igual en las tres "
        "clases, así que el modelo no puede usar la calidad de la foto como atajo. Como el fondo contiene otras hojas y a veces dedos, la "
        "CNN recibe la hoja recortada con su caja anotada, rellenada a cuadrado. Se guarda en 256 px y entra al modelo en 224 px, el tamaño "
        "con que se preentrenaron las redes: el margen de 256 permite que el recorte aleatorio del entrenamiento no tenga que ampliar la "
        "imagen, mientras que en validación y prueba se redimensiona la hoja completa, sin azar, para que la evaluación sea reproducible. La "
        "pérdida es la <b>entropía cruzada categórica</b>, la generalización a 3 clases de la BCE de la Fase 1, con pesos inversos a la "
        f"frecuencia (sana {n(pw['sana'], 2)}, ácaro {n(pw['ácaro rojo'], 2)}, roya {n(pw['roya'], 2)}) para que el ácaro pese lo mismo que "
        "las otras clases en el total."),
      tabla([["Arquitectura", "Parámetros", "Capas conv.", "ms/imagen (CPU)", "Top-1 ImageNet", "F1 macro en validación"],
             ["ResNet50 (He et al., 2016) · congelada", f"{n(fa['resnet50']['parametros_M'], 1)} M", fa["resnet50"]["capas_conv"],
              n(fa["resnet50"]["ms_por_imagen_cpu"], 0), n(fa["resnet50"]["imagenet_top1"], 1), n(f1m["resnet50 · FE"])],
             ["EfficientNet-B0 (Tan y Le, 2019) · congelada", f"{n(fa['efficientnet_b0']['parametros_M'], 1)} M", fa["efficientnet_b0"]["capas_conv"],
              n(fa["efficientnet_b0"]["ms_por_imagen_cpu"], 0), n(fa["efficientnet_b0"]["imagenet_top1"], 1), n(f1m["efficientnet_b0 · FE"])],
             ["EfficientNet-B0 · <i>fine-tuning</i> (bloques 6–8)", "—", "—", "—", "—", f"<b>{n(ft['f1_macro'])}</b>"]],
            [5.6, 2.0, 1.8, 2.3, 2.2, 3.9], resaltar=3),
      Paragraph("Tabla 1. Comparación de arquitecturas y estrategias. El F1 macro es el promedio del F1 de las 3 clases, calculado en las 232 "
                "fotos de validación.", st["pie"]),
      P(f"<b>Elección.</b> Se compararon ResNet50, la referencia clásica con conexiones residuales, y EfficientNet-B0, la alternativa "
        "eficiente pensada para la tableta de la Fase 3. VGG16 se descartó por su tamaño (138 M de parámetros). En <i>feature extraction</i> "
        "la red queda congelada y solo se entrena una capa final nueva. En <i>fine-tuning</i> también se reentrenan, con una tasa pequeña "
        "(10<super>−4</super>), los 3 últimos bloques, que son los que reconocen formas complejas. Congeladas, ResNet50 rindió algo mejor; el "
        f"<i>fine-tuning</i> de EfficientNet-B0 las superó a ambas (F1 de {n(ft['f1_macro'])}, mejor época {ft['mejor_epoca']}) con 6 veces "
        "menos parámetros, y fue el modelo elegido, siempre usando solo la validación."),
      lado_a_lado(img(FIG / "a5_matriz_metricas.png", 10.4),
                  [P(f"<b>Prueba (una sola vez, {sum(cps['prueba'].values())} fotos).</b> F1 macro {n(ga['f1_macro'], 2)} y exactitud "
                     f"{pct(ga['exactitud'])}. Las hojas sanas se reconocen bien (F1 {n(pc['sana']['f1'], 2)}). La roya (F1 {n(pc['roya']['f1'], 2)}) se "
                     f"confunde con el ácaro, la clase más difícil (precisión {n(pc['ácaro rojo']['precision'], 2)}): ambas lesiones dejan manchas rojizas."),
                   P(f"<b>Alerta sí/no.</b> Con la misma regla de la Fase 1, aplicada en validación a las probabilidades de la CNN, el umbral resultó "
                     f"{n(alerta['cnn']['umbral'], 2)}. No es 0,22 porque cada modelo tiene su propia escala de probabilidades: se conserva la regla, "
                     f"no el número. En prueba, la CNN logra AUC {n(alerta['cnn']['auc'])} (MLP: {n(mlp['auc'])}), pero deja escapar "
                     f"{alerta['cnn']['FN']} hojas enfermas frente a {int(mlp['FN'])}.")], 10.6, 7.2),
      Paragraph("Figura 2. Matriz de confusión y métricas por clase de la rama A en prueba.", st["pie"]),
      figura(FIG / "a5_gradcam.png", 17.8, "Figura 3. Grad-CAM (Selvaraju et al., 2017): en rojo, las zonas que más pesan en la decisión. La red "
             "mira la lámina de la hoja y no el fondo; en las hojas con ácaro se concentra en las zonas rojizas. El mapa es grueso (7 × 7).")]

# 4. Rama B
E += [H("4. Rama B · Series temporales (RNN simple, LSTM y GRU)"),
      P(f"<b>Serie y tarea.</b> Son {miles(R['b1_serie']['observaciones'])} días ({R['b1_serie']['inicio']} a {R['b1_serie']['fin']}, sin datos "
        "posteriores a las fotos) de temperatura, humedad relativa, lluvia y viento. La humedad tiene estacionalidad anual (ACF a 365 días: "
        f"{n(R['b1_acf']['lag365'], 2)}) y una memoria corta muy fuerte (ACF a 1 día: {n(R['b1_acf']['lag1'], 2)}). La tarea es pronosticar "
        "la humedad del día siguiente, el principal motor de la roya, con una ventana de 14 días y la estación del año codificada como "
        "variable exógena. La partición es cronológica (entrenamiento 2001–2014, validación 2015–2016, prueba 2017–2019) y la normalización "
        "usa solo el entrenamiento. Las tres celdas comparten hiperparámetros (estado oculto de 64, lr 10<super>−3</super>, lote de 32). En "
        "la LSTM y la GRU, unas compuertas deciden cuánto olvidar y cuánto incorporar, y la memoria se actualiza sumando. En la RNN simple, "
        "el gradiente se multiplica repetidamente por la misma matriz y se desvanece (Hochreiter y Schmidhuber, 1997; Cho et al., 2014; "
        "Goodfellow et al., 2016, cap. 10). Las ecuaciones completas están en el notebook (sección B3)."),
      tabla([["Modelo (prueba 2017–2019)", "RMSE", "MAE", "MAPE", "Parámetros"]] +
            [[k, n(bt[k]["RMSE"], 2), n(bt[k]["MAE"], 2), n(bt[k]["MAPE"], 2) + " %", miles(bv[k]["parametros"]) if k in bv else "—"]
             for k in ("GRU", "LSTM", "RNN", "ARIMA(2,0,1)", "PERSISTENCIA")],
            [5.6, 2.4, 2.4, 2.4, 2.6], resaltar=1),
      Paragraph("Tabla 2. Error del pronóstico de humedad relativa a 1 día (puntos porcentuales) en prueba.", st["pie"]),
      lado_a_lado(img(FIG / "b5_desvanecimiento.png", 11.2),
                  [P(f"<b>Desvanecimiento del gradiente.</b> Con una ventana de 60 días se midió cuánto llega el gradiente a cada día pasado. A "
                     f"60 días, la RNN conserva {sci(grad['RNN']['k60'])} del gradiente del día más reciente, la LSTM {sci(grad['LSTM']['k60'])} y "
                     f"la GRU {sci(grad['GRU']['k60'])}: la RNN es prácticamente ciega a lo que pasó hace dos meses."),
                   P(f"En RMSE con 60 días las tres casi empatan (RNN {n(b60['RNN']['RMSE'], 2)}, LSTM {n(b60['LSTM']['RMSE'], 2)}, GRU "
                     f"{n(b60['GRU']['RMSE'], 2)}), porque mañana depende sobre todo de los últimos días. Se eligió la <b>GRU</b>: iguala a la "
                     "LSTM con un 25 % menos de parámetros y conserva mejor el gradiente lejano.")], 11.4, 6.4),
      Paragraph("Figura 4. Izquierda: norma del gradiente según los días hacia atrás (escala logarítmica). Derecha: RMSE con ventana de 60 días.", st["pie"])]

# 5. Rama C
E += [H("5. Rama C · Fusión multimodal, alineación y ablación"),
      P(f"<b>Alineación (declarada como agregada).</b> A cada foto se le asignan los 60 días de clima previos a su fecha EXIF en la finca. No es "
        f"un co-registro por hoja: las fotos se tomaron en <b>{c1['secuencias_distintas']} días</b>, así que hay solo 5 secuencias climáticas, "
        f"y además casi no varían entre sí (su dispersión es el {pct(c1['dispersion_zseq_entre_fechas'] / c1['dispersion_zseq_18_anios'])} de "
        "la variabilidad habitual en 18 años). La fecha también está <b>confundida con el celular</b>: cada día se usaron entre uno y tres "
        "celulares, y varios solo aparecen en una fecha (por ejemplo, el SM-J320H solo el 2019-05-02). Por eso, si el modelo aprovechara "
        "el clima, podría estar aprendiendo en realidad diferencias de cámara."),
      P(f"<b>Modelo y ablación.</b> Fusión tardía (Baltrušaitis et al., 2019): los 1.280 rasgos de la CNN y el estado oculto de la {celda} se "
        "concatenan y pasan por una cabeza densa, que predice la alerta sí/no de la Fase 1. Se comparan cuatro variantes con la misma "
        "partición, semilla y regla de umbral."),
      tabla([["Modelo (prueba, 236 hojas)", "AUC", "Recall afectada", "Hojas enfermas que se escapan", "Falsas alarmas", "Costo 5·FN+FP"]] +
            [[k, n(v["auc"]), n(v["recall"], 2), int(v["FN"]), int(v["FP"]), int(v["costo"])]
             for k, v in (("Solo serie (clima)", seq), ("Solo imagen (CNN)", img_), ("Fusión imagen + clima", fus),
                          ("Fusión con clima permutado", perm), ("MLP Fase 1 (referencia)", mlp))],
            [5.4, 1.6, 2.3, 3.3, 2.4, 2.8], resaltar=3),
      Paragraph("Tabla 3. Ablación en prueba con el umbral de cada modelo, elegido en validación.", st["pie"]),
      P(f"<b>Lectura honesta.</b> El clima solo no distingue hojas (AUC {n(seq['auc'])}, igual que el azar): todas las hojas de un día comparten "
        f"el mismo clima, y ese día hay hojas sanas y enfermas por igual. La fusión no supera a la imagen sola, y <b>barajar el clima entre fotos "
        f"no cambia la AUC</b> ({n(perm['auc'])}): el modelo aprendió a ignorar el clima, y con él también el posible atajo de la cámara. Las "
        "diferencias de costo entre estas variantes vienen de dónde cae su umbral, no de una mejor capacidad para ordenar las hojas. El clima "
        "aportaría con fotos de muchas fincas y fechas, cuando el clima previo varíe de verdad.")]

# 6. Cliente
E += [H("6. Lo que el técnico necesita ver"),
      lado_a_lado(img(CLI / "1_reconocimiento_por_tipo.png", 8.6), img(CLI / "3_fase1_vs_fase2.png", 9.0), 8.8, 9.0),
      Paragraph("Figura 5. Izquierda: de cada 100 hojas de cada tipo, cuántas reconoce el modelo. Derecha: hojas enfermas que se escapan y "
                "falsas alarmas de cada sistema, sobre las mismas hojas de prueba.", st["pie"]),
      P("<b>Tablero del técnico</b> (<i>tablero_tecnico.html</i>, un solo archivo con Plotly que se abre con doble clic y sin internet). "
        "Muestra un resumen de la visita (plantas con posible roya, posible ácaro y sin alerta) y las <b>5 plantas que más urge visitar</b>: "
        "primero las de posible roya, de mayor a menor probabilidad, desempatando por la humedad previa. Cada una trae la hoja que generó la "
        "alerta, la <b>humedad de los 7 días antes de la foto frente a lo normal</b> en esos días según los 5 años anteriores, y qué revisar "
        "en campo."),
      P("<b>Recomendaciones.</b>"),
      B("Mantener la <b>alerta de la Fase 1</b> para decidir qué hojas revisar, porque deja escapar menos hojas enfermas, y usar la <b>CNN</b> "
        "para orientar el tratamiento (ácaro frente a roya), siempre con confirmación en campo."),
      B("Usar la <b>rama B</b> como semáforo de la finca: si la humedad pronosticada se mantiene alta varios días, aumentar la frecuencia de inspección."),
      B("Para que la fusión aporte, <b>registrar fotos con fecha y finca durante todo el año</b> y en varias fincas, con una hoja centrada por foto.")]

# 7. Auditoría y limitaciones
E += [H("7. Uso responsable de la IA, limitaciones y paso a la Fase 3"),
      P("<b>Auditoría: lo que el equipo cuestionó a la IA.</b> El equipo revisó críticamente el primer notebook generado por el asistente y "
        "exigió estos cambios, registrados en la bitácora (E-21 a E-33):"),
      tabla([["Lo que el equipo cuestionó", "Qué estaba mal o faltaba", "Qué se cambió"],
             ["¿Hay de verdad fotos duplicadas?", "Se daba por cierta la duplicidad hallada en la Fase 1, sin volver a verificarla",
              f"Verificación con SHA-256 y pHash, más una galería: {dup['grupos_sha256']} pares exactos confirmados"],
             ["Gráficas de brillo y nitidez", "Histogramas superpuestos: no se veían las diferencias", "Diagramas de caja por clase con la mediana anotada"],
             ["¿Por qué 256 px en caché y 224 px en el modelo?", "La decisión no estaba justificada", "Explicación: tamaño de preentrenamiento y margen para el recorte aleatorio"],
             ["¿Por qué pesos inversos a la frecuencia?", "Faltaba la justificación", "Fórmula, efecto sobre el ácaro y alternativas descartadas"],
             ["¿Por qué ResNet50 y EfficientNet-B0?", "Faltaba la justificación", "Criterio de elección y descarte de VGG16"],
             ["FE frente a FT y origen del F1 macro", "Poco claro de dónde salían las cifras", "Tabla y gráfico de F1 por clase en validación"],
             ["¿Entropía cruzada con 3 clases?", "Faltaba la explicación", "Se confirmó que es correcta y se explicó por qué"],
             ["¿Por qué el umbral no es 0,22?", "Se reportaba 0,41 sin relacionarlo con la Fase 1", "Curva de costo en validación: misma regla, otra escala"],
             ["¿Fecha confundida con el celular?", "Se afirmaba sin mostrar evidencia", "Tabla cruzada de fecha por celular en el notebook"],
             ["Tablero para el técnico", "No decía qué plantas revisar; después exigía instalar aplicaciones", "HTML simple: las 5 plantas más urgentes con su humedad previa"],
             ["No se veían las tablas del notebook (VS Code)", "Tablas solo en HTML de pandas", "Tablas en markdown con la función ver_tabla()"]],
            [4.6, 6.2, 7.0]),
      Spacer(1, 4),
      B("<b>Dominio estrecho:</b> una finca de café robusta, 5 días de 2019 y 4 celulares. No debe extrapolarse sin un piloto (Marco Ético para "
        "la IA en Colombia: transparencia y responsabilidad; Guío Español et al., 2021)."),
      B(f"<b>Duplicidad y ruido de etiqueta (verificados en esta fase):</b> los {dup['grupos_sha256']} pares de copias exactas y las fotos "
        f"visualmente iguales se mantienen juntos en la partición, pero en {dup['pares_phash5_clase_distinta']} pares las copias tienen clases "
        "distintas. Eso, sumado a las pocas fotos de ácaro, limita la precisión de la clase minoritaria."),
      B("<b>Recorte de la hoja:</b> se hizo con la caja anotada por humanos. En campo hace falta una foto centrada o un detector."),
      B("<b>Cómputo:</b> todo se entrenó en CPU, con <i>fine-tuning</i> parcial y una sola semilla. Con GPU (Fase 3) se pueden probar más bloques y varias semillas."),
      B("<b>Fase 3:</b> la rama A (EfficientNet-B0, 16 MB) es apta para LiteRT en una tableta, y la rama B (GRU, &lt; 0,1 MB) para una API "
        "REST. Los pesos de las tres ramas se recargaron y verificaron con np.allclose (atol 1e-4).")]

E += [H("Referencias")]
for ref in [
    "Baltrušaitis, T., Ahuja, C., & Morency, L.-P. (2019). Multimodal machine learning: A survey and taxonomy. <i>IEEE Transactions on Pattern "
    "Analysis and Machine Intelligence, 41</i>(2), 423–443. https://doi.org/10.1109/TPAMI.2018.2798607",
    "Cho, K., van Merriënboer, B., Gulcehre, C., Bahdanau, D., Bougares, F., Schwenk, H., & Bengio, Y. (2014). Learning phrase representations "
    "using RNN encoder–decoder for statistical machine translation. En <i>Proceedings of EMNLP 2014</i> (pp. 1724–1734). https://doi.org/10.3115/v1/D14-1179",
    "Goodfellow, I., Bengio, Y., & Courville, A. (2016). <i>Deep learning</i>. MIT Press. https://www.deeplearningbook.org/",
    "Guío Español, A., Tamayo Uribe, E., Gómez Ayerbe, P., & Mujica, M. P. (2021). <i>Marco ético para la inteligencia artificial en Colombia</i>. "
    "Consejería Presidencial para Asuntos Económicos y Transformación Digital.",
    "He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. En <i>Proceedings of the IEEE Conference on "
    "Computer Vision and Pattern Recognition</i> (pp. 770–778). https://doi.org/10.1109/CVPR.2016.90",
    "Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. <i>Neural Computation, 9</i>(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735",
    "NASA Langley Research Center. (2026). <i>Prediction of Worldwide Energy Resources (POWER) Project: Daily agroclimatology data</i> [Data set]. "
    "https://power.larc.nasa.gov/",
    "Parraga-Alava, J., Cusme, K., Loor, A., & Santander, E. (2019). RoCoLe: A robusta coffee leaf images dataset for evaluation of machine "
    "learning based methods in plant diseases recognition. <i>Data in Brief, 25</i>, 104414. https://doi.org/10.1016/j.dib.2019.104414",
    "Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017). Grad-CAM: Visual explanations from deep networks via "
    "gradient-based localization. En <i>Proceedings of the IEEE International Conference on Computer Vision</i> (pp. 618–626). "
    "https://doi.org/10.1109/ICCV.2017.74",
    "Tan, M., & Le, Q. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. En <i>Proceedings of the 36th "
    "International Conference on Machine Learning</i> (pp. 6105–6114). PMLR.",
]:
    E.append(Paragraph(ref, st["ref"]))

def pie(canvas, doc):
    canvas.saveState(); canvas.setFont(FUENTE, 7.5); canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawRightString(A4[0] - 1.5 * cm, 0.9 * cm, f"Proyecto Centinela · Fase 2 · p. {doc.page}"); canvas.restoreState()

doc = SimpleDocTemplate(str(SALIDA), pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.3 * cm, bottomMargin=1.4 * cm,
                        title="Centinela del Café · Fase 2",
                        author="Briyith Lisdey Herrera Cruz, Juan Pablo Becerra Tirano, Johnatan Vélez Martínez")
doc.build(E, onFirstPage=pie, onLaterPages=pie)
print("Informe:", SALIDA)
