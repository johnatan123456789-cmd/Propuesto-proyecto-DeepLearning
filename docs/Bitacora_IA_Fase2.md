# Bitácora de IA · Proyecto Centinela · Fase 2

> **Nota.** La numeración de la fase 2 continúa a partir de E7, que corresponde al último registro de la fase 1.

## 1. Datos de la entrega

| Campo | Detalle |
|---|---|
| Integrantes | Briyith Lisdey Herrera Cruz · Juan Pablo Becerra Tirano · Johnatan Vélez Martínez |
| Proyecto | Centinela del Café · Fase 2 (CNN + LSTM/GRU + fusión) |
| Identificador inicial | E-8 |
| Fecha de entrega | `[2026-11-14]` |

## 2. Declaración de uso

| Herramienta | Modelo | Propósito |
|---|---|---|
| Claude Code (aplicación de escritorio, Anthropic) | Claude Opus 5.5 | Leer la actividad, diseñar las tres ramas, escribir y ejecutar el notebook, el informe, el tablero y esta bitácora |

- **Datos compartidos:** el asistente ejecutó código local sobre RoCoLe (imágenes de hojas, sin personas) y NASA POWER (clima público). El campo `Created By` no se usa.


## 3. Registro de interacciones

### Sesión 1 (2026-11-11): construcción inicial

| ID | Qué propuso o devolvió la IA | Decisión | Justificación |
|---|---|---|---|
| **E-8** | Detectó que la actividad dice: *"Ese escenario queda vetado como entrega… no supera la compuerta de la Propuesta de Datos"*, y **recomendó consultar al docente antes de construir** | **Rechazada** (se continuó) | La Fase 1 se construyó sobre RoCoLe. El equipo decidió diferenciar el problema (3 clases, pronóstico de humedad, alineación medida y permutación) y declarar el riesgo <img width="766" height="274" alt="E8" src="https://github.com/user-attachments/assets/6a1ed621-7f4a-4112-94c1-b50d6689055d" />|
| **E-9** | Agrupar las 6 clases en 3: sana / ácaro rojo / roya (niveles 1–4) | **Aceptada** | La actividad pide al menos 3 categorías. Los niveles 3 y 4 de roya tienen 62 y 30 fotos |
| **E-10** | Entregar a la CNN la hoja recortada con su caja anotada, no la foto completa | **Aceptada con limitación** | El fondo trae otras hojas, a veces enfermas. En campo hará falta una foto centrada o un detector |
| **E-11** | Comparar ResNet50 y EfficientNet-B0 en *feature extraction* y hacer *fine-tuning* parcial de EfficientNet-B0 | **Aceptada** | El *fine-tuning* subió el F1 macro de validación a 0,711, frente a 0,665 y 0,647 de las redes congeladas |
| **E-12** | Rama B: pronosticar la humedad a 1 día con 18 años de NASA POWER, partición cronológica y líneas base ARIMA y persistencia | **Aceptada** | La humedad es el motor de la roya; GRU y LSTM (RMSE 2,25) superan a ARIMA (2,49) |
| **E-13** | Reportar los resultados negativos: la fusión no mejora y la CNN no supera al MLP en costo | **Aceptada** | La actividad valora el análisis honesto; la prueba de permutación lo respalda |

### Sesiones 2 y 3 (2026-11-12 y 2026-11-14): revisión crítica del equipo

