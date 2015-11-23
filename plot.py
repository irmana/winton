from __future__ import division
import operator
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import subplots, show
import seaborn as sns
import pandas as pd

data = pd.read_csv('train.csv')

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(data.Id, data.Feature_1, 'k', color='blue', rasterized=True, label='Feature 1')
ax.plot(data.Id, data.Feature_2, 'k', color='green', rasterized=True, label='Feature 2')
ax.plot(data.Id, data.Ret_2, 'k', color='red', rasterized=True, label='Return 2')

ax.set_title('Features comparison', fontsize=32)
plt.xlabel('Id', fontsize=36)
plt.ylabel('Feature value', fontsize=36)
ax.tick_params(axis='x', labelsize=32)
ax.tick_params(axis='y', labelsize=32)
legend = ax.legend(loc='upper right', numpoints=1, prop={'size':32}, frameon=1)
frame = legend.get_frame()
frame.set_color('white')

fig.set_size_inches(19.20, 10.80)
fig.tight_layout()
fig.savefig('output.png')
plt.show()
plt.close(fig)

