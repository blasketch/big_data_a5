# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os

def generar_datos():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.join(directorio_actual, '..')
    
    ruta_datalake = os.path.join(ruta_raiz, 'datalake')
    ruta_postgres = os.path.join(ruta_raiz, 'postgres-init')

    #SEMILLA 42
    np.random.seed(42)

    # Para Postgres
    n_clientes = 1000
    clientes = pd.DataFrame({
        'id_cliente': range(1, n_clientes + 1),
        'nombre': [f'Cliente_Corp_{i}' for i in range(1, n_clientes + 1)],
        'pais': np.random.choice(['USA', 'Mexico', 'Argentina', 'Francia', 'Italia'], n_clientes),
        'score_credito': np.random.randint(300, 850, n_clientes)
    })
    
    clientes.to_csv(os.path.join(ruta_postgres, 'clientes_seed.csv'), index=False)

    #Para el Data Lake en Parque
    n_ventas = 100000
    ventas = pd.DataFrame({
        'id_venta': range(1, n_ventas + 1),
        'id_cliente': np.random.randint(1, n_clientes + 1, size=n_ventas),
        'monto': np.round(np.random.uniform(10.0, 1000.0, size=n_ventas), 2),
        'fecha': pd.date_range(start='2025-01-01', periods=n_ventas, freq='min')
    })

    # Guardar en formato Parquet
    archivo_parquet = os.path.join(ruta_datalake, 'ventas_historicas.parquet')
    ventas.to_parquet(archivo_parquet, index=False, engine='pyarrow')

    print(f"Parquet creado en: {archivo_parquet}")
    print(f"CSV de referencia en: {ruta_postgres}/clientes_seed.csv")

if __name__ == "__main__":
    generar_datos()