| ID | Qué cuestionó el equipo | Qué había entregado la IA | Decisión | Qué se cambió |
|---|---|---|---|---|
| **E-14** | "¿Efectivamente hay fotos duplicadas? Compruébalo con pHash" | Daba por cierta la duplicidad de la Fase 1 sin volver a verificarla | **Modificada** | Nueva §0.1: SHA-256 + pHash + galería visual. Resultado: 67 pares exactos y 82 pares con pHash ≤ 5. Se comprueba con `assert` que ningún par queda repartido <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/8ddb7772-1fc3-43a9-b389-4cb0525891b0" />|
| **E-15** | "Las gráficas de brillo y nitidez se solapan" | Histogramas superpuestos de 3 clases | **Modificada** | Diagramas de caja por clase con la mediana anotada<img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/bddc2008-c0b2-4913-9ebe-7b5ecdf5a78c" /> |
| **E-16** | "¿Por qué 256 px en caché y 224 px en el modelo?" | La decisión no estaba explicada | **Modificada** | Explicación en §A2: 224 es el tamaño de ImageNet y 256 deja margen al recorte aleatorio; la evaluación no usa azar <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/808061bd-f78f-4e0b-81c0-300783adb4a2" /> |
| **E-17** | "¿Por qué pesos inversos a la frecuencia?" | Pesos sin justificar | **Modificada** | Fórmula, efecto (el ácaro pesa unas 3 veces) y alternativas descartadas (sobremuestreo y *focal loss*) <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/c3bef356-6d91-487b-af04-c5919c69fb9d" /> |
| **E-18** | "¿Por qué ResNet50 y EfficientNet-B0?" | Sin justificar la elección | **Modificada** | Criterio: referencia clásica frente a eficiente para la Fase 3; VGG16 descartada <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/13c4f404-5490-47b8-9a8a-1a69ca7f42e2" /> |
| **E-19** | "No es claro FE frente a FT, ni de dónde sale el F1 macro" | Una tabla sin contexto | **Modificada** | Tabla comparativa FE/FT con analogía, definición del F1 macro y gráfico de F1 por clase en validación <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/1fe747d8-0184-4a14-9cfa-36e8530f41f3" /> |
| **E-20** | "¿Es correcta la entropía cruzada con 3 clases?" | No se explicaba | **Aceptada (se mantuvo) + documentada** | Es la generalización categórica de la BCE (softmax + log-verosimilitud), con pesos de clase<img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/fbe51f4f-5bb9-48d2-9fbd-b6534ee4b171" /> |
| **E-21** | "¿De dónde sale el umbral 0,41 si en la Fase 1 fue 0,22?" | Reportaba el umbral sin relacionarlo con la Fase 1 | **Modificada** | Curva de costo en validación: se mantiene la misma regla, pero cada modelo tiene su escala de probabilidad <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/26a7c1c9-2b21-4cd9-ba42-daf84edf2fcc" />|
| **E-22** | "¿Cómo es eso de que la fecha está confundida con el celular?" | Lo afirmaba sin evidencia | **Modificada** | Tabla cruzada de fecha por celular en §C1, con explicación<img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/e29d1c85-f527-49e0-be69-41f3c5706fc6" /> |
| **E-23** | "El tablero no le sirve al técnico" | Tablero Plotly con 4 gráficos generales | **Rechazada** (el diseño) | Se rediseñó como aplicación Streamlit, con plantas a revisar y foto subida<img width="735" height="227" alt="E23" src="https://github.com/user-attachments/assets/3e507bee-8110-4b30-a92a-3c0a52fd446e" /> |
| **E-24** | "Elimina el comentario de C2b" | Sección de auditoría de la cabeza de fusión | **Rechazada** | Se eliminó la sección; la configuración final queda justificada en §C2 <img width="628" height="571" alt="E18_28" src="https://github.com/user-attachments/assets/3fcab1b9-8e71-4244-b82b-5ee4bcb54c09" />|
| **E-25** | "Subir la foto requiere más aplicaciones; quiero un HTML con Plotly, simple y no técnico, con el top 5 de plantas a visitar y la humedad previa" | Aplicación Streamlit (requería Python, PyTorch y un servidor) | **Rechazada** | Tablero en un único HTML con Plotly (`app/generar_tablero.py` → `tablero_tecnico.html`): resumen de la visita, las 5 plantas más urgentes (roya primero; empates resueltos por la humedad previa), la hoja, la humedad de los 7 días previos frente a lo normal en 5 años y qué hacer<img width="836" height="220" alt="E25_26" src="https://github.com/user-attachments/assets/7669eef4-517f-4e7a-83b0-b584411ab90b" /> |
| **E-26** | "No veo las tablas del notebook" (en VS Code) | Tablas de pandas en HTML | **Modificada** | Función `ver_tabla()`: cada tabla se entrega en markdown, que VS Code, Jupyter y Colab renderizan siempre <img width="836" height="220" alt="E25_26" src="https://github.com/user-attachments/assets/a38bc015-517e-4c18-8725-0c86f990ef6f" /> |

## 4. Auditoría a la IA

**Tipo:** real. Son fallos detectados por el equipo al revisar el trabajo del asistente.

| Campo | Contenido |
|---|---|
| Entradas relacionadas | E-14 (duplicados), E-21 (umbral) y E-22 (confusión fecha–celular) |
| Contexto | Revisión del primer notebook de la Fase 2 entregado por la IA |
| Qué dijo la IA | (1) Asumió la duplicidad de la Fase 1 sin volver a verificarla. (2) Reportó un umbral de alerta de 0,41 sin explicar por qué difiere del 0,22 de la Fase 1. (3) Afirmó que la fecha está confundida con el celular sin mostrar la evidencia |
| Por qué estaba mal | (1) Una conclusión heredada debe volver a comprobarse cuando cambia el pipeline: ahora se usa la imagen completa de la hoja, no rasgos. (2) Sin la curva de costo, el lector podía creer que se cambió la regla de decisión. (3) Una afirmación sin evidencia no es verificable, y es la base para justificar la prueba de permutación |
| Cómo se detectó | Preguntas directas del equipo al revisar el notebook |
| Corrección aplicada | (1) §0.1, con SHA-256, pHash, galería y `assert` sobre la partición. (2) §A5, curva de costo en validación con ambos umbrales marcados. (3) §C1, tabla cruzada de fecha por celular |
| Resultado de medición | (1) Se confirmaron 67 pares exactos y 82 pares con pHash ≤ 5, y ninguno repartido entre subconjuntos. (2) El umbral 0,41 es el mínimo de costo en validación; 0,22 aplicado a la CNN no es comparable. (3) Por ejemplo, el SM-J320H solo aparece el 2019-05-02 y el SM-G610M solo el 2019-04-11 |
| Lección | La IA tiende a **heredar conclusiones y afirmar sin mostrar**. Cada cifra o afirmación del notebook debe tener una celda que la produzca |

## 5. Firmas

| Integrante | | Fecha |
|---|---|---|
| Briyith Lisdey Herrera Cruz | | `[2026-11-14]` |
| Juan Pablo Becerra Tirano | | `[2026-11-14]` |
| Johnatan Vélez Martínez | | `[2026-11-14]` |
