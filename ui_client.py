import streamlit as st
import pandas as pd
import datetime
#from sklearn import datasets
import altair as alt
import xmlrpc.client as client
import plotly.express as px

server = client.ServerProxy("http://localhost:8012/RPC2")

st.write("""
# Аналитика работы веб-сервиса
""")
st.sidebar.title("Фильтры")

st.sidebar.header('Дата', divider=True)
start_date = datetime.date.today()# - datetime.timedelta(days=1)
start_date = st.sidebar.date_input(label="С", value=start_date)
tmp = start_date + datetime.timedelta(days=1)
end_date = st.sidebar.date_input(label="До", min_value=tmp, value=tmp)

st.sidebar.header('Фильтры')
interval_width = st.sidebar.slider('Интервал анализа, час', 1, 24, 4)
proc_type = st.sidebar.text_input("Тип операции")

with st.spinner('Загрузка...'):
    proc_type = [] if proc_type == "" else [proc_type]
    print(proc_type)
    data = pd.read_json(server.slice_log(proc_type, start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S"), 0.0, 30000.0))

    fig1 = px.histogram(data, x='action_name', width=800, height=400)
    fig1.update_layout(
        title_text="Гистограмма",
        xaxis_title_text="Тип операции",
        yaxis_title_text="Количество",
        bargap=0.02,  # Промежуток между столбцами
        bargroupgap=0.1,  # Промежуток между группами столбцов
    )

    fig2 = px.histogram(data, x='date', nbins=int(24/interval_width), width=800, height=400)
    fig2.update_layout(
        title_text="Гистограмма",
        xaxis_title_text="Даты",
        yaxis_title_text="Количество",
        bargap=0.02,  # Промежуток между столбцами
        bargroupgap=0.1,  # Промежуток между группами столбцов
    )

    # Создаем круговую диаграмму с использованием plotly
    fig3 = px.pie(data, names='action_name', title='Соотношение количества зопросов по типу')
    fig4 = px.pie(data, names='action_name', values="duration", title='Соотношение времени запросов по типу')

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)

    st.subheader('Все данные лог-файлов')
    st.write(pd.read_json(server.slice_log()))

    st.subheader('Отобранные данные лог-файлов')
    st.write(data)

st.success('Done!')