#/usr/bin/env python

#%% Preamble
from pandas import DataFrame
import pandas as pd
import numpy as np

#%% Get data
diamonds = pd.read_csv('/Users/abhijit/diamonds.csv')
diamonds.rename(columns = {'x':'length','y':'width','z':'depth'}, inplace=True)
diamonds.columns.values[5] = 'depthperc'

#%%
diamonds['cubic'] = diamonds[['length','width','depth']].product(axis=1)
diamonds['total'] = diamonds[['length','width','depth']].sum(axis=1)

#%% column means

diamonds.iloc[:,[1]+range(5,12)].mean()

#%% Aggregate
newdat=diamonds[['cut','clarity','depthperc','table','price','length','width','depth','cubic']]
newdat.groupby(['cut','clarity']).aggregate(np.mean)
newdat.groupby(['cut','clarity'], as_index=False).aggregate(np.mean)

diamonds['carat2'] = np.round(diamonds.carat/0.25)*0.25
Summary = (
    diamonds[['cut','color','clarity','carat2','depthperc',
              'table','price','length','width','depth','cubic']]
    .groupby(['cut','color','clarity','carat2'],as_index=False)
    .aggregate(np.mean) # Does means of the rest
    )
    
#%% Pivot table

PT = pd.pivot_table(diamonds[['color','clarity','price']], 
                    index='color',
                    columns = 'clarity',
                    aggfunc = np.mean)

#%% VLookups
Summary.rename(columns = {'price':'avgprice'}, inplace=True)
VL = pd.merge(diamonds, Summary[['cut','color','clarity','carat2','avgprice']],
              on = ['cut','color','clarity','carat2'])

#%% Conditional variable creation
diamonds['Size'] = 'Small'
diamonds.loc[diamonds['carat']>= 0.5, 'Size'] = 'Medium'
diamonds.loc[diamonds['carat'] > 1, 'Size'] = 'Large'
diamonds['Size'] = pd.Categorical(diamonds['Size'], 
    categories = ['Small','Medium','Large'])

#%% Charts
import matplotlib.pyplot as plt

x = diamonds.Size.value_counts(sort=False, normalize=True)
x.plot(kind='bar')

#%% Boxplot
diamonds.boxplot(column = 'price', by='cut')

#%% Scatter plot
diamonds.plot(kind='scatter', x='carat',y='price')

#%% Grouped scatter plot
groups = diamonds.groupby('clarity')
fig, ax = plt.subplots()
for name, group in groups:
    ax.plot(group.carat, group.price, marker='o', linestyle='', label=name)
ax.legend(numpoints=1)
plt.xlabel('Carat')
plt.ylabel('Price')
plt.show()

