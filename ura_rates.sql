
CREATE DATABASE IF NOT EXISTS ura_rates;
USE ura_rates;

DROP TABLE IF EXISTS ura_rates;

CREATE TABLE IF NOT EXISTS ura_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ppCode VARCHAR(20),
    ppName VARCHAR(255),
    weekdayMin VARCHAR(20),
    weekdayRate DECIMAL(10, 2),
    satdayMin VARCHAR(20),
    satdayRate DECIMAL(10, 2),
    sunPHMin VARCHAR(20),
    sunPHRate DECIMAL(10, 2),
    startTime TIME,
    endTime TIME
);


