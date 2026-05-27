-- Create the schema
CREATE SCHEMA IF NOT EXISTS automation_schema;

-- Create the items table within the schema
CREATE TABLE IF NOT EXISTS automation_schema.items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantity INT NOT NULL DEFAULT 0
);