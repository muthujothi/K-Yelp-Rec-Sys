import json
import numpy as np
import sys
import difflib
import csv
from pprint import pprint
from collections import OrderedDict
from collections import defaultdict

category_count = dict()
category_stars = dict()
category_average = dict()


print "Open, Parse and Play with the Business Training Set file"
with open('C:/Pst Files/Kaggle/YelpRecSys/yelp_training_set/yelp_training_set_business_subset_trainset.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        categories = data[u'categories']
        for category in categories:
            if category not in category_count:
                category_count[category] = 1
            else:
                category_count[category] = category_count[category]+1

            if category not in category_stars:
                category_stars[category] = [data[u'stars']]
            else:
                category_stars[category].append(data[u'stars'])

print category_count

print "Compute the category mean..."

for key in category_stars.iterkeys():
    arrayform_category_rating = np.asarray(category_stars[key])
    cat_mean = np.mean(arrayform_category_rating)
    category_average[key] = cat_mean

print category_average

print "Open, Parse and compute the mean of the categories (no most specialized nor most generalized) of the test set"

open_file_object = csv.writer(open("C:/Pst Files/Kaggle/YelpRecSys/learningprograms/cross_validation_prediction.csv", "wb"))
with open('C:/Pst Files/Kaggle/YelpRecSys/yelp_training_set/yelp_training_set_business_subset_crossvalidationset.json') as data_file:
    for line in data_file:
        cat_avg_list = []
        data = json.loads(line)
        categories = data[u'categories']
        for category in categories:
            if category in category_average:
                cat_avg_list.append(category_average[category])

        #print cat_avg_list
        if cat_avg_list:
            arrayform_cat_rating = np.asarray(cat_avg_list)
            cat_predict_mean = np.mean(arrayform_cat_rating)
            open_file_object.writerow([data[u'stars'],cat_predict_mean])
        else:
            open_file_object.writerow([data[u'stars'],100])

print "completed..."
