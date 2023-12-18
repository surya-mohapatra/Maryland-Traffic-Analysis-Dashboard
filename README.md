# Maryland-Traffic-Analysis-Dashboard
## Interactive Dashboard for Analyzing and Visualizing Maryland's Traffic Patterns

## Problem Statement

Traffic congestion in Maryland presents a significant challenge, impacting daily commutes, increasing travel times, and affecting overall quality of life. Understanding traffic patterns and identifying congestion hotspots are crucial for effective urban planning and congestion management. This project aims to analyze and visualize traffic data in Maryland to identify areas with high congestion and understand traffic trends over time. 

## Solution Summary

To address this problem, an interactive dashboard was created which allows users to visualize and analyze traffic patterns across Maryland. The dashboard provides visualizations of traffic data, such as bar charts displaying average traffic volumes by county and comparisons of traffic trends across different years. By offering insights into traffic volumes and patterns, the dashboard aids in identifying potential congestion areas, assisting in traffic management and urban planning.

## Technical Solution

The solution involves a Streamlit-based web application that dynamically visualizes traffic data obtained from Maryland's Department of Transportation(2). Key features include interactive menus for selecting specific years for comparison, and the ability to generate bar plots and data tables. The backend is powered by Python app.py script, with data analysis conducted using Pandas module and visualizations created with Seaborn and Matplotlib modules. This approach makes the dashboard interactive and responsive, allowing for data exploration.

## Repository Contents

1. EDA.ipynb: This Jupyter Notebook contains detailed exploratory data analysis (EDA) of the Maryland traffic dataset. It includes various functions and visualizations that delve into different aspects of the data, such as traffic volume distributions, time series analysis, and comparisons across different road types and counties. The notebook is designed to provide an in-depth understanding of the data, uncover patterns and trends, and support the findings presented in the Streamlit dashboard.
   
2. app.py: The main Streamlit application file containing the dashboard logic, data analysis functions, and visualization code.
   
3. MDOT_SHA_Annual_Average_Daily_Traffic_(AADT).csv: The dataset used for analysis, containing traffic volumes in Maryland.
   
4. requirements.txt: A list of requirements needed to run the application.
   
5. README.md: This file, providing an overview of the project, instructions, and contact information.

6. Data_Dictionary_AADT_RAW.pdf: This pdf contains the data dictionary for MDOT_SHA_Annual_Average_Daily_Traffic_(AADT).csv dataset used for analysis

## Contact Information

For more information or inquiries about this project, please reach out to:

Email: gyanasur@ualberta.ca

GitHub: surya-mohapatra

## References

1. https://www.streetlightdata.com/what-is-aadt/
   
2. https://data.imap.maryland.gov/maps/77010abe7558425997b4fcdab02e2b64/about

3. https://data.imap.maryland.gov/datasets/3f4b959826c34480be3e4740e4ee025f_1/explore?showTable=t


