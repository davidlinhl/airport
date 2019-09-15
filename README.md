# airport
tdengine:

数据导入
TDengine提供两种方便的数据导入功能，一种按脚本文件导入，一种按数据文件导入。

按脚本文件导入

TDengine的shell支持source filename命令，用于批量运行文件中的SQL语句。用户可将建库、建表、写数据等SQL命令写在同一个文件中，每条命令单独一行，在shell中运行source命令，即可按顺序批量运行文件中的SQL语句。以‘#’开头的SQL语句被认为是注释，shell将自动忽略。

按数据文件导入

TDengine也支持在shell对已存在的表从CSV文件中进行数据导入。每个CSV文件只属于一张表且CSV文件中的数据格式需与要导入表的结构相同。其语法如下

insert into tb1 file a.csv b.csv tb2 c.csv …
import into tb1 file a.csv b.csv tb2 c.csv …



时间维度聚合
TDengine支持按时间段进行聚合，可以将表中数据按照时间段进行切割后聚合生成结果，比如温度传感器每秒采集一次数据，但需查询每隔10分钟的温度平均值。这个聚合适合于降维(down sample)操作, 语法如下：

SELECT function_list FROM tb_name
  [WHERE where_condition]
  INTERVAL (interval)
  [FILL ({NONE | VALUE | PREV | NULL | LINEAR})]
SELECT function_list FROM stb_name
  [WHERE where_condition]
  [GROUP BY tags]
  INTERVAL (interval)
  [FILL ({ VALUE | PREV | NULL | LINEAR})]
聚合时间段的长度由关键词INTERVAL指定，最短时间间隔10毫秒（10a）。聚合查询中，能够同时执行的聚合和选择函数仅限于单个输出的函数：count、avg、sum 、stddev、leastsquares、percentile、min、max、first、last，不能使用具有多行输出结果的函数（例如：top、bottom、diff以及四则运算）。
WHERE语句可以指定查询的起止时间和其他过滤条件
FILL语句指定某一时间区间数据缺失的情况下的填充模式。填充模式包括以下几种：
不进行填充：NONE(默认填充模式)。

VALUE填充：固定值填充，此时需要指定填充的数值。例如：fill(value, 1.23)。

NULL填充：使用NULL填充数据。例如：fill(null)。

PREV填充：使用前一个非NULL值填充数据。例如：fill(prev)。

说明：

使用FILL语句的时候可能生成大量的填充输出，务必指定查询的时间区间。针对每次查询，系统可返回不超过1千万条具有插值的结果。
在时间维度聚合中，返回的结果中时间序列严格单调递增。
如果查询对象是超级表，则聚合函数会作用于该超级表下满足值过滤条件的所有表的数据。如果查询中没有使用group by语句，则返回的结果按照时间序列严格单调递增；如果查询中使用了group by语句分组，则返回结果中每个group内不按照时间序列严格单调递增。
示例：温度数据表的建表语句如下：

create table sensor(ts timestamp, degree double, pm25 smallint)
针对传感器采集的数据，以10分钟为一个阶段，计算过去24小时的温度数据的平均值、最大值、温度的中位数、以及随着时间变化的温度走势拟合直线。如果没有计算值，用前一个非NULL值填充。

SELECT AVG(degree),MAX(degree),LEASTSQUARES(degree), PERCENTILE(degree, 50) FROM sensor
  WHERE TS>=NOW-1d
  INTERVAL(10m)
  FILL(PREV);




car_id time_gps(转换成时间戳) status jing_gps wei_gps
