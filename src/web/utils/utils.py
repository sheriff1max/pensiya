import streamlit as st
import pandas as pd 
import numpy as np
from io import BytesIO
import joblib
from sklearn.pipeline import Pipeline
import shap
import matplotlib.pyplot as plt

def data_pre_calc(df:pd.DataFrame):
    return df


def main_calc(df:pd.DataFrame):
    pass


def df2excel(df, sheet_names):
    bi = BytesIO()
    writer = pd.ExcelFile(bi, engine='openpyxl')
    for i, df in enumerate(sheet_names):
        df.to_excel(writer, sheet_name = sheet_names[i])
    writer.close()
    pr_data = bi.getvalue()
    return pr_data


def plot_shap_values(shap_explanation, type_plot):
    '''
    Визуализация shap значения для модели
    '''
    if type_plot == 'all':
        fig, ax = plt.subplots()
        shap.plots.beeswarm(shap_explanation)
    else:
        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_explanation[0])
    
    st.pyplot(fig)
    

def shap_calc(accnt_id, all_cls, df, plot=False):
    '''
    Расчет значения shap для лучшей интерпритации 
    '''
    # Выгружаем модель под конкретную выборку
    acc_sample = df[df.accnt_id == accnt_id]
    df = df[cols]
    print("ЭТО САМПЛ",  acc_sample)
    selection = acc_sample.slctn_nmbr
    try:
        selection = acc_sample.slctn_nmbr[0]
        print(selection)
        cls = all_cls[int(selection)]
    except:
        selection = acc_sample.slctn_nmbr
        cls = all_cls[0]
    ru_col = translate_features(df.columns.to_list())
    
    num_value = acc_sample.index
    df_transformed = cls.named_steps['ohe_scal'].transform(df)
    explainer = shap.LinearExplainer(cls.named_steps['cls'],  df_transformed, feature_perturbation="correlation_dependent")
    shap_values = explainer.shap_values(df_transformed)
    if accnt_id:
        shap_explanation = shap.Explanation(values=shap_values[num_value],  # shap_values для первого наблюдения
                                        base_values=explainer.expected_value,
                                        data=df_transformed[num_value],  # данные для первого наблюдения
                                        feature_names=ru_col)
    else: 
        shap_explanation = shap.Explanation(values=shap_values,  # shap_values для первого наблюдения
                                        base_values=explainer.expected_value,
                                        data=df_transformed,  # данные для первого наблюдения
                                        feature_names=ru_col)
    return shap_explanation
        



def translate_features(features):
    """
    Функция для перевода списка признаков на русский язык с заменой _ на пробелы.
    
    :param features: Список признаков на английском языке.
    :return: Список признаков на русском языке с пробелами вместо _.
    """
    translated_features = [feature_translations.get(feature, feature) for feature in features]
    return translated_features


# Словарь с переводами признаков
feature_translations = {
    'prvs_npf': 'предыдущий НПФ',
    'north_region': 'северный регион',
    'brth_yr': 'год рождения',
    'sum__sum_values': 'сумма сумма значений',
    'sum__median': 'сумма медиана',
    'sum__mean': 'сумма среднее',
    'sum__length': 'сумма длина',
    'sum__standard_deviation': 'сумма стандартное отклонение',
    'sum__variance': 'сумма дисперсия',
    'sum__root_mean_square': 'сумма среднеквадратичное значение',
    'sum__maximum': 'сумма максимум',
    'sum__absolute_maximum': 'сумма абсолютный максимум',
    'sum__minimum': 'сумма минимум',
    'infl__sum_values': 'инфляция сумма значений',
    'infl__median': 'инфляция медиана',
    'infl__mean': 'инфляция среднее',
    'infl__length': 'инфляция длина',
    'infl__standard_deviation': 'инфляция стандартное отклонение',
    'infl__variance': 'инфляция дисперсия',
    'infl__root_mean_square': 'инфляция среднеквадратичное значение',
    'infl__maximum': 'инфляция максимум',
    'infl__absolute_maximum': 'инфляция абсолютный максимум',
    'infl__minimum': 'инфляция минимум',
    'gpd__sum_values': 'ВВП сумма значений',
    'gpd__median': 'ВВП медиана',
    'gpd__mean': 'ВВП среднее',
    'gpd__length': 'ВВП длина',
    'gpd__standard_deviation': 'ВВП стандартное отклонение',
    'gpd__variance': 'ВВП дисперсия',
    'gpd__root_mean_square': 'ВВП среднеквадратичное значение',
    'gpd__maximum': 'ВВП максимум',
    'gpd__absolute_maximum': 'ВВП абсолютный максимум',
    'gpd__minimum': 'ВВП минимум',
    'without_job__sum_values': 'без работы сумма значений',
    'without_job__median': 'без работы медиана',
    'without_job__mean': 'без работы среднее',
    'without_job__length': 'без работы длина',
    'without_job__standard_deviation': 'без работы стандартное отклонение',
    'without_job__variance': 'без работы дисперсия',
    'without_job__root_mean_square': 'без работы среднеквадратичное значение',
    'without_job__maximum': 'без работы максимум',
    'without_job__absolute_maximum': 'без работы абсолютный максимум',
    'without_job__minimum': 'без работы минимум',
    'population_growth__sum_values': 'рост населения сумма значений',
    'population_growth__median': 'рост населения медиана',
    'population_growth__mean': 'рост населения среднее',
    'population_growth__length': 'рост населения длина',
    'population_growth__standard_deviation': 'рост населения стандартное отклонение',
    'population_growth__variance': 'рост населения дисперсия',
    'population_growth__root_mean_square': 'рост населения среднеквадратичное значение',
    'population_growth__maximum': 'рост населения максимум',
    'population_growth__absolute_maximum': 'рост населения абсолютный максимум',
    'population_growth__minimum': 'рост населения минимум'
}
cols = ['prvs_npf', 'north_region', 'brth_yr', 'sum__sum_values', 'sum__median',
       'sum__mean', 'sum__length', 'sum__standard_deviation', 'sum__variance',
       'sum__root_mean_square', 'sum__maximum', 'sum__absolute_maximum',
       'sum__minimum', 'infl__sum_values', 'infl__median', 'infl__mean',
       'infl__length', 'infl__standard_deviation', 'infl__variance',
       'infl__root_mean_square', 'infl__maximum', 'infl__absolute_maximum',
       'infl__minimum', 'gpd__sum_values', 'gpd__median', 'gpd__mean',
       'gpd__length', 'gpd__standard_deviation', 'gpd__variance',
       'gpd__root_mean_square', 'gpd__maximum', 'gpd__absolute_maximum',
       'gpd__minimum', 'without_job__sum_values', 'without_job__median',
       'without_job__mean', 'without_job__length',
       'without_job__standard_deviation', 'without_job__variance',
       'without_job__root_mean_square', 'without_job__maximum',
       'without_job__absolute_maximum', 'without_job__minimum',
       'population_growth__sum_values', 'population_growth__median',
       'population_growth__mean', 'population_growth__length',
       'population_growth__standard_deviation', 'population_growth__variance',
       'population_growth__root_mean_square', 'population_growth__maximum',
       'population_growth__absolute_maximum', 'population_growth__minimum']
