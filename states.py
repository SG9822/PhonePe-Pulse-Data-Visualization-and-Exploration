import pandas as pd
from fuzzywuzzy import process
import geopandas as gpd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote
import sqlite3

user = 'root'
password = quote('your MySQL Password')
host = '127.0.0.1'
port = 3306
database = 'Phonepe'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')


def geodata():
    file_path = './INDIA_DISTRICTS.geojson'
    gdf = gpd.read_file(file_path)
    gdf_dist = gdf['dtname'].unique()
    return [gdf, gdf_dist]


gdf_file = geodata()

states_dict = {
    'Andhra Pradesh': ['andhra-pradesh', 15.9129, 79.7400],
    'Arunachal Pradesh': ['arunachal-pradesh', 28.2180, 94.7278],
    'Assam': ['assam', 26.2006, 92.9376],
    'Bihar': ['bihar', 25.0961, 85.3131],
    'Chhattisgarh': ['chhattisgarh', 21.2787, 81.8661],
    'Goa': ['goa', 15.2993, 74.1240],
    'Gujarat': ['gujarat', 22.2587, 71.1924],
    'Haryana': ['haryana', 29.0588, 76.0856],
    'Himachal Pradesh': ['himachal-pradesh', 31.1048, 77.1734],
    'Jharkhand': ['jharkhand', 23.6102, 85.2799],
    'Karnataka': ['karnataka', 15.3173, 75.7139],
    'Kerala': ['kerala', 10.8505, 76.2711],
    'Madhya Pradesh': ['madhya-pradesh', 22.9734, 78.6569],
    'Maharashtra': ['maharashtra', 19.7515, 75.7139],
    'Manipur': ['manipur', 24.6637, 93.9063],
    'Meghalaya': ['meghalaya', 25.4670, 91.3662],
    'Mizoram': ['mizoram', 23.1645, 92.9376],
    'Nagaland': ['nagaland', 26.1584, 94.5624],
    'Odisha': ['odisha', 20.9517, 85.0985],
    'Punjab': ['punjab', 31.1471, 75.3412],
    'Rajasthan': ['rajasthan', 27.0238, 74.2179],
    'Sikkim': ['sikkim', 27.5330, 88.5122],
    'Tamil Nadu': ['tamil-nadu', 11.1271, 78.6569],
    'Telangana': ['telangana', 18.1124, 79.0193],
    'Uttarakhand': ['uttarakhand', 30.0668, 79.0193],
    'Uttar Pradesh': ['uttar-pradesh', 26.8467, 80.9462],
    'Tripura': ['tripura', 23.9408, 91.9882],
    'West Bengal': ['west-bengal', 22.9868, 87.8550],
    'Andaman & Nicobar': ['andaman-&-nicobar', 11.7401, 92.6586],
    'Chandigarh': ['chandigarh', 30.7333, 76.7794],
    'Dadra And Nagar Haveli And Daman And Diu': ['dadra-and-nagar-haveli-and-daman-and-diu', 20.1809, 73.0169],
    'Lakshadweep': ['lakshadweep', 10.5667, 72.6417],
    'Delhi': ['delhi', 28.6139, 77.2090],
    'Puducherry': ['puducherry', 11.9416, 79.8083],
    'Ladakh': ['ladakh', 34.1526, 77.5770],
    'Jammu & Kashmir': ['jammu-&-kashmir', 33.7782, 76.5762]
}

