# Screencast AA5 (FP502) — Grupo 10

**Asignatura:** Big Data I (FP502)
**Máster FP en Inteligencia Artificial y Big Data — UOC**
**Duración objetivo:** 4-5 min (target real: ~5:00)
**Modo de grabación:** asíncrono — cada integrante graba su bloque por separado y Adrián monta el vídeo final en iMovie

---

## Integrantes y reparto

| Integrante | Rol | Bloque(s) que graba |
| --- | --- | --- |
| Adrián Blasco Lozano | Rol 4 — Documentación + edición | Bloque 0a (Intro) + Bloque 4 (Conclusión) |
| Antonio Sala Llaudis | Rol 2 — Datos | Bloque 0b (Caso de negocio) |
| Enric Gil Baquero | Rol 1 — Infraestructura | Bloque 1 (Arquitectura) |
| Hugo Romero Casado | Rol 3 — Query y rendimiento | Bloque 2 (Demo) + Bloque 3 (EXPLAIN) |

## Resumen de tiempos

| Bloque | Tiempo | Acumulado | Ponente |
| --- | --- | --- | --- |
| 0a — Intro | 15s | 0:15 | Adrián |
| 0b — Caso de negocio | 15s | 0:30 | Antonio |
| 1 — Arquitectura | 60s | 1:30 | Enric |
| 2 — Demostración | 120s | 3:30 | Hugo |
| 3 — Análisis del EXPLAIN | 60s | 4:30 | Hugo |
| 4 — Conclusión | 30s | 5:00 | Adrián |

> **Importante:** la rúbrica premia cumplir estrictamente el tiempo y penaliza excederse o quedarse corto. Cada uno controla su bloque con cronómetro al ensayar.

---

## Workflow asíncrono de grabación

Cada uno graba su bloque por separado. Reglas comunes para que el montaje quede coherente.

### Estándares técnicos (todos)

- **Formato:** MP4 (códec H.264 + audio AAC) — lo que generan QuickTime, OBS, Loom y Screen Recording por defecto
- **Resolución:** 1920×1080 (1080p) mínimo, todos igual
- **Frame rate:** 30 fps suficiente (60 fps si tu herramienta lo permite sin esfuerzo)
- **Audio:** micrófono de auriculares o externo (NO el del portátil), 128 kbps mínimo
- **Padding:** cada clip empieza con **2 segundos de silencio** y acaba con **2 segundos de silencio** — esto le da margen a Adrián para cortar limpio en edición
- **Sin handoffs verbales:** ningún clip puede decir *"y ahora Hugo nos enseña..."* — las transiciones las hace Adrián en edición con cortes y tarjetas

### Cómo grabar la pantalla

- **macOS nativo:** atajo `Cmd+Shift+5` → "Grabar pantalla completa" o "Grabar parte seleccionada". Asegúrate de marcar tu micro en "Options → Microphone"
- **OBS Studio:** más control sobre escenas, mezcla de audio y cámara superpuesta. Recomendado si vais a usar webcam + pantalla simultáneamente
- En cualquier caso, exportar como **MP4 1080p**

### Compartir los clips

Carpeta compartida en **Google Drive del grupo**. Nomenclatura fija (importante para que Adrián los ordene rápido):

- `bloque0a_intro_adrian.mp4`
- `bloque0b_casonegocio_antonio.mp4`
- `bloque1_arquitectura_enric.mp4`
- `bloque2_demo_hugo.mp4`
- `bloque3_explain_hugo.mp4`
- `bloque4_conclusion_adrian.mp4`

### Deadlines internos

- **T-72h** (3 días antes de la entrega oficial): clúster funcionando + datos cargados + query probada por Hugo
- **T-48h:** todos los clips subidos a Drive (Hugo es el último porque depende del pipeline)
- **T-24h:** vídeo montado por Adrián y revisado por el grupo
- **T-12h:** vídeo en YouTube como oculto + enlace verificado en incógnito
- **Entrega:** ZIP final con todo

