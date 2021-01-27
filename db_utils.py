import os, traceback
import psycopg2

def new_db_connection():
    connection_string = "dbname={dbname} user={user} host={host} password={password} port={port}".format(
    dbname = os.getenv('PG_DB'), user = os.getenv('PG_USER'), host = os.getenv('PG_HOST'),  password = os.getenv('PG_PASS'), port = os.getenv('PG_PORT'))
    try:
        db_conn = psycopg2.connect(connection_string)
    except Exception as e:
        print(e,traceback.format_exc())
        exit(1)
    return db_conn

db_conn = new_db_connection()

update_query = "UPDATE DATAFRAMES SET decoder_run_status = '{decoder_run_status}' WHERE cloud_filename = '{cloud_filename}';"

def update_run_status(input_file_name, status):
    input_file_name = input_file_name.lstrip('/')
    cursor = db_conn.cursor()
    cursor.execute(update_query.format(decoder_run_status=status, cloud_filename=input_file_name))
    db_conn.commit()
   




