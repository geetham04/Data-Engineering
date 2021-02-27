# this program loads Census ACS data using basic, slow INSERTs 
# run it with -h to see the command line options

import time
import psycopg2
import psycopg2.extras
import argparse
import re
import csv
import io

DBname = "postgres"
DBuser = "geetha"
DBpwd = "postgres"
TableName = 'CensusDataBatch'
Datafile = "Oregon2015.csv"  # name of the data file to be loaded
CreateDB = True  # indicates whether the DB table should be (re)-created
Year = 2015

def row2vals(row):
	# handle the null vals
	for key in row:
		if not row[key]:
			row[key] = 0
		row['County'] = row['County'].replace('\'','')  # eliminate quotes within literals

	ret = f"""
       {Year},                          -- Year
       {row['CensusTract']},            -- CensusTract
       '{row['State']}',                -- State
       '{row['County']}',               -- County
       {row['TotalPop']},               -- TotalPop
       {row['Men']},                    -- Men
       {row['Women']},                  -- Women
       {row['Hispanic']},               -- Hispanic
       {row['White']},                  -- White
       {row['Black']},                  -- Black
       {row['Native']},                 -- Native
       {row['Asian']},                  -- Asian
       {row['Pacific']},                -- Pacific
       {row['Citizen']},                -- Citizen
       {row['Income']},                 -- Income
       {row['IncomeErr']},              -- IncomeErr
       {row['IncomePerCap']},           -- IncomePerCap
       {row['IncomePerCapErr']},        -- IncomePerCapErr
       {row['Poverty']},                -- Poverty
       {row['ChildPoverty']},           -- ChildPoverty
       {row['Professional']},           -- Professional
       {row['Service']},                -- Service
       {row['Office']},                 -- Office
       {row['Construction']},           -- Construction
       {row['Production']},             -- Production
       {row['Drive']},                  -- Drive
       {row['Carpool']},                -- Carpool
       {row['Transit']},                -- Transit
       {row['Walk']},                   -- Walk
       {row['OtherTransp']},            -- OtherTransp
       {row['WorkAtHome']},             -- WorkAtHome
       {row['MeanCommute']},            -- MeanCommute
       {row['Employed']},               -- Employed
       {row['PrivateWork']},            -- PrivateWork
       {row['PublicWork']},             -- PublicWork
       {row['SelfEmployed']},           -- SelfEmployed
       {row['FamilyWork']},             -- FamilyWork
       {row['Unemployment']}            -- Unemployment
	"""
	return ret
	
def rformat(row):
  # handle the null vals
  for key in row:
    if not row[key]:
      row[key] = 0
    row['County'] = row['County'].replace('\'','')  # eliminate quotes within literals
  return row
  
def row2dict(row, append_year=False):
  row = rformat(row)
  if append_year:
    row['Year'] = Year
  return row


def initialize():
  global Year

  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--datafile", required=True)
  parser.add_argument("-c", "--createtable", action="store_true")
  parser.add_argument("-y", "--year", default=Year)
  args = parser.parse_args()

  global Datafile
  Datafile = args.datafile
  global CreateDB
  CreateDB = args.createtable
  Year = args.year

# read the input data file into a list of row strings
# skip the header row
def readdata(fname):
	print(f"readdata: reading from File: {fname}")
	with open(fname, mode="r") as fil:
		dr = csv.DictReader(fil)
		headerRow = next(dr)
		# print(f"Header: {headerRow}")

		rowlist = []
		for row in dr:
			rowlist.append(row)

	return rowlist

# convert list of data rows into list of SQL 'INSERT INTO ...' commands
def getSQLcmnds(rowlist):
	cmdlist = []
	for row in rowlist:
		valstr = row2vals(row)
		cmd = f"INSERT INTO {TableName} VALUES ({valstr});"
		cmdlist.append(cmd)
	return cmdlist

