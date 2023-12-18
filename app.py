import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# retrieve aadt data for a specific year
def get_yearly_traffic_data(data, year): #takes df and year as arguments
    year_column = f'AADT_{year}' # variable to select for aadt column  using f string
    if year_column in data.columns: #checks if year_column in df aadt_data columns
        return data[['ROADNAME', 'COUNTY', year_column]] # outputs dataframe with specified columns
    else:
        return None

# compares aadt_Data between two years
def compare_annual_traffic(data, year1, year2): #takes df and years to be compared as arguments
    col1, col2 = f'AADT_{year1}', f'AADT_{year2}' # created col1,col2 variables to select for aadt columns  using f stringa
    if col1 in data.columns and col2 in data.columns: #checks if col1,col2 in df aadt_data columns
        return data[['ROADNAME', 'COUNTY','ROAD_SECTION', col1, col2]] # outputs dataframe with specified columns
    else:
        return None

# average traffic volume by county for a specified year
def average_traffic_by_county(data, year):#takes df and year as arguments
    year_column = f'AADT_{year}' # variable to select for aadt column  using f string
    if year_column in data.columns: #checks if year_column in df aadt_data columns
        return data.groupby('COUNTY')[year_column].mean().sort_values(ascending=False) # groups by county and applies mean function to aadt_year column
    else:
        return None

# average traffic volume by road type for a specified year
def average_traffic_by_road_type(data, year):#takes df and year as arguments
    year_column = f'AADT_{year}' # variable to select for aadt column  using f string
    if year_column in data.columns: #checks if year_column in df aadt_data columns
        return data.groupby('ROAD_TYPE')[year_column].mean().sort_values(ascending=False) # groups by road_type and applies mean function to aadt_year column
    else:
        return None

# Load the AADT data
aadt_data = pd.read_csv('MDOT_SHA_Annual_Average_Daily_Traffic_(AADT).csv')

# Created list containing columns that are to be dropped from the dataset 
columns_to_drop = ['OBJECTID', 'LOCATION_ID', 'COUNTY_ID', 'MUN_SORT', 'LOC_ERROR','ID_RTE_NO',
                   'MP_SUFFIX','ID_MP','BEGIN_SECTION','END_SECTION','F_SYSTEM','ROUTEID','ROUTEID_RH',
                   'MAIN_LINE','COUNTED_FACTORED', 'STMP_SEQ','K_FACTOR', 'D_FACTOR','LINK','AAWDT_2013', 
                   'AAWDT_2014', 'AAWDT_2015', 'AAWDT_2016', 'AAWDT_2017','AAWDT_2018', 'AAWDT', 
                   'MOTORCYCLE_AADT', 'CAR_AADT', 'LIGHT_TRUCK_AADT', 'BUS_AADT', 'SINGLE_UNIT_AADT',
                   'COMBINATION_UNIT_AADT', 'LOC_ERROR', 'Shape__Length0','AAWDT_2019', 'AAWDT_2020',
                   'AAWDT_2021','SHAPE_Length','PEAK_HOUR_DIRECTION', 'NORTH_EAST_SPLIT', 'SOUTH_WEST_SPLIT','MUNICIPALITY'] 
aadt_data = aadt_data.drop(columns=columns_to_drop)

# Renamed Columns according to table found in source website https://data.imap.maryland.gov/datasets/3f4b959826c34480be3e4740e4ee025f_1/explore?location=38.753802%2C-77.269750%2C8.00&showTable=true
aadt_data.rename(columns={'COUNTY_DESC': 'COUNTY', 'ID_PREFIX': 'ROAD_TYPE', 'F_SYSTEM_DESC': 'ROAD_FUNCTION',
                          'AVMT':'AVERAGE_VEHICLE_MILES_TRAVELED','AADT':'AADT_2022'}, inplace = True)

#created dictionary with prefix definitions
road_type_dict = {
    'IS': 'Interstate Highways',
    'US': 'U.S. Routes',
    'MD': 'Maryland State Routes',
    'CO': 'County Roads',
    'MU': 'Municipal Roads',
    'SR': 'State Routes',
    'RP': 'Ramp'}
#used map function with dictionary as input and used fillna to set OP and GV prefixes as unknown
aadt_data['ROAD_TYPE'] = aadt_data['ROAD_TYPE'].map(road_type_dict).fillna('Unknown')

# Extract available years/counties/road_type from the dataset for use in streamlit dashboard

#list compehension iterating through columns starting with AADT_ and extracting year from column name using split
available_years = [col.split('_')[1] for col in aadt_data.columns if col.startswith('AADT_')] 
# unique values present in county column
available_counties = aadt_data['COUNTY'].unique()
#unique values present in road_type column
available_road_types = aadt_data['ROAD_TYPE'].unique()

# Streamlit application 
st.title('Maryland Traffic Analysis Dashboard') #title 

st.sidebar.title('Navigation') #choose between different pages in the sidebar
page = st.sidebar.radio("Choose a page", ["Overview", "Visualizations", "Summary Data Table","AADT Year Comparison"])

