import pandas as pd
from sqlalchemy import create_engine
from os import listdir
import json

# Data folder, use data/ on development and /data/ on production
engine = create_engine('postgresql://postgres:admin@localhost:5001/i4q_factor')

# Create a dataframe using the materialized view from the database
datanode_df = pd.read_sql_query('SELECT * from measurements_summary_quarter_hour order by measurement_bucket', engine)

# pivot table using the measurement_bucket as index,
# for every node_id, we need three columns, the min, max and avg, which are three columns in the dataframe
datanode_df = datanode_df.pivot_table(index='measurement_bucket', columns='node_id', values=['min', 'max', 'average'])

# Export to csv
datanode_df.to_csv('data.csv')
# Remove nan values
datanode_df_clean = datanode_df.dropna()

# export to csv
datanode_df_clean.to_csv('data_clean.csv')

# Fill nas with previous value and export to csv
datanode_df_filled = datanode_df.fillna(method='ffill')

# export to csv
datanode_df_filled.to_csv('data_filled.csv')