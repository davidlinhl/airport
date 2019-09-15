import os
from util import *

driver_files=os.listdir(driver_activity_analyse)

queue=[]
out_file=open(os.path.join("./data/new_queueing.csv"),"w")
for driver_file in driver_files:
    print("processing {}".format(driver_file))

    in_file=open(os.path.join(driver_activity_analyse,driver_file))


    for line in in_file.readlines():
        info=line.rstrip("\n").split(",")
        print(info)
        type=info[0]
        start=info[1]
        time=info[3]
        if type=="queue":
            queue.append([driver_file,start,time])

sorted_queue= sorted(queue,key=lambda x:x[1])

for hour in range(0,24):
    for minute in range(0,60,5):
        print("{}:{}~{}:{}".format(hour,minute,hour,minute+5),end=",",file=out_file)
        start="2018-04-01 {}:{}:{}".format(hour,minute,0)
        end="2018-04-01 {}:{}:{}".format(hour,minute+5,0)
        cars=[]
        for car in sorted_queue:
            if car[1]>=start and car[1]<end:
                cars.append(car)
        print(len(cars),end=",",file=out_file)
        if len(cars)==0:
            print("\n",end="",file=out_file)
            continue
        time=0
        for car in cars:
            time+=int(car[2])
        print(float(time)/float(len(cars)),end=",",file=out_file)

        for car in cars:
            print("{}->starting {} for {}".format(car[0],car[1],car[2]),end=",",file=out_file)

        print("\n",end="",file=out_file)



'''
file_paths=os.listdir(filtered_driver_activities_path)
for file_path in file_paths:
    line_cout=len(open(os.path.join(filtered_driver_activities_path,file_path)).readlines())
    if line_cout==1:  #说明只是经过
        os.remove(os.path.join(filtered_driver_activities_path,file_path))
        print("{} deleted".format(file_path))
'''
