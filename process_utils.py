import datetime, sys
import dateutil.parser



def get_filename_time(filename):
  parts = filename.split('_')
  return str(dateutil.parser.isoparse(parts[-1]))

def get_info_frame(frame_payload):
  for i in range(len(frame_payload)):
    if frame_payload[i] == 'c' and frame_payload[i+1] == 'd':
        frame_payload = frame_payload[i:]
        break
  return frame_payload

def flatten_json(nested_json):
   out = {}
   def flatten(x, name=''):
    if type(x) is dict:
      for key in x:
         flatten(x[key], name + key + '_')
    elif type(x) is list:
      i = 0
      for entry in x:
         flatten(entry, name + str(i) + '_')
         i +=1
    else:
      out[name[:-1]] = x  
    return out
   
   return flatten(nested_json)

# This is there because Elastic Search throws an error with datetime.timedelta
def clean_up_json(kv):
    for key in kv:
        val = kv[key]
        if isinstance(val, datetime.timedelta):
            kv[key] = str(val)
    return kv

def remove_key_spaces(kv):
  kv = {k.replace(' ', '_'): v
  for k, v in kv.items()}
  return kv
