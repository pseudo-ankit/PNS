import json
import os
from setting import CURR_DIR

f = open(os.path.join(CURR_DIR, 'last_used_csv.json'), 'w')
used_csv_files = {'details':[], 'profile':[]}

json.dump(used_csv_files, f, indent=2)
f.close()
print("last_used_csv.json has been reset")
