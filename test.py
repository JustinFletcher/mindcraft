	
Something like this: enter image description here

There is a very good package to do it in R. In python, the best that I could figure out is this, using the squarify package (inspired by a post on how to do treemaps):

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns # just to have better line color and width
import squarify
# for those using jupyter notebooks
%matplotlib inline 


df = pd.DataFrame({
                  'v1': np.ones(100), 
                  'v2': np.random.randint(1, 4, 100)})
df.sort_values(by='v2', inplace=True)

# color scale
cmap = mpl.cm.Accent
mini, maxi = df['v2'].min(), df['v2'].max()
norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
colors = [cmap(norm(value)) for value in df['v2']]

# figure
fig = plt.figure()
ax = fig.add_subplot(111, aspect="equal")
ax = squarify.plot(df['v1'], color=colors, ax=ax)
ax.set_xticks([])
ax.set_yticks([]);