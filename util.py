plt_path="/home/lin/Desktop/data/taxi/2018.4.1-plot/"
all_gps_path="/home/lin/Desktop/data/taxi/2018.4.1-all/"
all_pvg_empty_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-empty/"
all_pvg_service_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-service/"
empty_by_minute_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-empty-by-5-minute/"
all_pvg_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-all/"
driver_activities_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-drivers-activity/"
filtered_driver_activities_path="/home/lin/Desktop/data/taxi/2018.4.1-PVG-drivers-filtered-activity/"
check23_path="/home/lin/Desktop/data/taxi/check23/"
driver_activity_analyse="/home/lin/Desktop/data/taxi/2018.4.1-PVG-analyse-driver-activity/"

def get_is_empty(line):
    info=line.split("|")
    return int(info[3])

def get_gps_time(line):
    info=line.split("|")
    return info[9]

def time_between(time1,time2):
    time1=time1.split(" ")[1]
    time2=time2.split(" ")[1]

    time1=time1.split(":")
    time2=time2.split(":")

    dif=[int(time2[0])-int(time1[0]),int(time2[1])-int(time1[1]),int(time2[2])-int(time1[2])]
    for i in reversed(range(1,3)):
        if dif[i]<0:
            dif[i]+=60
            dif[i-1]-=1
    if dif[0]<0:
        dif[0]+=24
    return dif
# print(time_between("2018-04-01 12:11:38","2018-04-01 15:35:23"))


def long_interval(time1,time2):
    dif=time_between(time1,time2)
    if dif[1]>=5 or dif[0]>0:
        return True
    return False


def parse_line(line):
    info=line.split("|")

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