states_list = [
    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
    'Dadra And Nagar Haveli And Daman And Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
    'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
    'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]


def stateData():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        states = st.selectbox('select state', states_list, index=states_list.index('Tamil Nadu'))
    with col2:
        selected = st.selectbox('select tables', ['Transactions', 'Users'])
    with col3:
        years = st.selectbox('select what year', [2018, 2019, 2020, 2021, 2022, 2023])
    with col4:
        quarters = st.selectbox('select quarters', [1, 2, 3, 4])

    st.divider()

    if quarters == 4 and years == 2023:
        st.warning("Still 4th Quarter of the year 2023 is not updated")
    else:

        q1 = f"select distinct state, year, Quater, sum(transacion_count) transaction_count, sum(transacion_amount) transaction_amount from map_transaction where state= '{states_dict[states][0]}' and Quater = {quarters} and year = {years} group by state"
        q2 = f"select state, year, quater, sum(registered_user) reg_user, sum(app_opens) app_open from map_users where state = '{states_dict[states][0]}' and Quater = {quarters} and year = {years} group by state"

        q1_df = pd.read_sql_query(q1, engine)
        q2_df = pd.read_sql_query(q2, engine)

        tab1, tab2 = st.columns(2)

        with tab1:
            st.write(f'## :blue[Transactions of Year {years} Quarter {quarters}]')
            st.subheader("All Transactions")
            st.write(f"### :blue[{q1_df['transaction_count'].values[0]:,.0f}]")
            st.subheader("Transactions Amount")
            st.write(f"### :blue[₹{q1_df['transaction_amount'].values[0]:,.0f}]")
        with tab2:
            sub1, sub2 = st.columns([1, 4])
            with sub1:
                st.markdown(
                    """
                    <style>
                        .vertical-line {
                            border-left: 2px solid #CCCCCC; 
                            height: 40vh; 
                            margin: 0 5px; 
                        }
                    </style>
                    <div class="vertical-line"></div>
                    """,
                    unsafe_allow_html=True
                )
            with sub2:
                st.write(f'## :blue[Users of Year {years} Quarter {quarters}]')
                st.subheader("Registered Users")
                st.write(f"### :blue[{q2_df['reg_user'].values[0]:,.0f}]")
                st.subheader("App Opens")
                if q2_df['app_open'].values[0] == 0:
                    st.write(f"### :blue[Unavailable]")
                else:
                    st.write(f"### :blue[{q2_df['app_open'].values[0]:,.0f}]")


        st.divider()

        if selected == 'Transactions' and states and years and quarters:
            print('Transaction')
            phonepe_df = pd.read_sql_query(
                f'select state, District_Name, year, quater, sum(transacion_count) `Transaction Count`, sum(transacion_amount) `Transaction Amount` from map_transaction where state="{states_dict[states][0]}" and quater = {quarters} and year = {years} group by 1, 2',
                engine)
            print('SQL1')

            column = list(phonepe_df.columns)

            mapping = {}
            for phonepe_district_name in phonepe_df['District_Name'].unique():
                matched_geo_district_name, _ = process.extractOne(phonepe_district_name, gdf_file[1])
                mapping[phonepe_district_name] = matched_geo_district_name
            print('mapping1')

            phonepe_df['District_Name'] = phonepe_df['District_Name'].map(mapping)

            ph_geo = phonepe_df.merge(gdf_file[0][['geometry', 'dtname', 'dtcode11']], left_on=['District_Name'],
                                      right_on=['dtname'], how='left')
            print('merged1')
            ph_geo_gdf = gpd.GeoDataFrame(ph_geo, geometry='geometry')
            ph_geo_gdf['District_Name'] = ph_geo_gdf['District_Name'].str.title()

            st.write(f'## :blue[{states} Map for {years} Quarter {quarters}]')

            fig = px.choropleth_mapbox(
                ph_geo_gdf,
                geojson=ph_geo_gdf.geometry,
                locations=ph_geo_gdf.index,
                color=column[4],
                color_continuous_scale=px.colors.diverging.RdYlGn,
                range_color=(0, ph_geo_gdf[column[4]].max()),
                mapbox_style="carto-positron",
                zoom=5.75,
                center={"lat": states_dict[states][1], "lon": states_dict[states][2]},
                opacity=0.5,
                hover_name='District_Name',

            )

            fig.update_traces(
                hovertemplate=("<b>%{hovertext}</b><br><br>"
                               f"<b>Transaction Count</b><br>%{{z:,.0f}}<br><br><b>Transaction Amount</b><br>₹%{{customdata:,.0f}}"),
                hovertext=ph_geo_gdf['District_Name'].str.title(),
                customdata=ph_geo_gdf['Transaction Amount'],
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                title=f'{states} Map with Transaction Counts for {years} Quarter {quarters}',
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
                height=600, width=1000,
                hoverlabel_font_color='Purple',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Poppins",
                    bordercolor='Purple',
                )
            )
            print('Final1')
            # fig.show()
            st.plotly_chart(fig, use_container_width=True)

        elif selected == 'Users' and states and years and quarters:
            print('user')
            phonepe_df = pd.read_sql_query(
                f'select state, District_Name, year, quater, sum(registered_user) `Registration Counts`, sum(app_opens) `App Open` from map_users where state="{states_dict[states][0]}" and quater = {quarters} and year = {years} group by 1, 2',
                engine)
            print('SQL2')
            mapping = {}
            for phonepe_district_name in phonepe_df['District_Name'].unique():
                matched_geo_district_name, _ = process.extractOne(phonepe_district_name, gdf_file[1])
                mapping[phonepe_district_name] = matched_geo_district_name
            print('mapping2')
            phonepe_df['District_Name'] = phonepe_df['District_Name'].map(mapping)

            ph_geo = phonepe_df.merge(gdf_file[0][['geometry', 'dtname', 'dtcode11']], left_on=['District_Name'],
                                      right_on=['dtname'], how='left')
            print('merged2')
            ph_geo_gdf = gpd.GeoDataFrame(ph_geo, geometry='geometry')
            ph_geo_gdf['District_Name'] = ph_geo_gdf['District_Name'].str.title()

            st.write(f'## :blue[{states} Map for {years} Quarter {quarters}]')

            fig = px.choropleth_mapbox(
                ph_geo_gdf,
                geojson=ph_geo_gdf.geometry,
                locations=ph_geo_gdf.index,
                color='Registration Counts',
                color_continuous_scale='edge',
                range_color=(0, ph_geo_gdf['Registration Counts'].max()),
                mapbox_style="carto-positron",
                zoom=5.75,
                center={"lat": states_dict[states][1], "lon": states_dict[states][2]},
                opacity=0.5,
                # labels={'reg': 'Registration Counts'},
                hover_name='District_Name',
            )

            fig.update_traces(
                hovertemplate="<b>%{hovertext}</b><br><br><b>Registered Users</b><br>%{z:,.0f}<br><br><b>App Opens</b><br>%{customdata:,.0f}",
                hovertext=ph_geo_gdf['District_Name'].str.title(),
                customdata=ph_geo_gdf['App Open']
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                title=f'{states} Map with Users Counts for {years} Quarter {quarters}',
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
                height=600, width=1000,
                hoverlabel_font_color='Purple',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Poppins",
                    bordercolor='Purple',
                )
            )
            print('Final2')
            st.plotly_chart(fig, use_container_width=True)
