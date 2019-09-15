import os
from util import *
import math

all_pvg_files=os.listdir(all_pvg_path)
print(all_pvg_files)

for pvg_file in all_pvg_files:
    print("processing {}".format(pvg_file))

    pvg_file_path=os.path.join(all_pvg_path,pvg_file)
    print(pvg_file)
    in_file=open(pvg_file_path)

    lines=[]
    for line in in_file.readlines():
        lines.append(line)

    sorted_lines= sorted(lines,key=lambda line:get_gps_time(line))

    for line in sorted_lines:
        info=line.split("|")
        car_id=int(info[0])

        gps_time=info[9]
        if len(gps_time.split(" ")) !=2:
            continue
        with open(os.path.join(driver_activities_path,info[0]), 'a') as f:
            print(line,end="",file=f)
