import os, json, sys
import datetime

from azureml.core import Workspace, Run, Experiment
from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice


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


from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
import sklearn


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


aci_service_name = "spam-aci" + datetime.datetime.now().strftime("%m%d%H%M")

inference_config = InferenceConfig(entry_script='./scripts/scoring/score.py', environment=environment)
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1, tags={"area": "spam", "type": "classification"},
    description="Spam detector web service")


service = Model.deploy(workspace=ws,
                       name=aci_service_name,
                       models=[model, cv],
                       inference_config=inference_config,
                       deployment_config=aci_config,
                       overwrite=True)

try:
    service.wait_for_deployment(show_output = True)
except:
    print("**************LOGS************")
    print(service.get_logs())


print()
print("Service state: ", service.state)
print()
print(service.get_logs())

# Writing the ACI details to /aml_config/aci_webservice.json
aci_webservice = {}
aci_webservice["aci_name"] = service.name
aci_webservice["aci_url"] = service.scoring_uri
with open("./configuration/aci_webservice.json", "w") as outfile:
    json.dump(aci_webservice, outfile)
    
    
