from common.json_handing import h_json
import os
from common.t_json import  parse_json

hj = h_json()
local_dir = os.getcwd()
print("local_dir: %s " % local_dir)
res = hj.parse_json("../config/env.json")
print res


# local_dir = os.getcwd()
# print("local_dir: %s " % local_dir)
# res = parse_json("../config/env.json")
# print res
