import time
import datetime

# TODO: 时间戳
var = time.time()
print(var)

# TODO: 格式化的时间字符串
var = time.ctime()
print(var)
var = time.strftime('%Y-%m-%d %H:%M:%S')
print(var)

# TODO: 结构化时间
var = time.gmtime()
print(var)
var = time.localtime()
print(var)

# TODO: ---------- 时间戳 -> 其他 ----------

# 时间戳  -> 结构化时间
var = time.gmtime(time.time())
print(var)
var = time.localtime(time.time())
print(var)

# 时间戳 -> 格式化时间字符串
var = time.ctime(time.time())
print(var)

# TODO: ---------- 结构化时间 -> 其他 ----------

# 结构化时间 -> 时间戳
var = time.mktime(time.localtime())
print(var)

# 结构化时间 -> 格式化的时间字符串
var = time.strftime('%Y-%m-%d', time.gmtime())  # 参数说明: 格式化字符串和结构化时间
print(var)
var = time.asctime(time.localtime())
print(var)

# TODO: ---------- 格式化时间字符串 -> 其他 ----------

# 格式化时间字符串 -> 结构化时间
var = time.strptime('2018-11-12', '%Y-%m-%d')
print(var)
var = time.strptime('Sun Feb 11', '%a %b %d')
print(var)

# 格式化时间字符串 -> 时间戳
var = time.mktime(time.strptime('Sun Feb 11 11:21:47 2018', "%a %b %d %H:%M:%S %Y"))
print(var)
var = time.mktime(time.strptime('2018-02-11 11:23:57', "%Y-%m-%d %H:%M:%S"))
print(var)

# --------------------------------------------------------------------------------------------------

# TODO: datetime.datetime
var = datetime.datetime.now()
print(var)
var = datetime.datetime(year=2018, month=1, day=3)
print(var)

# TODO: datetime.timedelta
var = datetime.timedelta(days=5, seconds=1, microseconds=22222, minutes=11, hours=11, weeks=1)
print(var)

# TODO: datetime.date
var = datetime.date(year=2018, month=1, day=3)
print(var)

# TODO: datetime.time
var = datetime.time(hour=4, minute=32, second=23, microsecond=22222)
print(var)

# TODO: ---------- 其他 <-> datetime ----------

# 字符串 -> datetime对象
var = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
print(var)
var = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
print(var)

# 时间戳 -> datetime对象
var = datetime.datetime.fromtimestamp(time.time())
print(var)
var = datetime.datetime.utcfromtimestamp(time.time())
print(var)

# datetime对象 -> 格式化时间字符
var = datetime.datetime(2018, 1, 5, 15, 19, 59).strftime("%Y-%m-%d %H:%M:%S")
print(var)

# datetime对象 -> 结构化时间
var = datetime.datetime(2018, 1, 5, 15, 19, 59).timetuple()
print(var)
