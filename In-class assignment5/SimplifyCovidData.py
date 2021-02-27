import pandas as pd
import numpy as np
import datetime

covidData = pd.read_csv("COVID_county_data.csv")

counties = covidData["county"].unique()
List_entries = []
for county in counties:
    # Find all the entries for the county
    county_data = covidData[covidData['county'] == county]

    states = county_data['state'].unique()
    for state in states:
        # All the entries for this state and county
        state_county_data = county_data[county_data['state'] == state]

        # Calculations for the chosen fields
        total_cases = state_county_data['cases'].sum()
        total_deaths = state_county_data['deaths'].sum()

        dec2020_start = datetime.datetime(2020, 12, 1)
        dec2020_end = datetime.datetime(2020, 12, 31)
        dec2020_rows = pd.to_datetime(state_county_data['date']).between(dec2020_start, dec2020_end, inclusive=True)
        dec2020_data = state_county_data[dec2020_rows]
        
        casesReported_dec2020 = dec2020_data['cases'].sum()
        deathsReported_dec2020 = dec2020_data['deaths'].sum()
        
        # Append the fields
        List_entries.append([state, county, total_cases, total_deaths, casesReported_dec2020, deathsReported_dec2020])

# Write the saved values to a new csv
parsed_covid_data = pd.DataFrame(entries, columns=["State", "County", "TotalCases", "TotalDeaths", "Dec2020Cases", "Dec2020Deaths"])
parsed_covid_data.to_csv("parsed_covid_data.csv", index=False)

data = pd.read_csv("parsed_covid_data.csv")
Countyarray = ['Loudoun County', 'Washington County', 'Malheur County', 'Harlan County']
Statearray = ['Virginia', 'Oregon', 'Kentucky']
data.loc[(data['county'].isin(Countyarray)) & (data['state'].isin(Statearray))].reset_index(drop=True)
