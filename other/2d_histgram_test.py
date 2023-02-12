# https://qiita.com/supersaiakujin/items/ca47200393180a693bdf

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig = plt.figure()
ax = fig.add_subplot(111)

x, y = np.vstack((np.random.multivariate_normal([0, 0], [[10.0, 0],[0,20]], 5000) 
                 ,np.random.multivariate_normal([0,15], [[10.0, 0],[0, 5]], 5000))).T

H = ax.hist2d(x,y, bins=40, cmap=cm.jet)
ax.set_title('1st graph')
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(H[3],ax=ax)
plt.show()