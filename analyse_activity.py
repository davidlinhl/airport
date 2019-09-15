'''
找到所有在排队的时间段，写到对应文件
排队的情况包括：
    在机场重载变空载
    空载进重载出

过滤掉所有空载进空载出和重载进重载出的，所有只有一条记录的都是没意义的

进：
    第一行
出：

对所有的行生成批注：
    1.空载进
        空载出
        重载出
    2.重载进
        空载进
        重载出
'''
import os
from util import *

driver_files=os.listdir(filtered_driver_activities_path)

for driver_file in driver_files:
    print("processing {}".format(driver_file))

    in_file=open(os.path.join(filtered_driver_activities_path,driver_file))
    out_file=open(os.path.join(driver_activity_analyse,driver_file),"w")

    block=[]
    line_count=0
    for line in in_file.readlines():

        if line=="\n":
            if len(block)==1:
                if block[0][0]==0:
                    print("heavy in & out,{},{},{}".format(block[0][1],block[0][1],300),file=out_file)
                elif block[0][0]==1:
                    print("empty in & out,{},{},{}".format(block[0][1],block[0][1],300),file=out_file)
                print("[WARNING] Block of 1 entry")
            elif len(block)==2:
                if block[0][0]==1 and block[1][0]==0:  #空进重出
                    time_dif=time_between(block[0][1],block[1][1])
                    print("queue,{},{},{}".format(block[0][1],block[1][1],time_dif[0]*3600+time_dif[1]*60+time_dif[2]),file=out_file)
                elif block[0][0]==0 and block[1][0]==1:  #重进空出
                    time_dif=time_between(block[0][1],block[1][1])
                    print("deliver,{},{},{}".format(block[0][1],block[1][1],time_dif[0]*3600+time_dif[1]*60+time_dif[2]),file=out_file)
                else:
                    print("[ERROR] Unseen 2 entry block")
            elif len(block)==3:
                if block[0][0]==0 and block[1][0]==1 and block[2][0]==0:
                    time_dif=time_between(block[0][1],block[1][1])
                    print("deliver,{},{},{}".format(block[0][1],block[1][1],time_dif[0]*3600+time_dif[1]*60+time_dif[2]),file=out_file)
                    time_dif=time_between(block[1][1],block[2][1])
                    print("queue,{},{},{}".format(block[1][1],block[2][1],time_dif[0]*3600+time_dif[1]*60+time_dif[2]),file=out_file)
                else:
                    print("[ERROR] Unseen 3 entry block")
            else:
                print("[ERROR] Block with neither 2 or 3 entries".format(driver_file))
            block=[]
            continue

        time=get_gps_time(line)
        is_empty=get_is_empty(line)
        block.append([is_empty,time])


file_paths=os.listdir(driver_activity_analyse)
for file_path in file_paths:
    line_cout=len(open(os.path.join(driver_activity_analyse,file_path)).readlines())
    if line_cout==0:  #说明只是经过
        os.remove(os.path.join(driver_activity_analyse,file_path))
        print("{} deleted".format(file_path))
