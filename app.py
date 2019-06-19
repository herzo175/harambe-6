from datetime import datetime

import lstm


def convert_date_string(date_string):
    date_format_string = "%Y-%m-%d"
    return datetime.strptime(date_string, date_format_string)


def get_time_diff_days(start_date, end_date):
    start_datetime = convert_date_string(start_date)
    end_datetime = convert_date_string(end_date)
    return (end_datetime - start_datetime).days


def predict(symbol, trend_length=None, trend_start_date=None, trend_end_date=None):
    # NOTE: configurable filters?
    times = lstm.get_time_series_daily(symbol, filters=["1. open"], outputsize="full")

    # TODO: load model if there is one within 5% of the time range

    if not not trend_start_date and not not trend_end_date:
        print("has trend start and end dates")
        trend_length = get_time_diff_days(trend_start_date, trend_end_date)
        end_datetime = convert_date_string(trend_end_date)

        times = {
            time: times[time]
            for time in times
            if convert_date_string(time) <= end_datetime
        }
    elif trend_length is None or trend_length <= 0:
        raise ValueError("must specify trend_start_date and trend_end_date or trend_length > 0")

    vectors = lstm.times_to_vectors(times)[::-1]
    frames = lstm.get_frames(vectors, seq_len=trend_length, with_target=True)

    # TODO: cache predictions
    train_x, train_y = lstm.seperate_xy(lstm.normalize_frames(frames))
    model = lstm.setup_lstm_model(train_x, train_y)
    last_frame = frames[-1][1:]
    prediction = lstm.predict_sequences_multiple(model, [lstm.normalize_frame(last_frame)])

    prediction_val = prediction[0][0]
    prediction_val_denorm = lstm.denormalize_dim(prediction_val, last_frame[0][0])

    return float(prediction_val), float(prediction_val_denorm)
