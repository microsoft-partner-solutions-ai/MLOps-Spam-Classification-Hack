import os, json, sys
from sklearn.metrics import classification_report

from azureml.core import Workspace, Run, Experiment
from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication
from azureml.core import Environment
from azureml.core.webservice import Webservice, AciWebservice


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

try:
    with open("./configuration/aci_webservice.json") as f:
        config = json.load(f)
except:
    print("No new model, thus no deployment on ACI")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config["aci_name"]
# Get the hosted web service
service = Webservice(name=service_name, workspace=ws)

print()
print("Service state: ", service.state)
print()

import pandas as pd

data = pd.read_csv("./data/retraining_data/Youtube04-Eminem.csv")
data = data.rename(columns={"CONTENT": "text", "CLASS": "label"})
data = data.drop(['COMMENT_ID', 'AUTHOR', 'DATE'], axis=1)

data_X = data.drop("label", axis=1)
y = data["label"]

input_payload = json.dumps({
    'data': data_X['text'].tolist()
})

output = service.run(input_payload)
result = json.loads(output)['result']
print(result)

print()
print(classification_report(y, result))
print()

#pred_df = data
#pred_df['prediction'] = result
#pred_df[y!=result]
