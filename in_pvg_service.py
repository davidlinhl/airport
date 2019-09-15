import os
from util import *


all_gps_files=os.listdir(all_gps_path)
print(all_gps_files)

for gps_file in all_gps_files:
    if "{}in_PVG.txt".format(gps_file.rstrip("gps.txt")) in os.listdir(all_pvg_service_path):
        continue
    print("processing {}".format(gps_file))

    line_count=0
    gps_file_path=os.path.join(all_gps_path,gps_file)
    in_file=open(gps_file_path)
    out_file_path=os.path.join(all_pvg_service_path,"{}in_PVG.txt".format(gps_file.rstrip("gps.txt")))
    out_file=open(out_file_path,"w")

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


        '''
            浦东机场周边范围
            121.76,31.195
            121.88,31.10
        '''
        if info[4]!="3" and info[4]!="4" and info[4]!="5":
            if jing_gps>121.76 and jing_gps<121.88 and wei_gps>31.10 and wei_gps<31.195 and ~is_alarm and ~is_empty and speed<150 and sat_count>0:
                print(line,end="",file=out_file)
