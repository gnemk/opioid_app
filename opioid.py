# Import libraries
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly
import plotly.express as px

# Remove potential pd dataframe SettingWithCopyWarning
pd.options.mode.chained_assignment = None

# Set the app page width
st.set_page_config(layout="wide")

# Add an image with app title
image = Image.open('opioid_image.jpg')
st.image(image, use_column_width=True)

# Creating a dictionary for selectbox 
datasets = {"For All Plans":"medicaid_opioid_all.csv","Fee for Service":"medicaid_opioid_ffs.csv","Managed Care":"medicaid_opioid_mc.csv"}
option = st.selectbox('Choose a Medicaid plan', datasets.keys())
   
# Create sidebar sliders
st.sidebar.header("Short-Acting Opioid Claim Settings")

sh_opioid_clms = st.sidebar.slider('Total Number of Short-Acting Opioid Claims by State',10000, 6000000, 3000000)

st.sidebar.header("Long-Acting Opioid Claim Settings")

la_opioid_clms = st.sidebar.slider('Total Number of Long-Acting Opioid Claims by State',5000, 1000000, 500000)

# Create dataframe 
file_name = datasets.get(option)

df = pd.read_csv(file_name)

# Create a checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

# Explain short-acting and long-acting opiod drugs
st.subheader('Short-Acting Opioid: Fast release opioid drug | Long-Acting Opioid: Extended release opioid drug')

# Create tabs
tab1, tab2 = st.tabs(["Short-Acting Opioid", "Long-Acting Opioid"])

# Create a state_code
state_code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}

with tab1:
   # Add a subheader
   st.subheader('Short-acting opioid precription data by state')
   
   # Generate a new data frame
   df1 = df.loc[:, ~df.columns.isin(['la_tot_opioid_clms','la_opioid_prscrbng_rate','la_opioid_prscrbng_rate_1y_chg','la_opioid_prscrbng_rat_5y_chg'])]
   st.write(df1)

   df2= df1.groupby('state', as_index=False).agg({"latitude": "mean", "longitude": "mean", "tot_opioid_clms": "sum", "opioid_prscrbng_rate":"mean"})
   # st.write(df2)

   df3 = df2.loc[df2['tot_opioid_clms'] > sh_opioid_clms]

   # Add a subheader
   st.subheader('Medicaid opioid prescription mapping in U.S. - total number of short-acting opioid claims')

   # Create a map
   # st.map(df3)

   # Add one state code column in datafrme for map creation
   df3['state_code'] = df3['state'].map(state_code)
   # st.write(df3)

   # Create a plotly map for short-acting opioid
   fig_sh = px.choropleth(df3, locations='state_code',locationmode="USA-states", color='tot_opioid_clms', scope="usa")
   st.plotly_chart(fig_sh, use_container_width=True)
   
  # Add a subheader
   st.subheader('Medicaid opioid presriptions by state - total number of short-acting opiod claims')

   # Create a bar chart
   bar1 = alt.Chart(df3).mark_bar().encode(
         x= 'sum(tot_opioid_clms)',
         y= alt.Y('state:N', sort=alt.EncodingSortField('tot_opioid_clms',    
            op='sum', order='descending'))
      )

         # Add claim labels on bars
   text = bar1.mark_text(
         align='left',
         baseline='middle',
         dx=10 # Nudges text to right so it doesn't appear on top of the bar
      ).encode(
    text='sum(tot_opioid_clms)'
      )
   bars1 = (bar1 + text) # Generate bars with value labels
   
   # Generate a bar chart in Streamlit
   st.altair_chart(bars1, use_container_width=True)

   # Add a subheader
   st.subheader('Medicaid short-acting opioid claim and claim rate trends in each state')
   
   # Convert integer to datetime
   df1.year = pd.to_datetime(df1["year"], format="%Y")

   # st.write(df1)

   # Get a list of all US states for the selection box
   state_list_sh = list(df1['state'].unique())

   # Create selectbox for state selection
   state_select_sh = st.selectbox(label = "Choose a state for short-acing opioid prescription trend", options = state_list_sh)

   # Use selected values from selection box to filter dataset down to only the rows we need
   query_sh = f"state=='{state_select_sh}'"
   df1_filtered = df1.query(query_sh)

   # st.write(df1_filtered)

   col1, col2 = st.columns(2)
   with col1:
      # Add a caption
      st.caption('Number of short-acting opioid prescriptions')

      # Create a line chart for number of short-acting opioid presriptions
      line = alt.Chart(df1_filtered).mark_line().encode(
         x='year',
         y='sum(tot_opioid_clms)'
      )
      st.altair_chart(line, use_container_width=True)

   with col2:
      # Add a caption
      st.caption('Short-acting opioid prescription rate')

      # Create a line chart for short-acting opioid presription rate
      line1 = alt.Chart(df1_filtered).mark_line().encode(
         x='year:T',
         y='mean(opioid_prscrbng_rate):Q'
      )
      st.altair_chart(line1, use_container_width=True)

