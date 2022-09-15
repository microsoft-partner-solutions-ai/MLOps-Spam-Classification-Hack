from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace, Experiment
from azureml.core import Environment, ScriptRunConfig
import json
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

# Attach Experiment
experiment_name = "spam-mlops-localrun"
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace.name, sep="\n")


# Editing a run configuration property on-fly.
user_managed_env = Environment("user-managed-env")
user_managed_env.python.user_managed_dependencies = True

# You can choose a specific Python environment by pointing to a Python path 
#user_managed_env.python.interpreter_path = '/home/johndoe/miniconda3/envs/myenv/bin/python'

src = ScriptRunConfig(source_directory='./scripts', script='training/classifier.py')
src.run_config.environment = user_managed_env

run = exp.submit(src)

# Shows output of the run on stdout.
run.wait_for_completion(show_output=True, wait_post_processing=True)

# Raise exception if run fails
if run.get_status() == "Failed":
    raise Exception(
        "Training on local failed with following run status: {} and logs: \n {}".format(
            run.get_status(), run.get_details_with_logs()
        )
    )

# Writing the run id to /aml_config/run_id.json

run_id = {}
run_id["run_id"] = run.id
run_id["experiment_name"] = run.experiment.name
with open("./configuration/run_id.json", "w") as outfile:
    json.dump(run_id, outfile)
    

# Get all metris logged in the run
run.get_metrics()
metrics = run.get_metrics()
print(metrics)

print(run.get_file_names())