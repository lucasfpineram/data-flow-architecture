

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

--DROP TABLE pasajero CASCADE;
--DROP TABLE conductor CASCADE;
--DROP TABLE partnership CASCADE;
--DROP TABLE modelovehiculo CASCADE;
--DROP TABLE vehiculo CASCADE;
--DROP TABLE conductorvehiculo CASCADE;
--DROP TABLE viaje CASCADE;
--DROP TABLE pago CASCADE;

CREATE TABLE IF NOT EXISTS pasajero (
 "ID_pasajero" VARCHAR(200) PRIMARY KEY,
 nombre VARCHAR(50),
 telefono VARCHAR(20),
 correo_electronico VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS conductor (
 "ID_conductor" VARCHAR(200) PRIMARY KEY,
 nombre VARCHAR(50),
 telefono VARCHAR(20),
 correo_electronico VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS partnership (
 marca VARCHAR(50) PRIMARY KEY,
 es_partner BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS modelovehiculo (
 modelo VARCHAR(50) PRIMARY KEY,
 tipo_carroceria VARCHAR(50) CONSTRAINT selec_carro CHECK (tipo_carroceria IN ('Sedan', 'Hatchback', 'Suv', 'Coupe', 'Pick-up', 'Roadster', 'Minivan')),
 apto_discapacitado BOOLEAN NOT NULL,
 vclase_economica VARCHAR(50) CONSTRAINT economic_level CHECK (vclase_economica IN ('Economy', 'Mid-range', 'Luxury', 'Performance', 'Exotic')),
 emision_rating VARCHAR(50) CONSTRAINT co2_levels CHECK (emision_rating IN ('Cero', 'Bajo', 'Alto')),
 seguridad_rating INT CONSTRAINT test_results CHECK (seguridad_rating >= 0 AND seguridad_rating  <= 5 AND seguridad_rating = FLOOR(seguridad_rating)),
 marca VARCHAR(50),
 FOREIGN KEY (marca) REFERENCES partnership(marca)
);

CREATE TABLE IF NOT EXISTS vehiculo (
 patente VARCHAR(20) PRIMARY KEY,
 ano_fabricacion INT CONSTRAINT año_neg CHECK (ano_fabricacion >= 0),
 modelo VARCHAR(50),	
 FOREIGN KEY (modelo) REFERENCES modelovehiculo(modelo)
);

CREATE TABLE IF NOT EXISTS conductorvehiculo (
 "ID_conductor" VARCHAR(200),
 patente VARCHAR(20),
 estado BOOLEAN NOT NULL,
 PRIMARY KEY ("ID_conductor", patente),
 FOREIGN KEY ("ID_conductor") REFERENCES conductor("ID_conductor"),
 FOREIGN KEY (patente) REFERENCES vehiculo(patente)
);

CREATE TABLE IF NOT EXISTS viaje (
 "ID_viaje" INT PRIMARY KEY,
 origen VARCHAR(50),
 destino VARCHAR(50),
 fecha_hora TIMESTAMP NOT NULL,
 estado VARCHAR(20) CONSTRAINT estado_viaje CHECK (estado IN ('completado', 'cancelado')),
 calificacion INT CONSTRAINT calific_rango CHECK (calificacion >= 0 AND calificacion  <= 5 AND  calificacion = FLOOR(calificacion)),
 "ID_pasajero" VARCHAR(200),
 "ID_conductor" VARCHAR(200),
 patente VARCHAR(20),
 FOREIGN KEY ("ID_pasajero") REFERENCES pasajero("ID_pasajero"),
 FOREIGN KEY ("ID_conductor", patente) REFERENCES conductorvehiculo("ID_conductor", patente)
);

CREATE TABLE IF NOT EXISTS pago (
 "ID_pago" VARCHAR(200) PRIMARY KEY,
 monto DECIMAL(10, 2) CONSTRAINT nodinero_neg CHECK (monto >= 0),
 metodo_pago VARCHAR(50),
 "ID_viaje" INT,
 FOREIGN KEY ("ID_viaje") REFERENCES viaje("ID_viaje")
);

CREATE OR REPLACE FUNCTION verificar_estado_conductor_vehiculo()
RETURNS TRIGGER AS $$
BEGIN

 -- Verificar si existe un registro en ConductorVehiculo que cumpla las condiciones
 IF NOT EXISTS (
   SELECT 1 FROM conductorvehiculo
   WHERE "ID_conductor" = NEW."ID_conductor"
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
BEFORE INSERT OR UPDATE ON viaje
FOR EACH ROW EXECUTE FUNCTION verificar_estado_conductor_vehiculo();


-- Roles
--CREATE ROLE admin;
--CREATE ROLE operator;
--CREATE ROLE auditor;
	
-- GRANT ALL PRIVILEGES ON pasajero TO admin;
-- GRANT ALL PRIVILEGES ON conductor TO admin;
-- GRANT ALL PRIVILEGES ON partnership TO admin;
-- GRANT ALL PRIVILEGES ON modelovehiculo TO admin;
-- GRANT ALL PRIVILEGES ON vehiculo TO admin;
-- GRANT ALL PRIVILEGES ON conductorvehiculo TO admin;
-- GRANT ALL PRIVILEGES ON viaje TO admin;
-- GRANT ALL PRIVILEGES ON pago TO admin;
-- GRANT SELECT, INSERT, UPDATE ON pasajero TO operator;
-- GRANT SELECT, INSERT, UPDATE ON conductor TO operator;
-- GRANT SELECT, INSERT, UPDATE ON vehiculo TO operator;
-- GRANT SELECT, INSERT, UPDATE ON conductorvehiculo TO operator;
-- GRANT SELECT, INSERT, UPDATE ON viaje TO operator;
-- GRANT SELECT, INSERT, UPDATE ON pago TO operator;
-- GRANT SELECT ON modelovehiculo TO operator;
-- GRANT SELECT ON partnership TO operator;
-- GRANT SELECT ON pasajero TO auditor;
-- GRANT SELECT ON conductor TO auditor;
-- GRANT SELECT ON partnership TO auditor;
-- GRANT SELECT ON modelovehiculo TO auditor;
-- GRANT SELECT ON vehiculo TO auditor;
-- GRANT SELECT ON conductorvehiculo TO auditor;
-- GRANT SELECT ON viaje TO auditor;
-- GRANT SELECT ON pago TO auditor;

