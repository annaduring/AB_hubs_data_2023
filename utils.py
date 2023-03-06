import pandas as pd
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def read_parquet(parquet_path, parquet_file):
    return pd.read_parquet(parquet_path+parquet_file)

# def write_to_csv(df, csv_name):

def connect_to_postgres(database, user, password, host):   
    return psycopg2.connect( database= database, user=user, password=password, host=host )

def check_date(df, col, start='2017-01-01', end='2024-01-01'):
    """
    The function checks whether the date type is correct (datetime64), else it fixes it.
    It also check for possible bad data like missing data, or very low date (like 1970-01-01) 
    due to date trasnformation of numbers     ---    >>   the range can be changed!
    INPUT: the column of a df containing dates and a date range 
    OUTPUT: an additional column in the dataframe of dates that need to be checked (1 = check, 0 = ok) 
    """
    bad_date_index = []
    df['check_date'] = [0]*df.shape[0]
    
    if df[col].dtype in ['datetime64[ns]']:
        print(' ---- data type is correct ------')
        
    else:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].astype('datetime64')
        print('--- data type has been fixed  ---')

 
    for ix, i in enumerate(df[col]):
        if i is pd.NaT or i not in pd.date_range(start=start, end=end):
            bad_date_index.append(ix)
            df.iloc[ix, -1] = 1

    if df['check_date'].sum() == 0:
        df.drop(columns = 'check_date', inplace = True)
        print('--- no other dates to check  ---')

    return df

def send_email(*, sender, recipients, subject, body):
    # if somethign goes wrong, send me an email
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    msg.attach(MIMEText(body))
    
        
    server.send_message(msg)
    server.quit()