import psycopg2
import config
import sql_queries
from utils import connect_to_postgres
import pandas as pd

class Database:
    def __init__(self, database, user, password, host='localhost', port=5432):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect_to_postgres(self):
            try:
                conn = psycopg2.connect(dbname=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
                return conn
            except Exception as e:
                print("Error: ", e)
                return None
            
    def create_table_in_postgres(self, sql_create):
        conn = self.connect_to_postgres()
        if conn is not None:
            try:
                conn.autocommit = True
                cursor = conn.cursor()
                return cursor.execute(sql_create)
            except Exception as e:
                print("Error: ", e)
                return None
    
    def copy_csv_to_postgres(self, sql_copy,table_name, file_name):
        conn = self.connect_to_postgres()
        if conn is not None:
            try:
                cursor = conn.cursor()
                with open(file_name) as f:
                    cursor.copy_expert(sql_copy.format(table_name), f)
                return conn.commit()
            except Exception as e:
                print("Error: ", e)
                return None

    def read_postgres_to_csv(self, sql_read, file_name):
        conn = self.connect_to_postgres()
        if conn is not None:
            try:
                cursor = conn.cursor()
                df = pd.read_sql_query(sql_read, conn)
                conn.close()
                return df.to_csv(f"files/{file_name}.csv", index=False)
            except Exception as e:
                print("Error: ", e)
                return None


