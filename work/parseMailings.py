from datetime import datetime


def dateTransform(date):
    if type(date) == str:
        if len(date) == 24:
            day = date.split('T')[0]
            time = date.split('T')[1]
            timeOnly = time.split('.')[0]
            dateTimeValue = day + ' ' + timeOnly
        else:
            dateTimeValue = date
    else:
        dateTimeValue = date

    return dateTimeValue
