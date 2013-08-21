import json
import numpy as np
import sys
import difflib
import csv
from pprint import pprint
from collections import OrderedDict
from collections import defaultdict

user_ratings = dict()
user_ratings_mean = dict()
business_ratings = dict()
business_ratings_mean = dict()
all_business_ratings = []
user_review_count = dict()
business_review_count = dict()
business_chain_rating = dict()
business_chain_rating_mean = dict()
business_city_rating = dict()
business_city_rating_mean = dict()

train_businessid_name = dict()
test_businessid_name = dict()
test_businessid_city = dict()

category_count = dict()
category_stars = dict()
category_average = dict()

test_business_cats = dict()

#Open the yelp_training_user.json and compute the mean ratings per user.
#Global user mean is not required because, when a user info is
#not available in the test set, then we should go by the mean business rating.
#Even if the business ratings is not available, then go by gloabl mean business
#rating.
#The intutional questions are as follows,
#1. What is the average rating an user normally gives?
#2. If user info is not available, then what is the average rating that the business has got?
#3. Even if the user and the business is not available, then we can go by the global business mean.
#4. Further improvisation,
#4a. If the user and business info is not available,
#then we can go by what category the business belongs to. For that
#category of business we can learn from the training, what is the mean rating provided.
#4b. Or what is the average rating provided to businesses in the same or
#different category in that locality/neighbourhood.
#4c. Based on the count of check-ins. Normally a place with many people visiting
#may be liked by an individual too if he is falling into the normal curve.
#4d. Find out in what ways you can find how good/popular a business is. The more
#good the business more the chances of the user giving a good review.

#Aug 20, 2013 - In coldstart cases, find out the specific category if the business in the respective city and predict the average rating of that category of business
#in that city.
#How to find the specific category of the business in the respective city?
#From the training set, for each business split the categories [Food, Icecream&Yoghurt] in Chandler as FoodChandler -- 4536, Icecream&YoghurtChandler -- 236
#Now get the list if category+city combination for the test record as well.
#Now find which of the test category+city combination has the lowest count in the training map. Then most probably would be more specific category+city match.
#Predict the mean rating of that combination as the rating for this test record as well.

#Instead of city based prediction use the category based prediction. - Good Improvement.

#Try weighted Average of the categories based on the importance of the category. May be Icecream is valuable than Food.

