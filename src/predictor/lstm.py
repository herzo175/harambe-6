import time
import random
from datetime import datetime

import requests
import numpy as np
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from config import config


def get_time_series_daily(symbol, filters=[], outputsize="", apikey=config.get_config_key("ALPHAVANTAGE_API_KEY")):
    return get_alphavantage(
        "TIME_SERIES_DAILY",
        "Time Series (Daily)",
        attributes=[f"symbol={symbol}", f"outputsize={outputsize}"],
        filters=filters,
        apikey=apikey
    )


def get_vwap(symbol, interval="15min"):
    return get_alphavantage(
        "VWAP",
        "Technical Analysis: VWAP",
        attributes=[f"symbol={symbol}", f"interval={interval}"]
    )


def get_alphavantage(function, rootkey, attributes=[], filters=[], apikey=config.get_config_key("ALPHAVANTAGE_API_KEY")):
    url = f"https://www.alphavantage.co/query?function={function}&{'&'.join(attributes)}&apikey={apikey}"
    data = requests.get(url).json()

    times = data[rootkey]

    if filters != []:
        return {time: {fil: times[time][fil] for fil in filters} for time in times}
    else:
        return times


def times_to_vectors(times, include_time=False):
    def get_col(time, col):
        val = times[time][col]

        if include_time:
            if len(time) > 10:
                ptime = datetime.strptime(time, "%Y-%m-%d %H:%M")
            else:
                ptime = datetime.strptime(time, "%Y-%m-%d")

            return (ptime, val)
        else:
            return val

    return [[get_col(time, col) for col in times[time]] for time in times]


def get_frames(vectors, seq_len, with_target=False):
    return [
        vectors[i:seq_len+i+(1 if with_target else 0)]
        for i in range(len(vectors) - (seq_len+(1 if with_target else 0)))
    ]


def normalize_frames(frames):
    return [normalize_frame(frame) for frame in frames]


def normalize_frame(frame):
    return [
        [(float(dim) / float(frame[0][i])) - 1 for i, dim in enumerate(vector)]
        for vector in frame
    ]


def denormalize_dim(dim, first_dim):
    return (float(dim)+1) * float(first_dim)


def seperate_xy(frames):
    # x (input set), y (output)
    return [frame[:-1] for frame in frames], [frame[-1] for frame in frames]


def partition_data(data_list, partition_coefficient=0.8):
    split_at = int(partition_coefficient * (len(data_list)-1))

    train = data_list[:split_at]
    test = data_list[split_at:]

    random.shuffle(train)

    return train, test


def frame_to_np_array(frame):
    return np.array([np.array(vector, dtype=np.float64) for vector in frame])


def frames_to_np_array(frames):
    return np.array([frame_to_np_array(frame) for frame in frames])
    # return np.array(frame_to_np_array(frame) for frame in frames)


def predict_sequences_multiple(model, frames):
    return [model.predict(frames_to_np_array([frame]))[0] for frame in frames]


def setup_lstm_model(x_train, y_train):
    # expect x_train and y_train to be 3D ([[[(vector)] (frame)] (frames)])
    x_train = frames_to_np_array(x_train)
    y_train = frames_to_np_array(y_train)

    model = Sequential()
    model.add(LSTM(
        input_shape=(None, x_train[0][0].size),
        units=x_train[0].size,
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        100,
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        units=1))
    model.add(Activation('linear'))

    start = time.time()
    model.compile(loss='mse', optimizer='rmsprop')
    print('compilation time : ', time.time() - start)

    model.fit(
        x_train,
        y_train,
        batch_size=512,
        epochs=1,
        validation_split=0.05)

    return model


def zip_times(datasets):
    # key must be a key in all other datasets
    first_dataset = datasets[0]
    other_datasets = datasets[1:]

    zipped = {}

    for key in first_dataset:
        add_fields = True
        # combine fields for each date for all datasets
        fields = {f: first_dataset[key][f] for f in first_dataset[key]}

        for dataset in other_datasets:
            if key not in dataset:
                add_fields = False
                break
            else:
                for f in dataset[key]:
                    fields[f] = dataset[key][f]

        if add_fields:
            zipped[key] = fields

    return zipped