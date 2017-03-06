import pickle
from data_loader import DataLoader
from data_set import UserPayInfoBase
from utils.multi_processor import MultiProcessor

loader_data = DataLoader.load_data()
shop_info = loader_data['shop_info']
user_pay = loader_data['user_pay']
shop_ids = range(1, 2001)


def generator(shop_id):
    shop_info_data = shop_info.iloc[shop_id - 1].to_dict()
    user_pay_data = user_pay[user_pay.shop_id == shop_id]
    user_pay_data = user_pay_data.sort_values(by='time_stamp')
    user_pay_data['date'] = user_pay_data['time_stamp'].apply(lambda x: x[:10])
    ordinary_dates = list(set(user_pay_data['date']))
    ordinary_dates.sort()
    user_pay_info = UserPayInfoBase(shop_id, shop_info_data, ordinary_dates)
    user_pay_info.set_flow(user_pay_data, ordinary_dates)
    return (shop_id, user_pay_info)


processor = MultiProcessor(generator, shop_ids)
result = processor.pool_map_async_result(processors=32)
result = dict(result)
pickle.dump(result, open('user_pay_info', 'w+'))
