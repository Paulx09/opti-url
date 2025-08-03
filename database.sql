-- Base de datos para OptiURL
CREATE DATABASE IF NOT EXISTS db_opti_url;
USE db_opti_url;

-- Tabla para almacenar los enlaces
CREATE TABLE IF NOT EXISTS LINKS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    URL TEXT NOT NULL,
    SHORT_LINK VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de prueba (opcional)
-- INSERT INTO LINKS (URL, SHORT_LINK) VALUES ('https://ejemplo.com', 'abc1234');
