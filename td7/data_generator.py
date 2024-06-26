import datetime
import random
from faker import Faker
from faker.providers import address, date_time, internet, passport, phone_number
import uuid
from custom_types import Records

PHONE_PROBABILITY = 0.7
Faker.seed(1234) # fijo una seed para que genere los mismos datos

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

#     def generate_people(self, n: int) -> Records:
#         """Generates n people.

#         Parameters
#         ----------
#         n : int
#             Number of people to generate.

#         Returns
#         -------
#         List[Dict[str, Any]]
#             List of dicts that include first_name, last_name, phone_number,
#             address, country, date_of_birth, passport_number and email.

#         Notes
#         -----
#         People are guaranteed to be unique only within a function call.
#         """
#         people = []
#         for _ in range(n):
#             people.append(
#                 {
#                     "first_name": self.fake.unique.first_name(),
#                     "last_name": self.fake.unique.last_name(),
#                     "phone_number": self.fake.unique.phone_number(),
#                     "address": self.fake.unique.address(),
#                     "country": self.fake.unique.country(),
#                     "date_of_birth": self.fake.unique.date_of_birth(),
#                     "passport_number": self.fake.unique.passport_number(),
#                     "email": self.fake.unique.ascii_email(),
#                 }
#             )
#         return people

#     def generate_sessions(
#         self,
#         people: list,
#         base_time: datetime.datetime,
#         window: datetime.timedelta,
#         n: int,
#     ) -> Records:
#         """Generates sessions for people.

#         Parameters
#         ----------
#         people : list
#             People to generate events for.
#         base_time : datetime.datetime
#             Base time for sessions.
#         window : datetime.timedelta
#             Time window for sessions. Events will fill
#             the whole window equidistantly.
#         n : int
#             Number of events to generate.

#         Returns
#         -------
#         List[Dict[str, Any]]
#             List of dicts for events including properties such as
#             person_passport_number, event_time, user_agent, session_id.

#         Notes
#         -----
#         Events can be considered to be unique across function calls
#         since a surrogate key is generated using UUID4.
#         """
#         sessions = []
#         frequency = window / n
#         for i in range(n):
#             person = people[random.randint(0, len(people)-1)]
#             if random.random() < PHONE_PROBABILITY:
#                 useragent = self.fake.android_platform_token()
#             else:
#                 useragent = self.fake.chrome()

#             sessions.append(
#                 {
#                     "person_passport_number": person["passport_number"],
#                     "event_time": base_time + i * frequency,
#                     "user_agent": useragent,
#                     "session_id": str(uuid.uuid4()),
#                 }
#             )
#         return sessions

# # ejemplo de generacion de datos

# if __name__ == "__main__":
#     generator = DataGenerator()
#     sample_people = generator.generate_people(5)  # Generate 5 people for example
#     for person in sample_people:
#         print(person)

    def generate_pasajero(self, n: int) -> Records:
        """Generates n pasajeros.

        Parameters
        ----------
        n : int
            Number of pasajeros to generate.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include nombre, telefono, and correo_electronico.
        """
        pasajeros = []
        for _ in range(n):
            id_pasajero = str(uuid.uuid4())  # Genera un ID único para el pasajero
            pasajeros.append(
                {
                    "ID_pasajero": id_pasajero,
                    "nombre": self.fake.name(),
                    "telefono": self.fake.phone_number(),
                    "correo_electronico": self.fake.email(),
                }
            )
        return pasajeros

    def generate_conductor(self, n: int) -> Records:
        """Generates n conductores.

        Parameters
        ----------
        n : int
            Number of conductores to generate.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include nombre, telefono, and correo_electronico.
        """
        conductores = []
        for _ in range(n):
            id_conductor = str(uuid.uuid4())  # Genera un ID único para el conductor
            conductores.append(
                {
                    "ID_conductor": id_conductor,
                    "nombre": self.fake.name(),
                    "telefono": self.fake.phone_number(),
                    "correo_electronico": self.fake.email(),
                }
            )
        return conductores

    def generate_partnership(self) -> Records:
            """Generates partnerships with car brands.
            genera tantos registros como marcas haya en el diccionario brand_partnership

            Returns
            -------
            List[Dict[str, Any]]
                List of dicts that include marca (car brand) and es_partner.
            """
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
        """Generates n modelo_vehiculos.

        Parameters
        ----------
        n : int
            Number of modelo_vehiculos to generate.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include modelo, tipo_carroceria, apto_discapacitado,
            vclase_economica, emision_rating, seguridad_rating, and marca.
        """
        car_brands = ["Toyota", "Ford", "BMW", "Audi", "Honda", "Mercedes", "Chevrolet", "Volkswagen", "Hyundai", "Nissan"]
        modelo_vehiculos = []
        for _ in range(n):
            marca = self.fake.random_element(elements=car_brands)
            modelo = self.fake.random_element(elements=self.get_modelos(marca))
            tipo_carroceria, apto_discapacitado, vclase_economica, emision_rating, seguridad_rating = self.get_atributos_modelos(marca, modelo)
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
        """Returns a list of car models for a given brand.

        Parameters
        ----------
        marca : str
            Car manufacturer (brand).

        Returns
        -------
        list
            List of car models for the given brand.
        """
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
        # Agregar más marcas y modelos según sea necesario

    def get_atributos_modelos(self, marca: str, modelo: str) -> tuple:
        """Returns model attributes for a given brand and model.

        Parameters
        ----------
        marca : str
            Car manufacturer (brand).
        modelo : str
            Car model.

        Returns
        -------
        tuple
            Tuple containing tipo_carroceria, apto_discapacitado, vclase_economica, and emision_rating.
        """
        if marca == "Toyota":
            if modelo in ["Corolla", "Camry", "Avalon"]:
                return "Sedan", False, "Mid-range", "Medio", 4
            elif modelo in ["RAV4", "Highlander", "4Runner"]:
                return "SUV", False, "Mid-range", "Bajo", 4
            elif modelo == "Tacoma":
                return "Truck", False, "Mid-range", "Medio", 3
            elif modelo == "Prius":
                return "Sedan", True, "Economy", "Alto", 5
            elif modelo == "Sienna":
                return "Minivan", True, "Mid-range", "Medio", 3
        elif marca == "Ford":
            if modelo in ["Mustang", "Fusion"]:
                return "Coupe", False, "Performance", "Alto", 3
            elif modelo in ["F-150", "Ranger"]:
                return "Truck", False, "Mid-range", "Medio", 4
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
                return "Truck", False, "Mid-range", "Medio", 4
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
            elif modelo in ["Golf", "Golf GTI"]:
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
            elif modelo in ["Palisade"]:
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
                return "Truck", False, "Mid-range", "Medio", 4
            elif modelo == "Leaf":
                return "Hatchback", False, "Economy", "Alto", 5
        else:
            return "", False, "", "", 0
        # Agregar más marcas con modelos y atributos correspondientes

