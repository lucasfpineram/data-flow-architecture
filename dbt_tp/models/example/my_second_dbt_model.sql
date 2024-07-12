select *
from {{ ref('my_first_dbt_model') }}
where id = 1

-- calificaciones, rango horario
-- viajes cancelados
-- 