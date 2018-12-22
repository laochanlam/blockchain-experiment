import pandas as pd
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print('Usage : %s <name>' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as file:
    data = [[x for x in line.split()] for line in file]

#  = [data]

print(data)

unit = 10000
index = ['0.01 Mbit', '0.05 Mbit', '0.1 Mbit']
delay = [data[0][0], data[1][0]
        , data[2][0]]
num_fork = [data[0][1], data[1][1], data[2][1]]
num_block = [data[0][2], data[1][2], data[2][2]]

df = pd.DataFrame({'Network Delay': delay, 'Number of Forks': num_fork,
                   'Number of Blocks Generated': num_block}, index=index).astype(float)


print(df)

df.plot.bar(rot=0, subplots=True, logy=False, title='Network Bandwidth')
plt.show()
