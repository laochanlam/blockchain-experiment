import pandas as pd
import matplotlib.pyplot as plt

with open('summary.txt') as f:
    data = [[x for x in line.split()] for line in f]

index = ['Delay 1 block confirmed', 'Delay 2 blocks confirmed', 'Delay 3 blocks confirmed']

df = pd.DataFrame({'20% power controlled': data[0], '40% power controlled': data[1], '50% power controlled': data[2],
                          '60% power controlled': data[3], '80% power controlled': data[4]}, index=index).astype(float)
ax = df.plot.bar(rot=0)
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
ax.set_title("Percentage of successful attacks (48 times)")
plt.show()