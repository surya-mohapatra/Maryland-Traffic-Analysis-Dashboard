import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data Analysis Functions
def get_yearly_traffic_data(data, year):
    year_column = f'AADT_{year}'
    if year_column in data.columns:
        return data[['ROADNAME', 'COUNTY_DESC', year_column]]
    else:
        return None

def compare_annual_traffic(data, year1, year2):
    col1, col2 = f'AADT_{year1}', f'AADT_{year2}'
    if col1 in data.columns and col2 in data.columns:
        return data[['ROADNAME', 'COUNTY_DESC', col1, col2]]
    else:
        return None

def average_traffic_by_county(data, year):
    year_column = f'AADT_{year}'
    if year_column in data.columns:
        return data.groupby('COUNTY_DESC')[year_column].mean().sort_values(ascending=False)
    else:
        return None

def average_traffic_by_road_type(data, year):
    year_column = f'AADT_{year}'
    if year_column in data.columns:
        return data.groupby('ID_PREFIX')[year_column].mean().sort_values(ascending=False)
    else:
        return None

# Load the AADT data
aadt_data = pd.read_csv('MDOT_SHA_Annual_Average_Daily_Traffic_(AADT).csv')

# Streamlit application layout
st.title('Maryland Traffic Analysis Dashboard')

st.sidebar.title('Navigation')
page = st.sidebar.radio("Choose a page", ["Homepage", "Visualizations", "Data Tables"])

if page == "Homepage":
    st.header("Welcome to the Maryland Traffic Analysis Dashboard")
    st.write("Explore traffic data visualizations and tables.")

elif page == "Visualizations":
    st.header("Traffic Visualizations")
    
    # Visualization: Average AADT by County (2021)
    st.subheader('Average Annual Daily Traffic by County in Maryland (2021)')
    avg_traffic_2021 = average_traffic_by_county(aadt_data, '2021')
    fig, ax = plt.subplots()
    sns.barplot(x=avg_traffic_2021.values, y=avg_traffic_2021.index, ax=ax)
    ax.set_title('Average AADT by County (2021)')
    ax.set_xlabel('Average AADT')
    ax.set_ylabel('County')
    st.pyplot(fig)

elif page == "Data Tables":
    st.header("Traffic Data Tables")
    
    # Data Table: Comparison between 2019 and 2021
    st.subheader("Traffic Data Comparison between 2019 and 2021")
    comparison_data = compare_annual_traffic(aadt_data, '2019', '2021')
    st.dataframe(comparison_data)
