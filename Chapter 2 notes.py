# Python for data analysis chapter 2
# Babyname exercise

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

names = pd.read_csv('names/babynames.txt', \
	names = ['year', 'sex', 'name', 'births'])
total_births = names.pivot_table('births', \
	index = 'year', columns = 'sex', aggfunc = sum)
total_births.tail()
total_births.plot(title = 'Total births by sex and year')

def add_prop(group):
	# Integer division floors
	births = group.births.astype(float)

	group['prop'] = births / births.sum()
	return group
names = names.groupby(['year', 'sex']).apply(add_prop)

# Check that group sums add to 1 (or close enough)
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

pieces = []
for year, group in names.groupby(['year', 'sex']):
	pieces.append(group.sort_values(by = 'births', ascending = False)[:1000])
	top1000 = pd.concat(pieces, ignore_index = True)

# Check length
len(top1000.index)

# Analysing naming trends
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table('births', index = 'year', \
	columns = 'name', aggfunc = sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots = True, figsize = (12, 10), grid = False, \
	title = 'Number of births per year')

table = top1000.pivot_table('prop', index = 'year', \
	columns = 'sex', aggfunc = sum)
table.plot(title = 'Sum of table1000.prop by year and sex', \
	yticks = np.linspace(0, 1.2, 13), \
	xticks = range(1880, 2020, 10))

# Computing name diversity in top 50%
df = boys[boys.year == 2010]
prop_cumsum = df.sort_values(by = 'prop', ascending = False).prop.cumsum()
prop_cumsum[:10]
prop_cumsum.searchsorted(0.5)

df = boys[boys.year == 1900]
in1900 = df.sort_values(by = 'prop', ascending = False).prop.cumsum()
in1900.searchsorted(0.5) + 1

def get_quantile_count(group, q = 0.5):
	group = group.sort_values(by = 'prop', ascending = False)
	return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.dtypes
diversity[['F', 'M']] = diversity[['F', 'M']].astype(int)
diversity.plot(title = 'Number of popular names in top 50%')

# Extract last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index = last_letters, \
	columns = ['sex', 'year'], aggfunc = sum)

subtable = table.reindex(columns = [1910, 1960, 2010], level = 'year')
subtable.head()

subtable.sum()
letter_prop = subtable / subtable.sum().astype(float)
fig, axes = plt.subplots(2, 1, figsize = (10, 8))
letter_prop['M'].plot(kind = 'bar', rot = 0, ax = axes[0], title = 'Male')
letter_prop['F'].plot(kind = 'bar', rot = 0, ax = axes[1], title = 'Female', \
	legend = False)

letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
dny_ts.head()

dny_ts.plot()

# Boy names that become girl names and vice versa

# Example Leslie
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
lesley_like
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()

table = filtered.pivot_table('births', index = 'year', columns = 'sex', \
	aggfunc = sum)
table = table.div(table.sum(1), axis = 0)
table.tail()

table.plot(style = {'M': 'k-', 'F': 'k--'})

# Example Jodie

all_names = top1000.name.unique()
mask = np.array(['jod' in x.lower() for x in all_names])
jodie_like = all_names[mask]
jodie_like
filtered = top1000[top1000.name.isin(jodie_like)]
filtered.groupby('name').births.sum()

table = filtered.pivot_table('births', index = 'year', columns = 'sex', \
	aggfunc = sum)
table = table.div(table.sum(1), axis = 0)
table.tail()

table.plot(style = {'M': 'k-', 'F': 'k--'}, \
	title = "Frequency of Jodie-like names by gender", \
	xticks = range(1940, 2010, 10))



