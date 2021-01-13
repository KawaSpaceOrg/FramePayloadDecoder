import datetime, sys

def flatten_json(nested_json):
   out = {}
   def flatten(x, name=''):
    if type(x) is dict:
      for key in x:
         flatten(x[key], name + key + ' ')
    elif type(x) is list:
      i = 0
      for entry in x:
         flatten(entry, name + str(i) + ' ')
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


