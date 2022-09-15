import os, json, sys
import datetime
import sklearn

from azureml.core import Workspace, Environment
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication

from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig

from azureml.core.compute import ComputeTarget, AksCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.webservice import AksWebservice

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

import sklearn

environment = CondaDependencies.create(conda_packages=[
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

with open("./scripts/scoring/conda_dependencies.yml","w") as f:
    f.write(environment.serialize_to_string())

myenv = Environment.from_conda_specification(name="myenv", file_path="./scripts/scoring/conda_dependencies.yml")

inference_config = InferenceConfig(entry_script='./scripts/scoring/score.py', environment=myenv)

aks_name = "spam-aks"

creating_compute = False
try:
    aks_target = ComputeTarget(ws, aks_name)
    print("Using existing AKS compute target {}.".format(aks_name))
except ComputeTargetException:
    print("Creating a new AKS compute target {}.".format(aks_name))

    # Use the default configuration (can also provide parameters to customize).
    prov_config = AksCompute.provisioning_configuration()
    aks_target = ComputeTarget.create(workspace=ws,
                                      name=aks_name,
                                      provisioning_configuration=prov_config)
    creating_compute = True


if creating_compute and aks_target.provisioning_state != "Succeeded":
    aks_target.wait_for_completion(show_output=True)
    
print("AKS Target state: ", aks_target.provisioning_state)
print("AKS Target provisioning errors: ", aks_target.provisioning_errors)

aks_deployment_config = AksWebservice.deploy_configuration(enable_app_insights=True)

if aks_target.provisioning_state == "Succeeded":
    aks_service_name = "spam-aks" + datetime.datetime.now().strftime("%m%d%H%M")
    aks_service = Model.deploy(ws,
                               aks_service_name,
                               [model, cv],
                               inference_config,
                               aks_deployment_config,
                               deployment_target=aks_target,
                               overwrite=True)
    aks_service.wait_for_deployment(show_output=True)
    print(aks_service.state)
else:
    raise ValueError("AKS cluster provisioning failed. Error: ", aks_target.provisioning_errors)


# Writing the ACI details to /aml_config/aci_webservice.json
aks_webservice = {}
aks_webservice["aks_name"] = aks_service.name
aks_webservice["aks_url"] = aks_service.scoring_uri
with open("./configuration/aks_webservice.json", "w") as outfile:
    json.dump(aks_webservice, outfile)
    
    
