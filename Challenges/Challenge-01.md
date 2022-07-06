# Challenge 1 - Run model locally & and set up Azure DevOps repository

[< Previous Challenge](./Challenge-00.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-02.md)

## Introduction

In this challenge, you will use a dataset containing comments from the top five most popular YouTube videos in 2015. This dataset will train a binary classification model that determines whether comments should be labeled as `spam` or `not_spam` depending on its contents. 

You will use the scripts provided to load the dataset, preprocess the dataset, register the dataset in the AML Workspace, train a model, register the model in the AML Workspace, and finally deploy the model to an ACI Web Instance and AKS Cluster. This entire lifecycle will be done using [Azure ML Python SDK](https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py).


## Description

- Clone the GitHub repository containing the [scripts provided for this hack](https://github.com/ShivaKumarChittamuru/Spam_Classification_MLOps/).
  - The script files will be in the `aml_code` folder in the repository.
  - [Create new service connections](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml) in Project Settings for your Azure ML service and Azure Subscription using Azure Resource Manager service principal. This will enable you to connect to external and remote services to execute tasks in a pipeline.
- Clone into VS Code and run the projects files locally to understand the classification project and explore the different files available.    
  **NOTE:** This is the data science part. The focus of this hack is **not** on data science, but more on MLOps to help you understand how you can apply DevOps practices and principles to accelerate your ML projects and increase the efficiency, quality, and consistency of your ML workflows.
- Install library requirements to setup your environment.
- Configure your Azure ML Workspace for the project.
  - **HINT:** Add workspace details in `config.json`. You can download this file from the Azure Portal in the resource's overview page.
  - **NOTE:** Alternatively, you can configure your Azure ML Workspace by using Azure DevOps pipeline variables.
- Now that you have environment setup, explore and run locally the python files in the folder `aml_code`. What are these files trying to do? What should be the order of execution? 

## Success Criteria

- Understand the purposes and contents of the Python scripts under `aml_code`.
- Display the top 10 rows of spam training data extracted into `data/training` folder LOCALLY using a Python script in VS Code or any popular IDE.
- Binary classification model created locally using VS Code.
- Classifier project imported into Azure DevOps.

## Learning resources

- [MLOps Home page to discover more](<https://azure.microsoft.com/en-us/services/machine-learning/mlops/>)
- [MLOps documentation: Model management, deployment, and monitoring with Azure Machine Learning](<https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment>)
- [A blog on MLOps - How to accelerate DevOps with ML Lifecycle Management](<https://azure.microsoft.com/en-us/blog/how-to-accelerate-devops-with-machine-learning-lifecycle-management/>)
