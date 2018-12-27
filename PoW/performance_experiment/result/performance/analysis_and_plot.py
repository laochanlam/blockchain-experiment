import sys
import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    print('Usage : %s <name>' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = f.readlines()


# determined start and end line
for i, line in enumerate(lines):
    if line.startswith('start'):
        startlineIndex = i
    if line.startswith('end'):
        endlineIndex = i
        break

# print(lines)
lines = lines[startlineIndex+1:endlineIndex]

num_fork = 0
num_send = 0
delaytime_list = []

for i, line in enumerate(lines):
    line = line.split()
    if (line[1] == 'fork'):
        num_fork += 1
    if (line[1] == 'send'):
        num_send += 1
        send_time = float(line[3])
        j = i + 1
        while True:
            predict_line = lines[j].split()
            if (predict_line[1] == 'receive'):
                receive_time = float(predict_line[3])
                delaytime_list.append(receive_time - send_time)
                break
            j += 1

delaytime_list = np.array(delaytime_list)
# print(delaytime_list)
print('Delay time: ' + str(delaytime_list.mean()))
print('Num of Fork: ' + str(num_fork))
print('Num of Block generated: ' + str(num_send))


