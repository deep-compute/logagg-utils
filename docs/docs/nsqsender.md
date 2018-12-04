# NSQSender
Publishes logs and heartbeats to a given topic in [NSQ](https://nsq.io/). Also keeps a checks if the depth(Max number of msgs) is not exceeded before sending.

## Setup
####  [Install](http://nsq.io/deployment/installing.html) the `nsq` package, at where we need to bring up the `nsq` server.
- Run the following commands to install `nsq`:
```
$ sudo apt-get install libsnappy-dev
$ wget https://s3.amazonaws.com/bitly-downloads/nsq/nsq-1.0.0-compat.linux-amd64.go1.8.tar.gz
$ tar zxvf nsq-1.0.0-compat.linux-amd64.go1.8.tar.gz
$ sudo cp nsq-1.0.0-compat.linux-amd64.go1.8/bin/* /usr/local/bin
```

#### Bring up the `nsq` instances at the required server with following commands:
- **NOTE:** Run each command in a seperate Terminal window
- nsqlookupd
```
$ nsqlookupd
```
- nsqd -lookupd-tcp-address *<ip-addr or DNS\>*:4160
```
$ nsqd -lookupd-tcp-address localhost:4160
```
- nsqadmin -lookupd-http-address *<ip-addr or DNS\>*:4161
```
$ nsqadmin -lookupd-http-address localhost:4161
```

## Usage
#### Sending logs to NSQ to a topic
```
$ python3
>>> from logagg_utils import NSQSender
>>> from logagg_utils.utils import DUMMY
>>>
>>> logs_sender = NSQSender(nsqd_http_address='localhost:4151', nsq_topic='logs', log=DUMMY)
>>>
>>> import time
>>> def prepare_log_list():
...     log_msg = 'This is log number {}, at time {}'
...     logs = list()
...     for i in range(500): logs.append({'log': log_msg.format(i, time.time())})
...     return logs
... 
>>> logs = prepare_log_list()
>>> logs_sender.handle_logs(logs)
```

#### Read logs from a NSQ topic
```
$ nsq_tail -nsqd-tcp-address localhost:4150 -topic logs
...
...
This is log number 494, at time 1543906852.718413
This is log number 495, at time 1543906852.7184162
This is log number 496, at time 1543906852.7184188
This is log number 497, at time 1543906852.7184217
This is log number 498, at time 1543906852.7184246
This is log number 499, at time 1543906852.7184308
```