with tab2:
   # Add a subheader
   st.subheader('Long-acting opioid precription data by state')
   
   # Show data table
   df4 = df.loc[:, ~df.columns.isin(['tot_opioid_clms','opioid_prscrbng_rate','opioid_prscrbng_rate_1y_chg','opioid_prscrbng_rate_5y_chg'])]
   st.write(df1) # Need to show short-term opioid data

   df5= df4.groupby('state', as_index=False).agg({"latitude": "mean", "longitude": "mean", "la_tot_opioid_clms": "sum"})
   # st.write(df2)

   df6 = df5.loc[df5['la_tot_opioid_clms'] > la_opioid_clms]

   # Add a subheader
   st.subheader('Medicaid opioid prescription mapping in U.S. - total number of long-acting opioid claims')

   # Create a map
   # st.map(df6)

    # Add one state code column in datafrme for map creation
   df6['state_code'] = df6['state'].map(state_code)
   # st.write(df6)

   # Create a plotly map for long-acting opioid
   fig_la = px.choropleth(df6, locations='state_code',locationmode="USA-states", color='la_tot_opioid_clms', scope="usa")
   st.plotly_chart(fig_la, use_container_width=True)

   # Add a subheader
   st.subheader('Medicaid opioid presriptions by state - total number of long-acting opioid claims')

   # Create a bar chart
   bar2 = alt.Chart(df6).mark_bar().encode(
         x= 'sum(la_tot_opioid_clms)',
         y= alt.Y('state:N', sort=alt.EncodingSortField('la_tot_opioid_clms',    
            op='sum', order='descending'))
      )

         # Add claim labels on bars
   text = bar2.mark_text(
         align='left',
         baseline='middle',
         dx=10 # Nudges text to right so it doesn't appear on top of the bar
      ).encode(
         text='sum(la_tot_opioid_clms)'
      )
   bars2 = (bar2 + text) # Generate bars with value labels
   
   # Generate chart in Streamlit
   st.altair_chart(bars2, use_container_width=True)

   # Add a subheader
   st.subheader('Medicaid long-acting opioid claim and claim rate trends in each state')
   
   # Convert integer to datetime
   df4.year = pd.to_datetime(df4["year"], format="%Y")

   # Get a list of all US states for the selection box
   state_list_la = list(df4['state'].unique())

   # Create selection box for state selection
   state_select_la = st.selectbox(label = "Choose a state for long-acing opioid prescription trend", options = state_list_la)

   # use selected values from selection box to filter dataset down to only the rows we need
   query_la = f"state=='{state_select_la}'"
   df4_filtered = df4.query(query_la)

   # st.write(df4_filtered)

   col1, col2 = st.columns(2)
   with col1:
      # Add a caption
      st.caption('Number of long-acting opioid prescriptions')

      # Create a line chart for number of short-acting opioid presriptions
      line = alt.Chart(df4_filtered).mark_line().encode(
         x='year',
         y='sum(la_tot_opioid_clms)'
      )
      st.altair_chart(line, use_container_width=True)

   with col2:
      # Add a caption
      st.caption('Long-acting opioid prescription rate')

      # Create a line chart for short-acting opioid presription rate
      line1 = alt.Chart(df4_filtered).mark_line().encode(
         x='year:T',
         y='mean(la_opioid_prscrbng_rate):Q'
      )
      st.altair_chart(line1, use_container_width=True)