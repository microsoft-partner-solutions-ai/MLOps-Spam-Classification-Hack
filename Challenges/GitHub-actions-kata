<h1>AzureML Github Actions</h1>

### Duration: [Duration in minutes; max 25 minutes]

### Prerequisites

- Fork the MLOps Spam or Ham Classification Repo [https://github.com/microsoft-partner-solutions-ai/MLOps-Spam-Classification-Hack] into your own personal GitHub repo
- Connect your GitHub account to your Azure subscription to establish credentials [https://docs.microsoft.com/en-us/azure/developer/github/connect-from-azure?tabs=azure-portal%2Clinux&tryIt=true&source=docs#use-the-azure-login-action-with-a-service-principal-secret]

## Steps

### [GitHub Actions Steps] 
1. Go to the Actions tab in your repo and create a SIMPLE WORKFLOW, name the workflow `spam_azureml_workflow.yml`
2. Give your script a name.
3. Delete lines for `Push` or `Pull_Requests`, as we are going to trigger the workflow manually
4. Ensure that the `build` runs on `ubuntu:latest`
5. Login with Azure credentials by passing `'${{ secrets.AZURE_CREDENTIALS }}'`
7. Install Python Dependencies by running `pip install -r environment_setup/requirements.txt`
8. Run Workspace File by `python aml_code/Workspace.py`
9. Run Prepare Training Data file by `python aml_code/PrepareTrainingData.py`
10. Run Train Data file by `python aml_code/TrainOnLocal.py`
11. Register Model by `python aml_code/RegisterModel.py`
12. Deploy to Docker Container by `python aml_code/DeployToAci.py`

### [Validate GitHub Actions Steps] 
1. Ensure that dataset has been stored in AML Studio
2. Ensure that models have been registered in AML Studio
3. Ensure that Web Service has been deployed in AML Studio


### Reflection
[Prefined set of questions to ask upon execution of the Kata.]
