#%%
import pandas as pd

df = pd.read_csv('data/faers.csv')
df.head()
# %%
from sqlalchemy import URL, create_engine, text

# Matches the postgres service in docker-compose.yml
url = URL.create(
    drivername='postgresql+psycopg',
    username='postgres',
    password='postgres',
    host='localhost',  # use 'postgres' when running inside the app container
    port=5432,
    database='faers',
)
engine = create_engine(url)

with engine.connect() as conn:
    print(conn.execute(text('select version()')).scalar())
# %%
df.to_sql('faers', con=engine, if_exists='replace', index=False)