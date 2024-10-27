import streamlit as st 
import pandas as pd
from utils import utils

def get_example_file():
    df = pd.DataFrame({
        'slctn_nmbr': [None], 'clnt_id': [None], 'accnt_id': [None], 'gndr': [None], 'brth_yr': [None], 'prsnt_age': [None],
       'accnt_bgn_date': [None], 'cprtn_prd_d': [None], 'erly_pnsn_flg': [None], 'accnt_status': [None],
       'pnsn_age': [None], 'prvs_npf': [None], 'brth_plc': [None], 'addrss_type': [None], 'rgn': [None], 'dstrct': [None],
       'city': [None], 'sttlmnt': [None], 'pstl_code': [None], 'okato': [None], 'phn': [None], 'email': [None], 'lk': [None],
       'assgn_npo': [None], 'assgn_ops': [None]})
    df = df.T.reset_index()
    with st.expander('Пример файла'):
        st.markdown(df.style.hide(axis='index').to_html(),
                    unsafe_allow_html=True)
    
    
def get_data_csv():
    uploaded_file = st.file_uploader(
        "Загрузите файл для предсказания в формате csv", 
        type=['.csv'])
    get_example_file() 
    if uploaded_file:
        df_client = pd.read_csv(uploaded_file)
        return df_client


def get_annotation():
     with st.expander('Краткое описание функциона сервиса', expanded=False):
        st.markdown('''
        Данный сервис предназначается для прогноза наиболее склонных к уходу на досрочный период клиентам Пенсионного Страхования.
        Пользователю сервиса необходимо выгрузить файл
        , или указать в ручную параметры клиента в левем меню. Данные о транзакциях автоматически поддтягиваются из базы данных.

        Далее необходимо нажать на кнопку Расчитать для старта процесса прогноза.

        Для прогноза используется модель машинного обучения линейная классификация с метрикой  99.94
        Визализацию метрик, а также интерпритацию признаков можно посмотреть во вкладке - 
        ''')


def get_download_button(data):
    
    data_excel = utils.df2excel([data], ['Прогноз'])
    st.download_button(
        label = 'Скачать прогноз', 
        data = data_excel, 
        file_name = 'file_forecast.xlsx', 
    )
    