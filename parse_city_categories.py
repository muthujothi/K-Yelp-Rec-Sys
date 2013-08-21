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
with open('C:/LearningMaterials/Kaggle/YelpRecSys/yelp_training_set/yelp_training_set_business.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        categories = data[u'categories']
        for category in categories:
            if category+data[u'city'] not in category_count:
                category_count[category+data[u'city']] = 1
            else:
                category_count[category+data[u'city']] = category_count[category+data[u'city']] + 1

#print category_count
print len(category_count)

cat_city_count = []
for key in category_count.iterkeys():
    cat_city_count.append(category_count[key])

print cat_city_count
print len(cat_city_count)

print np.median(cat_city_count)
