file=open("./data/empty_count_5_minute.csv")

def get_cars(line):
    cars=line.split(",")
    time=cars[0]
    del cars[0]
    del cars[0]
    del cars[len(cars)-1]
    return time,cars

out_file=open("./data/new_cars_waiting.csv","w")

line_pre=file.readline()
_,cars_pre=get_cars(line_pre)

for line_now in file.readlines():
    time_now,cars_now=get_cars(line_now)
    cars_new=[]
    for i in range(len(cars_now)):
        if cars_now[i] not in cars_pre:
            cars_new.append(cars_now[i])
    cars_pre=cars_now
    print("{},{},".format(time_now,len(cars_new)),end="",file=out_file)
    for i in range(len(cars_new)):
        print("{},".format(cars_new[i]),end="",file=out_file)
    print("",file=out_file)

out_file.close()
