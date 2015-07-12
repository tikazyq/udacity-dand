#!/usr/bin/python

import sys
import pickle
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

### features_list is obtained from ExtraTreesClassifier
features_list = [
    'poi',
    'exercised_stock_options',
    'from_poi_to_this_person',
    'expenses',
    'from_this_person_to_poi',
    'total_stock_value',
    'salary',
    'long_term_incentive',
    'bonus',
    'restricted_stock',
    'to_messages'
]

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r"))

### Task 2: Remove outliers
data_dict.pop('TOTAL')

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()    # Provided to give you a starting point. Try a varity of classifiers.
params = {
    'max_depth': range(5, 250, 10)
}
# clf = GridSearchCV(DecisionTreeClassifier(), params)
clf = DecisionTreeClassifier(max_depth=5)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)