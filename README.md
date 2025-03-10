# commodity service

## Overview
This is a FastAPI service, that exposes Crude oil imports data

---

## Features
- **GET /commodity/oil/**: listing endpoint that supports pagination and filter vai query params and returns the list of crude oil import data
- **GET /commodity/oil/record/{id}**: Gets the crude oil import record by id
- **PATCH /commodity/oil/record/{id}**: Supports partial and full update to a single record by id
- **PUT /commodity/oil/record/**: Creates new record
- **DELETE /commodity/oil/{id}**: Deletes record by id 

---

## Prerequisites
Before starting the service, ensure you have:
- Docker

---

## Installation

### Clone the Repository
https://github.com/AjinkyaKaley/annalect-take-home-project.git

### Run docker
start the docker application on local machine

### How to start the application
1. Open terminal
2. Navaigate to the directory where the repository is cloned
3. Check if the shell has access to docker and docker compose command
4. Run `docker compose build`
5. Run `docker compose up`
6. Fastapi API Application setup complete and service is ready for use

## Accessing Swagger UI
http://localhost:8000/docs


## Tech Stack
- FastAPI
- Pydantic
- Postresql
- Psycopg3 (db driver)
- Docker

## Technical specfications 

This application use python3.12 which is declared in Dockerfile
When `docker comopose up` runs, it starts the following 3 services
- web
- db
- pgadmin

**web** - service that builds the docker image from `Dockerfile`, which doees the following
- pull python image `python:3.12-slim-bookworm`
- install `uv` package and project manager
- creates virutal environment
- sets the `STAGE=prod` (If you are running locally set the environment variable STAGE)
- installs python dependencies listed in `pyproject.toml`
- runs command `uvicorn main:app --host 0.0.0.0 --port 8000`

**db** - service that creates postgre server and data volume, using the credentials listed in .env files
- init-scripts directory contains DDL scripts, that creates schema, table and insert
- `01_create_schema.sql` creates a commodity schema
- `02_create_tables.sql` creates a oil table and adds addtional `id` column as primary key
- `03_insert_data.sql` bulk loads the data into the table

The docker compose is setup to create to volumes, where the table data is stored and for csv file data its stored under `./data:/var/lib/postgresql/csv_files`

**pgadmin** - service thats the pgadmin app on docker container, and can be accessed via http://localhost:5050


## Troubleshooting guide
### For clean restart
- open new terminal
- run `docker compose down`
- run `docker volume ls` and get volume by name `take_home_test_postgres-data`
- run `docker volume rm take_home_test_postgres-data` to delete the volume, this will wipe out all the data in pg database
- run `docker compose build` (builds)
- run `docker compose up`   (starts)
- clean restart complete
