import sqlalchemy
import pandas

engine = sqlalchemy.create_engine('postgresql+psycopg2://testuser:1234@34.116.192.247/db')

df = pandas.read_sql('SELECT * FROM tab', engine)

print(df)
