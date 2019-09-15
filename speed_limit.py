import os
from util import *
import math

all_pvg_files=os.listdir(all_pvg_empty_path)
print(all_pvg_files)


for pvg_file in all_pvg_files:

    print("processing {}".format(pvg_file))

    line_count=0
    pvg_file_path=os.path.join(all_pvg_empty_path,pvg_file)
    print(pvg_file_path)

    hour=pvg_file.split("-")[1]
    hour=int(hour)
    print(hour)

    files=[]
    for minute in range(0,60,5):
        path=os.path.join(empty_by_minute_path,"{:02d}:{:02d}".format(hour,minute))
        file=open(path,"w")
        files.append(file)

    in_file=open(pvg_file_path)

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


        minute=gps_time.split(" ")
        if len(minute)!=2:
            continue
        minute=minute[1]
        minute=int(minute.split(":")[1])

        index=int(math.floor(minute/5))
        print(line,end="",file=files[index])

'''
2018-04-01 00:00:02

'''
