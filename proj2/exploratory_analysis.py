from pandas import *
import matplotlib.pyplot as plt
from pymongo import MongoClient

mongo = MongoClient()
db = mongo.osm


def plot_daily_contributions():
    raw = []
    cursor = db.manchester_england.aggregate([
        {'$group': {'_id': {'$substr': ['$created.timestamp', 0, 10]}, 'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}])
    for doc in cursor:
        raw.append(doc)

    df = DataFrame(raw)
    del raw

    df['timestamp'] = to_datetime(df['_id'])
    df.set_index('timestamp').plot()


if __name__ == '__main__':
    plot_daily_contributions()
