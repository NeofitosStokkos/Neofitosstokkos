import streamlit as st
import pandas as pd
import numpy as np
import scipy as sp
import plotly.express as px
import plotly.graph_objects as go


# Streamlit page setup
st.set_page_config(page_title="Touristic Attractions", layout="centered")

# Title and subtitle
st.title("Tourism in Lebanon: A Data-Driven Exploration of Opportunities and Gaps")
st.write("An interactive dashboard to visualize tourism potential and development gaps across Lebanese governorates.")

st.markdown("<h2>Touristic Attractions That Can Be Exploited</h2>", unsafe_allow_html=True)

# Load data
df = pd.read_csv("Tourism-Lebanon-2023.csv")

# Clean 'refArea' and create 'Governorate' column
df["Governorate"] = df["refArea"].apply(
    lambda x: x.split("/")[-1].replace("_", " ").replace(" Governorate", "") if isinstance(x, str) else x
)

# Filter for Governorate-level entries only
df_gov = df[df["refArea"].str.contains("Governorate", na=False)]

# Governorate dropdown filter
governorates = df_gov["Governorate"].dropna().unique()
selected_gov = st.selectbox("Filter by Governorate", ["All"] + sorted(governorates))

# Apply filter if not "All"
if selected_gov != "All":
    df_gov = df_gov[df_gov["Governorate"] == selected_gov]

# Clean up 'Attractions' labels
df_gov['Attractions'] = df_gov["Existence of touristic attractions prone to be exploited and developed - exists"].map({
    True: "Exists", False: "Does Not Exist", "exists": "Exists", "does not exist": "Does Not Exist"
})

# Count values for pie chart
attractions_counts = df_gov['Attractions'].value_counts().reset_index()
attractions_counts.columns = ['Status', 'Count']

# Custom colors
custom_colors = {
    "Exists": "green",
    "Does Not Exist": "tomato"
}

# Pie chart
fig = px.pie(
    attractions_counts,
    names='Status',
    values='Count',
    title="Potential for Sustainable Tourism",
    color='Status',
    color_discrete_map=custom_colors,
)

fig.update_traces(
    textposition='inside',
    textinfo='percent',
    insidetextfont=dict(
        color='black',
        family='Arial black',
        size=20
    )
)

fig.update_layout(
    width=700,
    height=570,
    title_x=0.5,
    title_font=dict(size=18, family="Arial "),
    legend=dict(
        x=0.7,
        y=1,
        xanchor='left',
        font=dict(size=16, family="Arial", color="black")
    )
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "<p style='text-align: center; font-size:16px;'><em>Looks like some governorates need a little tourist glow-up… where the attractions at?</em></p>",
    unsafe_allow_html=True
)

# ---------------- HISTOGRAM ---------------- #
st.markdown("###  Distribution of Tourism Index by Attraction Availability")

# Governorate filter just for this chart
df["Governorate"] = df["refArea"].apply(
    lambda x: x.split("/")[-1].replace("_", " ").replace(" Governorate", "") if isinstance(x, str) else x
)

gov_options_hist = df["Governorate"].dropna().unique()
selected_gov_hist = st.selectbox("Filter this chart by Governorate", ["All"] + sorted(gov_options_hist), key="hist_filter")

# Clean attraction labels
df['Attractions Exist?'] = df['Existence of touristic attractions prone to be exploited and developed - exists'].replace({
    0: 'Does Not Exist', 1: 'Exists',
    False: 'Does Not Exist', True: 'Exists',
    "does not exist": "Does Not Exist", "exists": "Exists"
})

# Filter by Governorate
if selected_gov_hist != "All":
    df_filtered_hist = df[df["Governorate"] == selected_gov_hist]
else:
    df_filtered_hist = df.copy()

# Drop missing values
df_filtered_hist = df_filtered_hist.dropna(subset=["Tourism Index", "Attractions Exist?"])

#  Add Tourism Index slider
min_index = int(df_filtered_hist["Tourism Index"].min())
max_index = int(df_filtered_hist["Tourism Index"].max())

index_range = st.slider(
    " Select a Tourism Index range:",
    min_value=min_index,
    max_value=max_index,
    value=(min_index, max_index),
    key="tourism_index_slider"
)

# Apply slider filter
df_filtered_hist = df_filtered_hist[
    (df_filtered_hist["Tourism Index"] >= index_range[0]) &
    (df_filtered_hist["Tourism Index"] <= index_range[1])
]
st.markdown(f"**Tourism Index range selected:** {index_range[0]} to {index_range[1]}")

# Plot histogram
fig2 = px.histogram(
    df_filtered_hist,
    x='Tourism Index',
    color='Attractions Exist?',
    nbins=20,
    labels={
        'Tourism Index': 'Tourism Index',
        'count': 'Number of Towns',
        'Attractions Exist?': 'Attractions'
    },
    color_discrete_map={
        'Exists': '#2ECC71',
        'Does Not Exist': '#E74C3C'
    }
)

fig2.update_layout(
    width=1000,
    height=500,
    bargap=0.05,
    plot_bgcolor='white',
    font=dict(size=14, family='Segoe UI'),
    xaxis=dict(title='Tourism Index', gridcolor='white'),
    yaxis=dict(title='Number of Towns', gridcolor='lightgrey')
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown(
    f" This selected range highlights variation in touristic infrastructure among towns in '{selected_gov_hist}', with Tourism Index scores between {index_range[0]} and {index_range[1]}. The chart reveals both development strengths and areas with unexploited tourism potential."
)

st.markdown(
    "Data used in this project was obtained from the **PKGCubes Explorer**, available at [PKGCubes Explorer](https://linked.aub.edu.lb:8502/PKGCubes_Explorer)."
)
st.markdown("**Developed by [Neofitos Stokkos](https://www.linkedin.com/in/neofitos-stokkos-41b16530b/)**")