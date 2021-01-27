
from google.cloud import storage
from payload_decoder import PayloadDecoder
from es_utils import es

from process_utils import remove_key_spaces, flatten_json, clean_up_json, get_info_frame, get_filename_time
from datetime import datetime
import constant, traceback
import sys, pprint, os, json
from binascii import unhexlify

from db_utils import db_conn, update_run_status

decoder_project = os.getenv("GOOGLE_PROJECT", "staging-kawa")
storage_client = storage.Client(decoder_project)

# Get access to input data frames
inputs = sys.argv[1]
try:
   data = json.loads(inputs)
except Exception as e:
   print(e,traceback.format_exc())
   exit(1)


bucket = storage_client.get_bucket(os.getenv("SATELLITE_DATAFRAMES_BUCKET", "satellite-data-frames"))

input_file_names_csv = data['input_file_names']
input_file_names = input_file_names_csv.split(',')
es_index_name = data['es_index_name']

for input_file_name in input_file_names:

   try:
      blob = bucket.blob(input_file_name)
      input_file_name = "/"+input_file_name
      blob.download_to_filename(input_file_name)
   except Exception as e:
      print(input_file_name+":")
      print(e,traceback.format_exc())
      update_run_status(input_file_name, constant.FAILURE)
      continue
   
   try:
      total_frame_payload = open(input_file_name, 'rb').read()
      info_frame_payload = get_info_frame(total_frame_payload)
      raw_frame_payload = unhexlify(info_frame_payload)
      output_telemetry_JSON = PayloadDecoder.decode(raw_frame_payload)
   except Exception as e:
      print(input_file_name+":")
      print(e,traceback.format_exc())
      update_run_status(input_file_name, constant.FAILURE)
      continue

   flattened_telemetry_JSON = flatten_json(output_telemetry_JSON)
   final_telemetry_JSON = remove_key_spaces(clean_up_json(flattened_telemetry_JSON))

   try:
      final_telemetry_JSON['_current_time'] = get_filename_time(input_file_name)
   except:
      print(input_file_name+":")
      print("could not get time from input filename")
      update_run_status(input_file_name, constant.FAILURE)
      continue
   
   try:
      es.index(es_index_name, final_telemetry_JSON)
   except Exception as e:
      print(input_file_name+":")
      print(e, traceback.format_exc())
      update_run_status(input_file_name, constant.FAILURE)
      continue
   
   try:
      update_run_status(input_file_name, constant.SUCCESS)
      print("successfully decoded the file: "+input_file_name)

   except Exception as e:
      print(input_file_name+":")
      print("file decoded but could not update status in DB")
      print(e, traceback.format_exc())

if (db_conn):
   db_conn.close()



