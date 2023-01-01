CREATE DATABASE edgar_sec_xbrl;

USE edgar_sec_xbrl;

CREATE TABLE IF NOT EXISTS symbols (
    symbol VARCHAR(10) NOT NULL,
    cik INT NOT NULL,
    company_name varchar(128) NOT NULL,
    exchange VARCHAR(20) NULL,
    date_updated DATE,
    PRIMARY KEY (symbol),
    CONSTRAINT unique_symbol_const UNIQUE(symbol)
);

CREATE TABLE IF NOT EXISTS company_info (
    symbol VARCHAR(10) NOT NULL,
    company_name VARCHAR(128) NOT NULL,
    company_desc VARCHAR(256),
    sector VARCHAR(64),
    industry VARCHAR(64),
    exchange VARCHAR(24),
    company_address VARCHAR(128) NOT NULL,
    country VARCHAR(24) NOT NULL,
    PRIMARY KEY (symbol),
    FOREIGN KEY (symbol) REFERENCES symbols(symbol) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_fundamentals (
    symbol VARCHAR(10) NOT NULL,
    fiscal_year_end DATE,
    FOREIGN KEY (symbol) REFERENCES symbols(symbol) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS common_shares_outstanding (
    symbol VARCHAR(10) NOT NULL,
    end_date DATE NOT NULL,
    units INT NOT NULL,
    fiscar_year INT NOT NULL,
    fiscal_quarter varchar(2) NOT NULL,
    FOREIGN KEY (symbol) REFERENCES symbols(symbol) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public_float (
    symbol VARCHAR(10) NOT NULL,
    end_date DATE NOT NULL,
    units INT NOT NULL,
    fiscar_year INT NOT NULL,
    fiscal_quarter varchar(2) NOT NULL,
    FOREIGN KEY (symbol) REFERENCES symbols(symbol) ON DELETE CASCADE
);