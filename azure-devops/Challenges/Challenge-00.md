# Challenge 0: Getting set up

**[Home](../README.md)** - [Next Challenge >](./Challenge-01.md)

## Introduction

Similar to DevOps, MLOps is a very broad topic and you have lots of choices when it comes to the tools that you use. In this challenge, our focus is to make sure you have right tools installed on your computer.

## Description

In this challenge we'll be setting up all the tools we will need to complete our challenges.

- Azure subscription
- [Azure Machine Learning service workspace](https://ml.azure.com/) 
- Azure DevOps organization. If you do not have one, you can sign up for a [free account](https://azure.microsoft.com/en-us/services/devops/).
  - Install [Azure DevOps Machine Learning extension](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml).
  - Request Admin access to [create Service Connections](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml) within Azure DevOps to connect with Azure ML Workspace. If the access is not granted, have admin create those service connections ahead of time. To do that, create a new project and [create new service connections](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml) in Project Settings for your Azure Subscription and Azure ML service using a Azure Resource Manager service principal.

    **Note:** Azure ML Workspace must be created first before creating Service Connections.
- If using a Windows machine, it is recommended to install [Linux on Windows with WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
- Python Installation, version at least \>= 3.6.5. Miniconda is recommended for traditional Data Science tasks and the purposes of this hack.
  - Miniconda - <https://docs.conda.io/en/latest/miniconda.html>
  - Python - <https://www.python.org/downloads/>
- Ensure Python modules are available to download via pip (from [PyPI](https://pypi.org) or from an internal package manager).
  - azure-cli==2.22.1
  - azureml-sdk[cli]
  - joblib
  - matplotlib
  - numpy
  - pandas
  - scipy
  - scikit-learn
- Visual Studio Code or any Python IDE
  - Python extensions

**NOTE**: You will need privileges to create projects in the Azure DevOps organization. Also, you need privileges to create Service Principal in the tenant that has **Contributor** RBAC access to your subscription/resource group. This translates to **Ensure that the user has 'Owner' or 'User Access Administrator' permissions on the Subscription**.

## Success Criteria

- You have an Azure ML Workspace created on your Azure subscription.
- You have an Azure DevOps account with the Azure Machine Learning extension installed.
- You have Python installed along with some IDE to run python code.
