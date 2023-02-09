import requests
from sqlalchemy import create_engine
import pandas as pd
import psycopg2

engine = create_engine(
    "postgresql+psycopg2://root:root@0.0.0.0:5432/test_db")

query = """
select *
from billboard
limit 100
"""

df = pd.read_sql_query(query, engine)