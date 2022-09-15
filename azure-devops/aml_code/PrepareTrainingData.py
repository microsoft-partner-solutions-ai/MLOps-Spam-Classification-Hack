import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json, sys

from azureml.core import Workspace, Datastore, Dataset
from azureml.core.authentication import AzureCliAuthentication

with open("./config.json") as f:
    config = json.load(f)

workspace_name = config["workspace_name"]
resource_group = config["resource_group"]
subscription_id = config["subscription_id"]
location = config["location"]

cli_auth = AzureCliAuthentication()

# Get workspace
#ws = Workspace.from_config(auth=cli_auth)
ws = Workspace.get(
        name=workspace_name,
        subscription_id=subscription_id,
        resource_group=resource_group,
        auth=cli_auth
    )

"""Load labeled spam dataset."""

# Path where csv files are located
base_path = "./data/csv_data"

# List of csv files with full path
csv_files = [os.path.join(base_path, csv) for csv in os.listdir(base_path)]

dfs = []
# List of dataframes for each file
for filename in csv_files:
    if filename.endswith('.csv'):
        dfs.append(pd.read_csv(filename))
        
# Concatenate all data into one DataFrame
df = pd.concat(dfs)

# Rename columns
df = df.rename(columns={"CONTENT": "text", "CLASS": "label"})

# Set a seed for the order of rows
df = df.sample(frac=1, random_state=824)

df = df.reset_index()

print(df.tail())

# Print actual value count
print(f"Value counts for each class:\n\n{df.label.value_counts()}\n")

# Display pie chart to visually check the proportion
#df.label.value_counts().plot.pie(y='label', title='Proportion of each class')
#plt.show()

# Drop unused columns
df = df.drop(['index', 'COMMENT_ID', 'AUTHOR', 'DATE'], axis=1)


try:
    os.makedirs('./data/training_data', exist_ok=True)
    df.to_csv('./data/training_data/spam.csv', index=False, header=True)
    print('spam.csv training data created')
except:
    print("directory already exists")
    
datastore = ws.get_default_datastore()  
datastore.upload_files(files = ['./data/training_data/spam.csv'], target_path = 'spam_mlops_data/', overwrite = True,show_progress = True)

dataset = Dataset.Tabular.from_delimited_files(path=datastore.path('spam_mlops_data/spam.csv'))
dataset = dataset.keep_columns(['text','label'])

dataset.register(workspace = ws, name = 'spam_csv', description='coursera spam dataset for mlops', create_new_version=True)

dataset = Dataset.get_by_name(workspace=ws, name='spam_csv')
df = dataset.to_pandas_dataframe()
print(df.head())

