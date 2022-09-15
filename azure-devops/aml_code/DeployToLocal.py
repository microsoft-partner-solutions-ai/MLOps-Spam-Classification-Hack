import os, json, sys
import sklearn
from azureml.core import Workspace, Run, Experiment
from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication

from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig


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
    with open("./configuration/model.json") as f:
        config = json.load(f)
except:
    print("No new model to register thus no need to create new scoring image")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)
    
    
model_name = config["model_name"]
model_version = config["model_version"]

model_list = Model.list(workspace=ws)
model, = (m for m in model_list if m.version == model_version and m.name == model_name)
print(
    "Model picked: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)


try:
    with open("./configuration/cv.json") as f:
        cv_config = json.load(f)
except:
    print("No new model to register thus no need to create new scoring image")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)
    

cv_name = cv_config["cv_name"]
cv_version = cv_config["cv_version"]


cv_list = Model.list(workspace=ws)
cv, = (m for m in model_list if m.version == cv_version and m.name == cv_name)
print(
    "Model picked: {} \nModel Description: {} \nModel Version: {}".format(
        cv.name, cv.description, cv.version
    )
)



environment = Environment('my-sklearn-environment')
environment.python.conda_dependencies = CondaDependencies.create(conda_packages=[
    'pip==20.2.4'],
    pip_packages=[
    'azureml-defaults',
    'inference-schema[numpy-support]',
    'joblib',
    'numpy',
    'pandas',
    'matplotlib',
    'scikit-learn=={}'.format(sklearn.__version__)
])


from azureml.core.model import InferenceConfig

inference_config = InferenceConfig(entry_script='./scripts/scoring/score.py', environment=environment)

from azureml.core.webservice import LocalWebservice

# This is optional, if not provided Docker will choose a random unused port.
deployment_config = LocalWebservice.deploy_configuration(port=6789)

local_service = Model.deploy(ws, "spam-local-test", [model, cv], inference_config, deployment_config, overwrite=True)
try:
    local_service.wait_for_deployment(show_output = True)
except:
    print("**************LOGS************")
    print(local_service.get_logs())

print()
print("Service state: ", local_service.state)
print()
#print(local_service.get_logs())

import pandas as pd

data = pd.read_csv("./data/retraining_data/Youtube04-Eminem.csv")
data = data.rename(columns={"CONTENT": "text", "CLASS": "label"})
data = data.drop(['COMMENT_ID', 'AUTHOR', 'DATE'], axis=1)

data_X = data.drop("label", axis=1)
y = data["label"]

input_payload = json.dumps({
    'data': data_X['text'].tolist()
})

output = local_service.run(input_payload)
result = json.loads(output)['result']
print(result)

from sklearn.metrics import classification_report
print(classification_report(y, result))