# Bitácora de IA · Proyecto Centinela · Fase 2

> **Nota para el equipo.** Esta bitácora la redactó el asistente a partir de lo ocurrido en las sesiones del 2026-11-11 y del 2026-11-12. Revísenla, completen los campos `[ ]` (hora, integrante, captura) y **confirmen o cambien cada decisión**: deben poder defenderlas en la sustentación. La numeración continúa la de la Fase 1 (E-1 a E-10).

## 1. Datos de la entrega

| Campo | Detalle |
|---|---|
| Integrantes | Briyith Lisdey Herrera Cruz · Juan Pablo Becerra Tirano · Johnatan Vélez Martínez |
| Proyecto | Centinela del Café · Fase 2 (CNN + LSTM/GRU + fusión) |
| Identificador inicial | E-11 |
| Fecha de entrega | `[AAAA-MM-DD]` |

## 2. Declaración de uso

| Herramienta | Modelo | Propósito |
|---|---|---|
| Claude Code (aplicación de escritorio, Anthropic) | Claude Opus 5.5 | Leer la actividad, diseñar las tres ramas, escribir y ejecutar el notebook, el informe, el tablero y esta bitácora |

- **Datos compartidos:** el asistente ejecutó código local sobre RoCoLe (imágenes de hojas, sin personas) y NASA POWER (clima público). El campo `Created By` no se usa.
- **Partes hechas sin IA:** `[completar]`.

## 3. Registro de interacciones

### Sesión 1 (2026-11-11): construcción inicial

| ID | Qué propuso o devolvió la IA | Decisión | Justificación |
|---|---|---|---|
| **E-11** | Detectó que la actividad dice: *"Ese escenario queda vetado como entrega… no supera la compuerta de la Propuesta de Datos"*, y **recomendó consultar al docente antes de construir** | **Rechazada** (se continuó) | La Fase 1 se construyó sobre RoCoLe. El equipo decidió diferenciar el problema (3 clases, pronóstico de humedad, alineación medida y permutación) y declarar el riesgo |
| **E-12** | Agrupar las 6 clases en 3: sana / ácaro rojo / roya (niveles 1–4) | **Aceptada** | La actividad pide al menos 3 categorías. Los niveles 3 y 4 de roya tienen 62 y 30 fotos |
| **E-13** | Entregar a la CNN la hoja recortada con su caja anotada, no la foto completa | **Aceptada con limitación** | El fondo trae otras hojas, a veces enfermas. En campo hará falta una foto centrada o un detector |
| **E-14** | Comparar ResNet50 y EfficientNet-B0 en *feature extraction* y hacer *fine-tuning* parcial de EfficientNet-B0 | **Aceptada** | El *fine-tuning* subió el F1 macro de validación a 0,711, frente a 0,665 y 0,647 de las redes congeladas |
| **E-15** | Rama B: pronosticar la humedad a 1 día con 18 años de NASA POWER, partición cronológica y líneas base ARIMA y persistencia | **Aceptada** | La humedad es el motor de la roya; GRU y LSTM (RMSE 2,25) superan a ARIMA (2,49) |
| **E-16** | `serie.index.get_loc(fecha)` para ubicar la fecha de cada foto | **Modificada** | La serie termina el 2019-05-01 y la última foto es del 2019-05-02, así que `get_loc` fallaba. Si se "arreglaba" incluyendo el día de la foto, se usaría clima del mismo día. Se cambió a `searchsorted`, que garantiza que la ventana termine el día anterior |
| **E-17** | Guardar en el *checkpoint* el F1 como `numpy.float64` y recargarlo con `torch.load` por defecto | **Modificada** | Error `UnpicklingError` con `weights_only=True`. Se convirtió a `float` |
| **E-18** | `groupby([...]).size().to_dict()` en el JSON de resultados | **Modificada** | JSON no admite claves de tupla; se cambió a texto `"real → pred"` |
| **E-19** | Cabeza de fusión con lr 10⁻³, sin Dropout de entrada y con una vista por foto | **Modificada** | La parada temprana elegía la época 1. Se usaron lr 3·10⁻⁴, Dropout 0,5 y 3 vistas aumentadas (justificado en §C2 del notebook). La mejora fue pequeña (pérdida mínima de validación de 0,298 a 0,291) |
| **E-20** | Reportar los resultados negativos: la fusión no mejora y la CNN no supera al MLP en costo | **Aceptada** | La actividad valora el análisis honesto; la prueba de permutación lo respalda |

### Sesión 2 (2026-11-12): revisión crítica del equipo

