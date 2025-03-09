CREATE TABLE IF NOT EXISTS commodity.oil(
    id SERIAL PRIMARY KEY,
    year integer,
    month integer,
    originName text,
    originTypeName text,
    destinationName text,
    destinationTypeName text,
    gradeName text,
    quantity integer
)