print "Learning from User Ratings..."   
with open('C:/LearningMaterials/Kaggle/YelpRecSys/yelp_training_set/yelp_training_set_user.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        user_avg_stars = data[u'average_stars']
        user_rev_cnt = data[u'review_count']

        if data[u'user_id'] in user_ratings:
            user_ratings[data[u'user_id']].append(user_avg_stars)
        else:
            user_ratings[data[u'user_id']] = [user_avg_stars]

        if data[u'user_id'] not in user_review_count:
            user_review_count[data[u'user_id']] = user_rev_cnt


print "Learning from Business Ratings..."
with open('C:/LearningMaterials/Kaggle/YelpRecSys/yelp_training_set/yelp_training_set_business.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        business_avg_stars = data[u'stars']
        bus_rev_cnt = data[u'review_count']

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
        
        all_business_ratings.append(business_avg_stars)
        
        if data[u'business_id'] in business_ratings:
            business_ratings[data[u'business_id']].append(business_avg_stars)
        else:
            business_ratings[data[u'business_id']] = [business_avg_stars]

        if data[u'business_id'] not in business_review_count:
            business_review_count[data[u'business_id']] = bus_rev_cnt

        if data[u'name'] in business_chain_rating:
            business_chain_rating[data[u'name']].append(business_avg_stars)
        else:
            business_chain_rating[data[u'name']] = [business_avg_stars]

        if data[u'city'] in business_city_rating:
            business_city_rating[data[u'city']].append(business_avg_stars)
        else:
            business_city_rating[data[u'city']] = [business_avg_stars]

        if data[u'business_id'] not in train_businessid_name:
            train_businessid_name[data[u'business_id']] = data[u'name']

#test_business_cats
print "Business ID and Name Mapping from Test Business Json File..."
with open('C:/LearningMaterials/Kaggle/YelpRecSys/yelp_test_set/yelp_test_set_business.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        if data[u'business_id'] not in test_businessid_name:
            test_businessid_name[data[u'business_id']] = data[u'name']
        if data[u'business_id'] not in test_businessid_city:
            test_businessid_city[data[u'business_id']] = data[u'city']
        if data[u'business_id'] not in test_business_cats:
            test_business_cats[data[u'business_id']] = data[u'categories']


print "Global Business Mean..."
arrayform_all_business_ratings = np.asarray(all_business_ratings)
gl_business_mean = np.mean(arrayform_all_business_ratings)
print gl_business_mean

print "Computing user rating mean..."
for key in user_ratings.iterkeys():
    arrayform_user_rating = np.asarray(user_ratings[key])
    user_mean = np.mean(arrayform_user_rating)
    user_ratings_mean[key] = user_mean

print "Computing business rating mean..."
for key in business_ratings.iterkeys():
    arrayform_business_ratings = np.asarray(business_ratings[key])
    business_mean = np.mean(arrayform_business_ratings)
    business_ratings_mean[key]=business_mean

print "Computing the business chain mean rating across the state AZ..."
for key in business_chain_rating.iterkeys():
    arrayform_business_chain_ratings = np.asarray(business_chain_rating[key])
    bus_chain_mean = np.mean(arrayform_business_chain_ratings)
    business_chain_rating_mean[key] = bus_chain_mean

print "Computing the business mean rating across the every city in state AZ..."
for key in business_city_rating.iterkeys():
    arrayform_business_city_ratings = np.asarray(business_city_rating[key])
    bus_city_mean = np.mean(arrayform_business_city_ratings)
    business_city_rating_mean[key] = bus_city_mean

print "Computing the Category Mean..."
for key in category_stars.iterkeys():
    arrayform_category_rating = np.asarray(category_stars[key])
    cat_mean = np.mean(arrayform_category_rating)
    category_average[key] = cat_mean


#print train_businessid_name
#print business_chain_rating_mean

print "Predicting the stars for a user/business pair..."
user_and_business_in_train = 0
user_andbusiness_in_train_goby_bus = 0
user_andbusiness_in_train_goby_user = 0
user_based_predictions = 0
business_based_predictions = 0
global_business_predictions = 0
business_name_based_predictions = 0
business_city_based_predictions = 0
user_present_wentby_bus_chain = 0
cold_start_cat_based_prediction = 0
data_row = 0
open_file_object = csv.writer(open("C:/LearningMaterials/Kaggle/YelpRecSys/learningprograms/New_Mode_User_Prediction.csv", "wb"))
with open('C:/LearningMaterials/Kaggle/YelpRecSys/yelp_test_set/yelp_test_set_review.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        data_row = data_row + 1
        if data[u'user_id'] in user_ratings_mean and data[u'business_id'] in business_ratings_mean:
            user_and_business_in_train = user_and_business_in_train + 1
            business_rating = business_ratings_mean[data[u'business_id']]
            user_rating = user_ratings_mean[data[u'user_id']]
            bus_rev_count = business_review_count[data[u'business_id']]
            user_rev_count = user_review_count[data[u'user_id']]

            if bus_rev_count >= user_rev_count:
                rating_tobe_predicted = business_ratings_mean[data[u'business_id']]
                user_andbusiness_in_train_goby_bus = user_andbusiness_in_train_goby_bus + 1
            else:
                rating_tobe_predicted = user_ratings_mean[data[u'user_id']]
                user_andbusiness_in_train_goby_user = user_andbusiness_in_train_goby_user + 1

        elif data[u'user_id'] in user_ratings_mean:
            rating_tobe_predicted = user_ratings_mean[data[u'user_id']]
            #test_bu_name = test_businessid_name[data[u'business_id']]
            #if test_bu_name in business_chain_rating_mean:
            #    rating_tobe_predicted = business_chain_rating_mean[test_bu_name]
            #    user_present_wentby_bus_chain = user_present_wentby_bus_chain + 1
            user_based_predictions = user_based_predictions + 1
        elif data[u'business_id'] in business_ratings_mean:
            rating_tobe_predicted = business_ratings_mean[data[u'business_id']]
            business_based_predictions = business_based_predictions + 1
        else:
            test_bus_name = test_businessid_name[data[u'business_id']]
            test_bus_city = test_businessid_city[data[u'business_id']]
            test_bus_categories = test_business_cats[data[u'business_id']]
            cat_avg_list = []
            cat_wt_list = []
            axis = 0
            for category in test_bus_categories:
                if category in category_average:
                    cat_avg_list.append(category_average[category])
                if category in category_count:
                    cat_wt_list.append(1./category_count[category])

            if test_bus_name in business_chain_rating_mean:
                rating_tobe_predicted = business_chain_rating_mean[test_bus_name]
                #if cat_avg_list:
                #    catavg_busnameavg = []
                #    arrayform_cat_rating = np.asarray(cat_avg_list)
                #    cat_predict_mean = np.mean(arrayform_cat_rating)
                #    catavg_busnameavg.append(cat_predict_mean)
                #    catavg_busnameavg.append(rating_tobe_predicted)
                #    arrayform_cat_busname = np.asarray(catavg_busnameavg)
                #    rating_tobe_predicted = np.mean(arrayform_cat_busname)
                business_name_based_predictions = business_name_based_predictions + 1
            #elif test_bus_city in business_city_rating_mean:
            #    rating_tobe_predicted = business_city_rating_mean[test_bus_city]
            #    business_city_based_predictions = business_city_based_predictions + 1
            elif cat_avg_list:
                #arrayform_cat_rating = np.asarray(cat_avg_list)
                #cat_predict_mean = np.mean(arrayform_cat_rating)
                #rating_tobe_predicted = cat_predict_mean
                rating_tobe_predicted = np.average(cat_avg_list,axis,cat_wt_list)
                cold_start_cat_based_prediction = cold_start_cat_based_prediction + 1
            else:
                rating_tobe_predicted = gl_business_mean
                global_business_predictions = global_business_predictions + 1

        open_file_object.writerow([data_row,rating_tobe_predicted])

print "Predictions Done..."
print "User and Business in Training Set.."
print user_and_business_in_train
print "User and Business in Training set, but went with business rating as the business was strongly doing good or bad..."
print user_andbusiness_in_train_goby_bus
print "User and Business in Training Set, but went with User rating as there was no strong evidence to say if the business was doing good or bad..."
print user_andbusiness_in_train_goby_user
print "User Based Predictions"
print user_based_predictions
print "Through user was present in training set, went by business chain rating..."
print user_present_wentby_bus_chain
print "Business Based Predictions"
print business_based_predictions
print "Business name based predictions which does not have user/business entry in training set..."
print business_name_based_predictions
print "Cold start Business Category based predictions..."
print cold_start_cat_based_prediction
print "Business City Based Predictions"
print business_city_based_predictions
print "Global Business Mean Predictions"
print global_business_predictions

print "percentages.."
print (user_and_business_in_train/22956.0)*100.0
print (user_andbusiness_in_train_goby_bus/user_and_business_in_train*1.0)*100
print (user_andbusiness_in_train_goby_user/user_and_business_in_train*1.0)*100
print (user_based_predictions/22956.0)*100.0
print (business_based_predictions/22956.0)*100.0
print (global_business_predictions/22956.0)*100.0
print (5/2)*1.0
