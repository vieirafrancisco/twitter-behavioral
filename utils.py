import os
import re
import json
from typing import Pattern, AnyStr, List, DataFrame

import pandas as pd
import numpy as np

import feature_functions as ff


def get_files_names(path: str, pattern: str) -> List[str]:
    files_names = [f for f in os.listdir(path) if pattern.match(f)]
    return files_names


def get_file_pattern(pattern: str) -> Pattern[AnyStr]:
    file_pattern = f"timeline_table_{pattern}_(\\d+).csv"
    return re.compile(file_pattern)


def save_dataframe(df: DataFrame, path: str, file_name: str) -> None:
    file_path = path+file_name

    if file_name in os.listdir(path):
        curr_df = pd.read_csv(file_path)
        curr_df = curr_df.append(df, ignore_index=True, sort=False)
        curr_df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, index=False)


def generate_behavioral_dataset(path: str, pattern: str) -> None:
    file_pattern = get_file_pattern(pattern)
    files_names = get_files_names(path, file_pattern)

    for file_name in files_names:
        curr_df = get_df_with_generated_features(path, file_name)
        save_dataframe(curr_df, "./resultset/", "teste.csv")


def get_df_with_generated_features(path: str, file_name: str) -> DataFrame:
    # read csv
    df = pd.read_csv(path + file_name)
    # ids values in type of list
    ids = df.id.unique()
    # final list that stores all the data
    _list = []

    # navigate id
    for i in ids:
        dfTemp = df[df.id == i]

        # user dates
        dates = []

        # total tweets number
        number_tweets = len(dfTemp)

        week_days = [0, 0, 0, 0, 0, 0, 0]

        # hashtags
        list_hashtags = []
        tweets_with_hashtags = 0
        total_hashtags = 0

        # status in type of list
        valuesTemp = dfTemp['status_object'].values

        # navigate instance
        for instance in range(len(valuesTemp)):
            # instance json
            f = json.loads(valuesTemp[instance])

            # dates in datetime type
            dates.append(ff.string_to_date(f['created_at']))

            week_days[ff.verify_day(f['created_at'])] += 1

            tweets_with_hashtags += ff.verify_hashtags(
                 f['entities']['hashtags']
            )

            total_hashtags += ff.number_hashtags(f['entities']['hashtags'])

            list_hashtags.append(total_hashtags)

        intervals = ff.get_intervals(dates)

        _list.append({
            'id': i,
            'mean_interval_tweets': np.mean(intervals),
            'std_interval_tweets': np.sqrt(np.var(intervals)),
            'monday_rf': week_days[0]/number_tweets,
            'tuesday_rf': week_days[1]/number_tweets,
            'wednesday_rf': week_days[2]/number_tweets,
            'thursday_rf': week_days[3]/number_tweets,
            'friday_rf': week_days[4]/number_tweets,
            'saturday_rf': week_days[5]/number_tweets,
            'sunday_rf': week_days[6]/number_tweets,
            'std_day_week': np.sqrt(np.var(week_days)),
            'hashtag_per_tweet': total_hashtags/tweets_with_hashtags,
            'std_hashtags': np.sqrt(np.var(list_hashtags))
        })

        columns = [
            "id", "mean_interval_tweets", "std_interval_tweets", "monday_rf",
            "tuesday_rf", "wednesday_rf", "thursday_rf", "friday_rf",
            "saturday_rf", "sunday_rf", "std_day_week", "hashtag_per_tweet",
            "std_hashtags"
        ]

        curr_df = pd.DataFrame(_list, columns=columns)
        return curr_df
