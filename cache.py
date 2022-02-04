from utils import database_util
from datetime import datetime


cache = []
temp = False
prev_time = datetime.now()


def update_data(l):
    global cache, temp, prev_time

    n = 60
    if len(cache) == 0:
        prev_time = datetime.now()
    cache.append(l)
    if (datetime.now() - prev_time).seconds >= n:
        prev_time = datetime.now()
        avg = [cache[-1][0], 0, 0, 0, 0, 0]
        for i in cache:
            avg[1] += i[1]
            avg[2] += i[2]
            avg[3] += i[3]
            avg[4] += i[4]
            avg[5] += i[5]
        avg[1] /= len(cache)
        avg[2] /= len(cache)
        avg[3] /= len(cache)
        avg[4] /= len(cache)
        avg[5] /= len(cache)
        database_util.save_data_to_db(
            [avg[0]] + [round(i, 2) for i in avg if type(i) == float])
        database_util.update_csv()

    if len(cache) > n:
        cache.remove(cache[0])


def get_cache():
    global cache
    return cache[:]
