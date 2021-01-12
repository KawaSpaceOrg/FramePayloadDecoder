
from google.cloud import storage
from payload_decoder import PayloadDecoder
from es_utils import es
from process_utils import flatten_json, clean_up_json
from datetime import datetime
import sys, pprint, os

# Get access to input data frames
input_file_name = sys.argv[1]
decoder_project = os.getenv("GOOGLE_PROJECT", "staging-kawa")
storage_client = storage.Client(decoder_project)

bucket = storage_client.get_bucket(os.getenv("SATELLITE_DATAFRAMES_BUCKET", "satellite-data-frames"))
blob = bucket.blob(input_file_name)
input_file_name = "/"+input_file_name
blob.download_to_filename(input_file_name)


try:
   raw_frame_payload = open(input_file_name, 'rb').read()
   output_telemetry_JSON = PayloadDecoder.decode( raw_frame_payload)
except Exception as e:
   print(e)
   exit(1)

flattened_telemetry_JSON = flatten_json(output_telemetry_JSON)
final_telemetry_JSON = clean_up_json(flattened_telemetry_JSON)
final_telemetry_JSON['updated_at'] = datetime.utcnow()

try:
   es.index(sys.argv[2], final_telemetry_JSON)
except Exception as e:
   print(e)
   exit(2)

