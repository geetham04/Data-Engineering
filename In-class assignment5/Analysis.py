import pandas as pd
import numpy as np
import seaborn as sns
import csv 

d1 = pd.read_csv("parsed_census_data.csv")
d2 = pd.read_csv("parsed_covid_data.csv")
d2['County'] = d2['County'].astype(str) + ' County'

# Combine data
combined = d1.merge(d2, on=['County', 'State'], how='inner')
oregon_data = combined.loc[(combined['State'] == 'Oregon')]
print(oregon_data)
oregon_data.to_csv("oregon_data.csv", index=False)

combined['nTotalCases'] = (combined.TotalCases * 100000)/combined.Population
combined['nTotalDeaths'] = (combined.TotalDeaths * 100000)/combined.Population
combined['nDec2020Cases'] = (combined.Dec2020Cases * 100000)/combined.Population
combined['nDec2020Deaths'] = (combined.Dec2020Deaths * 100000)/combined.Population

oregon_data1 = combined.loc[(combined['State'] == 'Oregon')]
#print(oregon_data1)
oregon_data1.to_csv("oregon_data1.csv", index=False)

# Analysis
R = df['nTotalCases'].corr(df['Poverty'])
Ra = df['nTotalDeaths'].corr(df['Poverty'])
Rb = df['nTotalCases'].corr(df['PerCapitaIncome'])
Rc = df['nTotalDeaths'].corr(df['PerCapitaIncome'])
Rd = df['nDec2020Cases'].corr(df['Poverty'])
Re = df['nDec2020Deaths'].corr(df['Poverty'])
Rf = df['nDec2020Cases'].corr(df['PerCapitaIncome'])
Rg = df['nDec2020Deaths'].corr(df['PerCapitaIncome'])

print(R,'\n', Ra, '\n', Rb, '\n', Rc, '\n', Rd, '\n', Re, '\n', Rf, '\n', Rg)


# Oregon data
R = combined['nTotalCases'].corr(df['Poverty'])
Ra = combined['nTotalDeaths'].corr(df['Poverty'])
Rb = combined['nTotalCases'].corr(df['PerCapitaIncome'])
Rc = combined['nTotalDeaths'].corr(df['PerCapitaIncome'])
Rd = combined['nDec2020Cases'].corr(df['Poverty'])
Re = combined['nDec2020Deaths'].corr(df['Poverty'])
Rf = combined['nDec2020Cases'].corr(df['PerCapitaIncome'])
Rg = combined['nDec2020Deaths'].corr(df['PerCapitaIncome'])

print(R,'\n', Ra, '\n', Rb, '\n', Rc, '\n', Rd, '\n', Re, '\n', Rf, '\n', Rg)

sns_plot = sns.scatterplot(data=combined, x="nTotalDeaths", y="perCapitaIncome")
sns_plot.figure.savefig("result.png")