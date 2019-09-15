
/*
常量的定义
  行人速度1m/s
  开门到进去3s
  放行李10s  （最简单的模型每个人都放行李）
  车长4m
  走到0号位置0m，1号位置6m。。


自己的时间线队列类
  封装优先队列，每次get的时候都检查这一秒是不是
  找到某个对象下个动作

车和人的队列
  包含队列，和生成取出程序
  当一个车走了叫下一个车和下一个人

车道类
  记录当前的布局，车辆号

上车的规则
  一排车道

    乘客找最近的车，乘客不等车开过来，到了他就直接走向最近的车
    乘客一排车道都从右侧上车，因此不会堵住左侧车道

  两排车道
    上完车了没有阻塞就可以走
    前面的车都走完了才能进下一批
格式化log

write 2 lanes first

TODO event的排序添加id，所有的event在执行之前必须test条件，先到先得肯定排的上

events
  car come :
    if queue empty:
      if can drive in:
        insert car drive in, same timestamp
      else
        wait for being triggered in the queue
    else
      wait for being triggered in the queue

  car drive in :
    if can drive in
      choose a front most pos
      lock the pos
      requeset passenger
      insert car arrive
    else
      wait for beign triggered in the queue

  car in pos :
    if have pending passenger
      insert car leaving after luggage and hop in
    else
      set status in pos
      wait for being triggered on lane or passenger to arrive

  car leaving :
    if no congestion
      inset car left lane
    else
      set status ready to leave
      wait on lane for being triggered

  car left lean :
    log
    if spot ready to leave on lane
      trigger car leaving for all ready to leave

car dont take care of any event that is determined by passenger status like when to leave after arriving in pos


  passenger come :
    if queue empty
      if spot pending passenger car in lane
        move in
      else
        if request a car granted
          move on lane
    else
      wait in the queue for being triggered
  passenger on lane :  (must have passed on lane check, having a cacant car)
    lock the car
    insert passenger arrive
  passenger arrive :
    if car in pos
      set car status loading passenger
      insert car leaving after loading luggage and hop in
    else
      wait for being triggered on lane

*/

#include<algorithm>
#include<iostream>
#include<time.h>
#include<queue>
#include<vector>
#include<string>
#include<random>
#include<stdlib.h>




const int CAR_INCOMING_PER_MINUTE=30;
const int GROUP_INCOMING_PER_MINUTE=20;
#define MAX_TIME 3600
#define CAR_LENGTH 4
#define PARK_SPACE_LENGTH 6
#define LANE_TOT 2
#define POS_TOT 4


using namespace std;


enum Car_status {pending_for_passenger,pending_to_leave};

class Car
{
public:
  static int count;
  static double INCOMING_PER_MINUTE;
  enum Car_status;

  int id;
  double time_gen=-1;
  double time_out_queue=-1;
  double time_board=-1;
  double time_leave=-1;
  bool empty=true;

  Car(double time):time_gen(time)
  {
    id=Car::count++;
  }

  bool is_empty()   //since passenger walking at a car it is not empty
  {
    return empty;
  }
  int arrive(double time);
  int drive_in_lane();   //pending for passenger status change
  int in_lane_trigger(int car_id);   //trigger group to come 
  int car_leaving(int car_id);
  int car_left(int car_id);
  int car_left_trigger(int car_id);

};
int Car::count=0;
double Car::INCOMING_PER_MINUTE=CAR_INCOMING_PER_MINUTE;

class Group
{
public:
  static double INCOMING_PER_MINUTE;
  static const int PACE=1;   //  m/s
  static const int LUGGAGE_BASE=6;  //s
  static const int GET_IN_BASE=3;  //s
  static int count;

  int id;
  double time_gen=-1;
  double time_out_queue=-1;
  double time_boarded=-1;
  double time_leave=-1;

  int num;   //how many people in the group
  int luggage;  //how many luggage they carry

