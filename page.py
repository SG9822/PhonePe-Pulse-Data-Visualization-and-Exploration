from streamlit_option_menu import option_menu
import streamlit as st
# import pandas as pd

st.set_page_config(layout="wide",
                   page_title="PhonePe-Pulse",
                   page_icon="https://www.phonepe.com/pulsestatic/767/pulse/icons/icon-48x48.png?v=1e5c98f168b1aeec4e1d02c0739fa229")

tit1, tit2 = st.columns([1, 3])

with tit1:
    st.markdown("### [:blue[पे PhonePe Pulse | Project]](https://github.com/SG9822/PhonePe-Pulse-Data-Visualization-and-Exploration) <style>a { text-decoration: none; }</style>", unsafe_allow_html=True)
with tit2:
    selected = option_menu(
        menu_title=None,
        options=["Home", "State-District", "Visualisation", "About Project"],
        icons=["house", "globe-central-south-asia", "graph-up-arrow", "info-square-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal", )

from youtube_streamlit import countryData
from states import stateData
from visualisation import visualisation
from about import aboutProject

if selected == 'Home':
    countryData()
elif selected == 'State-District':
    stateData()
elif selected == 'Visualisation':
    visualisation()
elif selected == "About Project":
    aboutProject()
