
CREATE TABLE environment_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    image TEXT,
    timestamp TIMESTAMP
);
