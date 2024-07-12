{{ config(materialized='table') }}

WITH viajes_data AS (
    SELECT
        v.id_viaje,
        mv.modelo,
        p.monto,
        v.rango
    FROM
        viaje v
    JOIN
        vehiculo ve ON v.patente = ve.patente
    JOIN
        modelovehiculo mv ON ve.modelo = mv.modelo
    LEFT JOIN
        pago p ON v.id_viaje = p.id_viaje
    WHERE
        v.estado = 'Completado'
)

SELECT
    modelo,
    rango,
    COUNT(id_viaje) AS total_viajes,
    AVG(monto) AS avg_monto
FROM
    viajes_data
GROUP BY
    modelo, rango
ORDER BY
    total_viajes DESC;
