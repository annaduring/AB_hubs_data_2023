import pandas as pd
import psycopg2
from utils import read_parquet, check_date, connect_to_postgres
from sql_queries import sql_create_parts, sql_create_part_measures, sql_grant, sql_copy, solution_1, solution_2
from extract_parts_info import create_table_parts, create_part_measures
# from sql_functions import create_table_in_postgres, copy_csv_to_postgres, read_postgres_to_csv
from sql_functions_class import Database
import config
import time

try:
    parquet_path = getattr(config, 'parquet_path')
    parquet_file = "files/DE_case_dataset.gz.parquet"

    # Extract data from the parquet and transform it to create 2 csv files: 
    # table_parts & table_part_measures
    start_time = time.time()

    table_parts = create_table_parts(parquet_path, parquet_file, ['uuid', 'created', 'updated', 'queued', 'units', 'status', 'time'], file_name = "table_parts")
    table_parts_measures  = create_part_measures(parquet_path, parquet_file, file_name = "table_part_measures")
    t1 = time.time()
    print("""Time to extract in from the parquet file and create two csv files: {} seconds""".format(t1 - start_time))

    # connect to postgres
    database = getattr(config, 'database')
    user = getattr(config, 'username')
    password = getattr(config, 'password')
    host = getattr(config, 'host') # I added this one in case you don't use the localhost
    port = getattr(config, 'port') # I add this in case you don't use port 5324

    db = Database(database, user, password)

    # print('Connect to postgres')
    # conn = connect_to_postgres(database, user, password, host)

    # CReate a tble in postgres
    create_queries = [sql_create_parts, sql_create_part_measures]

    for query in create_queries:
        # Create tables in postgres
        db.create_table_in_postgres(query)
        print(f"Table created")


    # load csv in the tables just created
    tables = ['public.partsAB', 'public.part_measuresAB']
    created_csv = ["files/table_parts.csv", "files/table_part_measures.csv"]

    for table, csvfile in zip(tables, created_csv):
        db.copy_csv_to_postgres(sql_copy, table, csvfile)
        print(f"Tables {table} copied")

    # Create the final csv file -  Solution 1 : which uuid are faulty
    db.read_postgres_to_csv(solution_2, 'solution_2')
    print("Created Solution 2")

    t4 = time.time()
    print("""Time to complete the ELTL: {} seconds""".format(t4 - start_time))

except:
    print("Something went wrong")
    from utils import send_email
    import traceback
    
    send_email(sender      = 'Anna Bogo<anna.during.nl@gmail.com>',
                    recipients  = 'anna.during.nl@gmail.com',
                    subject     = f'The ELTL went wrong, find the error below',
                    body        =  traceback.format_exc())   