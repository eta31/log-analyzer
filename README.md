### Prerequisites

The scripts were written on Python 2.7. Before use them, please make sure that you installed Python 2.7 on your machine.



# log-generator

Simple python script to generate random log into custom folder

### Usage

```
python log-generator.py --logPath <targetPath> [--logDate YYYY-mm-DD]
Example: python log-generator.py --logPath /logs --logDate 2018-12-19
```



# log-query

Simple python script to get log datas for query which user gives

### Usage

```
python log-query.py --logPath <targetPath>
Example: python log-query.py --logPath /logs

QUERY [<server ip>] [start time] [end time]
Example: query 192.168.0.1 1 2018-12-19 00:00 2018-12-19 00:02
```

