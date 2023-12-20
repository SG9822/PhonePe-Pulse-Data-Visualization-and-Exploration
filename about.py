import streamlit as st


def aboutProject():
    st.title(":violet[PhonePe Pulse Data Visualization and Exploration]")

    st.markdown("""
    ## :blue[Project Overview:]

    **Description:**
    PhonePe Pulse Data Visualization and Exploration is a user-friendly tool developed using Streamlit and Plotly to extract, visualize, and explore data provided by PhonePe. The project involves cloning data from GitHub, loading it into MySQL, and creating an interactive data visualization platform.

    **Targeted Audience:**
    This project is designed for academic purposes, making it accessible to students or anyone interested in exploring data visualization techniques using Python.

    **Technologies Used:**
    - **Python:** Main programming language for data manipulation and visualization.
    - **MySQL:** Database management system for storing and retrieving data.
    - **Plotly and Streamlit:** Frameworks for creating interactive and visually appealing data visualizations.
    - **Pandas:** Python library for data manipulation and analysis.
    - **Jupyter Notebook:** Utilized for cloning data from GitHub and loading datasets into MySQL.
    - **PyCharm:** Integrated Development Environment (IDE) for developing Streamlit applications.

    ## :blue[Project Goals:]

    The primary goals of the PhonePe Pulse Data Visualization and Exploration project are:

    1. **Data Extraction:** Clone data from GitHub and load it into MySQL for efficient data management.

    2. **Visualization Skills Showcase:** Demonstrate strong visualization skills through interactive charts and graphs using Plotly.

    3. **User-Friendly Interface:** Create an intuitive and user-friendly interface with Streamlit, allowing users to explore and interact with the visualized data seamlessly.

    This academic project aims to contribute to the learning experience by showcasing practical applications of data visualization and exploration techniques.
    """)

    st.divider()

    st.markdown("## :violet[Data of the Project]")
    st.write("#### This is where the data is extracted and did some magical works and makes visual treats to you, "
             "I believe 😊")

    st.markdown("#### :blue[Data that Powers the Project](https://github.com/PhonePe/pulse)")



