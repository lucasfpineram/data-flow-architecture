import datetime
import random
from faker import Faker
from faker.providers import address, date_time, internet, passport, phone_number
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from custom_types import Records

PHONE_PROBABILITY = 0.7
#Faker.seed(1234) # fijo una seed para que genere los mismos datos

# defino una clase con distintos metodos que generan data para nuestras distintas tablas
class DataGenerator:
    def __init__(self):
        """Instantiates faker instance"""
        self.fake = Faker()
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)
        self.brand_partnerships = {
            "Toyota": True,
            "Ford": True,
            "BMW": False,
            "Audi": False,
            "Honda": True,
            "Mercedes": False,
            "Chevrolet": False,
            "Volkswagen": False,
            "Hyundai": True,
            "Nissan": True
        }

    def generate_pasajero(self, n: int) -> Records:
        pasajeros = []
        for _ in range(n):
            id_pasajero = str(uuid.uuid4())  # Genera un ID único para el pasajero
            pasajeros.append(
                {
                    "id_pasajero": id_pasajero,
                    "nombre": self.fake.name(),
                    "telefono": self.fake.phone_number(),
                    "correo_electronico": self.fake.email(),
                }
            )
        return pasajeros

    def generate_conductor(self, n: int) -> Records:
        conductores = []
        for _ in range(n):
            id_conductor = str(uuid.uuid4())  # Genera un ID único para el conductor
            conductores.append(
                {
                    "id_conductor": id_conductor,
                    "nombre": self.fake.name(),
                    "telefono": self.fake.phone_number(),
                    "correo_electronico": self.fake.email(),
                }
            )
        return conductores
    
    def generate_partnership(self) -> Records:
            car_brands = list(self.brand_partnerships.keys())
            partnerships = []
            for marca in car_brands:
                es_partner = self.brand_partnerships.get(marca, False) # busca el valor asociado a la clave marca en el diccionario brand_partnerships. Si la clave marca no se encuentra en el diccionario, devuelve el valor False por defecto.
                partnerships.append(
                    {
                        "marca": marca,
                        "es_partner": es_partner,
                    }
                )
            return partnerships

    def generate_modelo_vehiculo(self, n: int) -> Records:
        car_brands = ["Toyota", "Ford", "BMW", "Audi", "Honda", "Mercedes", "Chevrolet", "Volkswagen", "Hyundai", "Nissan"]
        modelo_vehiculos = []
        for _ in range(n):
            marca = self.fake.random_element(elements=car_brands)
            modelo = self.fake.random_element(elements=self.get_modelos(marca))
            # Fetch the attributes and handle None cases
            attributes = self.get_atributos_modelos(marca, modelo)
            if attributes is None:
                # Handle the case where attributes could not be fetched
                tipo_carroceria, apto_discapacitado, vclase_economica, emision_rating, seguridad_rating = "Unknown", False, "Unknown", "Unknown", 0
            else:
                tipo_carroceria, apto_discapacitado, vclase_economica, emision_rating, seguridad_rating = attributes

            modelo_vehiculos.append(
                {
                    "modelo": modelo,
                    "tipo_carroceria": tipo_carroceria,
                    "apto_discapacitado": apto_discapacitado,
                    "vclase_economica": vclase_economica,
                    "emision_rating": emision_rating,
                    "seguridad_rating": seguridad_rating,
                    "marca": marca,
                }
            )
        return modelo_vehiculos

    def get_modelos(self, marca: str) -> list:
        if marca == "Toyota":
            return ["Corolla", "Camry", "RAV4", "Highlander", "Tacoma", "Prius", "4Runner", "Sienna", "Avalon"]
        elif marca == "Ford":
            return ["Mustang", "F-150", "Explorer", "Escape", "Focus", "Fusion", "Edge", "Expedition", "Ranger"]
        if marca == "BMW":
            return ["3 Series", "5 Series", "X3", "X5", "X1", "7 Series", "Z4", "M3", "i8"]
        elif marca == "Audi":
            return ["A4", "A6", "Q5", "Q7", "A3", "Q3", "TT", "A5", "RS5"]
        if marca == "Honda":
            return ["Accord", "Civic", "CR-V", "Pilot", "Odyssey", "Fit", "HR-V", "Ridgeline", "Insight"]
        elif marca == "Mercedes":
            return ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "A-Class", "CLA", "GLA", "AMG GT"]
        if marca == "Chevrolet":
            return ["Silverado", "Equinox", "Malibu", "Traverse", "Camaro", "Impala", "Suburban", "Colorado", "Bolt EV"]
        elif marca == "Volkswagen":
            return ["Jetta", "Golf", "Tiguan", "Atlas", "Passat", "Beetle", "Arteon", "Touareg", "Golf GTI"]
        if marca == "Hyundai":
            return ["Sonata", "Elantra", "Tucson", "Santa Fe", "Palisade", "Veloster", "Kona", "Accent", "Venue"]
        elif marca == "Nissan":
            return ["Altima", "Rogue", "Sentra", "Pathfinder", "Maxima", "Murano", "Frontier", "Titan", "Leaf"]

    def get_atributos_modelos(self, marca: str, modelo: str) -> tuple:
        if marca == "Toyota":
            if modelo in ["Corolla", "Camry", "Avalon"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["RAV4", "Highlander", "4Runner"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo == "Tacoma":
                return "Pick-up", False, "Mid-range", "Medio", 3
            elif modelo == "Prius":
                return "Sedan", True, "Economy", "Alto", 5
            elif modelo == "Sienna":
                return "Minivan", True, "Mid-range", "Medio", 3
        elif marca == "Ford":
            if modelo in ["Mustang", "Fusion"]:
                return "Coupe", False, "Performance", "Alto", 3
            elif modelo in ["F-150", "Ranger"]:
                return "Pick-up", False, "Mid-range", "Medio", 4
            elif modelo in ["Explorer", "Escape", "Edge"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo in ["Focus", "Expedition"]:
                return "Sedan", False, "Economy", "Medio", 3
        elif marca == "BMW":
            if modelo in ["3 Series", "5 Series", "7 Series"]:
                return "Sedan", False, "Luxury", "Medio", 5
            elif modelo in ["X3", "X5", "X1"]:
                return "SUV", False, "Luxury", "Bajo", 4
            elif modelo in ["Z4", "M3", "i8"]:
                return "Coupe", False, "Performance", "Alto", 5
        elif marca == "Audi":
            if modelo in ["A4", "A6", "A3", "A5"]:
                return "Sedan", False, "Luxury", "Medio", 4
            elif modelo in ["Q5", "Q7", "Q3"]:
                return "SUV", False, "Luxury", "Bajo", 5
            elif modelo in ["TT", "RS5"]:
                return "Coupe", False, "Performance", "Alto", 4
        elif marca == "Honda":
            if modelo in ["Accord", "Civic", "Insight"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["CR-V", "Pilot", "HR-V"]:
                return "SUV", False, "Mid-range", "Bajo", 5
            elif modelo in ["Odyssey", "Ridgeline"]:
                return "Minivan", True, "Mid-range", "Medio", 3
            elif modelo == "Fit":
                return "Hatchback", True, "Economy", "Alto", 4
        elif marca == "Mercedes":
            if modelo in ["C-Class", "E-Class", "S-Class"]:
                return "Sedan", False, "Luxury", "Medio", 5
            elif modelo in ["GLC", "GLE", "GLA"]:
                return "SUV", False, "Luxury", "Bajo", 4
            elif modelo in ["A-Class", "CLA"]:
                return "Sedan", False, "Luxury", "Alto", 4
            elif modelo == "AMG GT":
                return "Coupe", False, "Performance", "Alto", 5
        elif marca == "Chevrolet":
            if modelo in ["Silverado", "Colorado", "Suburban"]:
                return "Pick-up", False, "Mid-range", "Medio", 4
            elif modelo in ["Equinox", "Traverse"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo in ["Malibu", "Impala"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["Camaro"]:
                return "Coupe", False, "Performance", "Alto", 5
            elif modelo == "Bolt EV":
                return "Hatchback", True, "Economy", "Alto", 5
        elif marca == "Volkswagen":
            if modelo in ["Jetta", "Passat", "Arteon"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["Golf", "Golf GTI", "Beetle"]:
                return "Hatchback", False, "Mid-range", "Bajo", 4
            elif modelo in ["Tiguan", "Atlas"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo == "Touareg":
                return "SUV", False, "Luxury", "Alto", 5
        elif marca == "Hyundai":
            if modelo in ["Sonata", "Elantra", "Accent"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["Tucson", "Santa Fe", "Venue"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo in ["Palisade", "Kona"]:
                return "SUV", False, "Luxury", "Alto", 5
            elif modelo in ["Veloster"]:
                return "Coupe", False, "Performance", "Alto", 4
        elif marca == "Nissan":
            if modelo in ["Altima", "Maxima"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["Rogue", "Murano"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo in ["Sentra"]:
                return "Sedan", False, "Economy", "Medio", 3
            elif modelo in ["Pathfinder", "Frontier", "Titan"]:
                return "Pick-up", False, "Mid-range", "Medio", 4
            elif modelo == "Leaf":
                return "Hatchback", False, "Economy", "Alto", 5
        return "Unknown", False, "Unknown", "Unknown", 0
            

    def generate_vehiculo(self, n: int) -> Records:
        car_brands = ["Toyota", "Ford", "BMW", "Audi", "Honda", "Mercedes", "Chevrolet", "Volkswagen", "Hyundai", "Nissan"]
        vehiculos = []
        for _ in range(n):
            marca = self.fake.random_element(elements=car_brands)
            modelos = self.get_modelos(marca)
            modelo = self.fake.random_element(elements=modelos)
            vehiculos.append(
                {
                    "patente": self.fake.license_plate(),
                    "ano_fabricacion": self.fake.random_int(min=2000, max=2023),
                    "modelo": modelo,
                }
            )
        return vehiculos

    def generate_conductor_vehiculo(self, conductores, vehiculos) -> Records:
        '''
        genera n random vehiculos de sampleados de "vehiculos" para los conductores.
        Aseguramos que no hayan conductores sin vehiculos.
        '''
        conductor_vehiculo = []
        for conductor in conductores:
            num_vehiculos = random.randint(1, 2)
            vehiculos_seleccionados = random.sample(vehiculos, num_vehiculos)
            for vehiculo in vehiculos_seleccionados:
                conductor_vehiculo.append(
                    {
                        "id_conductor": conductor["id_conductor"],
                        "patente": vehiculo["patente"],
                        "estado": self.fake.boolean(),
                    }
                )
        return conductor_vehiculo

    def generate_viaje(self, n, conductores_vehiculos, pasajeros, rango) -> Records:
        viajes = []
        active_conductores_vehiculos = [cv for cv in conductores_vehiculos if cv['estado']]
        for _ in range(n):
            id_viaje = str(uuid.uuid4())  # Genera un ID único para el viaje
            conductor_vehiculo = random.choice(active_conductores_vehiculos)
            pasajero = random.choice(pasajeros)
            fecha_hora = self.fake.date_time_this_decade(before_now=True, after_now=False)
            if rango == "manana":
                random_hour = random.randint(2, 11)  # Hora aleatoria entre 2 y 11
            elif rango == "tarde":
                random_hour = random.randint(12, 19)  # Hora aleatoria entre 12 y 19
            elif rango == "noche":
                random_hour = random.choice(list(range(20, 24)) + [0, 1])  # Hora aleatoria entre 20 y 23, 0 y 1
            else:
                raise ValueError("Rango no válido. Use 'manana', 'tarde', o 'noche'.")
            fecha_hora = fecha_hora.replace(hour=random_hour, minute=random.randint(0, 59), second=random.randint(0, 59))
            fecha_hora_str = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
            viajes.append(
                {
                    "id_viaje": id_viaje,
                    "origen": self.fake.address(),
                    "destino": self.fake.address(),
                    "fecha_hora": fecha_hora_str,  # fecha aleatoria dentro del rango (mañana, tarde o noche)
                    "estado": random.choice(['Completado', 'Cancelado']),
                    "calificacion": random.randint(0, 5),
                    "id_pasajero": pasajero["id_pasajero"],
                    "id_conductor": conductor_vehiculo["id_conductor"],
                    "patente": conductor_vehiculo["patente"],
                    "rango": rango
                }
            )
        return viajes
        
    def generate_pago(self, viajes) -> list:
        pagos = []
        for viaje in viajes:
            if viaje["estado"] == "Completado":
                id_pago = str(uuid.uuid4())  
                monto = round(self.fake.random.uniform(2000, 22000), 0)  
                metodo_pago = self.fake.random_element(elements=('Tarjeta de credito', 'Tarjeta de debito', 'Transferencia', 'Efectivo'))
                pagos.append({
                    "id_pago": id_pago,
                    "monto": monto,
                    "metodo_pago": metodo_pago,
                    "id_viaje": viaje["id_viaje"]
                })
        return pagos

def main():
    # Instanciar el generador de datos
    generator = DataGenerator()

    # Generar pasajeros
    pasajeros = generator.generate_pasajero(5)
    print("Pasajeros generados:")
    for pasajero in pasajeros:
        print(pasajero)

    # Generar conductores
    conductores = generator.generate_conductor(5)
    print("\nConductores generados:")
    for conductor in conductores:
        print(conductor)

    # Generar partnership
    partnerships = generator.generate_partnership()
    print("\nPartnerships generados:")
    for partnership in partnerships:
        print(partnership)

    # Generar modelo_vehiculo
    modelos = generator.generate_modelo_vehiculo(10)
    print("\nModelos generados:")
    for modelo in modelos:
        print(modelo)

    # Generar vehículos
    vehiculos = generator.generate_vehiculo(20)
    print("\nVehiculos generados:")
    for vehiculo in vehiculos:
        print(vehiculo)

    # Generar relación conductor-vehículo
    conductor_vehiculo = generator.generate_conductor_vehiculo(conductores, vehiculos)
    print("\nRelacion conductor_vehiculo generada:")
    for cv in conductor_vehiculo:
        print(cv)

    # Generar viajes
    viajes = generator.generate_viaje(10, conductor_vehiculo, pasajeros, rango="manana")
    print("\nViajes generados:")
    for viaje in viajes:
        print(viaje)

    # Generar pagos para los viajes completados
    pagos = generator.generate_pago(viajes)
    print("\nPagos generados:")
    for pago in pagos:
        print(pago)

if __name__ == "__main__":
    main()