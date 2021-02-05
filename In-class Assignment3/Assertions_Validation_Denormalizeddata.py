# importing necessary libraries
import pandas as pd
import numpy as np
import math

# Reading the csv file into a pandas Dataframe
df = pd.read_csv ('Oregon Hwy 26 Crash Data for 2019.csv')

# Existence Assertions

# 1. Every record has a Crash ID
# Checking for Crash ID null records
count_nan=0
for item, data in enumerate(df['Crash ID']):
    if(math.isnan(data)):
        df.drop(df.index[item])
        count_nan += 1
if(count_nan>0):
    print('Not valid records', count_nan)
else:
    print("All are valid records")


# 2. Every record has a Record Type
# Checking for Record Type null records
count_nan=0
for item, data in enumerate(df['Record Type']):
    if(math.isnan(data)):
        df.drop(df.index[item])
        count_nan += 1
if(count_nan>0):
    print('Not valid records', count_nan)
else:
    print("All are valid records")


#-----------------------------------------------------------------------------    
# Limit Assertions

# 1. Latitude Degrees field must be between 41 and 46 inclusive
empty_records=0
nan_count=0
for data in df['Latitude Degrees']:
    if(data>=41 and data<47):
        empty_records+=1
    elif math.isnan(data):
        nan_count+=1
        
print('Not Valid records',empty_records)
print('Records with null values',nan_count)

# 2. Crash Month field value must be in list 01-12
empty_records=0
nan_count=0
for data in df['Crash Month']:
    if(data>=1 and data<=12):
        empty_records+=1
    elif math.isnan(data):
        nan_count+=1
        
print('Not Valid records',empty_records)
print('Records with null values',nan_count)

# 3. Crash Hour should be between 0-23 inclusive and 99 for unknown time
invalid_records=0
unknown_time_records=0
for index, row in df.iterrows():
    if(row['Record Type'] == 1):
        hour = row['Crash Hour']
        if((hour >=0 and hour < 24) or hour == 99):
            if(hour == 99):
                unknown_time_records += 1
            else:
                pass
        else:
            print('Not a valid crash hour')
            invalid_records += 1
if(invalid_records == 0):
    print('All are valid records')
if(unknown_time_records > 0):
    print('Unknown crash records are {}'.format(unknown_time_records))


# Intra-record check assertions
# 1. Combination of crash month, crash day and crash year makes a valid date

import datetime
import pandas as pd
import numpy as np

year=df[df['Crash Year']==2019]
float_column = year.select_dtypes(include=['float64'])
float_columnsList = list(float_column.columns.values)
for col in float_columnsList:
        year[col] = year[col].astype('Int64')
dateFormat = pd.DataFrame(year, columns= ['Crash Month', 'Crash Day','Crash Year'])
dateFrame=dateFormat['Crash Month'].astype(str)+"-"+dateFormat['Crash Day'].astype(str)+"-"+dateFormat['Crash Year'].astype(str)
for i in date_frame:
    dateString=str(i)
    format = "%m-%d-%Y"
    if(datetime.datetime.strptime(dateString, format)):
        print("valid date")
    else:
        print("Not a valid date")

# Summary Assertions
# 1. Every crash has a unique crash id

import collections
collections.Counter(data['Crash ID'])

# Referential Integrity Assertions
# 1. For every record of type2, vehicle id should not be null

invalid_records = 0
for ind, row in df.iterrows():
    if(row['Record Type'] == 2):
        vehicle_id = row['Vehicle ID']
        if( math.isnan(vehicle_id)):
            df.drop(df.index[ind])
            invalid_records += 1
if(invalid_records == 0):
    print("All are valid records")

# 2. For every record of type3, both vehicle id and participant id should not be null

invalid_records = 0
for ind, row in df.iterrows():
    if(row['Record Type'] == 3):
        vehicle_id = row['Vehicle ID']
        participant_id = row['Participant ID']
        if( math.isnan(vehicle_id) and math.isnan(participant_id)):
            df.drop(df.index[ind])
            invalid_records += 1
if(invalid_records == 0):
    print("All are valid records")

# 3. For every record of type1, serial # should not be null

invalid_records = 0
for ind, row in df.iterrows():
    if(row['Record Type'] == 1):
        serial_num = row['Serial #']
        if( math.isnan(serial_num)):
            df.drop(df.index[ind])
            invalid_records += 1
if(invalid_records == 0):
    print("All are valid records")








    

