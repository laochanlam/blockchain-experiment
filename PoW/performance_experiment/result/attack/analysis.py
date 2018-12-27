import sys
import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    print('Usage : %s <name>' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = f.readlines()


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
                if ((line[0] == '11109') | (line[0] == '11110')) & ((pre_miner == '11109') | (pre_miner == '11110')) :
                    # print(line[0] + 'attack success')
                    attackSuccessFlag = True
                    # pre_pre_pre_miner = pre_pre_miner
                    # pre_pre_miner = pre_miner
                    pre_miner = line[0]

                else:
                    # pre_pre_pre_miner = pre_pre_miner
                    # pre_pre_miner = pre_miner
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