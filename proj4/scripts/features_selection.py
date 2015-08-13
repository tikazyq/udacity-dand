#!/usr/bin/python

import sys
import os
import pickle
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import numpy as np

basedir = os.path.dirname(__file__)
os.chdir("../scripts")
sys.path.append(os.path.abspath(os.path.join(basedir, '../tools')))

from feature_format import featureFormat, targetFeatureSplit

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
financial_vars = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                  'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                  'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
email_vars = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi',
              'shared_receipt_with_poi']
label_vars = ['poi']

features_list = label_vars + financial_vars + email_vars

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))
### remove outliers
data_dict.pop('TOTAL')

my_dataset = data_dict

data = featureFormat(my_dataset, features_list, sort_keys=True)

# scale the features
from sklearn.preprocessing import MinMaxScaler
scalar = MinMaxScaler()
data = scalar.fit_transform(data)

labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import f_regression

from sklearn.feature_selection import SelectKBest

clf = SelectKBest(f_regression)
clf.fit(features, labels)

scores = clf.scores_
indices = np.argsort(scores)[::-1]

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

n = len(indices)
plt.bar(range(n), scores[indices])
plt.xticks(range(n), np.array(features_list)[1:][indices])
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.title('Feature Scores with SelectKBest')
plt.ylabel('feature score')
plt.tight_layout()
plt.savefig('../figures/figure_2_feature_selection.png')
plt.show()
