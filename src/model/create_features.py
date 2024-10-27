"""Создание признаков из датасетов."""

import pandas as pd
from tsfresh.feature_extraction import settings
from tsfresh import extract_features


def get_noth_region(data: pd.DataFrame) -> pd.DataFrame:
    """Создаём признак северного региона."""

    db = data.copy()

    db['north_region'] = 0
    db.loc[db.okato == 86000000000, 'north_region'] = 1
    db.loc[db.okato == 87000000000, 'north_region'] = 1
    db.loc[db.okato == 98000000000, 'north_region'] = 1
    db.loc[db.okato == 93000000000, 'north_region'] = 1
    db.loc[db.okato == 30000000000, 'north_region'] = 1
    db.loc[db.okato == 4000000000, 'north_region'] = 1
    db.loc[db.okato == 8000000000, 'north_region'] = 1
    db.loc[db.okato == 11000000000, 'north_region'] = 1
    db.loc[db.okato == 25000000000, 'north_region'] = 1
    db.loc[db.okato == 44000000000, 'north_region'] = 1
    db.loc[db.okato == 47000000000, 'north_region'] = 1
    db.loc[db.okato == 64000000000, 'north_region'] = 1
    db.loc[db.okato == 11100000000, 'north_region'] = 1
    db.loc[db.okato == 77000000000, 'north_region'] = 1
    db.loc[db.okato == 71140000000, 'north_region'] = 1
    db.loc[db.okato == 71100000000, 'north_region'] = 1

    db.north_region = db.north_region.astype('category')
    return db


def get_macro_feature(df_transactions: pd.DataFrame) -> pd.DataFrame:
    '''
    Добавляет макроэкономические данные по годам транзакций.
    infl: https://xn----ctbjnaatncev9av3a8f8b.xn--p1ai/%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B-%D0%B8%D0%BD%D1%84%D0%BB%D1%8F%D1%86%D0%B8%D0%B8
    GDP: https://gogov.ru/articles/vvp-rf
    Безработица: https://infotables.ru/statistika/79-ekonomicheskaya-statistika-rossii/1021-uroven-bezrabotitsy-v-rossii
    Естественный прирост: https://infotables.ru/statistika/31-rossijskaya-federatsiya/784-rozhdaemost-smertnost
    infl, GDP (трлн. руб.), безработица, естественный прирост
    '''

    df_transactions = df_transactions[['accnt_id', 'oprtn_date', 'sum']].copy()
    df_transactions['year'] = df_transactions.oprtn_date.apply(lambda x: x[:4])

    macro = {'1999': [36.56, 4.823, 10.7, -6,15, 65.2],#
         '2000': [20.2, 7.306, 10.6, -6.6, 65.3],#
         '2001': [18.085, 9.73625, 9.9, -6.325, 65.2],#
         '2002': [15.97, 12.1665, 9.2, -6.05, 65],#
         '2003': [13.855, 14.59675, 8.5, -5.775, 64.9],#
         '2004': [11.74, 17.027, 7.8, -5.5, 65.3],#
         '2005': [10.91, 21.61, 7.1, -5.9, 65.4],#
         '2006': [9, 26.917, 7.1, -4.8, 66.7],#
         '2007': [11.87, 33.248, 6, -3.3, 67.6],#
         '2008': [13.28, 41.277, 6.2, -2.5, 68],#
         '2009': [8.8, 38.807, 8.3, -1.8, 68.8],#
         '2010': [8.78, 46.309, 7.3, -1.7, 68.9],#
         '2011': [6.1, 60.114, 6.5, -0.9, 69.83],#
         '2012': [6.58, 68.103, 5.5, 0, 70.24],#
         '2013': [6.45, 72.986, 5.5, 0.2, 70.76],#
         '2014': [11.36, 79.03, 5.2, 0.2, 70.93],#
         '2015': [12.91, 83.087, 5.6, 0.3, 71.39],#
         '2016': [5.38, 86.043, 5.5, -0.01, 71.87],#
         '2017': [2.52, 91.843, 5.2, -0.9, 72.7],
         '2018': [4.27, 103.862, 4.8, -1.6, 72.91],
         '2019': [3.05, 109.608, 4.6, -2.2, 73.34],
         '2020': [4.91, 107.658, 5.8, -4.8, 71.54],
         '2021': [8.39, 135.774, 4.8, -7.1, 70.06],
         '2022': [11.92, 155.188, 3.9, -4, 72.73],
         '2023': [7.42, 172.148, 3.2, -3, 73.41],
         '2024': [7.42, 178.862, 3.1, -3, 73.6]}

    df_transactions['infl'] = df_transactions.year.apply(lambda x: macro[x][0])
    df_transactions['gpd'] = df_transactions.year.apply(lambda x: macro[x][1])
    df_transactions['without_job'] = df_transactions.year.apply(lambda x: macro[x][2])
    df_transactions['population_growth'] = df_transactions.year.apply(lambda x: macro[x][3])
    df_transactions = df_transactions.drop(columns=['year'])
    return df_transactions


def get_time_series_feature(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """Создание признаков из транзакций и макроэкономических
    параметров."""

    setup = settings.MinimalFCParameters()

    agg_transactions = extract_features(
        df_transactions.copy(),
        column_id='accnt_id',
        column_sort='oprtn_date',
        default_fc_parameters=setup,
    )
    agg_transactions = agg_transactions.reset_index(names='accnt_id')
    return agg_transactions


FILENAME_CLIENTS = ''
FILENAME_TRANSACTIONS = ''


if __name__ == '__main__':
    db_client = pd.read_csv(FILENAME_CLIENTS, encoding='cp1251', sep=';')
    db_check = pd.read_csv(FILENAME_TRANSACTIONS, encoding='cp1251', sep=';')

    db_client = get_noth_region(db_client)
    db_check = get_macro_feature(db_check)
    agg_transactions = get_time_series_feature(db_check)

    df_clients = db_client.copy()
    df_clients = pd.merge(df_clients, agg_transactions, how="inner", on="accnt_id")
