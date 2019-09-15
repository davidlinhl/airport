import os
from util import *
import numpy as np

all_pvg_files=os.listdir(all_pvg_path)
print(all_pvg_files)
for pvg_file in all_pvg_files:

    print("processing {}".format(pvg_file))

    line_count=0
    pvg_file_path=os.path.join(all_pvg_path,pvg_file)
    print(pvg_file_path)

    in_file=open(pvg_file_path)

    speeds=[]

    for line in in_file.readlines():
        line_count+=1
        info=line.split("|")
        print("line:{},id:{}".format(line_count,info[0]))

        car_id=info[0]
        if info[1]=='A' and info[2]=='0':
            is_alarm=0
        else:
            is_alarm=1
        is_empty=int(info[3])
        is_break=info[6]
        date=info[8]
        gps_time=info[9]
        jing_gps=float(info[10])
        wei_gps=float(info[11])
        speed=float(info[12])
        sat_count=int(info[14])

        if info[4]!="3" and info[4]!="4" and info[4]!="5":
            speeds.append(speed)
    print(len(speeds))

    avg_speed=np.average(np.array(speeds))

    out_file_path="./data/avg_speed.txt"
    out_file=open(out_file_path,'a')
    print("{} has {} valid gps points and average speed is {}".format(pvg_file,line_count,avg_speed),file=out_file)
