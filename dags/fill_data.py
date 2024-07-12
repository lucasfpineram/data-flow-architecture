from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
import random
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

def generate_data(base_time: str, n: int, rango: str):
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

    modelo_vehiculos = generator.generate_modelo_vehiculo(1000) # por que generamos tantos vehiculos?
    schema.insert(modelo_vehiculos, "modelovehiculo")

    vehiculos = generator.generate_vehiculo(10)
    schema.insert(vehiculos, "vehiculo")

    conductores_vehiculos = generator.generate_conductor_vehiculo(conductores, vehiculos)    
    schema.insert(conductores_vehiculos, "conductorvehiculo")

    viajes = generator.generate_viaje(2, conductores_vehiculos, pasajeros, rango)
    schema.insert(viajes, "viaje")

    pagos = generator.generate_pago(viajes)
    schema.insert(pagos, "pago")
    
# Función para seleccionar la rama
def choose_branch():
    # current_hour = datetime.datetime.now().hour
    current_hour = random.randint(0, 23)
    if 5 <= current_hour <= 11:
        return 'mañana'
    elif 12 <= current_hour <= 19:
        return 'tarde'
    else: # de 20 a 1
        return 'noche'

with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 7, 12, tz="UTC"),
    schedule_interval=datetime.timedelta(minutes=1), 
    catchup=True,   
) as dag:
    
    branch_op = BranchPythonOperator(
        task_id='branch_task',
        python_callable=choose_branch,
        provide_context=True,
    )

    ingestion_task_morning = PythonOperator(
        task_id='mañana',
        python_callable=generate_data,
        #argumentos que le paso a mi funcion generate_data
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}", rango = "manana"), # tengo que pasarle a generate_data "mañana" como parametro
    )
    
    ingestion_task_afternoon = PythonOperator(
        task_id='tarde',
        python_callable=generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}", rango = "tarde"),
    )
    
    ingestion_task_night = PythonOperator(
        task_id='noche',
        python_callable=generate_data,
        op_kwargs=dict(n=EVENTS_PER_DAY, base_time="{{ ds }}", rango = "noche"),
    )
    
    # Definir las dependencias
    branch_op >> [ingestion_task_morning, ingestion_task_afternoon, ingestion_task_night]



#schedule_interval=datetime.timedelta(minutes=1)
#schedule_interval="@daily"