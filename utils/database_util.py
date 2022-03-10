import csv
import os
from datetime import datetime,timedelta


def save_data_to_db(data):
    with open(os.path.join(os.getcwd(), "data1.csv"), 'a+', newline='') as f:
        writer = csv.writer(f)
        data[0] = data[0].strftime('%Y-%m-%d %H:%M')
        writer.writerow(data)


def update_csv():
    with open(os.path.join(os.getcwd(), "data1.csv"), 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    with open(os.path.join(os.getcwd(), "data1.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        t = datetime.now()-timedelta(days=31)
        for i in data:
            a = datetime.strptime(i[0], '%Y-%m-%d %H:%M')
            if a >= t:
                writer.writerow(i)


def get_data_from_date(date1, date2):
    with open(os.path.join(os.getcwd(), "data1.csv"), 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    temp = []
    for i in data:
        a = datetime.strptime(i[0], '%Y-%m-%d %H:%M')
        if not (date1 <= a <= date2):
            temp.append(i)
    for i in temp:
        data.remove(i)
    return data
