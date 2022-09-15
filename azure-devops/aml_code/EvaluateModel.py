import os, json
import azureml.core
from azureml.core import Workspace, Experiment, Run
from azureml.core.model import Model
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

# Get the latest run_id
with open("./configuration/run_id.json") as f:
    config = json.load(f)

new_model_run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace=ws, name=experiment_name)

run_id = {}
try:
    # Get most recently registered model, we assume that is the model in production. Download this model and compare it with the recently trained model by running test with same data set.
    model_list = Model.list(ws)
    production_model = next(
        filter(
            lambda x: x.created_time == max(model.created_time for model in model_list),
            model_list,
        )
    )
    production_model_run_id = production_model.tags.get("run_id")
    run_list = exp.get_runs()
    # production_model_run = next(filter(lambda x: x.id == production_model_run_id, run_list))

    # Get the run history for both production model and newly trained model and compare R2
    production_model_run = Run(exp, run_id=production_model_run_id)
    new_model_run = Run(exp, run_id=new_model_run_id)

    production_model_acc = production_model_run.get_metrics().get("Accuracy")
    new_model_acc = new_model_run.get_metrics().get("Accuracy")
    print(
        "Current Production model accuracy: {}, New trained model accuracy: {}".format(
            production_model_acc, new_model_acc
        )
    )

    promote_new_model = False
    run_id["run_id"] = production_model_run_id
    
    if new_model_acc >= production_model_acc:
        promote_new_model = True
        run_id["run_id"] = new_model_run_id
        print("New trained model performs equal or better, thus it will be registered")
except:
    promote_new_model = True
    print("This is the first model to be trained, thus nothing to evaluate for now")
    run_id["run_id"] = new_model_run_id
    
    
run_id["experiment_name"] = experiment_name
with open("./configuration/run_id.json", "w") as outfile:
    json.dump(run_id, outfile)
    
    