
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    pais VARCHAR(50),
    score_credito INT
);


INSERT INTO clientes (id_cliente, nombre, pais, score_credito) VALUES 
(1, 'Empresa de Prueba 1', 'España', 700),
(2, 'Empresa de Prueba 2', 'México', 650);