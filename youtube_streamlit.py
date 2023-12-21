import streamlit as st
import pandas as pd
import json
import requests
from sqlalchemy import create_engine
from urllib.parse import quote
import pymysql
import plotly.express as px

# st.set_page_config(layout="wide")

myconnection = pymysql.connect(host='127.0.0.1', user='root', passwd='your MySQL Password', database='Phonepe')
cur = myconnection.cursor()
cur.execute("use Phonepe")

user = 'root'
password = quote('your MySQL Password')
host = '127.0.0.1'
port = 3306
database = 'Phonepe'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# URL to the GeoJSON file
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

# Make a request to the URL and get the content
response = requests.get(url)

geojson_data = ''
if response.status_code == 200:
    geojson_data = json.loads(response.content)

    for i in range(0, 36):
        geojson_data['features'][i]['properties']['id'] = i
        features = geojson_data['features'][i]['properties']['ST_NM'].lower().replace(' ', '-')
        geojson_data['features'][i]['properties']['ST_NM'] = features

else:
    print("Failed to fetch GeoJSON data")

def countryData():
    col1, col2, col3 = st.columns(3)

    with col1:
        select = st.selectbox('Select Table:', ['Transaction', 'User'])

    with col2:
        year = st.selectbox('Select Year:', [2018, 2019, 2020, 2021, 2022, 2023])

    with col3:
        if year == 2023:
            quarter = st.selectbox('Select Quarter:', [1, 2, 3])
        else:
            quarter = st.selectbox('Select Quarter:', [1, 2, 3, 4])

    st.divider()

    if select == 'Transaction' and year and quarter:
        query = f"select sum(Transacion_count) Total, sum(Transacion_amount) total_amt from aggregated_transaction where quater = {quarter} and year = {year}"
        q = pd.read_sql_query(query, engine)
        tab1, tab2 = st.columns(2)
        with tab1:
            st.write(f'## :blue[Transactions of Year {year} Quarter {quarter}]')
            st.subheader("All Transactions")
            st.write(f"### :blue[{q['Total'].values[0]:,.0f}]")
            st.subheader("Transactions Amount")
            st.write(f"### :blue[₹{q['total_amt'].values[0]:,.0f}]")
        with tab2:
            sub1, sub2 = st.columns([1, 4])
            with sub1:
                st.markdown(
                    """
                    <style>
                        .vertical-line {
                            border-left: 2px solid #CCCCCC; 
                            height: 45vh; 
                            margin: 0 5px; 
                        }
                    </style>
                    <div class="vertical-line"></div>
                    """,
                    unsafe_allow_html=True
                )
            with sub2:
                cat_query = f"select Transacion_type `Transaction Type`, sum(Transacion_count) `Transaction Count`, sum(Transacion_amount) `Transaction Amount` from aggregated_transaction where quater = {quarter} and year = {year} group by Transacion_type"
                cat_df = pd.read_sql_query(cat_query, engine)
                cat_df['Transaction Count'] = cat_df['Transaction Count'].apply(lambda x: '{:,.0f}'.format(x))
                cat_df['Transaction Amount'] = cat_df['Transaction Amount'].apply(lambda x: '₹ {:,.0f}'.format(x))
                markdown_table = cat_df.to_markdown(index=False)

                st.write(f'## :blue[Categories of Year {year} Quarter {quarter}]')
                st.markdown(markdown_table, unsafe_allow_html=True)
        st.divider()

        st.write(f"## :blue[Map for year {year}, Q{quarter}]")

        radio = st.radio("Choose Option:", ["Transaction Count", "Transaction Amount"], horizontal=True)

        df = pd.DataFrame()

        if radio == "Transaction Count":
            df = pd.read_sql_query(
                f'select state, year, quater, sum(transacion_count) `Transaction Count` from aggregated_transaction where '
                f'Quater = {quarter} and year = {year} group by state, year', engine)

        elif radio == "Transaction Amount":
            df = pd.read_sql_query(
                f'select state, year, quater, sum(transacion_amount) `Transaction Amount` from aggregated_transaction where '
                f'Quater = {quarter} and year = {year} group by state, year', engine)

        column = list(df.columns)

        try:
            fig = px.choropleth(
                df,
                geojson=geojson_data,
                featureidkey='properties.ST_NM',
                locations='state',
                color=column[3],
                hover_name='state',
                color_continuous_scale='fall',

            )

            hover_text_template = ()
            if radio == "Transaction Count":
                hover_text_template = (
                    "<b>%{hovertext}</b><br><br>"
                    f"<b>{column[3]}</b><br>%{{z:,.0f}}"
                )
            elif radio == "Transaction Amount":
                hover_text_template = (
                    "<b>%{hovertext}</b><br><br>"
                    f"<b>{column[3]}</b><br>₹%{{z:,.0f}}")

            fig.update_traces(
                hovertemplate=hover_text_template,
                hovertext=df['state'].str.title(),
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                title_text=f'Map with {column[3]} year {year}, Q{quarter}',
                height=600,
                width=1200,
                margin=dict(l=0, r=0, b=0, t=0, pad=0, autoexpand=True),
                title=dict(y=1, x=0.3),
                hoverlabel_font_color='Purple',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Poppins",
                    bordercolor='Purple',

                )
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.warning("Please select any one option")

    elif select == 'User' and year and quarter:
        query = f"select sum(Registered_User) reg_user, sum(app_opens) app_opens from aggregated_user where quater = {quarter} and year = {year}"
        q = pd.read_sql_query(query, engine)


        st.write(f'## :blue[Users]')
        user_col1, user_col2 = st.columns(2)
        with user_col1:
            st.subheader(f"Registered PhonePe users Q{quarter} {year}")
            st.write(f"### :blue[{q['reg_user'].values[0]:,.0f}]")
        with user_col2:
            st.subheader("App Open")
            if q['app_opens'].values[0] == 0:
                st.write(f"### :blue[Unavailable]")
            else:
                st.write(f"### :blue[{q['app_opens'].values[0]:,.0f}]")
        st.divider()

        st.write(f"## :blue[Map for year {year}, Q{quarter}]")

        radio = st.radio("Choose Option:", ["Registered Users", "App Open"], horizontal=True)

        u_df = pd.DataFrame()

        if radio == "Registered Users":
            u_df = pd.read_sql_query(
                f'select state, year, quater, sum(registered_user) `Registered User` from aggregated_user where '
                f'Quater = {quarter} and year = {year} group by state, year', engine)

        elif radio == "App Open":
            u_df = pd.read_sql_query(f'select state, year, quater, sum(App_Opens) `App Open` from aggregated_user where '
                                   f'Quater = {quarter} and year = {year} group by state, year', engine)

        column = list(u_df.columns)

        try:
            fig = px.choropleth(
                u_df,
                geojson=geojson_data,
                featureidkey='properties.ST_NM',
                locations='state',
                color=column[3],
                hover_name='state',
                # hover_data=['open'],
                color_continuous_scale='brbg',
            )

            hover_text_template = (
                "<b>%{hovertext}</b><br><br>"
                f"<b>{column[3]}</b><br>%{{z:,.0f}}"
            )

            fig.update_traces(
                hovertemplate=hover_text_template,
                hovertext=u_df['state'].str.title(),
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                title_text=f'Map with {column[3]} Counts year {year}, Q{quarter}',
                height=600,
                width=1200,
                margin=dict(l=0, r=0, b=0, t=0, pad=0, autoexpand=True),
                title=dict(y=1, x=0.3),
                hoverlabel_font_color='Purple',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Poppins",
                    bordercolor='Purple',

                )
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.warning("Please select any one option")
