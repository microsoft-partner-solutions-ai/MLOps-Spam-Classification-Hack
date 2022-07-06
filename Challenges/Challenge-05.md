# Challenge 5 – Retraining and Model Evaluation

[< Previous Challenge](./Challenge-04.md) - **[Home](../README.md)**

## Introduction

When the new data deviates from the original trained data that the model was trained, the model performance deteriorates. This concept, known as model drift, can be mitigated by retraining the model when new data becomes available, to reflect the current reality.

In Azure DevOps, you can retrain the model on a schedule or when new data becomes available. The machine learning pipeline orchestrates the process of retraining the model in an asynchronous manner. A simple evaluation test compares the new model with the existing model. Only when the new model is better does it get promoted. Otherwise, the model is not registered with the Azure ML Model Registry.

## Description

- Additional YouTube video comments data that was not included in the first iteration of the model can be found in the `data/retraining` folder. The hope is that this additional data will improve your model!
    - Is updating the classifier code necessary? If yes, what needs to be changed? Check the training code in `classifier.py` in `scripts/training/` folder. The initial model was trained on data of three YouTube videos.
    - Concatenate these two datasets/dataframes and build a classifier trained model on this bigger dataset.
- Re-run the `Build` pipeline to reflect the changes in training.
- Re-run the `Release` pipeline with the latest build. If the new model has better evaluation metrics than the previous model, then a new web service is created for your retrained model.
- Review artifacts and outputs from `Build` and `Release` pipelines.

## Success criteria

- A retrained model (if necessary with better performance) is created and registered within the Azure ML Model Registry.
- A “Healthy” ACI deployment for your retrained model is created under Azure ML Endpoints from Pre-prod stage.
- A “Healthy” AKS deployment for your retrained model is created under Azure ML Endpoints from Prod stage.

## Learning resources

- [MLOps documentation: Model management, deployment, and monitoring with Azure Machine Learning](<https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment>)
- [MLOps Reference Architecture](<https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/ai/mlops-python>)

## Congratulations

You have finished the challenges for this Hack. We are updating the content continuously. In the upcoming phase 2 of this hack content we will be extending this solution to encompass AKS Data Drift in Challenge 5 as well as incorporate other ML platforms, such as ONNX and mlflow. Stay tuned!
