-- Esquema inicial PostgreSQL para OPITA 360.
-- Esta versión frontend/backend usa datos demostrativos en memoria; el esquema aún no está conectado.
CREATE TABLE IF NOT EXISTS destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    municipality VARCHAR(100) NOT NULL,
    category VARCHAR(60) NOT NULL,
    description TEXT NOT NULL,
    estimated_price INTEGER NOT NULL DEFAULT 0,
    tags TEXT[] NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS itineraries (
    id SERIAL PRIMARY KEY,
    days INTEGER NOT NULL CHECK (days BETWEEN 1 AND 14),
    budget INTEGER NOT NULL CHECK (budget >= 0),
    interests TEXT[] NOT NULL DEFAULT '{}',
    estimated_total INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS itinerary_destinations (
    itinerary_id INTEGER NOT NULL REFERENCES itineraries(id) ON DELETE CASCADE,
    destination_id INTEGER NOT NULL REFERENCES destinations(id),
    visit_order INTEGER NOT NULL,
    PRIMARY KEY (itinerary_id, destination_id),
    UNIQUE (itinerary_id, visit_order)
);
