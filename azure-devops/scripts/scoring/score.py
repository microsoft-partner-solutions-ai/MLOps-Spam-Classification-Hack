import os
import pickle
import joblib
import json
import numpy
from azureml.core.model import Model
#from sklearn.feature_extraction.text import CountVectorizer


def init():
    global model, vectorizer

    # load the model from file into a global object
    model_path = Model.get_model_path(model_name='spam_classifier')
    cv_path = Model.get_model_path(model_name='count_vec')

    print("model_path: ", model_path)
    print("cv_path: ", cv_path)
    
    model = joblib.load(model_path) 
    vectorizer = joblib.load(cv_path)
   


def run(raw_data):
    try:
        data = json.loads(raw_data)["data"]  
        vec_data = vectorizer.transform(data)        
        result=model.predict(vec_data)
        return json.dumps({"result": result.tolist()})
    
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})


