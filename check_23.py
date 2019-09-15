import os
from util import *

driver_files=os.listdir(driver_activities_path)

count_23=0
for driver_file in driver_files:
    print("processing {}".format(driver_file))

    in_file=open(os.path.join(driver_activities_path,driver_file))
    out_file=open(os.path.join(check23_path,driver_file),"w")

    flag=0
    line_pre="null"
    for line in in_file.readlines():
        if flag==1:
            print(line,file=out_file)
            flag=0

        if get_is_empty(line)==2 or get_is_empty(line)==3:
            print(line_pre,end="",file=out_file)
            print(line,end="",file=out_file)
            flag=1
        line_pre=line


file_paths=os.listdir(check23_path)
for file_path in file_paths:
    line_cout=len(open(os.path.join(check23_path,file_path)).readlines())
    if line_cout==0:
        os.remove(os.path.join(check23_path,file_path))
        print("{} deleted".format(file_path))
