# this file get data

# import
import psutil
import datetime


# Get CPU USAGE data for macos
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=0.1)
    return cpu_usage


# get memory usage data
def get_memory_usage():
    memory_usage = psutil.virtual_memory()
    return memory_usage


# get disk usage data
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage


def get_all_parsed_data():

    cpu_usage_avg = get_cpu_usage()
    memory_usage = get_memory_usage()
    memory_total_bytes = memory_usage.total
    memory_used_bytes = memory_usage.total - memory_usage.available
    disk_usage = get_disk_usage()
    disk_total_bytes = disk_usage.total
    disk_used_bytes = disk_usage.used
    current_time = datetime.datetime.now()
    return [current_time, cpu_usage_avg, memory_total_bytes, memory_used_bytes, disk_total_bytes, disk_used_bytes]
