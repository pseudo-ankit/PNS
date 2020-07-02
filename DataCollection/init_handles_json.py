import json
import os
from setting import CURR_DIR
from TwitterHandles import handles
# f  = open('handles.json', 'r')
# data = json.load(f)

# for handle in data:
# 	print('name: '+handle+'value: '+str(data[handle]))

f = open(os.path.join(CURR_DIR, 'handles.json'), 'w')
data = {"handles":[]}

for handle in handles:
	temp = {}
	temp["screen_name"] = handle
	temp["since_id"] = None
	data["handles"].append(temp)

json.dump(data, f, indent=2)
f.close()
print("handles.json has been reset")
