import pandas as pd

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