---

## Bloque 0a — Intro (~15s)

### Ponente
**Adrián**

### Qué se ve en pantalla
- Webcam o slide simple con el nombre del grupo y los 4 integrantes

### Apertura
Empezar directamente, sin "hola" forzado.

### Viñetas
- "Somos el **Grupo 10** del Máster FP en Inteligencia Artificial y Big Data de la UOC."
- "Adrián Blasco, Antonio Sala, Enric Gil y Hugo Romero. Hemos desarrollado la Actividad 5 sobre **consultas federadas con Trino**."
- "A continuación os enseñamos el caso de negocio, la arquitectura del clúster, la demostración de la consulta y el análisis de su rendimiento."

### Cierre del clip
- Sonrisa neutra hacia cámara, 2 segundos de silencio, cortar

---

## Bloque 0b — Caso de negocio (~15s)

### Ponente
**Antonio**

### Qué se ve en pantalla
- Slide con un diagrama simple de las dos fuentes, o el `SCHEMA.md` del repo abierto

### Apertura
- "El caso de negocio que hemos modelado es..."

### Viñetas
- "Una **librería online** con dos fuentes heterogéneas."
- "Por un lado, **Postgres** como sistema transaccional: clientes, pedidos y líneas de pedido — datos vivos que cambian a diario."
- "Por otro lado, un **Data Lake en Parquet** como catálogo de referencia: libros y editoriales."
- "El KPI federado cruza ambas fuentes: **ingresos totales, ticket medio y unidades vendidas por género literario y país**."

### Cierre del clip
- "Esto es lo que vamos a calcular con una sola consulta SQL sobre Trino."
- 2 segundos de silencio, cortar

---

## Bloque 1 — Arquitectura (~60s)

### Ponente
**Enric**

### Qué se ve en pantalla
1. Editor con `docker-compose.yml` (~20s)
2. Ficheros `.properties` de los conectores (~20s)
3. Trino Web UI en `localhost:8080` con los 3 nodos visibles (~20s)

### Apertura
- "Nuestra arquitectura tiene cuatro servicios desplegados con Docker..."

### Viñetas
- "Cuatro servicios en una red Docker dedicada: un **Coordinator de Trino**, **dos Workers** y un **Postgres**."
- "Elegimos **Trino 451** en lugar de PrestoDB por mejor soporte multiplataforma e imágenes Docker actualizadas. Comparten arquitectura y sintaxis SQL. Decisión validada con el profesor."
- "El **Coordinator** recibe la query, genera el plan de ejecución y reparte los **splits** entre los Workers. Los **Workers** ejecutan los fragmentos en paralelo, leen directamente de las fuentes y agregan los resultados."
- (Mostrando `postgresql.properties`) "Configuramos dos catálogos. El conector **PostgreSQL** apunta a la BD `base_datos_grupo`."
- (Mostrando `hive.properties`) "El conector **Hive** lee ficheros Parquet del filesystem local, montado como volumen compartido `/opt/datalake` en los tres nodos. Los Workers paralelizan la lectura sin mover los datos físicamente."
- "Hemos ajustado la JVM para garantizar compatibilidad con distintas arquitecturas de CPU."

### Cierre del clip
- "Con esta arquitectura podemos ejecutar consultas federadas sobre ambas fuentes en paralelo."
- 2 segundos de silencio, cortar

---

## Bloque 2 — Demostración de la query (~120s)

### Ponente
**Hugo**

### Qué se ve en pantalla
1. Terminal con Trino CLI o cliente DBeaver con la query a la vista (~30s)
2. Ejecución SIN pushdown — wall time alto (~45s)
3. Ejecución CON pushdown — wall time bajo (~45s)

### Apertura
- "Os enseño la consulta federada que cruza las dos fuentes del caso de negocio..."

### Viñetas

