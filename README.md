# MLOps-Spam-Classification-Hack

## About This Repository
This repository encompasses a "What the Hack" event that teaches participants how to use Azure MLOps tools through a classification use case.It consists of five challenges that break down the steps required to implement an MLOps workflow using Azure DevOps and Azure Machine Learning.

Some key concepts include NLP, training a model using scikit-learn, deploying models to endpoints and containers, evaluating a classification model, and retraining a model.

## Introduction
MLOps empowers data scientists and app developers to help bring ML/AI models to production. It enables you to track, version and re-use every asset in your ML lifecycle, and provides orchestration services to streamline managing this lifecycle. This hack will help you understand how to build a [Continuous Integration and Continuous Delivery (CI/CD) pipeline](https://docs.microsoft.com/en-us/azure/devops/pipelines/apps/cd/azure/cicd-data-overview?view=azure-devops) for an AI application using Azure DevOps and Azure Machine Learning.

The solution involved in the hack is built on a YouTube dataset to predict whether or not video comments are spam. However, the CI/CD process and methodology can be easily adapted for any AI scenario beyond classification.

## Learning Objectives
In this hack you will solve a common challenge for companies to continuously deploy an AI model and maintain it in production. You will see how you can adopt standard engineering practices around DevOps and CICD process on ML lifecycle to get real business value.

You are working with data consisting of comments from the top five most popular YouTube videos in 2015. Your job is to use this dataset to create a classification model that will determine whether future comments are spam or not. 

Once you have a trained model, then what? You will need to make sure your model is reproducible and the results are accessible for consumption via an endpoint. This means that someone else should be able to utilize your code from a different machine when you're on vacation. Additionally, whenever new comments come in, model needs to be able to be tested offline and retrained locally before pushing out new results.

MLOps will help your team collaborate better on model training, scoring, and deployment steps within DevOps. Additionally, the existing model should remain live in production even while the retraining process is occurring.

Your team may not be a bunch of data scientists at heart, but you understand what is going on from a conceptual level. You have been given the Python scripts that were used for the modeling, now you need to make sense of it and start finding a way to get it into Azure DevOps.

Some questions that might surface throughout this hack:

- What are the needs of maintaining an ML model and its deployment?
- How to enable Continuous Integration for our AI project by creating a Build pipeline?
- What artifacts do we deploy into the repo and what is our architecture end state?
- How to enable Continuous Delivery for our AI project by creating a Release pipeline?
- How do we automate our ML lifecycle and score our data?
- What is retraining?
- How to evaluate the best model between the current model and previous models?
- How to convert a model into an endpoint?


## Challenges
-----
-  [Challenge 0: Prerequisities](./Challenges/Challenge-00.md)
-  [Challenge 1: Setup your local environment and run code locally](./Challenges/Challenge-01.md)
-  [Challenge 2: Create a Workflow with Build Job in Azure DevOps](./Challenges/Challenge-02.md)
-  [Challenge 3: Add Staging Job to your Workflow](./Challenges/Challenge-03.md)
-  [Challenge 4: Add Production Job to your Workflow](./Challenges/Challenge-04.md)
-  [Challenge 5: Retraining and Model Evaluation](./Challenges/Challenge-05.md)

## Contributors
- Ahmed Sherif
- Amanda Wong
- Shiva Chittamuru