# connect to the database
def dbconnect():
	connection = psycopg2.connect(
        host="localhost",
        database=DBname,
        user=DBuser,
        password=DBpwd,
	)
	connection.autocommit = True
	return connection

# create the target table 
# assumes that conn is a valid, open connection to a Postgres database
def createTable(conn):

	with conn.cursor() as cursor:
		cursor.execute(f"""
        	DROP TABLE IF EXISTS {TableName};
	    	CREATE UNLOGGED TABLE {TableName} (
            	Year                INTEGER,
                CensusTract         NUMERIC,
            	State               TEXT,
            	County              TEXT,
            	TotalPop            INTEGER,
            	Men                 INTEGER,
            	Women               INTEGER,
            	Hispanic            DECIMAL,
            	White               DECIMAL,
            	Black               DECIMAL,
            	Native              DECIMAL,
            	Asian               DECIMAL,
            	Pacific             DECIMAL,
            	Citizen             DECIMAL,
            	Income              DECIMAL,
            	IncomeErr           DECIMAL,
            	IncomePerCap        DECIMAL,
            	IncomePerCapErr     DECIMAL,
            	Poverty             DECIMAL,
            	ChildPoverty        DECIMAL,
            	Professional        DECIMAL,
            	Service             DECIMAL,
            	Office              DECIMAL,
            	Construction        DECIMAL,
            	Production          DECIMAL,
            	Drive               DECIMAL,
            	Carpool             DECIMAL,
            	Transit             DECIMAL,
            	Walk                DECIMAL,
            	OtherTransp         DECIMAL,
            	WorkAtHome          DECIMAL,
            	MeanCommute         DECIMAL,
            	Employed            INTEGER,
            	PrivateWork         DECIMAL,
            	PublicWork          DECIMAL,
            	SelfEmployed        DECIMAL,
            	FamilyWork          DECIMAL,
            	Unemployment        DECIMAL
         	);
                ALTER TABLE {TableName} ADD PRIMARY KEY (Year, CensusTract);
           	""")

		print(f"Created {TableName}")



def load_batch(conn, rowlist):
  with conn.cursor() as cursor:
    rowlist = [ dict(row2dict(row, append_year=True)) for row in rowlist ]
    print(f"Loading {len(rowlist)} rows")

    start = time.perf_counter()

    psycopg2.extras.execute_batch(cursor, f"""
      INSERT INTO {TableName} VALUES (
        %(Year)s,
        %(CensusTract)s,
        %(State)s,
        %(County)s,
        %(TotalPop)s,
        %(Men)s,
        %(Women)s,
        %(Hispanic)s,
        %(White)s,
        %(Black)s,
        %(Native)s,
        %(Asian)s,
        %(Pacific)s,
        %(Citizen)s,
        %(Income)s,
        %(IncomeErr)s,
        %(IncomePerCap)s,
        %(IncomePerCapErr)s,
        %(Poverty)s,
        %(ChildPoverty)s,
        %(Professional)s,
        %(Service)s,
        %(Office)s,
        %(Construction)s,
        %(Production)s,
        %(Drive)s,
        %(Carpool)s,
        %(Transit)s,
        %(Walk)s,
        %(OtherTransp)s,
        %(WorkAtHome)s,
        %(MeanCommute)s,
        %(Employed)s,
        %(PrivateWork)s,
        %(PublicWork)s,
        %(SelfEmployed)s,
        %(FamilyWork)s,
        %(Unemployment)s
      );
      """, rowlist)

    elapsed = time.perf_counter() - start
    print(f'Finished Loading. Elapsed Time: {elapsed:0.4} seconds')		


def main():
    initialize()
    conn = dbconnect()
    rlis = readdata(Datafile)
    #cmdlist = getSQLcmnds(rlis)

    if CreateDB:
    	createTable(conn)

    #load(conn, cmdlist)
	load_batch(conn, rlis)


if __name__ == "__main__":
    main()