**Presentación de la query (~30s)**
- "Cruza tres tablas de Postgres — `orders`, `order_items` y `customers` — con dos tablas en Hive sobre Parquet: `books_catalog` y `publishers`."
- "Objetivo: **ingresos totales, ticket medio y unidades vendidas por género literario y país**, para pedidos completados del primer trimestre de 2026."
- "Usa funciones de agregación SUM, COUNT y AVG con GROUP BY — lo que pide el enunciado."

**Ejecución SIN pushdown (~45s)**
- "Primero la ejecuto **sin filtros aplicables al origen**, forzando a Trino a materializar todas las filas."
- *(ejecutar query)* "Wall time: aproximadamente **X segundos**." `[RELLENAR]`
- "Trino está leyendo todas las filas de Postgres y todos los Parquet, y aplicando los filtros en sus propios workers — sin aprovechar índices ni poda de ficheros."

**Ejecución CON pushdown (~45s)**
- "Ahora con los **mismos filtros pero estratégicamente colocados**: `order_date BETWEEN`, `status = 'completed'`, y `genre IN (...)`."
- *(ejecutar query)* "Wall time: **Y segundos**, una mejora de **Z veces**." `[RELLENAR]`
- "Trino ha bajado los filtros de fecha y estado al Postgres, que los resuelve con índices, y el filtro de género al conector Hive, que sólo lee los Parquet relevantes. Este comportamiento se llama **predicate pushdown** y es la base de la federación eficiente."

### Cierre del clip
- "Para entender qué está pasando internamente, vamos a inspeccionar el plan de ejecución."
- 2 segundos de silencio, cortar — o continuar directamente al Bloque 3 si grabas en un único clip

> **Nota para Hugo:** los bloques 2 y 3 los puedes grabar como **dos clips separados** (recomendado: si te equivocas en uno, re-grabas solo ese) o **uno solo continuo de ~3 min**. Si los unes, súbelo como `bloque23_demo_explain_hugo.mp4` y Adrián ya lo coloca en su sitio.

---

## Bloque 3 — Análisis del EXPLAIN (~60s)

### Ponente
**Hugo**

### Qué se ve en pantalla
1. Trino Web UI en `localhost:8080` — historial de queries (~10s)
2. Detalle de la query ejecutada, vista "Live Plan" / "Stages" (~40s)
3. Distribución de splits por worker (~10s)

### Apertura
- "En la Web UI de Trino tenemos el historial de queries ejecutadas..."

### Viñetas
- "El plan se divide en **stages**, cada stage en **tasks**, y cada task ejecuta varios **splits**. Aquí vemos **N splits** repartidos entre nuestros **2 workers**." `[RELLENAR N]`
- "Identificamos dos **TableScans**: uno contra el conector PostgreSQL — fijaos cómo el filtro `status = 'completed'` aparece como **filter pushdown** dentro del scan, no como operación posterior — y otro contra Hive leyendo los Parquet."
- "Trino ha decidido un **broadcast join**: como `books_catalog` es la tabla pequeña, la envía a todos los workers para evitar un shuffle costoso."
- "El stage final hace **agregación distribuida**: cada worker calcula los SUM y COUNT parciales, y el coordinator solo combina los resultados ya pre-agregados — esto es **partial aggregation pushdown**."
- "Este nivel de paralelismo es lo que da el speedup que hemos visto en la demo."

### Cierre del clip
- "Con esto cerramos el análisis técnico."
- 2 segundos de silencio, cortar

---

## Bloque 4 — Conclusión (~30s)

### Ponente
**Adrián**

### Qué se ve en pantalla
- Webcam o slide simple con los puntos clave + URL del repo

### Apertura
- "Para cerrar, los principales retos y mejoras futuras..."

