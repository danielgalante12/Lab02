# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Music Practice Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Instrumental Practice Analytics 📈")
st.write("This page visualizes your music practice data!")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Raw CSV Practice Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

csv_file = "data.csv"
json_file = "data.json"

csv_data = pd.DataFrame()
if os.path.isfile(csv_file) and os.path.getsize(csv_file)>0:
    try:
        csv_data = pd.read_csv(csv_file)
        csv_data.columns= csv_data.columns.str.strip() #removes leading/trailing whitespace
        st.write("CSV Data Preview:")
        st.write(csv_data)
    except:
        st.error(f"Error reading CSV")
else:
    st.warning("CSV file missing or empty")


json_file = "data.json"
json_data = {}

if os.path.isfile(json_file) and os.path.getsize(json_file)>0:
    try:
        with open (json_file, "r") as f:
            json_data = json.load(f)
    except:
        st.error(f"Error reading JSON")
else:
    st.warning("JSON file missing or empty")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider() #NEW
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Static: Practice Sessions Log (CSV)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

if not csv_data.empty:
    clean_practice = []
    clean_instruments = []

    for i in range(len(csv_data)):
        instrument = csv_data["Instrument"][i]
        value = csv_data["Practice"][i]
        try:
            hours = float(value)
            clean_instruments.append(instrument)
            clean_practice.append(hours)
        except:
            st.warning("Invalid number")

    cleaned_table = pd.DataFrame({
        "Instrument": clean_instruments,
        "Practice": clean_practice
    })

    st.scatter_chart(cleaned_table, x="Instrument", y="Practice")
    st.caption("Each point on the graph shows represents one practice log (instrument, hours practiced)")
else:
    st.warning("Complete survey first!")
    

    

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Dynamic: Bar Graph Based on Practice Log(CSV)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

if not csv_data.empty:

    csv_data["Practice"] = pd.to_numeric(csv_data["Practice"], errors = "coerce")
    instruments = csv_data["Instrument"].unique().tolist()
    selected_instruments = st.multiselect("Select instruments to display", instruments, default = instruments)
    filtered_data= csv_data[csv_data["Instrument"].isin(selected_instruments)]
    st.session_state["filtered_data"] = filtered_data #NEW
    
    if not filtered_data.empty:
        st.bar_chart(st.session_state.filtered_data.set_index("Instrument")["Practice"]) #NEW
        st.caption("This bar graph shows how much time (in hours) each instrument selected was practiced") #NEW
    else:
        st.warning("No instruments selected")
else:
    st.warning("Complete the survey first!")
    


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Dynamic: Line Graph of Practice Time vs. Performance Rating ") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

if json_data and "data_points" in json_data:
    df = pd.DataFrame(json_data["data_points"])
    df.columns = ["Practice Hour", "Performance Rating"]
    df["Practice Hour"] = pd.to_numeric(df["Practice Hour"], errors="coerce")
    df["Performance Rating"] = pd.to_numeric(df["Performance Rating"], errors="coerce")

    max_hour = int(df["Practice Hour"].max())
    hour_limit = st.slider("Show up to this many practice hours:", 1, max_hour, max_hour)

    df_filtered = df[df["Practice Hour"] <= hour_limit]

    st.line_chart(df_filtered.set_index("Practice Hour")["Performance Rating"])#NEW
    st.caption("This line graph shows the relationship between practice hours and corresponding perforamance rating, maxxing out at desired hour limit")
