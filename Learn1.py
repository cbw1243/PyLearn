# Print names with iteractions
user_name = input('Input: ')
print('Hello', user_name)

#%%
for i in range(0, 10):
    print(i, ' ', end = '')
#%%    


#%%
def square(n):
    return n * n

square(3)

def swap(a, b):
    return b, a

x, y = swap(2, 3)
x
y

#%% Python for Data Science
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

data = np.random.randn(3, 4)
data

# Named vector
obj = pd.Series([3,4, 2 ,2], index = ['a', 'sd', 'sde', 'wf'])
obj

# Create a data frame through a list
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}

frame = pd.DataFrame(data)
frame
frame.head(3)