# generator = DataGenerator()
# modelos = generator.generate_modelo_vehiculo(10)
# for modelo in modelos:
#     print(modelo)


    def generate_vehiculo(self, n: int) -> Records:
        """Generates n vehiculos.

        Parameters
        ----------
        n : int
            Number of vehiculos to generate.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include patente, año_fabricacion, and modelo.
        """
        car_brands = ["Toyota", "Ford", "BMW", "Audi", "Honda", "Mercedes", "Chevrolet", "Volkswagen", "Hyundai", "Nissan"]
        marca = self.fake.random_element(elements=car_brands)
        modelo = self.fake.random_element(elements=self.get_modelos(marca))
        vehiculos = []
        for _ in range(n):
            vehiculos.append(
                {
                    "patente": self.fake.license_plate(),
                    "año_fabricacion": self.fake.random_int(min=1980, max=2023),
                    "modelo": self.fake.random_element(elements=modelo),
                }
            )
        return vehiculos

    def generate_conductor_vehiculo(self, conductores, vehiculos) -> Records:
        """Generates conductor_vehiculo relationships.

        Parameters
        ----------
        conductores : list
            List of conductores.
        vehiculos : list
            List of vehiculos.

        Returns
        -------
        List[Dict[str, Any]]
            List of dicts that include ID_conductor, patente, and estado.
        """
        conductor_vehiculo = []
        for conductor in conductores:
            for vehiculo in vehiculos:
                conductor_vehiculo.append(
                    {
                        "ID_conductor": conductor["ID_conductor"],
                        "patente": vehiculo["patente"],
                        "estado": self.fake.boolean(),
                    }
                )
        return conductor_vehiculo

    def generate_viaje(self, conductores, vehiculos,  pasajeros) -> Records:
        """Generates n viajes.

        Parameters
        ----------
        n : int
            Number of viajes to generate.
        conductores : list
            List of conductores.
        vehiculos : list
            List of vehiculos.
        pasajeros : list
            List of pas"""
        viajes = []
        for _ in range(n):
            id_viaje = str(uuid.uuid4())  # Genera un ID único para el conductor
            viajes.append(
                {
                    "ID_viaje": id_viaje,
                    "origen": self.fake.city()
                    "destino": self.fake.city()
                    "fecha_hora": self.fake.date_time_this_decade(before_now=True, after_now=False) # fecha aleatoria dentro de la ultima decada. ej:2015-07-15 10:24:36
                    "estado": self.random.choice(['completado', 'en proceso', 'cancelado'])
                    "calificacion": self.random.randint(0, 5)
                    "ID_pasajero": pasajeros["ID_pasajero"]
                    "ID_conductor": conductores["ID_conductor"]
                    "patente": 
                }
            )
        return viajes
        
    def generate_pago(self, n: int, conductores: List[Dict[str, Any]], vehiculos: List[Dict[str, Any]], pasajeros: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generates n viajes.

        Parameters
        ----------
        n : int
            Number of viajes to generate.
        conductores : list
            List of conductores.
        vehiculos : list
            List of vehiculos.
        pasajeros : list
            List of pas"""

