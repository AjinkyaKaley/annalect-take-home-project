COPY commodity.oil(year,month,originName,originTypeName,destinationName,destinationTypeName,gradeName,quantity)
FROM '/var/lib/postgresql/csv_files/data.csv'
WITH (FORMAT CSV, HEADER true, DELIMITER ',');