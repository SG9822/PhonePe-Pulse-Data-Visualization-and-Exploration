from sqlalchemy import create_engine
from urllib.parse import quote
import streamlit as st
import pymysql
from states import states_list, states_dict
import pandas as pd
import plotly.express as px

# st.set_page_config(layout='wide')

myconnection = pymysql.connect(host='127.0.0.1', user='root', passwd='MySQL@123', database='Phonepe')
cur = myconnection.cursor()
cur.execute("use Phonepe")

user = 'root'
password = quote('MySQL@123')
host = '127.0.0.1'
port = 3306
database = 'Phonepe'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

state_codes = [
    'AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DN', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'LD', 'LW',
    'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UP', 'UK', 'WB'
]

def basicInsights():
    st.write("### :blue[Basic Insights]")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected = st.selectbox("Select State", states_list, index=states_list.index('Tamil Nadu'))
    with col2:
        table = st.selectbox("Select Table", ['Transaction', 'User'])
    with col3:
        year_selected = st.selectbox("Selected Year", [2018, 2019, 2020, 2021, 2022, 2023])
    with col4:
        if year_selected == 2023:
            quarter_selected = st.selectbox("Selected Quarter", [1, 2, 3])
        else:
            quarter_selected = st.selectbox("Selected Quarter", [1, 2, 3, 4])

    if selected and table == 'Transaction' and year_selected and quarter_selected:
        st.success("Your Insight")
        df_1 = f"select * from map_transaction where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"
        df_2 = f"select * from top_transaction_dist where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"
        df_3 = f"select * from top_transaction_pin where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"

        q_df_1 = pd.read_sql_query(df_1, engine)
        q_df_1['State'] = q_df_1['State'].str.replace('-', ' ').str.title()
        q_df_1['Transaction Count'] = q_df_1['Transacion_count'].apply(lambda x: '{:,.0f}'.format(x))
        q_df_1['Transaction Amount'] = q_df_1['Transacion_amount'].apply(lambda x: '₹ {:,.0f}'.format(x))

        q_df_2 = pd.read_sql_query(df_2, engine)
        q_df_2['District_Name'] = q_df_2['District_Name'].str.title()
        q_df_2['Transaction Count'] = q_df_2['Transacion_count'].apply(lambda x: '{:,.0f}'.format(x))
        q_df_2['Transaction Amount'] = q_df_2['Transacion_amount'].apply(lambda x: '₹ {:,.0f}'.format(x))

        q_df_3 = pd.read_sql_query(df_3, engine)
        q_df_3['Pin_Code'] = q_df_3['Pin_Code'].astype('object')
        q_df_3['Transaction Count'] = q_df_3['Transacion_count'].apply(lambda x: '{:,.0f}'.format(x))
        q_df_3['Transaction Amount'] = q_df_3['Transacion_amount'].apply(lambda x: '₹ {:,.0f}'.format(x))

        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.subheader(":blue[Transaction Count]")
            st.plotly_chart(px.bar(q_df_1, x='District_Name', y='Transaction Count', text='Transaction Count',
                                   color='District_Name'))
        with t_col2:
            st.subheader(":blue[Top 10 Districts]")
            st.plotly_chart(px.pie(q_df_2, values='Transacion_count', names='District_Name',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()

        u_col1, u_col2 = st.columns(2)
        with u_col1:
            st.subheader(":blue[Transaction Amount]")
            st.plotly_chart(px.bar(q_df_1, x='District_Name', y='Transaction Amount', text='Transaction Amount',
                                   color='District_Name'))
        with u_col2:
            st.subheader(":blue[Top 10 Districts]")
            st.plotly_chart(px.pie(q_df_2, values='Transacion_amount', names='District_Name',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.subheader(":blue[Top 10 Pincodes for Transaction Count]")
            st.plotly_chart(px.pie(q_df_3, values='Transacion_count', names='Pin_Code',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))
        with p_col2:
            st.subheader(":blue[Top 10 Pincodes for Transaction Amount]")
            st.plotly_chart(px.pie(q_df_3, values='Transacion_amount', names='Pin_Code',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()

    elif selected and table == 'User' and year_selected and quarter_selected:
        st.success("Your Insight")
        df_1 = f"select * from map_users where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"
        df_2 = f"select * from district_wise_users where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"
        df_3 = f"select * from pincode_wise_users where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"
        df_4 = f"select * from aggregated_user_brand where state='{states_dict[selected][0]}' and year={year_selected} and Quater = {quarter_selected}"

        q_df_1 = pd.read_sql_query(df_1, engine)
        q_df_1['State'] = q_df_1['State'].str.replace('-', ' ').str.title()
        q_df_2 = pd.read_sql_query(df_2, engine)
        q_df_2['District_Name'] = q_df_2['District_Name'].str.title()
        q_df_3 = pd.read_sql_query(df_3, engine)
        q_df_4 = pd.read_sql_query(df_4, engine)

        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.subheader(":blue[User Registration Count]")
            st.plotly_chart(px.bar(q_df_1, x='District_Name', y='Registered_User', text='Registered_User',
                                   color='District_Name'))
        with t_col2:
            st.subheader(":blue[Top 10 Districts]")
            st.plotly_chart(px.pie(q_df_2, values='Registered_User', names='District_Name',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()

        u_col1, u_col2 = st.columns(2)
        if q_df_1['App_Opens'].sum() == 0:
            st.subheader(
                f":blue[The App Open Count of {selected}, {year_selected} of Q{quarter_selected} is Unavailable please try another combination]")
        else:
            with u_col1:
                st.subheader(":blue[App Open Count]")
                st.plotly_chart(
                    px.bar(q_df_1, x='District_Name', y='App_Opens', text='App_Opens', color='District_Name'))
            with u_col2:
                st.subheader(":blue[Top 10 Districts]")
                q_df_1.sort_values('App_Opens', ascending=True, inplace=True)
                st.plotly_chart(px.pie(q_df_1.head(10), values='App_Opens', names='District_Name',
                                       color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()

        st.subheader(":blue[Top 10 Pincodes for Registration Count]")
        p_col1, p_col2 = st.columns([1, 3])
        with p_col2:

            st.plotly_chart(px.pie(q_df_3, values='Registered_User', names='Pin_Code',
                                   color_discrete_sequence=px.colors.diverging.RdYlGn))

        st.divider()
        if year_selected == 2023:
            st.subheader(
                f":blue[The Brand Details for 2023 is Not Available]")
        else:
            st.subheader(":blue[Top Registration Count by Mobile Brands]")
            b_col1, b_col2 = st.columns([1, 3])
            with b_col2:
                st.plotly_chart(
                    px.bar(q_df_4, x='Brands', y='Brandwise_Register', text='Brandwise_Register', color='Brands'))
        st.divider()


def performance():
    state_df = pd.DataFrame({'State Name': states_list, 'State Code': state_codes})
    df = pd.read_sql_query(
        'select a1.state, a1.year, sum(transacion_count) `Transaction Count`, sum(transacion_amount) '
        '`Transaction Amount`, sum(registered_user) `Registered User` from aggregated_transaction a1 '
        'join aggregated_user a2 on a1.State = a2.state and a1.year = a2.year and a1.Quater = '
        'a2.Quater group by 1, 2', engine)

    df['state'] = df['state'].str.replace('-', ' ').str.title()

    state = df.merge(state_df, left_on='state', right_on='State Name', how='left')
    state['State Name'] = state['State Code'] + '-' + state['State Name']

    st.write("### :blue[Performance over the years]")
    tab = st.selectbox('Select Overall Changes', ['Transaction Count', 'Transaction Amount', 'Registered User'])

    st.plotly_chart(
        px.bar(
            state,
            x="State Code",
            y=f"{tab}",
            animation_frame="year",
            color="State Name",
            hover_name="state",
            range_y=[0, state[f'{tab}'].max()],
        ).update_layout(
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=0, r=0, b=0, t=50)
        ),
        use_container_width=True
    )
def visualisation():
    tab1, tab2 = st.tabs(['Basic', 'Performance'])
    with tab1:
        basicInsights()
    with tab2:
        performance()

