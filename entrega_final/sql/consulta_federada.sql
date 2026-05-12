SELECT
    c.pais,
    COUNT(v.id_venta) AS total_operaciones,
    ROUND(SUM(v.monto), 2) AS facturacion_total,
    ROUND(AVG(v.monto), 2) AS media_operacion
FROM hive.default.ventas_historicas v
JOIN postgresql.public.clientes c
    ON v.id_cliente = c.id_cliente
WHERE c.pais = 'España'
GROUP BY c.pais;