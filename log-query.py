#!/usr/bin/env python

#################################
# log-query
#
# - small python script to get report from logs
#
#################################

import logging
import getopt
import sys
import time
import random
import os
import datetime
import re
import readline
import calendar


def main(argv):

    usage_info = '\nUSAGE:\n\n python log-query.py [--logPath <targetPath>] \n\n Example: >python log-query.py --logPath /logs'
    usage_query = '\nUSAGE QUERY:\n\n QUERY [<server ip>] [start time] [end time] \n Example: query 192.168.0.1 1 2018-12-19 00:00 2018-12-19 00:02'

    log_path = ''  # there would be destination path which stores logs
    log_pattern = '%(message)s'
    date_log = datetime.datetime.strptime('2018-12-18 00:00:00', "%Y-%m-%d %H:%M:%S").date().strftime("%s")

    if len(argv) == 0:
        print(usage_info)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "h", ["help", "logPath="])
    except:
        print(usage_info)
        sys.exit(2)

    # Checking if input arguments are valid
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(usage_info)
            sys.exit()

        elif opt in ("--logPath"):
            path = "." + arg
            # print(path)
            if os.path.exists(path) == True:
                log_path = path
            else:
                print(usage_info)
                print("\n Please write valid folder path. Please read usage of query!!!")
                sys.exit()
        else:
            print(usage_info)
            print("\n Please write valid folder path. Please read usage of query!!!")
            sys.exit()

    print("###################################")
    print("###     log-query running...")
    print("###################################")
    print("###     destination Path: " + log_path)
    print("###################################")
    print(usage_query + "\n")

    must_iterate = True

    while must_iterate:
        text = raw_input(">")

        inputs = text.split(" ")

        if(inputs[0].lower() == 'exit'):
            must_iterate = False
            sys.exit()

        elif(len(inputs) < 4):
            print(usage_query)
            print("\n Please write valid input. Please check usage of query!!!")
            continue

        elif(inputs[0].lower() != 'query' and inputs[0].lower() != 'exit'):
            print(usage_query)
            continue

        elif(inputs[0].lower() == 'exit'):
            must_iterate = False
            sys.exit()

        elif(inputs[0].lower() == 'query'):

            # Checking if input ip is valid
            ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
            valid_ip = re.match(ValidIpAddressRegex, inputs[1])

            if valid_ip is not None:
                server_ip = inputs[1]
            else:
                print(usage_query)
                print("\n Please enter valid ip!   Wrong ip: " + inputs[1])
                continue

            # Checking if input CPU is valid
            if inputs[2].isdigit() or len(inputs[2]) <= 2:
                cpu_number = inputs[2]
            else:
                print(usage_query)
                print("\n Please enter cpu number!     Wrong cpu number: " + inputs[2])
                continue

            # Checking if input start time is valid
            # ValidTimestampRegex = "^\\d{4}[-]?\\d{1,2}[-]?\\d{1,2} \\d{1,2}:\\d{1,2}:\\d{1,2}$"
            ValidTimestampRegex = "^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]$"

            check_start_time = inputs[3] + " " + inputs[4] + ":00"
            valid_start_time = re.match(ValidTimestampRegex, check_start_time)

            if valid_start_time is not None:
                start_time = check_start_time
            else:
                print(usage_query)
                print("\n Please enter valid start time!   Wrong start time: " + inputs[3] + " " + inputs[4])
                continue

            # Checking if input start time is valid
            check_end_time = inputs[5] + " " + inputs[6] + ":00"
            valid_end_time = re.match(ValidTimestampRegex, check_end_time)

            if valid_end_time is not None:
                end_time = check_end_time
            else:
                print(usage_query)
                print("\n Please enter valid end time!     Wrong end time: " + inputs[5] + " " + inputs[6])
                continue

            get_log(log_path, server_ip, cpu_number, start_time, end_time)
            # for name in files:
            # print(name)
        else:
            print(usage_query)
            continue

    sys.exit(0)

# Function that finds the logs for criteria of user


def get_log(path, ip, cpu_number, start_time, end_time):

    files = os.listdir(path)

    # getting unix times from criteria. Because our logs are saved in unix time
    unix_start_time = int(get_unix_time(start_time))
    unix_end_time = int(get_unix_time(end_time))

    # print("inputs: " + " " + path + " " + ip + " " + cpu + " " + start_time + " " + end_time)
    check_files = []
    results = []

    for name in files:
        # Assume that our log file is named by server-192.168.1.1.log. This logic can be changed depends on requirement
        if ip + ".log" in name:
            check_files.append(path + "/" + name)
            # print(check_files)
            # print(path + "/" + name)

    # Checking if the files exist for criteria that user created
    if len(check_files) == 0:
        print(" There is no report for your query!")
    else:
        for file in check_files:
            with open(file, "r") as f:
                for line in f:
                    line = line.strip('\n')
                    outputs = line.split(" ")
                    output_unix_time = int(outputs[0])
                    output_ip = outputs[1]
                    output_cpu = outputs[2]

                    if (output_unix_time > unix_end_time or output_ip != ip):
                        break
                    if (output_unix_time >= unix_start_time and output_unix_time <= unix_end_time and output_ip == ip and cpu_number == output_cpu):
                        outputs[0] = get_date_time_result(outputs[0])
                        results.append(outputs)
                        # print(outputs)
            f.close()

    # Print results for selection criteria
    if(len(results) > 0):
        print("\n#######     RESULT   #######")

        print("\nCPU{} usage on {}: \n".format(cpu_number, ip))

        sum_cpu_usage = 0
        for result in results:
            sum_cpu_usage += int(result[3])
            print("({}, {}%)".format(result[0], result[3]))

        first_time = results[0][0]
        last_time = results[len(results) - 1][0]

        print("\n### Time range: {} <--> {}".format(first_time, last_time))
        print("### Total minutes: {}".format(len(results) - 1))
        print("### Average CPU usage: {}%".format(str(sum_cpu_usage / len(results))))

    else:
        print("\n#######     RESULT   #######")
        print("\nNo data availabe for these selection criteria")


def get_unix_time(date_time):

    timeTuple = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    # print(timeTuple)
    timestamp_utc = calendar.timegm(timeTuple)
    return str(timestamp_utc)


def get_date_time(unix_time):
    ts = int(unix_time)
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def get_date_time_result(unix_time):
    ts = int(unix_time)
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M')


if __name__ == "__main__":
    main(sys.argv[1:])
