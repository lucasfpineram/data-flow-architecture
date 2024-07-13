from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
import random
import pendulum
import datetime
from td7.data_generator import DataGenerator
from td7.schema import Schema

EVENTS_PER_DAY = 100000


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

    modelo_vehiculos = generator.generate_modelo_vehiculo(1000) # son 90 max en realidad, necesito todas los modelos en la base para evitar errores de inserción en la tabla vehiculo
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
    current_hour = random.randint(0, 23)    # para poder testear todos los rangos
    if 5 <= current_hour <= 11:
        return 'mañana'
    elif 12 <= current_hour <= 19:
        return 'tarde'
    else: # de 20 a 5
        return 'noche'

with DAG(
    "fill_data",
    start_date=pendulum.datetime(2024, 7, 12, tz="UTC"),
    schedule_interval= datetime.timedelta(minutes=1), 
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



