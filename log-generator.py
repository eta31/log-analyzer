#!/usr/bin/env python

#################################
# log-generator
#
# - small python script to generate random log file into folder
# - Creating 1000 files in that case
#
#################################

# import progressbar
import logging
import getopt
import sys
import time
import random
import os
import datetime
import re
import calendar

# Inheriting custom class from logging.FileHandler for custom functionlity


class myFileHandler(logging.FileHandler):
    def __init__(self, path, fileName):
        path = "." + path
        if os.path.exists(path) == False:
            os.mkdir(path)
        super(myFileHandler, self).__init__(path + "/" + fileName)


def main(argv):
    usageInfo = '\nUSAGE:\n\n python logGenerator.py [--logPath <targetPath>] [--datePattern YYYY-MM-DD]'

    logPath = '/log'
    sourceData = ''
    logPattern = '%(message)s'
    date_time = "2018-12-18 00:00:00"
    dateLog = get_unix_time('2018-12-18 00:00:00')
    original_date_time = get_unix_time("2018-12-18 00:00:00")

    if len(argv) == 0:
        print(usageInfo)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "h", ["help", "logPath=", "logDate="])
    except:
        print(usageInfo)
        sys.exit(2)

    for opt, arg in opts:

        if opt in ('-h', "--help"):
            print(usageInfo)
            sys.exit()

        elif opt in ("--logPath"):
            logPath = arg

        elif opt in ("--logDate"):
            print(arg)
            mat = re.match('(\d{4})[-](\d{2})[-](\d{2})$', arg)
            print("match:" + str(mat))
            if mat is not None:
                date_time = arg + " 00:00:00"
                original_date_time = dateLog = get_unix_time(date_time)
                print(dateLog)
            else:
                print(usageInfo)
                sys.exit()

    # bring in source data

    print("###################################")
    print("### log-generator running...")
    print("###################################")
    print("Destination Path: " + logPath)
    print("Log Date: " + str(date_time))
    print("###################################")

    # setup logging
    #logging.Formatter.converter = time.gmtime
    # logger = logging.getLogger("log-generator")
    # logger.setLevel(logging.DEBUG)

    ip_4 = 0
    ip_3 = 0

    # sys.stdout.write('\r')
    # # the exact output you're looking for:
    # sys.stdout.write("[%-10s] %d%%" % ('=' * 1, 10))
    # sys.stdout.flush()

    for i in range(1000):

        updt_progress(1000, i + 1)

        if(ip_4 >= 255):
            ip_3 += 1
            ip_4 = 0
        else:
            ip_4 += 1

        server_ip = "192.168." + str(ip_3) + "." + str(ip_4)
        logFile = "server-" + server_ip + ".log"

        # logging.Formatter.converter = time.gmtime
        logger = logging.getLogger("log-generator")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(logPattern)
        fileHandler = myFileHandler(logPath, logFile)
        # fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        dateLog = original_date_time

        for x in range(24 * 60):

            # create random cpu usage
            cpu_percent0 = str(random.randint(0, 100))
            cpu_percent1 = str(random.randint(0, 100))

            logger.info('%s %s %s %s', dateLog, server_ip, '0', cpu_percent0)
            logger.info('%s %s %s %s', dateLog, server_ip, '1', cpu_percent1)

            dateLog = str(int(dateLog) + 60)
            # print(dateLog)

            # sys.stdout.write('\r')
            # # the exact output you're looking for:
            # sys.stdout.write("[%-10s]" % ('=' * i))
            # sys.stdout.flush()

        logger.removeHandler(fileHandler)

    # sys.stdout.write('\r')
    # # the exact output you're looking for:
    # sys.stdout.write("[%-10s] %d%%" % ('=' * i, 100))
    # sys.stdout.flush()

    sys.exit(0)


def updt_progress(total, progress):

    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "=" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()


def get_unix_time(date_time):

    timeTuple = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    # print(timeTuple)
    timestamp_utc = calendar.timegm(timeTuple)
    return str(timestamp_utc)


def get_date_time(unix_time):
    ts = int(unix_time)
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    main(sys.argv[1:])
