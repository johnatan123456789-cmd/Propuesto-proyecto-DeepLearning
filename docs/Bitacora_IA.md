# Bitácora de IA · Proyecto Centinela

> **Nota para el equipo.** Esta bitácora la redactó el asistente a partir de lo que ocurrió en la sesión del 2026-11-04. Cada integrante debe revisarla, completar los campos `[ ]` (hora, integrante, captura) y **confirmar o cambiar la decisión**: la decisión y su justificación tienen que ser del equipo. Las entradas remiten a celdas con la etiqueta de sección del notebook.

## 1. Datos de la entrega

| Campo | Detalle |
|---|---|
| Integrantes | Briyith Lisdey Herrera Cruz · Juan Pablo Becerra Tirano · Johnatan Vélez Martínez |
| Proyecto | Centinela del Café (hoja afectada sí/no, RoCoLe) |
| Fase | 1 |
| Identificador inicial | E-1 |
| Fecha de entrega | `[2026-11-04]` |

## 2. Declaración de uso (Opción A)

| Herramienta | Modelo y versión | Propósito |
|---|---|---|
| Claude Code (aplicación de escritorio, Anthropic) | Claude Opus 5.5 (`claude-opus-5-5`) | Reestructurar el repositorio por el cambio de dataset; diseñar el flujo; escribir el notebook, el generador del informe y los documentos; inspeccionar los datos localmente |

- **Partes redactadas sin IA:** `[completar: p. ej., la decisión de las D1–D5, el contacto con los autores del dataset de cacao, la búsqueda en Kaggle]`.
- **Datos compartidos con la IA:** el asistente ejecutó código local sobre `data/raw/`. Vio nombres de archivo, conteos, la estructura de columnas y valores de ejemplo de las anotaciones (polígonos y URL de Labelbox). **Los valores de `Created By` se omitieron explícitamente** en todas las inspecciones y nunca se mostraron. No hay datos personales en las imágenes.
- **Firmas:** `[cada integrante, con fecha]`.

## 3. Registro de interacciones

### E-1 · Reestructuración inicial y primer flujo

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 0 (Propuesta) |
| Integrante | `[nombre]` |
| Herramienta y modelo | Claude Code · Claude Opus 5.5 |
| Celda o *commit* | `README.md`, `Propuesta_de_datos.md`, `docs/flujo_logico_fase1.md` · `# E-1` |
| Objetivo | Documentar el cambio de dataset (cacao → RoCoLe) y proponer el flujo de la Fase 1 |
| Indicación (resumen) | Ajustar el README por el cambio de dataset, aplicar las plantillas 11–14 y entregar el diagrama sin desarrollar la fase |
| Qué devolvió la IA | README v2, Propuesta v2 y diagrama de 19 pasos con las decisiones D1–D4. Propuso como objetivo "roya vs no roya" |
| Datos compartidos | Ninguno (solo URL públicas) |
| Decisión | **Modificada** |
| Justificación | El equipo cambió D1 a "hoja afectada" (sana vs ácaro o roya), D3 a 60 días y D5 a organizaciones de monitoreo fitosanitario, y pidió detallar el EDA |
| Cómo se verificó | Revisión del equipo contra la rúbrica v1.4 |
| Evidencia de origen | Salida literal de la IA: *"D1 · Objetivo binario: Roya (1–4) vs no roya (sana + ácaro)"* `<img width="942" height="698" alt="E1 E2" src="https://github.com/user-attachments/assets/463e6b8c-bb24-47c2-a28d-26b95566b427" />
` |

### E-2 · Afirmación no verificada sobre trabajos previos

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 0 (Propuesta §4) |
| Celda o *commit* | `Propuesta_de_datos.md` §4 · `# E-2` |
| Objetivo | Argumentar por qué no es un reto resuelto |
| Qué devolvió la IA | *"No hay una solución pública que una RoCoLe con clima. Los trabajos publicados son clasificadores solo de imagen."* |
| Datos compartidos | Ninguno |
| Decisión | **Rechazada** (la afirmación) / **Modificada** (el texto) |
| Justificación | Era una afirmación sin búsqueda que la respaldara. Se reemplazó por la evidencia del Anexo B: los 3 notebooks de Kaggle que encontró el equipo |
| Cómo se verificó | Búsqueda del equipo en Kaggle → 3 coincidencias (Anexo B) |
| Evidencia de origen | Texto literal arriba (respuesta 1 de la sesión) `<img width="942" height="698" alt="E1 E2" src="https://github.com/user-attachments/assets/33240272-ab88-4318-bebf-dc2aa41d2fb7" />
>
` |

