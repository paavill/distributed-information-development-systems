import streamlit as st
import pandas as pd
#from sklearn import datasets


st.write("""
# Аналитика работы веб-сервиса
""")

st.sidebar.header('Ввод данных')

def user_input_features():
    data_length = st.sidebar.slider('Глубина анализа, день', 1, 30, 3)
    interval_width = st.sidebar.slider('Интервал анализа, час', 1, 24, 4)
    proc_type = st.sidebar.text_input("Тип операции")
    data = {'data_length': data_length,
            'interval_width': interval_width,
            'proc_type': proc_type}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.subheader('Введенные данные')
st.write(df)

st.subheader('Все данные лог-файлов')
st.write([])

st.subheader('Отобранные данные лог-файлов')
st.write([])