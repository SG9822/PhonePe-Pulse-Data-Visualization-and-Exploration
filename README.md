# PhonePe Pulse Data Visualization and Exploration

## Overview

PhonePe Pulse Data Visualization and Exploration is a Python-based project that utilizes MySQL for data storage and leverages various libraries such as pymysql, pandas, streamlit, plotly, and geopandas for data extraction, manipulation, and visualization. The project aims to explore and visualize transaction and user data from PhonePe Pulse.

## Important Notes

- Data for 2023 Quarter 4 is not available.
- App Open count data is available from 2018 1st quarter to 2019 1st quarter.

## Features

### 1. Home Page
   - Select Box 1: Choose between Transaction and User data.
   - Select Box 2: Select the year (2018-2023).
   - Select Box 3: Choose the quarter (1-4).
   - Map of India with dynamic visualization of transaction details and User Registration details.
   - Radio button to toggle between Transaction Count and Transaction Amount as well as between Registration count and App Opens.

### 2. State-District Page
   - Select Box 1: Choose a state or UT of India.
   - Select Box 2: Select between Transaction and User data.
   - Select Box 3: Choose the year (2018-2023).
   - Select Box 4: Choose the quarter (1-4).
   - Visualizations of transaction and user details for the selected state.

### 3. Visualization Page
   - **Basic Tab:**
     - Select Box 1: Choose Indian States & UT.
     - Select Box 2: Choose between Transaction and User data.
     - Select Box 3: Choose the year (2018-2023).
     - Select Box 4: Choose the quarter (1-4).
   - **Performance Tab:**
     - Select Box: Choose between Transaction Count, Transaction Amount, and Registration Count.
   - Displays visualizations based on the selected options.

### 4. About Page
   - Information about the project, its purpose, and methodologies.
   - Acknowledgments: Special thanks to PhonePe Pulse for contributing the data.
   - GitHub link for data extraction.

## Technologies Used

- **Python:** Core programming language for data analysis, manipulation, and visualization.
- **MySQL:** Database management system for storing and retrieving data.
- **Jupyter Notebook:** Used for GitHub repository cloning and data pushing to MySQL Workbench.
- **PyCharm:** Integrated Development Environment (IDE) for data extraction and visualization using Streamlit.
- **pymysql:** Python library for MySQL database connectivity.
- **pandas:** Data manipulation and analysis library.
- **streamlit:** Framework for creating interactive web applications.
- **plotly:** Library for creating interactive and dynamic plots.
- **geopandas:** Extension of pandas for handling geospatial data.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phonepe-pulse.git
   cd phonepe-pulse
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
3. Run Streamlit app
   ```bash
   streamlit run app.py


## Acknowledgments

Special thanks to PhonePe Pulse for providing the data used in this project.

