from util import *
import os
# files=[]
file=open("./data/time.txt","w")
for hour in range(0,24):
    for minute in range(0,60,5):
        print("{}:{}".format(hour,minute),file=file)


#
#
#
# for i in reversed(range(0,2)):
#     print(i)
#
#
#
#
#
#
#
#


'''
alarm=0
if ~alarm:
    print("in")

'''

'''
0 车机号
1 控制字（A：正常，M：报警)
2 业务状态（0：正常，1：报警）
3 载客状态（0：重车，1：空车）
4 顶灯状态（0：营运，1：待运，2：电调，3：暂停，4：求助，5：停运）
5 业务状态（0：地面道路，1：快速道路）
6 业务状态（0：无刹车，1：刹车）
7 无意义字段
8 接收日期
9 GPS时间
10 经度   121
11 纬度   31
12 速度
13 方向
14 卫星数
15 无意义字段

'''

'''
file=open("./data/gps_test.txt")
for line in file.readlines():
    info=line.split("|")
    car_id=info[0]
    if info[1]=='A' and info[2]==0:
        alarm=0
    else:
        alarm=1
    is_empty=info[3]
    is_break=info[6]
    date=info[8]
    gps_time=info[9]
    jing_gps=info[10]
    wei_gps=info[11]
    speed=info[12]
    sat_count=info[14]
    print(float(jing_gps))
'''
