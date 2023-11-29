import streamlit as st
import pandas as pd
import datetime
#from sklearn import datasets
import altair as alt
import xmlrpc.client as client

server = client.ServerProxy("http://localhost:8012/RPC2")

st.write("""
# Аналитика работы веб-сервиса
""")
st.sidebar.title("Фильтры")

st.sidebar.header('Дата', divider=True)
start_date = datetime.date.today() - datetime.timedelta(days=1)
start_date = st.sidebar.date_input(label="Начальная", value=start_date)
tmp = start_date + datetime.timedelta(days=1)
end_date = st.sidebar.date_input(label="Конечная", min_value=tmp, value=tmp)

st.sidebar.header('Фильтры')
data_length = st.sidebar.slider('Глубина анализа, день', 1, 30, 3)
interval_width = st.sidebar.slider('Интервал анализа, час', 1, 24, 4)
proc_type = st.sidebar.text_input("Тип операции")
data = {'data_length': data_length,
        'interval_width': interval_width,
        'proc_type': proc_type}
features = pd.DataFrame(data, index=[0])

with st.spinner('Загрузка...'):
    proc_type = [] if proc_type == "" else [proc_type]
    data = pd.read_json(server.slice_log(proc_type, start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S"), 0.0, 30000.0))

    chart = alt.Chart(data).mark_bar().encode(
        x='action_name',
        y='count()',
    ).interactive()

    chart2 = alt.Chart(data).mark_bar().encode(
        x=alt.X('date:T', title='Дата', bin=alt.Bin(maxbins=24/interval_width, ), axis=alt.Axis(format='%Y-%m-%d %H:%M:%S')),
        y='count()',
    ).interactive()

    tab1, tab2 = st.tabs(["Количество операций по типу", "asdas"])
    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with tab1:
        st.altair_chart(chart2, theme="streamlit", use_container_width=True)

    st.subheader('Все данные лог-файлов')
    st.write()

    st.subheader('Отобранные данные лог-файлов')
    st.write([])

st.success('Done!')