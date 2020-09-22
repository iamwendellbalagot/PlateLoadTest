import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
from matplotlib import style
import os

from getdata import GetData
getdf = GetData(path='../databases/serverdb.db')


style.use('ggplot')
sns.set_style('whitegrid')

fig, ax = plt.subplots(1,2,figsize=(12,5))
plt.suptitle('LIVE PLOTTING', fontsize=18)


def animate(i):
    df = getdf.get_dataframe(table='test',path='../databases/serverdb.db')
    data1 = df[['S1', 'S2']]
    data2 = df['S3']
    
    ax[0].set_title('SENSOR 1&2 OUTPUT')
    ax[1].set_title('SENSOR 3 OUTPUT')
    ax[0].clear()
    ax[1].clear()
    ax[0].plot(data1, lw=1)
    ax[1].plot(data2, lw=1, color='steelblue')

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.legend()
plt.show()