### E-3 · Inspección del dataset descargado

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 1 |
| Celda o *commit* | Notebook §1.2–1.3, §2.1–2.5 · `# E-3` |
| Objetivo | Verificar la clave temporal, la estructura de las anotaciones y los duplicados |
| Qué devolvió la IA | Encontró fechas EXIF en las 1.560 imágenes (5 días), 4 celulares, el patrón de nombre `C<n>P<n><H/E><n>`, 390 plantas × 4, 67 grupos de duplicados byte a byte, un nombre anómalo y 0 GPS. Detectó que los polígonos están en coordenadas crudas, comprobado con una superposición visual |
| Datos compartidos | Esquema y nombres de columnas; `Created By` omitido |
| Decisión | **Aceptada** |
| Justificación | Las cifras se reproducen en el notebook y coinciden con el artículo (791 / 344 / 166 / 62 / 30 / 167) |
| Cómo se verificó | El notebook §1.3 compara JSON y XLSX: la clase multiclase coincide en el 100 % de las fotos (`assert`) |
| Evidencia de origen | Salidas de las celdas §2.2, §2.4 y §2.5 |


### E-4 · Partición desbalanceada por grupos grandes

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 1 (partición) |
| Celda o *commit* | Notebook §6 · `# E-5` |
| Qué devolvió la IA | Asignó los pliegues 14/3/3 por índice con `StratifiedGroupKFold(20)` |
| Decisión | **Modificada** |
| Justificación | La partición resultó en 64,9 / 21,5 / 13,6 % porque hay un grupo de 92 imágenes. Se eligieron los pliegues por tamaño, sin usar la etiqueta |
| Cómo se verificó | Nueva partición: 70,0 / 14,9 / 15,1 %, con `assert` de cero grupos compartidos |
| Evidencia de origen | Salida de la primera ejecución: `pct_imagenes` 0,649 / 0,215 / 0,136 `<img width="725" height="102" alt="E5" src="https://github.com/user-attachments/assets/942b6b82-d101-406d-bbc4-34d2854f3d18" />
` |

### E-5 · Auditoría inducida de la partición por imagen

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 6 |
| Celda o *commit* | Notebook §13.2 · `# E-6` |
| Qué devolvió la IA | La celda reproducible que compara la partición ingenua con la agrupada |
| Decisión | **Aceptada** |
| Justificación | Cuantifica la fuga estructural (99,1 % de las imágenes de prueba con una hermana en entrenamiento; 20 copias exactas) |
| Cómo se verificó | Misma semilla y misma regla de umbral; ver `resultados.json → auditoria` |
| Evidencia de origen | Salida de la celda §13.2 |


### E-6 · Simplificación del notebook y exploración inicial

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Pasos 1–2 |
| Celda o *commit* | Notebook completo (§1–§3 rehechas) · `# E-8` |
| Objetivo | Que el flujo empiece por cómo vienen los datos y explique qué variables se agregan y por qué |
| Qué devolvió la IA (versión anterior) | Un EDA que empezaba directamente por los 28 rasgos derivados, sin mostrar cuántas plantas, hojas o fotos sanas y afectadas había, y con código denso (funciones genéricas, reasignación de variables globales) |
| Decisión | **Modificada** a pedido del equipo |
| Justificación | El EDA debe partir de los datos crudos. Ahora muestra 12 cultivos, 390 plantas, 1.560 fotos, unas 780 hojas inferidas, el balance 791/769 y la tabla de variables iniciales antes de construir los rasgos |
| Cómo se verificó | Ejecución completa desde cero sin errores. Las métricas finales son idénticas a las de la versión anterior (R3a, umbral 0,22, costo 54, AUC 0,936) |
| Evidencia de origen | Solicitud del equipo en la sesión del 2026-11-05 `<img width="800" height="354" alt="E8" src="https://github.com/user-attachments/assets/89cdc6d3-057f-471f-ba36-46817e776dfe" />
` |

### E-7 · Eliminar duplicados (rechazada)

| Campo | Contenido |
|---|---|
| Fecha | 2026-11-04 |
| Fase · paso | F1 · Paso 1 (datos) |
| Celda o *commit* | Notebook §2.5 y §5.2 · `# E-9` |
| Qué devolvió la IA | Identificar los duplicados de las imágenes y eliminarlos para evitar posibles fugas byte a byte |
| Datos compartidos | Ninguno |
| Decisión | **Rechazada** |
| Justificación | Con datos tabulares no es recomendable eliminar duplicados. La comparación de filas no reconoce el contexto ni las vecindades, como sí se hace en las imágenes, y es potencialmente riesgoso eliminar registros que no son realmente duplicados. Además, 27 de los 67 grupos de copias exactas tienen clases distintas |
| Cómo se verificó | El notebook conserva las 1.560 fotos. Los duplicados solo se usan para agrupar la partición (`assert` en §6) |
| Evidencia de origen | `<img width="669" height="88" alt="E9" src="https://github.com/user-attachments/assets/d24b00b0-3834-4ad3-9d13-cdb9aa25b4da" />
`
<img width="681" height="96" alt="E9 -2" src="https://github.com/user-attachments/assets/84233e23-3089-47e4-93dd-5906b84839cb" />
|
