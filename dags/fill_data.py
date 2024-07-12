from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema

EVENTS_PER_DAY = 100000


# def generate_data(base_time: str, n: int):
#     """Generates synth data and saves to DB.

#     Parameters
#     ----------

#         Base datetime to start events from.
#     n : int
#         Number of events to generate.
#     """
#     generator = DataGenerator()
#     schema = Schema()
#     people = generator.generate_people(100)
#     schema.insert(people, "people")

#     people_sample = schema.get_people(100)
#     sessions = generator.generate_sessions(
#         people_sample,
#         datetime.datetime.fromisoformat(base_time),
#         datetime.timedelta(days=1),
#         n,
#     )
#     schema.insert(sessions, "sessions")

# with DAG(
#     "fill_data",
#     start_date=pendulum.datetime(2024, 6, 1, tz="UTC"),
#     schedule_interval="@daily",
#     catchup=True,
# ) as dag:
#     op = PythonOperator(
#         task_id="task",
#         python_callable=generate_data,
#         op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
#     )

def generate_data(base_time: str, n: int):
    """Generates synth data and saves to DB.

    Parameters
    ----------
    base_time: strpoetry export --without-hashes --format=requirements.txt > requirements.txt

        Base datetime to start events from.
    n : int
        Number of events to generate.
    """
    generator = DataGenerator()
    schema = Schema()
    
    pasajeros = generator.generate_pasajero(5)
    schema.insert(pasajeros, "pasajero")

    conductores = generator.generate_conductor(5)
    schema.insert(conductores, "conductor")

    partnerships = generator.generate_partnership()
    schema.insert(partnerships, "partnership")

    modelo_vehiculos = generator.generate_modelo_vehiculo(1000)
    schema.insert(modelo_vehiculos, "modelovehiculo")

    vehiculos = generator.generate_vehiculo(10)
    schema.insert(vehiculos, "vehiculo")

    conductores_vehiculos = generator.generate_conductor_vehiculo(conductores, vehiculos)    
    schema.insert(conductores_vehiculos, "conductorvehiculo")

    viajes = generator.generate_viaje(2, conductores_vehiculos, pasajeros)
    schema.insert(viajes, "viaje")

    pagos = generator.generate_pago(viajes)
    schema.insert(pagos, "pago")
    

with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 7, 12, tz="UTC"),
    schedule_interval=datetime.timedelta(minutes=1),
    catchup=True,   
) as dag:
    op = PythonOperator(
        task_id="task",
        python_callable=generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}"),
    )


#schedule_interval=datetime.timedelta(minutes=1)
#schedule_interval="@daily"