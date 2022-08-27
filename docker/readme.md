# How to 

This project creates a local dockerized postgresql database where you can create custom databases and tables and read/write data from them.

## Prerequisites

* download and install `Docker` from the official website https://www.docker.com/
* install `docker-compose` (note that it usually comes with `Docker`)

## Run the project

* start `Docker`
* open a terminal within this folder and type `docker-compose up -d`

I everything runs smoothly, you should have your database up and running withing a container in seconds. To access the DB, you can use any clients; I personally use `DBeaver`, which you can get from https://dbeaver.io/. To start a new connection to the created DB, select postgres as your source and use the variables in the `.env` in the GUI.

## Pushing data to the DB

Since you know the credentials to the DB, it is easy to generate a connection string using `SQLAlchemy` and pushing some data through `pandas`. Run the code in `load_to_db_example.py` to fill the tables in the DB with dummy data.

## Stop the project

Go back to your terminal and input `docker-compose down` to stop the running containers.
