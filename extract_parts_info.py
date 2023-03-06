import config
import utils
import configparser
import time
import pandas as pd
import json
import datetime as dt
from utils import read_parquet

def create_table_parts(parquet_path, parquet_file, cols, file_name ):
    df = read_parquet(parquet_path, parquet_file)
    table_1 = df[cols].copy()

    try:
    # Fixed the date to be datetime
        for i in ['created', 'updated', 'queued']:
            table_1[i] = pd.to_datetime(table_1[i])
    except:
        print("one of these columns doesn't exist")

    # Add ingestion_time
    table_1['ingestion_time'] = dt.datetime.now()

    # Save to csv
    return table_1.to_csv(f"files/{file_name}.csv", index=False)


def create_part_measures(parquet_path, parquet_file, file_name):
    start_time = time.time()
    df = read_parquet(parquet_path, parquet_file)

    try:
        # Code that may raise an error or exception
        if 'holes' not in df.columns():
            raise ValueError("'holes' column doesn't exist")
        
    except:
        # # Extract the "part" values: TABLE 2 and append an ingestion date
        if df['holes'].count() == df.shape[0]:
            get_data_center  = df[['uuid', 'holes']].copy()    
        else:
            get_data_center  = df[df['holes'] != ''][['uuid', 'holes']].copy()

        get_data_center['holes'] = get_data_center['holes'].apply(json.loads)

        # Explode the lists of dictionaries into separate rows
        exploded_df = get_data_center.explode('holes')

        # # Normalize the json dict, keep it string for precision and the index for merging
        measures_df = pd.json_normalize(exploded_df['holes'])[['length', 'radius']].astype(object).set_index(exploded_df.index)
        # Merge
        table_2 = measures_df.join(get_data_center)[['uuid', 'length', 'radius']]

        # Add an ID
        table_2.insert(0, 'measure_id', range(1, 1 + len(table_2)))
        print("Table creation: {} seconds".format(time.time() - start_time))

        return table_2.to_csv(f"files/{file_name}.csv", index=False)