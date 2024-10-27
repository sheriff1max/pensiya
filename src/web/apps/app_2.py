import streamlit as st
import pandas as pd
from utils import st_utils, utils
from datetime import datetime
import time
import plotly.express as px
from sklearn.pipeline import Pipeline
import joblib

# @st.chache_data(ttl='1d')
# def get_data_trans():
#     df_trans = pd.read_parquet('./data/df_trans_precalc.parquet')

@st.cache_data(ttl='1d')
def read_piplines(path:str, num_models:int):
    """
    Функция считывания обученного пайплана моделей 
    """
    all_cls = []
    for i in range(num_models):
        loaded_transformer = joblib.load(f'{path}/ohe_scal_{i}.pkl')
        loaded_logreg = joblib.load(f'{path}/cls_{i}.pkl')
        pipe = Pipeline(steps=[
                ('ohe_scal', loaded_transformer),
                ('cls', loaded_logreg)
            ])
        all_cls.append(pipe)
    return all_cls

def page():
    
    with st.sidebar:
        st.subheader('Интерпритация обучения модели')
        st.text('Введите данные акканта для интерпритации')
        accnt = st.text_input("Введите account_id")
        button = st.button('Визуализировать')

    st.header('Подробная интерпритация результата предсказания и признаков модели')
    if button:
        with st.spinner('Подождите данные обрабатываются'):
            all_cls = read_piplines('data/pipelines', 4)
            df_client = pd.read_parquet('data/df_client.parquet')
            print(df_client.accnt_id.sample(1))
            ex_1 = utils.shap_calc(None, all_cls, df_client)
            ex_2 = utils.shap_calc(accnt, all_cls, df_client)

            utils.plot_shap_values(ex_1, 'all')
            utils.plot_shap_values(ex_2, 'acct')
        