if page == "Overview":
    st.header("Welcome to the Maryland Traffic Analysis Dashboard")
    st.write("Explore traffic data visualizations and tables.")

    st.subheader("Annual Average Daily Traffic (AADT)")
    st.write("""
    _Annual Average Daily Traffic (AADT) is a metric used to calculate the average daily traffic volume on a road or highway over a year. It sums up all vehicle trips on a road segment for a year and then divides by 365 days. It's expressed in vehicles per day (vpd)._

    **Applications**
    - **Infrastructure and Transport Planning**: Helps in designing roads and managing traffic congestion.
    - **Retail and Real Estate**: Used by retailers and real estate professionals to assess site potential.
    - **Law Enforcement**: Aids in accident investigations and legal cases.
    - **Legislative Use**: Assists lawmakers in budgeting and prioritizing transportation projects.

    **Limitations**: While AADT is widely used, it doesn't account for seasonal or day-of-week variations in traffic patterns, leading to a more generalized view of traffic flow.

    **AADT Dataset Info:**
    The Annual Average Daily Traffic (AADT) data is collected by Maryland Department of Transportation and contains information regarding geographic coverage, traffic volume information, and historical data for the past decade. The collected data is present in both linear road segment and point geometric features, with the linear road segment dataset used for this analysis. The data was collected using over 8700 counting stations and 84 Automatic Traffic Recorders (ATRs). Counts were taken every 3 or 6 year cycle and complemented by growth factor adjustments. This data serves as a critical resource for both federal and state agencies.
    """)

    # link to the data source
    st.markdown("### [Link to Data Source](https://data.imap.maryland.gov/datasets/3f4b959826c34480be3e4740e4ee025f_1/explore?showTable=true)")


elif page == "Visualizations":
    st.header("Traffic Visualizations")

    # interactive menu for Visualization Choices
    vis_choice = st.selectbox("Choose your visualization", ["Average Traffic by County", "Average Traffic by Road Type","Average Vehicle Miles Traveled by County"])

    # Year selection for visualization 
    if vis_choice != "Average Vehicle Miles Traveled by County": # does not need year selection
        # Year selection for visualization (only for the first two options)
        selected_year = st.selectbox("Select a Year", available_years) # dropdown menu to select year from available_years

    if vis_choice == "Average Traffic by County":
        # Visualization: Average AADT by County
        st.subheader(f'Average Annual Daily Traffic by County in Maryland ({selected_year})') 
        avg_traffic_county = average_traffic_by_county(aadt_data, selected_year) # generate avg_traffic df
        # Create figure and axis
        fig, ax = plt.subplots()
        # Plotting
        sns.barplot(x=avg_traffic_county.values, y=avg_traffic_county.index, ax=ax, palette = 'rocket')
        ax.set_title(f'Average AADT by County ({selected_year})')
        ax.set_xlabel('Average AADT')
        ax.set_ylabel('County')
        st.pyplot(fig) #shows figure on streamlit application

    elif vis_choice == "Average Traffic by Road Type":
        # Visualization: Average AADT by Road Type
        st.subheader(f'Average Annual Daily Traffic by Road Type in Maryland ({selected_year})')
        avg_traffic_road_type = average_traffic_by_road_type(aadt_data, selected_year)
        # Create figure and axis
        fig, ax = plt.subplots()
        # Plotting
        sns.barplot(x=avg_traffic_road_type.values, y=avg_traffic_road_type.index, ax=ax, palette = 'rocket')
        ax.set_title(f'Average AADT by Road Type ({selected_year})')
        ax.set_xlabel('Average AADT')
        ax.set_ylabel('Road Type')
        st.pyplot(fig)
    
    elif vis_choice == "Average Vehicle Miles Traveled by County":
        # Visualization AVMT by County    
        st.subheader('Average Vehicle Miles Traveled by County')
        AVMT_data = aadt_data.groupby("COUNTY")["AVERAGE_VEHICLE_MILES_TRAVELED"].sum().sort_values(ascending=False)
        # Create figure and axis
        fig, ax = plt.subplots()
        # Plotting
        sns.barplot(x = AVMT_data.index, y = AVMT_data.values,  palette = 'rocket')
        ax.set_title('Average Vehicle Miles Traveled by County')
        ax.set_xlabel('County')
        ax.set_ylabel('Miles (Millions)')
        plt.xticks(rotation=90)
        st.pyplot(fig)


elif page == "AADT Year Comparison":
    st.header("Compare Traffic Data Across Years")

    # Dropdown menu for selecting years
    year1 = st.selectbox("Select the first year for comparison", available_years)
    year2 = st.selectbox("Select the second year for comparison", available_years)

    if year1 and year2: # both year1 and year2 need to be selected to generate dataframe
        comparison_data = compare_annual_traffic(aadt_data, year1, year2)
        if comparison_data is not None: #once year is selected will generate df and subheader
            st.subheader(f"Traffic Data Comparison between {year1} and {year2}")
            st.dataframe(comparison_data)
        else:
            st.write("Data not available for the selected years.")
            
elif page == "Summary Data Table": #option to filter table by county and/or road type
    st.header("Explore Traffic Data Tables")

    # Data Table logic
    #list of counties and all option can be selected from dropdown
    county_selection = st.selectbox("Select a County", ['All'] + list(available_counties))
    #list of road_type and all option can be selected from dropdown
    road_type_selection = st.selectbox("Select a Road Type", ['All'] + list(available_road_types))
    
    filtered_data = aadt_data # set filtered_data to entire aadt_data df
    if county_selection != 'All': #if specific county selected then dataframe is filtered for the county
        filtered_data = filtered_data[filtered_data['COUNTY'] == county_selection] #mask created: df with boolean values
    if road_type_selection != 'All': #if specific road_type selected then dataframe is filtered for the road_type
        filtered_data = filtered_data[filtered_data['ROAD_TYPE'] == road_type_selection]

    st.dataframe(filtered_data)#displays dataframe
    
