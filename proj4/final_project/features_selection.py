#!/usr/bin/python

import sys
import os
import pickle
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import numpy as np

os.chdir("/Users/yeqing/projects/notebook/udacity/dand/proj4/ud120-projects/final_project")
sys.path.append("/Users/yeqing/projects/notebook/udacity/dand/proj4/ud120-projects/tools")
sys.path.append("/Users/yeqing/projects/notebook/udacity/dand/proj4/ud120-projects/final_project")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
financial_vars = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                  'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                  'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
email_vars = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi',
              'shared_receipt_with_poi']
label_vars = ['poi']
# features_list = [
#     'poi',
#     'salary',
#     'total_payments',
#     'bonus',
#     'total_stock_value',
#     'expenses',
#     'exercised_stock_options',
#     'from_poi_to_this_person',
#     'to_messages',
# ]

features_list = label_vars + financial_vars + email_vars

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))
### remove outliers
data_dict.pop('TOTAL')

my_dataset = data_dict

data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import GenericUnivariateSelect, SelectKBest
from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import ExtraTreesClassifier

clf = ExtraTreesClassifier()
clf.fit(features, labels)

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

import matplotlib.pyplot as plt

n = len(indices)
plt.bar(range(n), importances[indices])
plt.xticks(range(n), np.array(features_list)[1:][indices])
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.title('Feature Importance with ExtraTreesClassifier')
plt.ylabel('feature importance')
plt.tight_layout()
plt.savefig('feature_selection_ExtraTreesClassifier.png')
plt.show()

