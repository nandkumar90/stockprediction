from datetime import datetime, timedelta
import GetOldTweets3 as got
import json
import numpy as np

company = "Samsung"
dependencies = ("Xiaomi", "Sony", "toshiba")
start_date = "2019-09-01"
number_of_days = 150

def write_file(company, start_date, number_of_days, file_name):
    tweet_array = []
    retweet = 0
    likes = 0
    tweet_item = ''
    date = ''
    text = ''
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    for i in range(number_of_days - 1):
        empty = False
        start_date = (start_dt - timedelta(days=(i+1))).strftime('%Y-%m-%d')
        end_date = (start_dt - timedelta(days=i)).strftime('%Y-%m-%d')
        print ("{}:{}".format(start_date, end_date))
        print ((start_dt - timedelta(days=i+1)).weekday())
        if (start_dt - timedelta(days=i+1)).weekday() > 4:
            continue
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(company) \
            .setSince(start_date) \
            .setUntil(end_date) \
            .setMaxTweets(100)
        tweet_list = got.manager.TweetManager.getTweets(tweetCriteria)
        # print(len(tweet_list))
        if len(tweet_list) == 0:
            empty = True
        for tweet in tweet_list[::-1]:
            # print(tweet.text)
            for attr, value in tweet.__dict__.items():
                if (attr == 'date'): date = value.strftime('%Y-%m-%d')
                if (attr == 'retweets'): retweet = value
                if (attr == 'favorites'): likes = value
            if(retweet + likes) > 0:
                with open(file_name + '.csv', 'a', encoding='utf-8') as the_file:
                        the_file.write(start_date + ',' + tweet.text + '\n')
        if empty or (retweet + likes) <= 0 :
            with open(file_name + '.csv', 'a', encoding='utf-8') as the_file:
                the_file.write(start_date + ','  + '\n')

write_file(company, start_date, number_of_days, 'tweet_data')

for company in dependencies:
    write_file(company, start_date, number_of_days, 'tweet_data' + company)