  Group(double time,int num,int luggage):num(num),luggage(luggage),time_gen(time)
  {
    id=Group::count++;
  }
  double board_time(int lane_num,int pos_num)  //how many seconds it takes for them to board a car walk,place luggage and sit in
  {
    return double(pos_num*6)/PACE + LUGGAGE_BASE + GET_IN_BASE;
  }
  int arrive();
};
int Group::count=0;
double Group::INCOMING_PER_MINUTE=GROUP_INCOMING_PER_MINUTE;




template<class T>
class Queue
{
public:
  queue<T>q;
  int generate(double second);
  int top()
  {
    return q.top();
  }

  void pop()
  {
    q.pop();
  }

  int size()
  {
    return q.size();
  }

  int empty()
  {
    return q.empty();
  }
};
class Queue<class Car>car_queue;
class Queue<class Group>group_queue;

template<class T>
int Queue<T>::generate(double second)
{
  double margin= T::INCOMING_PER_MINUTE/double(60);
  srand(int(second));
  double random=rand()/double(RAND_MAX);
  if(random<margin)
  {

  }
}


int lane_min,pos_min;
void dfs_front(int lane_num,int pos_num);

class Lane
{
public:
  int layout[LANE_TOT][POS_TOT];   //lane and pos
  static const int GATE_POS=int(POS_TOT)/2;

  pair<int,int> get_frontest()
  {
    lane_min=LANE_TOT-1;
    pos_min=POS_TOT-1;
    dfs_front(LANE_TOT-1,POS_TOT-1);
    return pair<int,int>(lane_min,pos_min);
  }
  bool can_drive_in();
  int lock_pos(int lane_num,int pos_num);




  int passenger_triger_car(int group_id);


  bool is_congested(int lane,int pos);
  pair<int,int> can_move_in();
  int get_empty();
  int leave(int lane,int pos); // call next car
  int enter(class Car car,int lane,int pos);
};
class Lane lane;


void dfs_front(int lane_num,int pos_num)
{
  if(lane.layout[lane_num][pos_num]!=-1)
    return;
  if(lane_num<lane_min && pos_num<pos_min)
    lane_min=lane_num,pos_min=pos_num;
  if(lane_num==1 && pos_num>0)
    dfs_front(lane_num,pos_num-1),dfs_front(lane_num-1,pos_num);
  if(lane_num==0 && pos_num>0)
    dfs_front(lane_num,pos_num-1),dfs_front(lane_num+1,pos_num);
  return;
}


enum Types {car_leave};
class Event
{
public:
  static int count;
  int id;
  int car_id,group_id;
  double happen_time;
  enum Types type;
  Event(enum Types event_type,double time,int carid,int groupid):type(event_type),happen_time(time),car_id(carid),group_id(groupid)
  {
    id=Event::count++;
  }
  bool operator <(class Event e)const
  {
    return happen_time<e.happen_time;
  }
  bool operator >(class Event e)const
  {
    return happen_time>e.happen_time;
  }
};
int Event::count=0;


class Timeline
{
public:
  double now_time=0;
  priority_queue<class Event>pq;
  void push(class Event e)
  {
    pq.push(e);
  }
  void pop()
  {
    pq.pop();
  }
  class Event top()
  {
    return pq.top();
  }
  bool empty()
  {
    return pq.empty();
  }
  class Event get_next_event(class Event);
};
class Timeline timeline;






int Car::arrive(double time)
{
  if(!car_queue.empty())
  {
    if(lane.can_drive_in())
      lane.drive_in(*this);
    else
      car_queue.push(*this);
  }
  else
    car_queue.push(*this);
}


int Group::arrive(double time)
{

}








int main()
{
  for(int i=0;i<MAX_TIME;i++)
    car_queue.generate(i),group_queue.generate(i);


  while(!car_queue.empty() && !group_queue.empty() && !timeline.empty() && timeline.top().happen_time<MAX_TIME)
  {


    // class Event current_e=timeline.pop();

    // switch(current_e.type)
    // {
    //   case :
    //
    //     break;
    //   case :
    //
    //     break;
    //   case :
    //
    //     break;
    //   case :
    //
    //     break;
    //   default :
    //     cout<<"Unknown Event"<<endl;
    //
    // }
  }

  return 0;
}


// source /opt/rh/devtoolset-4/enable
