import pandas as pd
from sqlalchemy import create_engine
from os import listdir
import json
# Data folder, use data/ on development and /data/ on production
data_folder = '/data/'
# create the connection to the database
# The database engine is PostgreSQL
# The service is running on the same machine as the importer
# The database name is 'enerview'
# use localhost in development and timescale in production
engine = create_engine('postgresql://postgres:admin@timescale:5001/i4q_factor')

# Go through the folders in the data folder
# Each folder corresponds to a date
# Each file in the folder corresponds to a datanode
# First, let us create the sensors, go folder by folder an get all file names, and store it a dataframe:
ids = []
descriptions = []
for folder in listdir(data_folder):
    for file in listdir(data_folder + folder):
        file_name = data_folder + folder + '/' + file
        datanode_name = file[:file.find('.')]
        # Add a new row in ids if it does not exist:
        if datanode_name not in ids:
            ids.append(datanode_name)
            descriptions.append("Sensor: " + datanode_name)

datanode_df = pd.DataFrame({"id": ids, "description": descriptions})

# Write to the database,
datanode_df.to_sql('datanode', engine, index=False, if_exists='append')

# Now, we go through the measurements to insert the values
for folder in listdir(data_folder):
    for file in listdir(data_folder + folder):
        file_name = data_folder + folder + '/' + file
        with open(file_name, 'r') as f:
            data_dict = json.load(f)  # load the JSON data into a dictionary
        datanode_values_df = pd.DataFrame.from_dict(data_dict).rename(columns={"start": "start_time", "end": "end_time"})
        # now we append the id of the node as a column
        datanode_name = file[:file.find('.')]
        # remove NaN values
        datanode_values_df = datanode_values_df.dropna()

        # add the id of the node
        datanode_values_df['node_id'] = datanode_name
        # save to the database
        datanode_values_df.to_sql('measurement_value', engine, if_exists='append', index=False)
