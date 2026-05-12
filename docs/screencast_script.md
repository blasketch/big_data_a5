# Screencast AA5 (FP502) — Grupo 10

**Asignatura:** Big Data I (FP502)
**Máster FP en Inteligencia Artificial y Big Data — UOC**
**Duración objetivo:** 4-5 min (target real: ~5:00)

---

## Integrantes y reparto

| Integrante | Rol | Aparece en |
| --- | --- | --- |
| Adrián Blasco Lozano | Rol 4 — Documentación y screencast | Intro + Conclusión |
| Antonio Sala Llaudis | Rol 2 — Datos | Caso de negocio (dentro de la intro) |
| Enric Gil Baquero | Rol 1 — Infraestructura | Bloque 1 — Arquitectura |
| Hugo Romero Casado | Rol 3 — Query y rendimiento | Bloque 2 — Demo + Bloque 3 — EXPLAIN |

## Resumen de tiempos

| Bloque | Tiempo | Acumulado | Quien habla |
| --- | --- | --- | --- |
| Intro + caso de negocio | 30s | 0:30 | Adrián → Antonio |
| Bloque 1 — Arquitectura | 60s | 1:30 | Enric |
| Bloque 2 — Demostración | 120s | 3:30 | Hugo |
| Bloque 3 — Análisis del EXPLAIN | 60s | 4:30 | Hugo |
| Bloque 4 — Conclusión | 30s | 5:00 | Adrián |

> **Importante:** la rúbrica premia cumplir estrictamente el tiempo y penaliza excederse o quedarse corto. Ensayar con cronómetro antes de grabar.

---

## Bloque 0 — Intro y caso de negocio (~30s)

### Quién habla
**Adrián** (15s) → handoff a **Antonio** (15s)

### Qué se ve en pantalla
- Adrián: webcam o slide simple con nombre del grupo y los 4 integrantes
- Antonio: diagrama del esquema o las dos fuentes de datos en pantalla

### Adrián — viñetas
- "Hola, somos el **Grupo 10** del Máster FP en Inteligencia Artificial y Big Data de la UOC."
- "Mi nombre es Adrián Blasco. Junto a mis compañeros Antonio Sala, Enric Gil y Hugo Romero hemos desarrollado esta Actividad 5 sobre **consultas federadas con Trino**."
- "Antonio nos presenta el caso de negocio."

### Antonio — viñetas
- "Hemos modelado una **librería online** con dos fuentes heterogéneas."
- "Por un lado, **Postgres** como sistema transaccional: clientes, pedidos y líneas de pedido — datos vivos que cambian a diario."
- "Por otro lado, un **Data Lake en Parquet** que actúa como catálogo de referencia: libros y editoriales."
- "El KPI federado cruza ambas fuentes: ingresos totales, ticket medio y unidades vendidas por género literario y país."

### Transición
> Antonio: "Para entender cómo Trino unifica ambas fuentes, Enric nos enseña la arquitectura."

---

## Bloque 1 — Arquitectura (~60s)

### Quién habla
**Enric**

### Qué se ve en pantalla
1. Editor con `docker-compose.yml` (primeros ~20s)
2. Ficheros `.properties` de los conectores (siguientes ~20s)
3. Trino Web UI en `localhost:8080` mostrando los nodos activos (últimos ~20s)

### Enric — viñetas
- "Nuestro clúster tiene **cuatro servicios** en una red Docker dedicada: un **Coordinator de Trino**, **dos Workers** y un **Postgres**."
- "Elegimos **Trino 451** en lugar de PrestoDB porque comparten arquitectura, pero Trino tiene mejor soporte multiplataforma, imágenes oficiales actualizadas y una integración más limpia con Docker. Lo consultamos con el profesor antes de cambiar."
- "El **Coordinator** recibe la query SQL, genera el plan de ejecución y reparte los **splits** entre los Workers. Los **Workers** ejecutan los fragmentos en paralelo, leen directamente de las fuentes y agregan resultados."
- (Mostrando `postgresql.properties`) "Configuramos dos catálogos. El primero, el conector **PostgreSQL**, apunta a la BD `base_datos_grupo` para las tablas transaccionales."
- (Mostrando `hive.properties`) "El segundo, el conector **Hive**, lee ficheros Parquet directamente del filesystem local, montado como volumen compartido `/opt/datalake` en los tres nodos de Trino. Esto permite que los Workers paralelicen la lectura sin mover los datos."
- "Hemos ajustado la JVM para garantizar compatibilidad con distintas arquitecturas de CPU, lo que nos permitió desplegar el clúster en máquinas heterogéneas del equipo."

### Transición
> Enric: "Con la arquitectura clara, Hugo ejecuta la consulta federada en directo."

---

## Bloque 2 — Demostración de la consulta federada (~120s)

### Quién habla
**Hugo**

### Qué se ve en pantalla
1. Terminal con Trino CLI o cliente DBeaver conectado al Coordinator (~30s mostrando la query)
2. Ejecución SIN pushdown — wall time alto (~45s)
3. Ejecución CON pushdown — wall time bajo (~45s)

### Hugo — viñetas

**Presentación de la query (~30s)**
- "Esta es nuestra consulta federada. Cruza tres tablas de Postgres — `orders`, `order_items` y `customers` — con dos tablas en Hive sobre Parquet: `books_catalog` y `publishers`."
- "El objetivo: calcular **ingresos totales, ticket medio y unidades vendidas por género literario y país** para pedidos completados del primer trimestre de 2026."
- "La query usa funciones de agregación SUM, COUNT y AVG con GROUP BY — exactamente lo que pide el enunciado."

