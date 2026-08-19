CREATE DATABASE IF NOT EXISTS EcoMap;

USE EcoMap;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME DEFAULT NULL
);

-- Nova Tabela: Ecopontos (Pontos de Coleta)
CREATE TABLE IF NOT EXISTS ecopontos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) DEFAULT 'Palhoça',
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    materiais VARCHAR(255) DEFAULT 'Recicláveis Gerais',
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);