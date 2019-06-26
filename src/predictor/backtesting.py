import datetime

import backtrader

from predictor import lstm


# strategy to use by backtesting
class TestStrategy(backtrader.Strategy):
    params = (
        ("model", None),
        ("trend_length", 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.closings = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        
        print(f"order size: {order.size}")
        
#         new_s, r, done, _ = env.step(a)
#         q_table[s, a] += r + lr * (y * np.max(q_table[new_s, :]) - q_table[s, a])
#         s = new_s

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED:')

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log("SELL EXECUTED:")

            print(f"Price: {order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}")
            print(self.broker.getvalue())

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return

        current_frame = [[self.closings[i]] for i in range(0, -(self.p.trend_length), -1)]
        previous_frame = [[self.closings[i]] for i in range(-1, -(1+self.p.trend_length), -1)]

        current_normalized_frame = lstm.normalize_frame(current_frame)
        previous_normalized_frame = lstm.normalize_frame(previous_frame)
    
        current_prediction = lstm.predict_sequences_multiple(self.p.model, [current_normalized_frame])
        previous_prediction = lstm.predict_sequences_multiple(self.p.model, [previous_normalized_frame])
        
        current_prediction_denorm = lstm.denormalize_dim(current_prediction[0][0], current_frame[0][0])
        # previous_prediction_denorm = lstm.denormalize_dim(previous_prediction[0][0], previous_frame[0][0])
        
        # print(f"current: {current_frame}, prediction: {current_prediction_denorm}")
        
        pred_diff = current_prediction[0][0] - previous_prediction[0][0]
        share_price = current_frame[-1][0]
        
        if not self.position:
            # can only hold, buy, or short
            if pred_diff > 0:
                if current_prediction_denorm > share_price:
                    self.log("BUY")
                    self.order = self.buy()
                else:
                    self.log("SHORT")
                    self.order = self.sell()
        else:
            # can only close or hold
            self.log("CLOSING")
            self.order = self.close()
        

#         if pred_diff > 0 and current_prediction_denorm > share_price:
#             if not self.position:
#                 self.log("BUY")
#                 self.order = self.buy()
                
#         elif pred_diff < 0 and current_prediction_denorm < share_price:
#             if not self.position:
#                 self.log("SHORT")
#                 self.order = self.sell()
                
#         elif self.position:
#             self.log("CLOSING")
#             self.order = self.close()


class PercentIncrease(backtrader.sizers.FixedSize):
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if isbuy:
            return cash // 5 // data.open[0] - 1
        else:
            return position.size
