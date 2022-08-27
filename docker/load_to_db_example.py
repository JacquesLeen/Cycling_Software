import pandas as pd
from requests import post
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()

pg_user = os.environ.get("POSTGRES_USER")
pg_password = os.environ.get("POSTGRES_PASSWORD")
pg_host = os.environ.get("POSTGRES_HOST")
pg_port = os.environ.get("POSTGRES_PORT")
pg_db = os.environ.get("POSTGRES_DB")

teams = pd.DataFrame({"team_id": [1, 2, 3], "name": ["Lampre", "Mapei", "Liquigas"], "nationality": ["ITA", "ITA", "ITA"]})
cyclists = pd.DataFrame({"cyclist_id": [23, 45, 14], "name": ["Alessandro Ballan", "Andrea Tafi", "Ivan Basso"], "nationality": ["ITA", "ITA", "ITA"], "age": [43, 52, 19], "team_id": [1, 2, 3]})

postgres_engine = sqlalchemy.create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")

teams.to_sql("dim_teams", postgres_engine, schema="public", if_exists="replace", chunksize=5000, method="multi")
cyclists.to_sql("dim_cyclists", postgres_engine, schema="public", if_exists="replace", chunksize=5000, method="multi")
