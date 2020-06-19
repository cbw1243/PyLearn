import pandas as pd
import matplotlib.pyplot as plt
import os 

# Get the working directory
os.getcwd()

# Get data from 2009 to 2020
data = [] #pd.DataFrame()
for year in range(2009, 2020):
    url = 'https://www.uscis.gov/sites/default/files/USCIS/Data/Employment-based/H-1B/h1b_datahubexport-'+ str(year) +'.csv'
    # print(url)
    data.append(pd.read_csv(url))
    
data_all = pd.concat(data, ignore_index=True)
data_all = data_all.replace(',','', regex=True)

#data_all.rename(columns = {'Fiscal Year': 'Year'})
# Look at the column names
data_all.columns
# Simplify the column names
data_all.columns = ['Year', 'Employer', 'IA', 'ID', 'CA', 'CD', 'NAICS', 'TaxID', 'State', 'City', 'ZIP']
data_all[['Year', 'IA', 'ID', 'CA', 'CD']] = data_all[['Year', 'IA', 'ID', 'CA', 'CD']].astype(int)

# Describe the data
data_all.head(10)
data_all[['Year', 'IA', 'ID', 'CA', 'CD']].describe(include = 'all')

# Aggregate the data by tax ids. 
data_agg = data_all.groupby(['TaxID', 'Year'])['IA', 'ID', 'CA', 'CD'].sum()
# Get the company names
data_agg_name = data_all.groupby(['TaxID', 'Year'])['Employer'].first()
# Merge with the aggregate data
data_agg = data_agg.merge(data_agg_name, left_index = True, right_index = True)
# Convert index to columns
data_agg = data_agg.reset_index()

# Petition numbers by year
data_year_agg = data_all.groupby(['Year'])['IA', 'ID', 'CA', 'CD'].sum()
data_year_agg['totI'] = data_year_agg['IA'] + data_year_agg['ID'] 
data_year_agg['rateI'] = data_year_agg['IA']/data_year_agg['totI']
data_year_agg['rate2I'] = 85000/data_year_agg['IA']
data_year_agg = data_year_agg.reset_index()

print(data_year_agg)

# Plot the data.
ax = data_year_agg.plot.line(x = 'Year', y = 'rateI', rot = 0,
                            title = 'Initial approvals relative to total applications')

plt.savefig('test.png')




data_agg[data_agg.index.isin(['2019'], level=1)

# Get data for 2019
data19 = data_agg[data_agg.Year == 2019]
data19 = data19.sort_values(by= ['IA'], ascending = False)
data19.head(10)

# Approved H1B visa petitions 
print(data19agg['IA'].sum())
print(data19agg['ID'].sum())
print(data19agg['IA'].sum() + data19agg['ID'].sum())
# Total H1B petitions
print(data19agg['IA'].sum() + data19agg['ID'].sum() + data19agg['CA'].sum() + data19agg['CD'].sum())
# Total approved H1B
print(data19agg['IA'].sum() + data19agg['CA'].sum() )

# H1B initially approved include alines outside of the US and within the US