**Ejecución SIN pushdown (~45s)**
- "Primero la ejecuto **sin filtros aplicables al origen**, forzando a Trino a materializar todas las filas."
- *(ejecutar query)* "El wall time es de aproximadamente **X segundos**." `[RELLENAR con el dato real tras el ensayo]`
- "Trino lee todas las filas de Postgres y todos los ficheros Parquet y aplica los filtros en sus propios workers — sin aprovechar los índices del origen ni la poda de ficheros."

**Ejecución CON pushdown (~45s)**
- "Ahora la ejecuto con los **mismos filtros pero estratégicamente colocados**: `order_date BETWEEN ...`, `status = 'completed'` y `genre IN (...)`."
- *(ejecutar query)* "El wall time baja a **Y segundos**, una mejora de **Z veces**." `[RELLENAR]`
- "Trino ha bajado los filtros de fecha y estado al Postgres, que los resuelve con índices, y el filtro de género al conector Hive, que solo lee los Parquet relevantes. Este comportamiento se llama **predicate pushdown** y es la base de la federación eficiente."

### Transición
> Hugo: "Para entender qué está ocurriendo internamente, vamos a inspeccionar el plan de ejecución en la Web UI de Trino."

---

## Bloque 3 — Análisis del EXPLAIN (~60s)

### Quién habla
**Hugo** (continúa)

### Qué se ve en pantalla
1. Trino Web UI en `localhost:8080` — historial de queries (~10s)
2. Detalle de la query ejecutada, vista "Live Plan" o "Stages" (~40s)
3. Distribución de splits por worker (~10s)

### Hugo — viñetas
- "En la Web UI vemos el historial de queries ejecutadas. Si entramos al detalle de la última..."
- "El plan se divide en **stages**, cada stage en **tasks**, y cada task ejecuta varios **splits**. Aquí vemos **N splits** repartidos entre nuestros **2 workers**." `[RELLENAR N]`
- "Identificamos dos **TableScans**: uno contra el conector PostgreSQL — fijaos cómo el filtro `status = 'completed'` aparece como **filter pushdown** dentro del scan, no como operación posterior — y otro contra Hive leyendo los Parquet."
- "Trino ha decidido un **broadcast join**: como `books_catalog` es la tabla pequeña, la envía a todos los workers para evitar un shuffle costoso."
- "El stage final hace la **agregación distribuida**: cada worker calcula los SUM y COUNT parciales, y el coordinator solo combina los resultados ya pre-agregados — esto es **partial aggregation pushdown**."
- "Este nivel de paralelismo es lo que da el speedup que hemos visto antes."

### Transición
> Hugo: "Para cerrar, Adrián resume los principales retos y aprendizajes."

---

## Bloque 4 — Conclusión (~30s)

### Quién habla
**Adrián**

### Qué se ve en pantalla
- Webcam o slide simple con los puntos clave + URL del repo

### Adrián — viñetas
- "El **principal reto técnico** fue elegir el motor: PrestoDB tiene problemas de compatibilidad con Apple Silicon e imágenes Docker recientes. Saltamos a **Trino**, evolución mantenida del proyecto con la misma sintaxis SQL. Lo validamos con el profesor antes de invertir tiempo."
- "Como **mejoras futuras** plantearíamos: añadir un Hive Metastore real con backend Postgres para esquemas más complejos, incluir un tercer conector (MongoDB o S3 vía MinIO) y orquestar la carga con Apache Airflow."
- "Todo el código está en **github.com/blasketch/big_data_a5**. Gracias por vernos."

### Cierre
> Pausa de 1-2 segundos antes de cortar la grabación — facilita el montaje.

---

## Checklist pre-grabación

- [ ] El clúster arranca sin errores: `docker compose up -d` y todos los servicios en verde
- [ ] La Web UI de Trino responde en `localhost:8080`
- [ ] La query federada se ejecuta correctamente en ambas modalidades (con/sin pushdown)
- [ ] Hay al menos **5 queries ya ejecutadas** en el historial para que la captura del Tree View no esté vacía
- [ ] El editor de Enric tiene `docker-compose.yml` y los `.properties` abiertos en pestañas listas
- [ ] La terminal de Hugo está conectada al coordinator con la query lista para pegar (dos variantes: con y sin pushdown)
- [ ] Cada miembro ha ensayado su bloque al menos una vez con cronómetro
- [ ] Audio: micrófono externo o auriculares con micro (NO el del portátil)
- [ ] Datos rellenos en las viñetas marcadas con `[RELLENAR]` (wall times, número de splits)

## Setup técnico de grabación

- **Herramienta recomendada:** OBS Studio (gratis, profesional, multiplataforma)
- **Alternativa rápida:** Loom (limita a 5 min en plan free — justo nuestro caso)
- **Modo de grabación:** los cuatro en una llamada de Google Meet / Discord, cada uno comparte pantalla cuando le toca su bloque. Adrián captura la pantalla compartida + audio de todos los micrófonos
- **Resolución mínima:** 1080p para que el texto de la Trino UI se lea nítido
- **Bitrate sugerido:** 6000 kbps o superior

## Checklist post-grabación

- [ ] Revisar el vídeo entero antes de subir (especialmente transiciones y tiempos)
- [ ] Subir a YouTube del grupo
- [ ] Configurar visibilidad como **"Oculto" (Unlisted)** — NO "Privado", según el enunciado
- [ ] Verificar el enlace en pestaña incógnito (debe ser accesible sin login)
- [ ] Copiar el enlace del vídeo en el documento PDF final

## Notas finales

- Si hay que **recortar tiempo**, los bloques más comprimibles son la Intro y la Conclusión (~5-10s de margen cada uno).
- Si hay que **extender**, lo más natural es alargar el análisis del EXPLAIN con más detalle sobre stages y distribución de splits.
- Tiempo objetivo final: **4:50-5:00 min**.