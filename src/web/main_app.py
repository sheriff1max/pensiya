import streamlit as st
from apps import (
                    app_1, 
                    app_2
                  )

from utils import utils, st_utils
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Предсказание досрочного выхода на пенсию", layout='wide', page_icon='./data/page_icon.jpg')
st.sidebar.image('./data/sidebar_icon.jpg')


def main():
    st.sidebar.header('Навигация')
    select_pages = st.sidebar.radio(
        label='Выберите странцу', 
        options = [
            "Загрузка данных и прогноз", 
            'Интерпритация и виузализация'
        ])
    pages = {
        "Загрузка данных и прогноз": app_1, 
        'Интерпритация и виузализация': app_2
    }
    pages[select_pages].page()
    
main()