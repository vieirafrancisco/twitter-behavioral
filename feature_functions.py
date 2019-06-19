from datetime import datetime

import numpy as np


# return the string in datetime type
def string_to_date(string):
    temp_string = ' '.join(string.split(' ')[1:])
    temp_string = string.replace("+0000 ", "")
    temp_string = datetime.strptime(temp_string, '%a %b %d %H:%M:%S  %Y')

    return temp_string


def get_intervals(dates):
    intervals_list = []

    for idx, curr_date in enumerate(dates):
        if curr_date != dates[-1]:
            interval = curr_date - dates[idx+1]
            intervals_list.append(interval.total_seconds())

    lim_sup, lim_inf = limit_iqr(intervals_list)
    return eliminate_outliers((lim_sup, lim_inf), intervals_list)


def verify_day(date):
    w = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    date_day = date.split(' ', 1)[0]
    return w[date_day]


def limit_iqr(values):
    values.sort()
    quartile_1, quartile_3 = np.percentile(values, [25, 75])
    iqr = quartile_3 - quartile_1
    lim_sup = quartile_3 + (iqr * 1.5)
    lim_inf = quartile_1 - (iqr * 1.5)

    return lim_sup, lim_inf


def eliminate_outliers(limites, values):
    without_outliers = []
    lim_sup, lim_inf = limites
    for value in values:
        if(value <= lim_sup and value >= lim_inf):
            without_outliers.append(value)
    return without_outliers
