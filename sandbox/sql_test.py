import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# from loader import load_data_uncached

engine = create_engine(
    f"mysql+pymysql://root:{os.environ.get('ROOT_PASSWORD')}@localhost:3306/data"
)
connection = engine.connect()

# df = pd.read_csv(r'C:\dev\data-science\projects\ip-final-project\data\salaries.csv')

# df.to_sql(
#     name='salaries',
#     con=connection,
#     schema='data',
#     if_exists='replace'
# )

df = pd.read_sql_table(table_name="salaries", con=connection, schema="data")
print(df)
