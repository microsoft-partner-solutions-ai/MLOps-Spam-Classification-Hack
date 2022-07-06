import os, json, sys
from azureml.core import Workspace, Run, Experiment
from azureml.core.model import Model
from azureml.core.runconfig import RunConfiguration
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

# Get the latest evaluation result
try:
    with open("./configuration/run_id.json") as f:
        config = json.load(f)
    if not config["run_id"]:
        raise Exception("No new model to register as production model perform better")
except:
    print("No new model to register as production model perform better")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)
    
    
run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace=ws, name=experiment_name)

run = Run(experiment=exp, run_id=run_id)
names = run.get_file_names
print("Experiment run files:", names())
print("Run ID for last run: {}".format(run_id))

#model_local_dir = "model"
#os.makedirs(model_local_dir, exist_ok=True)


# Download Model to Project root directory
model_name = "spam_classifier.pkl"
cv_name = "count_vec.pkl"

run.download_file(
    name="./outputs/" + model_name, output_file_path="./model/" + model_name
)
run.download_file(
    name="./outputs/" + cv_name, output_file_path="./model/" + cv_name
)
print("Downloaded model {} to model directory".format(model_name))
print("Downloaded Vectorizer {} to model directory".format(cv_name))





model = Model.register(
    model_path="./model/spam_classifier.pkl",  # this points to a local file
    model_name='spam_classifier',  # this is the name the model is registered as
    tags={"area": "spam", "type": "classification", "run_id": run_id},
    description="Spam Classifier model",
    workspace=ws,
)

print(
    "Model registered: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)

# Writing the registered model details to /aml_config/model.json
model_json = {}
model_json["model_name"] = model.name
model_json["model_version"] = model.version
model_json["run_id"] = run_id
with open("./configuration/model.json", "w") as outfile:
    json.dump(model_json, outfile)
    
cv = Model.register(
    model_path="./model/count_vec.pkl",  # this points to a local file
    model_name='count_vec',  # this is the name the model is registered as
    tags={"area": "spam", "type": "vectorizer", "run_id": run_id},
    description="Count Vectorizer for Spam Classifier model",
    workspace=ws,
)
#os.chdir("..")
print(
    "Model registered: {} \nModel Description: {} \nModel Version: {}".format(
        cv.name, cv.description, cv.version
    )
)

# Writing the registered model details to /aml_config/model.json
cv_json = {}
cv_json["cv_name"] = cv.name
cv_json["cv_version"] = cv.version
cv_json["run_id"] = run_id
with open("./configuration/cv.json", "w") as outfile:
    json.dump(cv_json, outfile)
