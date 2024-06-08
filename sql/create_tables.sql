

-- CREATE TABLE IF NOT EXISTS people (
--     first_name VARCHAR(51),
--     last_name VARCHAR(52),
--     phone_number VARCHAR(53),
--     address VARCHAR(100),
--     country VARCHAR(54),
--     date_of_birth TIMESTAMP,
--     passport_number VARCHAR(55) PRIMARY KEY,
--     email VARCHAR(56)
-- );

-- CREATE TABLE IF NOT EXISTS sessions (
--     session_id VARCHAR(50) PRIMARY KEY,
--     event_time TIMESTAMP,
--     user_agent VARCHAR(300),
--     person_passport_number VARCHAR(55) REFERENCES people
-- );


CREATE TABLE IF NOT EXISTS Pasajero (
 ID_pasajero INT PRIMARY KEY,
 nombre VARCHAR(50),
 telefono VARCHAR(15),
 correo_electronico VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Conductor (
 ID_conductor INT PRIMARY KEY,
 nombre VARCHAR(50),
 telefono VARCHAR(15),
 correo_electronico VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Partnership (
 marca VARCHAR(50) PRIMARY KEY,
 es_partner BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS ModeloVehiculo (
 modelo VARCHAR(50) PRIMARY KEY,
 tipo_carroceria VARCHAR(50) CONSTRAINT selec_carro CHECK (tipo_carroceria IN ('Sedan', 'Hatchback', 'Suv', 'Coupe', 'Pick-up', 'Roadster', 'Minivan')),
 apto_discapacitado BOOLEAN NOT NULL,
 vclase_economica VARCHAR(50) CONSTRAINT economic_level CHECK (vclase_economica IN ('Economy', 'Mid-range', 'Luxury', 'Performance', 'Exotic')),
 emision_rating VARCHAR(50) CONSTRAINT co2_levels CHECK (emision_rating IN ('Cero', 'Bajo', 'Alto')),
 seguridad_rating INT CONSTRAINT test_results CHECK (seguridad_rating >= 0 AND seguridad_rating  <= 5 AND seguridad_rating = FLOOR(seguridad_rating)),
 marca VARCHAR(50),
 FOREIGN KEY (marca) REFERENCES Partnership(marca)
);

CREATE TABLE IF NOT EXISTS Vehiculo (
 patente VARCHAR(20) PRIMARY KEY,
 año_fabricacion INT CONSTRAINT año_neg CHECK (año_fabricacion >= 0),
 modelo VARCHAR(50),	
 FOREIGN KEY (modelo) REFERENCES ModeloVehiculo(modelo)
);

CREATE TABLE IF NOT EXISTS ConductorVehiculo (
 ID_conductor INT,
 patente VARCHAR(20),
 estado BOOLEAN NOT NULL,
 PRIMARY KEY (ID_conductor, patente),
 FOREIGN KEY (ID_conductor) REFERENCES Conductor(ID_conductor),
 FOREIGN KEY (patente) REFERENCES Vehiculo(patente)
);

CREATE TABLE IF NOT EXISTS Viaje (
 ID_viaje INT PRIMARY KEY,
 origen VARCHAR(50),
 destino VARCHAR(50),
 fecha_hora TIMESTAMP NOT NULL,
 estado VARCHAR(20) CONSTRAINT estado_viaje CHECK (estado IN ('completado', 'cancelado')),
calificacion INT CONSTRAINT calific_rango CHECK (calificacion >= 0 AND calificacion  <= 5 AND  calificacion = FLOOR(calificacion)),
 ID_pasajero INT,
 ID_conductor INT,
 patente VARCHAR(20),
 FOREIGN KEY (ID_pasajero) REFERENCES Pasajero(ID_pasajero),
 FOREIGN KEY (ID_conductor, patente) REFERENCES ConductorVehiculo(ID_conductor, patente)
);

CREATE TABLE IF NOT EXISTS Pago (
 ID_pago INT PRIMARY KEY,
 monto DECIMAL(10, 2) CONSTRAINT nodinero_neg CHECK (monto >= 0),
 metodo_pago VARCHAR(50),
 ID_viaje INT,
 FOREIGN KEY (ID_viaje) REFERENCES Viaje(ID_viaje)
);

CREATE OR REPLACE FUNCTION verificar_estado_conductor_vehiculo()
RETURNS TRIGGER AS $$
BEGIN

 -- Verificar si existe un registro en ConductorVehiculo que cumpla las condiciones
 IF NOT EXISTS (
   SELECT 1 FROM ConductorVehiculo
   WHERE ID_conductor = NEW.ID_conductor
     AND patente = NEW.patente
     AND estado = TRUE
 ) THEN
   -- Si no existe, se levanta un error y se rechaza la inserción o actualización
   RAISE EXCEPTION 'El conductor no está activo o no corresponde al vehículo.';
 END IF;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creación del trigger que utiliza la función antes de insertar o actualizar en Viaje
CREATE TRIGGER verificar_estado_conductor_vehiculo_trigger
BEFORE INSERT OR UPDATE ON Viaje
FOR EACH ROW EXECUTE FUNCTION verificar_estado_conductor_vehiculo();

-- Roles
CREATE ROLE admin;
CREATE ROLE operator;
CREATE ROLE auditor;
	
GRANT ALL PRIVILEGES ON Pasajero TO admin;
GRANT ALL PRIVILEGES ON Conductor TO admin;
GRANT ALL PRIVILEGES ON Partnership TO admin;
GRANT ALL PRIVILEGES ON ModeloVehiculo TO admin;
GRANT ALL PRIVILEGES ON Vehiculo TO admin;
GRANT ALL PRIVILEGES ON ConductorVehiculo TO admin;
GRANT ALL PRIVILEGES ON Viaje TO admin;
GRANT ALL PRIVILEGES ON Pago TO admin;
GRANT SELECT, INSERT, UPDATE ON Pasajero TO operator;
GRANT SELECT, INSERT, UPDATE ON Conductor TO operator;
GRANT SELECT, INSERT, UPDATE ON Vehiculo TO operator;
GRANT SELECT, INSERT, UPDATE ON ConductorVehiculo TO operator;
GRANT SELECT, INSERT, UPDATE ON Viaje TO operator;
GRANT SELECT, INSERT, UPDATE ON Pago TO operator;
GRANT SELECT ON ModeloVehiculo TO operator;
GRANT SELECT ON Partnership TO operator;
GRANT SELECT ON Pasajero TO auditor;
GRANT SELECT ON Conductor TO auditor;
GRANT SELECT ON Partnership TO auditor;
GRANT SELECT ON ModeloVehiculo TO auditor;
GRANT SELECT ON Vehiculo TO auditor;
GRANT SELECT ON ConductorVehiculo TO auditor;
GRANT SELECT ON Viaje TO auditor;
GRANT SELECT ON Pago TO auditor;

