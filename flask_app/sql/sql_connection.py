from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv()

sql_format = os.getenv("SQL_CONNECTION_FORMAT")
sql_username = os.getenv("SQL_USERNAME")
sql_password = os.getenv("SQL_PASSWORD")
sql_db = os.getenv("SQL_DATABASE")
sql_connection = sql_format % (sql_username, sql_password, sql_db)

engine = sqlalchemy.create_engine(sql_connection)