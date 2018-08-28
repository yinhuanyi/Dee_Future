# Python write by yhy
import threading
import os
import re
import datetime
import requests


# 这里不是不断的读取日志，而是实现tail -f的功能
def read_log(path):
   e = threading.Event()
   offset = 0
   while not e.is_set():
       with open(path) as f:
           if offset > os.stat(path).st_size:
                offset = 0
           f.seek(offset)
           for line in f:
               yield line
           offset = f.tell()

# 将日志转换为字典
p = '''(?P<ip>[\d\.]{4,}) - - \[(?P<time>[^\[\]]+)\] (?P<upstream_response_time>[\d\.]+) "(?P<method>\w+) (?P<url>.*) (?P<version>[\w|/\.\d]*)" (?P<status>\d+) (?P<length>\d+) "(?P<referer>[^"]+)" "(?P<UA>[^"]+)" "(?P<remoteAddr>.+)"'''
o = re.compile(p)
def parse_log(path):
    for line in read_log(path):
        m = o.match(line.rstrip('\n'))
        if m:
            data = m.groupdict()
            yield data

# 将汇聚的QPS , throughput ，error_rate数据存储在influxdb上
def send(qps,throughput,error_rate):
    line = 'yhyAnalyse qps={},throughput={},error_rate={}'.format(qps,throughput,error_rate)
    ret = requests.post('http://monitor.szzbmy.com:8086/write', data=line, params={'db': 'monitor'}) # db是数据库的意思，monitor是数据库的名字

    # line = 'yhyAnalyse qps={},throughput={},error_rate={}'.format(qps,throughput,error_rate)
    # requests.post('http://192.168.23.41:8086/write', data=line, params={'db':'monitor'}) # db是数据库的意思，

# 汇聚 QPS , throughput ，error_rate
def aggregate(path,interval = 1):
    qps = 0
    throughput = 0
    error = 0
    start = datetime.datetime.now()
    for item in parse_log(path):
        qps += 1
        throughput += int(item['length']) # 这里应该是+=
        # 如果
        if int(item['status']) >= 400:
            error += 1
        current = datetime.datetime.now()

        # 10秒发送一次数据
        if (current - start).total_seconds() > interval:
            error_rate = error / qps
            send(qps,throughput,error_rate)
            qps = 0
            throughput = 0
            error = 0
            start = current
# 主函数入口
if __name__ == '__main__':
    import sys
    aggregate(*sys.argv[1:])