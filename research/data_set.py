import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data.data_loader import DataLoader


class UserPayInfoBase(object):

    def __init__(self, shop_id, shop_info_data, ordinary_dates):
        self.shop_id = shop_id
        self.ordinary_dates = ordinary_dates
        self.city_name = shop_info_data['city_name']
        self.location_id = shop_info_data['location_id']
        self.per_pay = shop_info_data['per_pay']
        self.score = shop_info_data['score']
        self.comment_cnt = shop_info_data['comment_cnt']
        self.shop_level = shop_info_data['shop_level']
        self.cate_1_name = shop_info_data['cate_1_name']
        self.cate_2_name = shop_info_data['cate_2_name']
        self.cate_3_name = shop_info_data['cate_3_name']
        self.merchant_flow = []
        self.customer_flow = []

    @property
    def merchant_flow_dict(self):
        if not hasattr(self, '_merchant_flow_dict'):
            self._merchant_flow_dict = dict(zip(self.ordinary_dates, self.merchant_flow))
        return self._merchant_flow_dict

    @property
    def customer_flow_dict(self):
        if not hasattr(self, 'customer_flow_dict'):
            self._customer_flow_dict = dict(zip(self.ordinary_dates, self.customer_flow))
        return self._customer_flow_dict

    def set_flow(self, data, dates):
        for date in dates:
            tmp_data = data[data.date == date]
            self.merchant_flow.append(len(tmp_data))
            self.customer_flow.append(len(set(tmp_data['user_id'])))

    def plot_flow(self, start=None, end=None, style='m'):
        """
        Args:
            start: str
            end: str
            style: 'm', 'c', 'mc'
        """
        plt.figure(figsize=(10, 6))
        start_index = self.ordinary_dates.index(start) if start else 0
        end_index = self.ordinary_dates.index(end) + 1 if end else len(self.merchant_flow) + 1
        x_axis = map(lambda x: pd.datetime.strptime(x, '%Y-%m-%d'),
                     self.ordinary_dates[start_index:end_index])
        if style == 'm':
            plt.plot(x_axis, self.merchant_flow[start_index:end_index], 'r', linewidth=1.5)
            plt.legend(['merchant_flow'])
        elif style == 'c':
            plt.plot(x_axis, self.customer_flow[start_index:end_index], 'b', linewidth=1.5)
            plt.legend(['customer_flow'])
        elif style == 'mc':
            plt.plot(x_axis, self.merchant_flow[start_index:end_index], 'r', linewidth=1.5)
            plt.plot(x_axis, self.customer_flow[start_index:end_index], 'b', linewidth=1.5)
            plt.legend(['merchant_flow', 'customer_flow'])
        else:
            raise ValueError('{} is an invalid input of "style"!'.format(style))
        plt.grid(axis=0)
        plt.title('Merchant flow of shop {}'.format(self.shop_id))
        plt.show()

    def get_flow(self, dates, style='m'):
        """
        Args:
            dates: list of str
            style: 'm', 'c'
        """
        if isinstance(dates, basestring):
            dates = dates.split(',')
        if style == 'm':
            temp_flow_dict = self.merchant_flow_dict
        elif style == 'c':
            temp_flow_dict = self.customer_flow_dict
        else:
            raise ValueError('{} is an invalid input of "style"!'.format(style))
        temp_flow = {date: temp_flow_dict[date] for date in dates}
        return temp_flow

    def get_attributes(self, attributes):
        invalid_attributes = set(attributes) - set(self.__dict__.keys())
        if invalid_attributes:
            raise ValueError('There exists invalid attributes: {}!'.format(list(invalid_attributes)))
        return map(lambda x: self.__dict__.get(x, None), attributes)


class EnsembleModelReporter(object):
    def __init__(self, ensemble_model):
        self.ensemble_model = ensemble_model

    def get_best_model(self, shop_id):
        best_model, best_loss = None, 1
        for models in self.ensemble_model.itervalues():
            info = models.get(shop_id, None)
            if not info:
                continue
            if info[1] < best_loss:
                best_model, best_loss = info
        return best_model

    def get_best_loss(self, shop_id):
        best_model, best_loss = None, 1
        for models in self.ensemble_model.itervalues():
            info = models.get(shop_id, None)
            if not info:
                continue
            if info[1] < best_loss:
                best_model, best_loss = info
        return best_loss

    def best_models(self):
        result = {}
        for shop_id in range(1, 2001):
            result[shop_id] = self.get_best_model(shop_id)
        return result

    def get_qualified_shops(self, threshold=0.07):
        qualified_shops = [shop_id for shop_id in range(1, 2001) if self.get_best_loss(shop_id) <= threshold]
        return qualified_shops

    def get_unqualified_shops(self, threshold=0.07):
        unqualified_shops = [shop_id for shop_id in range(1, 2001) if self.get_best_loss(shop_id) > threshold]
        return unqualified_shops

    def get_mean_loss(self, threshold=0.07):
        all_loss = [self.get_best_loss(shop_id) for shop_id in range(1, 2001) if
                    self.get_best_loss(shop_id) < threshold]
        return np.mean(all_loss)


if __name__ == '__main__':
    loader_data = DataLoader.load_data()
    shop_info = loader_data['shop_info']
    user_pay = loader_data['user_pay']
    user_view = loader_data['user_view']
    shop_ids = range(1, 2001)
    ordinary_dates = pd.date_range(start='2015-10-10', end='2016-10-31', freq='D').strftime('%Y-%m-%d')
    business_dates = pd.date_range(start='2015-10-10', end='2016-10-31', freq='B').strftime('%Y-%m-%d')
    result = {}
    for shop_id in shop_ids[:1]:
        shop_info_data = shop_info.iloc[shop_id - 1].to_dict()
        user_pay_data = user_pay[user_pay.shop_id == shop_id]
        user_pay_data = user_pay_data.sort_values(by='time_stamp')
        user_pay_data['date'] = user_pay_data['time_stamp'].apply(lambda x: x[:10])
        user_pay_info = UserPayInfoBase(shop_id, shop_info_data, ordinary_dates)
        user_pay_info.set_flow(user_pay_data, ordinary_dates)
        result[shop_id] = user_pay_info

