from datetime import datetime, timedelta
import numpy as np

import backtrader

from predictor import lstm, backtesting, datasource

TRAINING_LENGTH=180


def convert_date_string(date_string):
    date_format_string = "%Y-%m-%d"
    return datetime.strptime(date_string, date_format_string)


def get_time_diff_days(start_date, end_date):
    start_datetime = convert_date_string(start_date)
    end_datetime = convert_date_string(end_date)
    return (end_datetime - start_datetime).days


def predict(symbol, trend_length=None, trend_start_date=None, trend_end_date=None):
    times = datasource.get_time_series_daily(
        symbol=symbol,
        start=(datetime.now() - timedelta(days=TRAINING_LENGTH)),
        end=datetime.now()
    )

    # TODO: load model if there is one within 5% of the time range

    if not not trend_start_date and not not trend_end_date:
        print("has trend start and end dates")
        trend_length = get_time_diff_days(trend_start_date, trend_end_date)
        times = datasource.get_time_series_daily(
            symbol=symbol,
            start=(convert_date_string(trend_start_date)- timedelta(days=TRAINING_LENGTH)),
            end=convert_date_string(trend_end_date)
        )
    elif trend_length is None or trend_length <= 0:
        raise ValueError("must specify trend_start_date and trend_end_date or trend_length > 0")

    vectors = lstm.times_to_vectors(times)
    frames = lstm.get_frames(vectors, seq_len=trend_length, with_target=True)

    # TODO: cache predictions
    train_x, train_y = lstm.seperate_xy(lstm.normalize_frames(frames))
    model = lstm.setup_lstm_model(train_x, train_y)
    last_frame = frames[-1][1:]
    prediction = lstm.predict_sequences_multiple(model, [lstm.normalize_frame(last_frame)])

    prediction_val = prediction[0][0]
    prediction_val_denorm = lstm.denormalize_dim(prediction_val, last_frame[0][0])

    # assert False, f"last frame: {last_frame}, last frame norm: {[lstm.normalize_frame(last_frame)]}, prediction: {prediction}, prediction val denorm: {prediction_val_denorm}"

    return float(prediction_val), float(prediction_val_denorm)


def backtest(symbol, start_date, end_date, trend_length):
    start = convert_date_string(start_date)
    end = convert_date_string(end_date)

    days_between = abs(np.busday_count(start.date(), end.date()))

    assert (days_between >= trend_length), f"Got {days_between} business days between dates, must be >= {trend_length}"

    times = datasource.get_time_series_daily(
        symbol=symbol,
        start=(start - timedelta(days=180)),
        end=end
    )

    training_times, _ = lstm.split_times(times, start_date)

    training_vectors = lstm.times_to_vectors(training_times, include_time=False)[::-1]
    training_frames = lstm.get_frames(training_vectors, trend_length, with_target=True)

    normalized_train = lstm.normalize_frames(training_frames)
    x_train, y_train = lstm.seperate_xy(normalized_train)

    model = lstm.setup_lstm_model(x_train, y_train)

    print(model)

    # setup inital testing strategy
    cerebro = backtrader.Cerebro()
    cerebro.broker.setcash(100000.0)
    # cerebro.addsizer(Reverser)
    cerebro.addsizer(backtesting.PercentIncrease)
    cerebro.broker.setcommission(commission=0.001)

    # add data and model to strategy
    cerebro.addstrategy(backtesting.TestStrategy, model=model, trend_length=trend_length)

    cerebro.adddata(
        backtrader.feeds.YahooFinanceData(
            dataname=symbol,
            fromdate=start,
            todate=end
        )
    )

    starting_value = cerebro.broker.getvalue()
    cerebro.run()
    ending_value = cerebro.broker.getvalue()

    percent_change = (ending_value - starting_value) / starting_value

    print(f"percent change: {percent_change}")
    return percent_change
