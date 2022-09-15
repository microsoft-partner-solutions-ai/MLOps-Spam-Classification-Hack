from azureml.core import Workspace
from azureml.core import Dataset, Run

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json, sys
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

run = Run.get_context()
ws = run.experiment.workspace
dataset = Dataset.get_by_name(workspace=ws, name='spam_csv')
df = dataset.to_pandas_dataframe()

# Save the text into the X variable
X = df.drop("label", axis=1)

# Save the true labels into the y variable
y = df["label"]

# Use 1/5 of the data for testing later
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Print number of comments for each set
print(f"There are {X_train.shape[0]} comments for training.")
print(f"There are {X_test.shape[0]} comments for testing")

plt.subplot(1, 3, 1)
y_train.value_counts().plot.pie(y='label', title='Proportion of each class for train set', figsize=(10, 6))

plt.subplot(1, 3, 3)
y_test.value_counts().plot.pie(y='label', title='Proportion of each class for test set', figsize=(10, 6))

plt.tight_layout()
plt.show()

# Allow unigrams and bigrams
vectorizer = CountVectorizer(ngram_range=(1, 5))
vectorizer

# Encode train text
X_train_vect = vectorizer.fit_transform(X_train.text.tolist())

# Fit model
clf=MultinomialNB()
clf.fit(X=X_train_vect, y=y_train)

# Vectorize test text
X_test_vect = vectorizer.transform(X_test.text.tolist())

# Make predictions for the test set
preds = clf.predict(X_test_vect)

# Return accuracy score
true_acc = accuracy_score(preds, y_test)
true_acc

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_true=y_test, y_pred=preds)

# Print the confusion matrix using Matplotlib
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')

plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

precision = precision_score(y_test, preds)
print('Precision: %.3f' % precision)

recall = recall_score(y_test, preds)
print('Recall: %.3f' % recall)

f1 = f1_score(y_test, preds)
print('f1: %.3f' % f1)

run.log('Accuracy', true_acc)
run.log('Precision', precision)
run.log('Recall', recall)
run.log('F1_Score', f1)

model_file_name = 'spam_classifier.pkl'
vec_file_name = 'count_vec.pkl'

os.makedirs('./outputs', exist_ok=True)
with open(model_file_name, 'wb') as file:
    joblib.dump(value=clf, filename='outputs/' + model_file_name)    

with open(vec_file_name, 'wb') as file:
    joblib.dump(value=vectorizer, filename='outputs/' + vec_file_name)
