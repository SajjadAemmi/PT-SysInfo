# Python script to fetch system information
# Author - Sajjad Aemmi
# Tested with Python3.10 on Ubuntu 12.04

import shutil
import math
import platform
import logging
import igpu

your_name = input("Please enter your name: ")

logging.basicConfig(filename=your_name + ".txt",
                    filemode='a',
                    format='%(message)s',
                    level=logging.DEBUG)
# logger = logging.getLogger('urbanGUI')

# Architecture
logging.info("Architecture: " + platform.architecture()[0])

# machine
logging.info("Machine: " + platform.machine())

# node
logging.info("Node: " + platform.node())

# processor
logging.info("\nProcessors: ")
with open("/proc/cpuinfo", "r")  as f:
    info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
for index, item in enumerate(cpuinfo):
    logging.info("    " + str(index) + ": " + item)

# system
logging.info("\nSystem: " + platform.system())

# Load
with open("/proc/loadavg", "r") as f:
    logging.info("Average Load: " + f.read().strip())

# Memory
logging.info("\nMemory Info: ")
with open("/proc/meminfo", "r") as f:
    lines = f.readlines()

logging.info("     " + lines[0].strip())
logging.info("     " + lines[1].strip())

# gpu
logging.info("\nGPU Info: ")
gpu_count = igpu.count_devices()
logging.info(f'This host has {gpu_count} devices.')

for i in range(gpu_count):
    gpu = igpu.get_device(i)
    logging.info(f'The first gpu is a {gpu.name} with {gpu.memory.total:.0f}{gpu.memory.unit}.')


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


logging.info("\nStorage Info: ")
total, used, free = shutil.disk_usage(__file__)

total = convert_size(total)
used = convert_size(used)
free = convert_size(free)
logging.info("total: " + total)
logging.info("used: " + used)
logging.info("free: " + free)
