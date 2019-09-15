file=open("./data/PVG_9.12_24_hour.txt")

times=[]
for line in file.readlines():
    time=line.split(" ")
    time[0]=int(time[0])
    time[1]=int(time[1])
    times.append(time)

# for i in range(0,len(times)):
#     print("{} {}".format(times[i][0],times[i][1]))
#     input("here")
#


file=open("./data/plane_histo.csv","w")
tot_count=0

for hour in range(0,24):
    for minute in range(0,60,5):
        print("{}:{}~{}".format(hour,minute,minute+5),end=",",file=file)

        count=0
        for i in range(0,len(times)):
            if(times[i][0]==hour and times[i][1]>=minute and times[i][1]<minute+5):
                count+=1
        tot_count+=count
        print("{}".format(count),end=",",file=file)

        for i in range(0,len(times)):
            if(times[i][0]==hour and times[i][1]>=minute and times[i][1]<minute+5):
                print("{}:{}".format(times[i][0],times[i][1]),end=",",file=file)
        print("\n",end="",file=file)

print("totally {} flights".format(tot_count),file=file)
