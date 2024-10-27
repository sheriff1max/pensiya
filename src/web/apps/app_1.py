import streamlit as st
import pandas as pd
from utils import st_utils
from datetime import datetime
import time
import plotly.express as px

@st.cache_data(ttl='1d')
def get_data_trans():
    df_trans = pd.read_parquet('./data/agg_transactions.parquet')
    return df_trans


def page():
    with st.sidebar:
        st.subheader('Введите данные для прогноза')
        file_download = st.toggle('Использовать данные в формате csv', value=True)
        
        if file_download:
            data = st_utils.get_data_csv()
        else:
            st.text('Введите данные акканта')
            accnt = st.text_input("Введите account_id")
            gender = st.radio("Выберите пол", ['Мужской', 'Женский'])
            bd_client = st.date_input('Введите дату рождения', value=datetime.today())
            
    st.header('Предсказание клиентов выходящих на досрочное получение пенсионных выплат')
    st_utils.get_annotation()
    button = st.button('Расчитать')
    
    if button & file_download:
        with st.spinner('Подождите данные обрабатываются'):
            df_trans = get_data_trans()
            data_total = data.merge(df_trans, how='left', on='accnt_id')
            # Заголовок приложения
            st.subheader('Анализ данных клиентов (EDA)')
            col1, col2 = st.columns(2)
            with col1:
                # График распределения по полу
                st.subheader('Распределение клиентов по полу')
                gender_counts = data['gndr'].value_counts()
                fig_gender = px.bar(gender_counts, x=gender_counts.index, y=gender_counts.values, labels={'x': 'Пол', 'y': 'Количество'})
                st.plotly_chart(fig_gender)
                
            with col2:
                # График распределения по годам рождения
                st.subheader('Распределение клиентов по годам рождения')
                birth_year_counts = data['brth_yr'].value_counts().sort_index()
                fig_birth_year = px.line(birth_year_counts, x=birth_year_counts.index, y=birth_year_counts.values, labels={'x': 'Год рождения', 'y': 'Количество'})
                st.plotly_chart(fig_birth_year)

            
            st.subheader('Результат прогноза модели')
            
            csv = data.to_csv(index=False)
            st.download_button(
                label="Скачать CSV",
                data=csv,
                file_name='client_data.csv',
                mime='text/csv',
            )
