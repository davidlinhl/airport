import os

base_dir="/home/lin/Desktop/data/taxi/2018.4.1-PVG-empty-by-5-minute/"
out_file="./data/empty_count_5_minute.csv"
file_names=os.listdir(base_dir)
out_file=open(out_file,"w")

for file_name in file_names:
    file=open(os.path.join(base_dir,file_name))
    line_count=0
    cars=[]
    for line in file.readlines():
        line_count+=1
        info=line.split("|")
        print("line:{},id:{}".format(line_count,info[0]))

        car_id=info[0]

        if car_id not in cars:
            cars.append(car_id)
    file.close()

    print("{},{},".format(file_name,len(cars)),end="",file=out_file)
    for i in range(0,len(cars)):
        print(cars[i],end=",",file=out_file)
    print("",file=out_file)
