import os
from util import *

driver_files=os.listdir(driver_activities_path)

for driver_file in driver_files:
    print("processing {}".format(driver_file))

    in_file=open(os.path.join(driver_activities_path,driver_file))
    out_file=open(os.path.join(filtered_driver_activities_path,driver_file),"w")

    lines=[]
    for line in in_file.readlines():
        lines.append(line)

    sorted_lines= sorted(lines,key=lambda line:get_gps_time(line))

    line_pre=sorted_lines[0]
    is_empty_pre=get_is_empty(line_pre)
    gps_time_pre=get_gps_time(line_pre)

    print(line_pre,end="",file=out_file)

    for line_now in sorted_lines:
        is_empty_now=get_is_empty(line_now)
        if is_empty_now == 3:
            continue
        if is_empty_now == 2:
            continue
        gps_time_now=get_gps_time(line_now)

        if long_interval(gps_time_pre,gps_time_now):
            print("\n{}".format(line_now),end="",file=out_file)
        elif is_empty_now!=is_empty_pre:
            print(line_now,end="",file=out_file)

        is_empty_pre=is_empty_now
        gps_time_pre=gps_time_now


file_paths=os.listdir(filtered_driver_activities_path)
for file_path in file_paths:
    line_cout=len(open(os.path.join(filtered_driver_activities_path,file_path)).readlines())
    if line_cout==1:  #说明只是经过
        os.remove(os.path.join(filtered_driver_activities_path,file_path))
        print("{} deleted".format(file_path))
