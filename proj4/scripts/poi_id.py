#!/usr/bin/python

import sys
import pickle
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

RANDOM_STATE = 10000

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### features_list is obtained from ExtraTreesClassifier
features_list = [
    'poi',
    # original features
    'exercised_stock_options',
    'total_stock_value',
    'bonus',
    'salary',
    'deferred_income',
    'long_term_incentive',
    'restricted_stock',
    'total_payments',
    'shared_receipt_with_poi',
    'from_poi_to_this_person',
    'loan_advances',
    # engineered features
    'total_income',
    'from_to_poi',
]

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))

### Task 2: Remove outliers
data_dict.pop('TOTAL')

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict
for k, v in my_dataset.iteritems():
    # total_income = salary + bonus
    try:
        salary = int(v.get('salary'))
        bonus = int(v.get('bonus'))
        my_dataset[k]['total_income'] = salary + bonus
    except:
        my_dataset[k]['total_income'] = 'NaN'
    try:
        exercised_stock_options = int(v.get('exercised_stock_options'))
        total_stock_value = int(v.get('total_stock_value'))
        my_dataset[k]['from_to_poi'] = exercised_stock_options + total_stock_value
    except:
        my_dataset[k]['from_to_poi'] = 'NaN'

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
target_metric = 'f1'
clf_list = [
    DecisionTreeClassifier(random_state=RANDOM_STATE),
    RandomForestClassifier(random_state=RANDOM_STATE),
    LogisticRegression(random_state=RANDOM_STATE),
    SGDClassifier(random_state=RANDOM_STATE),
]
params_list = [
    {
        'criterion': ['gini', 'entropy'],
        'min_samples_split': range(2, 5),
    },
    {
        'criterion': ['entropy', 'gini'],
        'min_samples_split': range(2, 5),
    },
    {
        'penalty': ['l1', 'l2'],
        'C': [1., 100., 1000.],
    },
    {
        'loss': ['hinge', 'log'],
        'alpha': [1e-4, 1e-3, 1e-2, 1e-1],
    },
]
### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
for clf, params in zip(clf_list, params_list):
    clf = GridSearchCV(clf, params, scoring=target_metric)

    test_classifier(clf, my_dataset, features_list, folds=1000)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

# choose DecisionTreeClassifier as the final classifier
clf_final = clf_list[0]

dump_classifier_and_data(clf_final, my_dataset, features_list)
