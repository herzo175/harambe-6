import time
import random

import requests

import numpy as np
import matplotlib.pyplot as plt

from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

import config


def get_time_series_daily(symbol, filters=[], outputsize="", apikey=config.ALPHAVANTAGE_API_KEY):
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


def get_alphavantage(function, rootkey, attributes=[], filters=[], apikey=config.ALPHAVANTAGE_API_KEY):
    url = f"https://www.alphavantage.co/query?function={function}&{'&'.join(attributes)}&apikey={apikey}"
    data = requests.get(url).json()

    times = data[rootkey]

    if filters != []:
        return {time: {fil: times[time][fil] for fil in filters} for time in times}
    else:
        return times


def times_to_vectors(times):
    return [[times[time][col] for col in times[time]] for time in times]


def get_frames(vectors, seq_len):
    return [vectors[i:seq_len+i+1] for i in range(len(vectors) - seq_len+1)]


def normalize_frames(frames):
    return [normalize_frame(frame) for frame in frames]


def normalize_frame(frame):
    return [
        [(float(dim) / float(frame[0][i])) - 1 for i, dim in enumerate(vector)]
        for vector in frame
    ]


def seperate_xy(frames):
    # x (input set), y (output)
    return [frame[:-1] for frame in frames], [frame[-1] for frame in frames]


def partition_data(frames, partition_coefficient=0.8):
    split_at = int(partition_coefficient * len(frames))

    train = frames[:split_at]
    test = frames[split_at:]

    random.shuffle(test)

    return train, test


def frame_to_np_array(frame):
    return np.array([np.array(vector, dtype=np.float64) for vector in frame])


def frames_to_np_array(frames):
    return np.array([frame_to_np_array(frame) for frame in frames])
    # return np.array(frame_to_np_array(frame) for frame in frames)


def predict_sequences_multiple(model, frames):
    # return [model.predict(np.reshape(frame, (dim_size, frame_size, 1)))[0,0] for frame in data]
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


def plot_results_multiple(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    plt.plot(
        np.reshape(predicted_data, (len(predicted_data))),
        label="Predicted",
        linestyle="dashed"
    )
    ax.plot(np.reshape(true_data, (len(true_data))), label="Actual")
    # #Pad the list of predictions to shift it in the graph to it's correct start
    # for i, data in enumerate(predicted_data):
    #     padding = [None for p in range(i * prediction_len)]
    #     plt.plot(padding + data, label='Prediction')
    #     plt.legend()
    plt.show()


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