| ID | Qué cuestionó el equipo | Qué había entregado la IA | Decisión | Qué se cambió |
|---|---|---|---|---|
| **E-21** | "¿Efectivamente hay fotos duplicadas? Compruébalo con pHash" | Daba por cierta la duplicidad de la Fase 1 sin volver a verificarla | **Modificada** | Nueva §0.1: SHA-256 + pHash + galería visual. Resultado: 67 pares exactos y 82 pares con pHash ≤ 5. Se comprueba con `assert` que ningún par queda repartido |
| **E-22** | "Las gráficas de brillo y nitidez se solapan" | Histogramas superpuestos de 3 clases | **Modificada** | Diagramas de caja por clase con la mediana anotada |
| **E-23** | "¿Por qué 256 px en caché y 224 px en el modelo?" | La decisión no estaba explicada | **Modificada** | Explicación en §A2: 224 es el tamaño de ImageNet y 256 deja margen al recorte aleatorio; la evaluación no usa azar |
| **E-24** | "¿Por qué pesos inversos a la frecuencia?" | Pesos sin justificar | **Modificada** | Fórmula, efecto (el ácaro pesa unas 3 veces) y alternativas descartadas (sobremuestreo y *focal loss*) |
| **E-25** | "¿Por qué ResNet50 y EfficientNet-B0?" | Sin justificar la elección | **Modificada** | Criterio: referencia clásica frente a eficiente para la Fase 3; VGG16 descartada |
| **E-26** | "No es claro FE frente a FT, ni de dónde sale el F1 macro" | Una tabla sin contexto | **Modificada** | Tabla comparativa FE/FT con analogía, definición del F1 macro y gráfico de F1 por clase en validación |
| **E-27** | "¿Es correcta la entropía cruzada con 3 clases?" | No se explicaba | **Aceptada (se mantuvo) + documentada** | Es la generalización categórica de la BCE (softmax + log-verosimilitud), con pesos de clase |
| **E-28** | "¿De dónde sale el umbral 0,41 si en la Fase 1 fue 0,22?" | Reportaba el umbral sin relacionarlo con la Fase 1 | **Modificada** | Curva de costo en validación: se mantiene la misma regla, pero cada modelo tiene su escala de probabilidad |
| **E-29** | "¿Cómo es eso de que la fecha está confundida con el celular?" | Lo afirmaba sin evidencia | **Modificada** | Tabla cruzada de fecha por celular en §C1, con explicación |
| **E-30** | "El tablero no le sirve al técnico" | Tablero Plotly con 4 gráficos generales | **Rechazada** (el diseño) | Se rediseñó como aplicación Streamlit, con plantas a revisar y foto subida |
| **E-32** | "Subir la foto requiere más aplicaciones; quiero un HTML con Plotly, simple y no técnico, con el top 5 de plantas a visitar y la humedad previa" | Aplicación Streamlit (requería Python, PyTorch y un servidor) | **Rechazada** | Tablero en un único HTML con Plotly (`app/generar_tablero.py` → `tablero_tecnico.html`): resumen de la visita, las 5 plantas más urgentes (roya primero; empates resueltos por la humedad previa), la hoja, la humedad de los 7 días previos frente a lo normal en 5 años y qué hacer |
| **E-33** | "No veo las tablas del notebook" (en VS Code) | Tablas de pandas en HTML | **Modificada** | Función `ver_tabla()`: cada tabla se entrega en markdown, que VS Code, Jupyter y Colab renderizan siempre |
| **E-31** | "Elimina el comentario de C2b" | Sección de auditoría de la cabeza de fusión | **Rechazada** | Se eliminó la sección; la configuración final queda justificada en §C2 (E-19) |

## 4. Auditoría a la IA

**Tipo:** real. Son fallos detectados por el equipo al revisar el trabajo del asistente.

| Campo | Contenido |
|---|---|
| Entradas relacionadas | E-21 (duplicados), E-28 (umbral) y E-29 (confusión fecha–celular) |
| Contexto | Revisión del primer notebook de la Fase 2 entregado por la IA |
| Qué dijo la IA | (1) Asumió la duplicidad de la Fase 1 sin volver a verificarla. (2) Reportó un umbral de alerta de 0,41 sin explicar por qué difiere del 0,22 de la Fase 1. (3) Afirmó que la fecha está confundida con el celular sin mostrar la evidencia |
| Por qué estaba mal | (1) Una conclusión heredada debe volver a comprobarse cuando cambia el pipeline: ahora se usa la imagen completa de la hoja, no rasgos. (2) Sin la curva de costo, el lector podía creer que se cambió la regla de decisión. (3) Una afirmación sin evidencia no es verificable, y es la base para justificar la prueba de permutación |
| Cómo se detectó | Preguntas directas del equipo al revisar el notebook |
| Corrección aplicada | (1) §0.1, con SHA-256, pHash, galería y `assert` sobre la partición. (2) §A5, curva de costo en validación con ambos umbrales marcados. (3) §C1, tabla cruzada de fecha por celular |
| Resultado de medición | (1) Se confirmaron 67 pares exactos y 82 pares con pHash ≤ 5, y ninguno repartido entre subconjuntos. (2) El umbral 0,41 es el mínimo de costo en validación; 0,22 aplicado a la CNN no es comparable. (3) Por ejemplo, el SM-J320H solo aparece el 2019-05-02 y el SM-G610M solo el 2019-04-11 |
| Lección | La IA tiende a **heredar conclusiones y afirmar sin mostrar**. Cada cifra o afirmación del notebook debe tener una celda que la produzca |

## 5. Firmas

| Integrante | Declaro que revisé y entiendo cada decisión | Fecha |
|---|---|---|
| Briyith Lisdey Herrera Cruz | `[firma]` | `[AAAA-MM-DD]` |
| Juan Pablo Becerra Tirano | `[firma]` | `[AAAA-MM-DD]` |
| Johnatan Vélez Martínez | `[firma]` | `[AAAA-MM-DD]` |
