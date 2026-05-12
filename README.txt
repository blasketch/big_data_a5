Guía de Inicio Rápido - Infraestructura Trino (Reto 5)

He configurado un clúster de Trino (versión 451) con un Coordinator y dos  Workers, además de la base de datos PostgreSQL. 
La he configurado con una versión de Trino 451 (no la lastversion) para que funcione tanto en PCs potentes como en algunos mas antiguos y menos potentes.
Está probado en dos equipos, el de mi trabajo, un equipo nuevo con 16Gb y Win11, y el de mi casa, portátil antiguo con 8Gb

1. Requisitos previos
Tener Docker Desktop instalado y funcionando.

Tener al menos 2GB de RAM libres en el sistema antes de arrancar.

2. Cómo arrancar el entorno
Descarga esta carpeta en tu ordenador.

Abre una terminal (PowerShell o CMD) dentro de la carpeta.

Ejecuta el comando:
docker compose up -d

Espera unos 15-20 segundos a que los tres contenedores se pongan en verde.

3. Puntos de acceso
Trino Web UI (Monitorización): http://localhost:8080

Usuario: Pon tu nombre (no pide contraseña).

PostgreSQL (Base de Datos): localhost:5432

Usuario: usuario_trino

Password: password123

DB: db_datos

4. Notas de compatibilidad
He ajustado la versión a la 451 y añadido parches en el jvm.config para asegurar que el entorno funcione en cualquier CPU (incluyendo las que no soportan x86-64-v3). 
Por favor, no cambiéis la versión de la imagen en el yaml para evitar errores de arquitectura.

5. Nodos de Procesamiento (Cómputo)
El clúster de Trino se divide en dos roles diferenciados, lo que permite escalar el rendimiento sin mover los datos:

Coordinator (1 nodo): Es el cerebro del sistema. Se encarga de recibir las consultas SQL, analizar el plan de ejecución (Explain Plan), 
optimizarlo y dividirlo en fragmentos (splits) que reparte entre los trabajadores.

Workers (2 nodos): Son el músculo del clúster. Ejecutan los cálculos, realizan las agregaciones y leen directamente de las fuentes de datos. 
Al tener dos workers, el sistema puede procesar datos en paralelo, reduciendo drásticamente el tiempo de respuesta en grandes volúmenes de datos.

6. Fuentes de Datos (Almacenamiento Heterogéneo)
Siguiendo los requisitos del proyecto, Trino actúa como un motor unificado que conecta con:

Capa Relacional (PostgreSQL): Un contenedor dedicado que gestiona las tablas transaccionales.

Capa de Archivos/Datalake (Hive Connector): Un sistema de archivos montado en el volumen ./datalake. 
Trino utiliza el conector de Hive para leer archivos (CSV/Parquet) de forma distribuida como si fueran tablas SQL, sin necesidad de importarlos a una base de datos.

7. Optimización y Compatibilidad
Eficiencia de Recursos: El entorno se ha optimizado para ser ligero, limitando la memoria de la JVM en cada nodo para asegurar la estabilidad del sistema en diferentes configuraciones de hardware.

Alta Compatibilidad: Se utiliza una versión específica del motor y configuraciones de diagnóstico de Java para garantizar que el clúster arranque correctamente en diversas arquitecturas de CPU, 
evitando errores de instrucciones avanzadas (x86-64-v3).

8. Generación de Datos (Python)
Antes de nada, debemos generar los archivos base. Asegúrate de tener instalada la librería pandas y pyarrow.
Después ejecutar:
python script/generar_dataset.py

9. Levantamiento con Docker
Levanta los contenedores limpiando cualquier rastro de ejecuciones anteriores:

docker-compose down -v
docker-compose up -d

10. Carga de Datos en Postgres (SQL)
Postgres inicia con una tabla vacía. Para cargar los miles de clientes generados por el script, ejecuta este comando en tu terminal:

docker exec -it postgres-db psql -U usuario_trino -d base_datos_grupo -c "TRUNCATE TABLE clientes; COPY clientes(id_cliente, nombre, pais, score_credito) FROM '/docker-entrypoint-initdb.d/clientes_seed.csv' DELIMITER ',' CSV HEADER;"

Registrar el Data Lake en Trino

Trino debe "mapear" los archivos Parquet para verlos como una tabla SQL.

Entra en Trino: docker exec -it trino-coordinator trino

Pega el siguiente bloque:CREATE SCHEMA IF NOT EXISTS hive.default;

CREATE TABLE IF NOT EXISTS hive.default.ventas_historicas (
    id_venta BIGINT,
    id_cliente INT,
    monto DOUBLE,
    fecha TIMESTAMP
)
WITH (
    format = 'PARQUET',
    external_location = '/opt/datalake'
);

11. Verificación Final (Analítica de Negocio)
Para confirmar que el clúster está procesando datos de ambas fuentes simultáneamente, ejecuta este JOIN en la consola de Trino:

SELECT 
    c.pais, 
    COUNT(v.id_venta) AS total_operaciones,
    ROUND(SUM(v.monto), 2) AS facturacion_total
FROM hive.default.ventas_historicas v
JOIN postgresql.public.clientes c ON v.id_cliente = c.id_cliente
GROUP BY c.pais
ORDER BY facturacion_total DESC;