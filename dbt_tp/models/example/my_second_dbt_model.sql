{{ config(materialized='view') }}

WITH trips_data AS (
    SELECT
        v.id_viaje,
        v.rango,
        v.calificacion,
        p.monto
    FROM
        viaje v
    LEFT JOIN
        pago p ON v.id_viaje = p.id_viaje
    WHERE
        v.estado = 'Completado'
)

SELECT
    rango AS time_of_day,
    COUNT(id_viaje) AS total_trips,
    ROUND(AVG(calificacion), 1) AS avg_rating,
    ROUND(SUM(monto), 2) AS total_revenue,
    ROUND(AVG(monto), 2) AS avg_revenue_per_trip
FROM
    trips_data
GROUP BY
    rango
ORDER BY
    CASE 
        WHEN rango = 'manana' THEN 1
        WHEN rango = 'tarde' THEN 2
        WHEN rango = 'noche' THEN 3
    END
