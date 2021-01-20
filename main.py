
from google.cloud import storage
from payload_decoder import PayloadDecoder
from es_utils import es
from process_utils import remove_key_spaces, flatten_json, clean_up_json, get_info_frame, get_filename_time
from datetime import datetime
import sys, pprint, os, json
from binascii import unhexlify

decoder_project = os.getenv("GOOGLE_PROJECT", "staging-kawa")
storage_client = storage.Client(decoder_project)

# Get access to input data frames
inputs = sys.argv[1]
try:
   data = json.loads(inputs)
except Exception as e:
   print(e)
   exit(1)

input_file_name = data['input_file_name']
bucket = storage_client.get_bucket(os.getenv("SATELLITE_DATAFRAMES_BUCKET", "satellite-data-frames"))
blob = bucket.blob(input_file_name)
input_file_name = "/"+input_file_name
blob.download_to_filename(input_file_name)


try:
   total_frame_payload = open(input_file_name, 'rb').read()
   info_frame_payload = get_info_frame(total_frame_payload)
   raw_frame_payload = unhexlify(info_frame_payload)
   output_telemetry_JSON = PayloadDecoder.decode(raw_frame_payload)
except Exception as e:
   print(e)
   exit(2)

flattened_telemetry_JSON = flatten_json(output_telemetry_JSON)
final_telemetry_JSON = remove_key_spaces(clean_up_json(flattened_telemetry_JSON))

try:
   final_telemetry_JSON['_current_time'] = get_filename_time(input_file_name)
except:
   print("could not get time from input filename")
   exit(3)

es_index_name = data['es_index_name']
try:
   es.index(es_index_name, final_telemetry_JSON)
except Exception as e:
   print(e)
   exit(4)


