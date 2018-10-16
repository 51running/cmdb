#encoding:utf-8

import os
import psutil
if __name__ == '__main__':
    # fhandler = os.popen('top -bn 1')
    # lines = fhandler.readlines()
    # cpu = lines[2].split()[1]
    # mem = 100 * float(lines[3].split()[7]) / float(lines[3].split()[3])
    # fhandler.close
    cpu= psutil.cpu_percent(2)
    mem = psutil.virtual_memory().percent
    print(cpu)
    print(mem)
