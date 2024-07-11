from typing import Optional

from custom_types import Records
from database import Database

class Schema:
    def __init__(self):
        self.db = Database()        
    
    # def get_people(self, sample_n: Optional[int] = None) -> Records:
    #     query = "SELECT * FROM people"
    #     if sample_n is not None:
    #         query += f" LIMIT {sample_n}"
    #     return self.db.run_select(query)

# Estos métodos recuperan todos los registros de las tablas  y ejecuta una consulta SQL para seleccionarlos 
# todos devolviendo los resultados.
    def get_pasajero(self) -> Records:
        return self.db.run_select("SELECT * FROM pasajero")
    
    def get_conductor(self) -> Records:
        return self.db.run_select("SELECT * FROM conductor")
    
    def get_partnership(self) -> Records:
        return self.db.run_select("SELECT * FROM partnership")
    
    def get_modelovehiculo(self) -> Records:
        return self.db.run_select("SELECT * FROM modelovehiculo")

    def get_vehiculo(self) -> Records:
        return self.db.run_select("SELECT * FROM vehiculo")
    
    def get_conductorvehiculo(self) -> Records:
        return self.db.run_select("SELECT * FROM conductorvehiculo")
    
    def get_viaje(self) -> Records:
        return self.db.run_select("SELECT * FROM viaje")
    
    def get_pago(self) -> Records:
        return self.db.run_select("SELECT * FROM pago")

# Este método inserta registros en una tabla específica.
# Toma dos argumentos: records, que son los registros a insertar, y table, que es el nombre de 
# la tabla donde se insertarán los registros. Utiliza self.db.run_insert(records, table) para 
# realizar la inserción en la base de datos.
    def insert(self, records: Records, table: str):
        self.db.run_insert(records, table)
    