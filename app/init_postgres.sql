DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'amn_datawarehouse') THEN
      CREATE DATABASE amn_datawarehouse;
   END IF;
END
$$;


CREATE TABLE IF NOT EXISTS bitcoin (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);