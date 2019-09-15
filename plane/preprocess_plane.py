file = open("./data/PVG_9.12_purify.csv", "r")

time_raw=[]
for l in range(0,439):
    line=file.readline()
    print(line)
    time_raw.append(line.rstrip("\n"))
print(time_raw)

'''
    csv格式是 , 换格， \n换行
    10:13 AM

'''

file=open("./data/PVG_9.12_24_hour.txt","w")
for i in range(0,len(time_raw)):
    time=time_raw[i]
    apm=time.split(" ")[1]
    hour=int(time.split(" ")[0].split(":")[0])
    minute=int(time.split(" ")[0].split(":")[1])
    if apm=="PM":
        hour+=12
    print("{} {}".format(hour,minute),file=file)
