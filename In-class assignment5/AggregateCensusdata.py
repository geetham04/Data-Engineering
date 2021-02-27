import pandas as pd
import numpy as np


censusData = pd.read_csv("acs2017_census_tract_data.csv")

counties = censusData["County"].unique()

list_entries = []
for county in counties:
    # All the entries for the county
    county_data = censusData[censusData['County'] == county]

    states = county_data['State'].unique()
    
    for state in states:
        # All the entries for this state and county
        state_county_data = county_data[county_data['State'] == state]
        
        # Calculations of the fields chosen
        total_population = state_county_data['TotalPop'].sum()
        
        people_in_poverty = np.array(state_county_data['TotalPop']) * (np.array(state_county_data['Poverty'])/100)
        #x = x[~numpy.isnan(x)]
        people_in_poverty = people_in_poverty[~np.isnan(people_in_poverty)]
        
        overall_poverty_percentage = (np.sum(people_in_poverty) / total_population) * 100
        overall_poverty_percentage = overall_poverty_percentage[~np.isnan(overall_poverty_percentage)]

        total_incomes_per_population = np.array(state_county_data['TotalPop']) * np.array(state_county_data['IncomePerCap'])
        total_incomes_per_population = total_incomes_per_population[~np.isnan(total_incomes_per_population)]
        total_income_per_capita = np.sum(total_incomes_per_population) / total_population

        # Append all the values
        list_entries.append([state, county, total_population, total_income_per_capita, overall_poverty_percentage])

# Write the saved values to a new csv
parsed_census_data = pd.DataFrame(list_entries, columns=["State", "County", "Population", "IncomePerCapita", "Poverty"])
parsed_census_data.to_csv("parsed_census_data.csv", index=False)
data = pd.read_csv("parsed_census_data.csv")
#data = data.style.hide_index()
Countyarray = ['Loudoun County', 'Washington County', 'Malheur County', 'Harlan County']
Statearray = ['Virginia', 'Oregon', 'Kentucky']
data.loc[(data['County'].isin(Countyarray)) & (data['State'].isin(Statearray))].reset_index(drop=True)



        
        