### Viñetas
- "El **principal reto técnico** fue elegir el motor: PrestoDB tiene problemas de compatibilidad con Apple Silicon e imágenes Docker recientes. Saltamos a **Trino**, evolución mantenida del proyecto con la misma sintaxis SQL. Validado con el profesor antes de invertir tiempo."
- "Como **mejoras futuras**: añadir un Hive Metastore real con backend Postgres, incluir un tercer conector (MongoDB o S3 vía MinIO), y orquestar la carga con Apache Airflow."
- "Todo el código en **github.com/blasketch/big_data_a5**. Gracias por vernos."

### Cierre del clip
- Sonrisa neutra, 2 segundos de silencio, cortar

---

## Plan de edición (Adrián, en iMovie)

1. **Descargar los 6 clips** (o 5 si Hugo los unió) de la carpeta de Google Drive a tu Mac.
2. **Crear proyecto nuevo en iMovie** → "Película" → resolución 1080p HD.
3. **Importar los clips** y arrastrarlos a la timeline en orden:
   `bloque0a → bloque0b → bloque1 → bloque2 → bloque3 → bloque4`
4. **Para cada clip:**
   - Recortar los ~2s de silencio del principio y del final, dejando ~0.5s de margen
   - Verificar volumen — si un clip suena más bajo, subir su ganancia en el panel de audio del inspector
5. **Transiciones entre clips:** "Cross Dissolve" de 0.5s entre cada par. iMovie → pestaña "Transitions" → arrastrar el efecto entre dos clips.
6. **Opcional pero recomendado:** añadir un **título inferior** ("Bloque 1 — Arquitectura · Enric Gil") al principio de cada bloque. iMovie → "Titles" → "Lower Third" → editar texto. Dura 2-3 segundos, queda mucho más profesional.
7. **Verificar duración total:** debe quedar entre 4:30 y 5:00. Si supera 5:00, recortar pausas internas; si baja de 4:30, alguien re-graba con más detalle.
8. **Exportar:** File → Share → File → 1080p, calidad "Alta" → guardar como `screencast_aa5_grupo10.mp4`.
9. **Subir a YouTube** en visibilidad **Oculto** (no Privado).
10. **Verificar en pestaña incógnito** que el enlace funciona sin necesidad de login.

---

## Checklist pre-grabación (cada persona)

- [ ] He ensayado mi bloque con cronómetro y entro dentro del tiempo
- [ ] He preparado las pantallas que voy a compartir (apps abiertas, ficheros a la vista)
- [ ] Mi audio se escucha claro (no del micro del portátil)
- [ ] El sitio donde grabo está en silencio y bien iluminado
- [ ] He apagado notificaciones de email, Slack, Discord, etc. para que no aparezcan en pantalla
- [ ] He hecho una toma de prueba de 10s y la he revisado: se ve y se oye bien

## Checklist específico para Hugo (Bloques 2 y 3)

- [ ] El clúster está arrancado y todos los servicios en verde
- [ ] La query funciona en ambas modalidades (con y sin pushdown)
- [ ] Hay al menos **5 queries ya ejecutadas** en el historial (para que la captura del Tree View no esté vacía en el bloque 3)
- [ ] La terminal tiene las dos versiones de la query listas para pegar
- [ ] La Web UI en localhost:8080 responde
- [ ] Datos rellenos en las viñetas marcadas con `[RELLENAR]`: wall times en segundos y número de splits

## Checklist post-grabación (cada persona)

- [ ] He revisado mi clip completo antes de subirlo a Drive
- [ ] El nombre del fichero sigue la nomenclatura exacta
- [ ] El clip dura aproximadamente lo previsto (puede sobrar 4-5s por los silencios, eso es normal)
- [ ] Lo he subido a la carpeta correcta del Google Drive del grupo
- [ ] He avisado a Adrián por el chat del grupo

## Checklist final (Adrián, antes de entregar)

- [ ] Vídeo montado, exportado y de duración correcta (4:30-5:00)
- [ ] Vídeo subido a YouTube como **Oculto** (no Privado)
- [ ] Enlace verificado en pestaña incógnito
- [ ] Enlace copiado en el PDF final
- [ ] Todo el grupo ha visto el vídeo antes de la entrega