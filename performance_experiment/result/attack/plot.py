import sys
import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    print('Usage : %s <name>' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = f.readlines()


# # determined start and end line
# for i, line in enumerate(lines):
#     if line.startswith('start'):
#         startlineIndex = i
#     if line.startswith('end'):
#         endlineIndex = i
#         break

# # print(lines)
# lines = lines[startlineIndex+1:endlineIndex]

# num_fork = 0
# num_send = 0
# delaytime_list = []
i = 0
j = 0
pre_miner = ''
pre_pre_miner = ''
pre_pre_pre_miner = ''
attackSuccessFlag = False
success_count = 0
fail_count = 0
while i < len(lines):
    if lines[i].startswith('start'):
        attackSuccessFlag = False
        i += 1
        while True:
            line = lines[i].split()
            if lines[i].startswith('end'):
                # print("Bingo")
                break
            elif (line[1] == 'send'):
                if ((line[0] == '8828') | (line[0] == '8851')   | (line[0] == '8852')) & ((pre_miner == '8828') | (pre_miner == '8851')  | (pre_miner == '8852')) & ((pre_pre_miner == '8828') | (pre_pre_miner == '8851')  | (pre_pre_miner == '8852')) & ((pre_pre_pre_miner == '8828') | (pre_pre_pre_miner == '8851')  | (pre_pre_pre_miner == '8852')):
                    # print(line[0] + 'attack success')
                    attackSuccessFlag = True
                    pre_pre_pre_miner = pre_pre_miner
                    pre_pre_miner = pre_miner
                    pre_miner = line[0]

                else:
                    pre_pre_pre_miner = pre_pre_miner
                    pre_pre_miner = pre_miner
                    pre_miner = line[0]
            i += 1
        if (attackSuccessFlag):
            print(str(j) + 'th 8828 attack success! ')
            success_count += 1
        else:
            print(str(j) + 'th 8828 attack fail')
            fail_count += 1
        j += 1
    i += 1
print(success_count / float(success_count + fail_count) * 100)