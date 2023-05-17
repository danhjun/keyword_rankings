import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser

# Load CSV data using Kedro's data catalog
@st.cache
def load_data():
    df = pd.read_csv(r"C:\Users\Dan\Desktop\keyword_rankings\keyword-rankings\data\01_raw\phonk.csv", index_col=0)
    return df

# Load data
data = load_data()

# Select country
countries = data.index.tolist()
selected_country = st.selectbox("Select a country", countries)

# Remove unexpected columns
data = data.loc[:, ~data.columns.str.startswith('Unnamed')]

# Plot the data for the selected country
fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the figure size as desired

# Select a subset of dates to display
num_dates = data.shape[1]  # Total number of dates
num_display_dates = 20  # Number of dates to display (increase this value for more dates)
display_dates = np.linspace(0, num_dates - 1, num=num_display_dates, dtype=int)  # Select evenly spaced dates
dates = data.columns[display_dates]

# Convert values to numeric
data_numeric = data.loc[selected_country, dates].apply(pd.to_numeric, errors='coerce')

ax.plot(dates, data_numeric, marker='o', linestyle='-', label='Data')
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title(f'{selected_country} Data')

# Reduce number of visible ticks on the x-axis
num_ticks = num_display_dates
step_size = len(dates) // (num_ticks - 1)
visible_dates = dates[::step_size]
ax.set_xticks(visible_dates)

# Set y-axis limits with padding
padding = 5  # Adjust the padding as desired
min_value = 0
max_value = np.ceil(data_numeric.max() / 5) * 5  # Round up the max value to the nearest multiple of 5
ax.set_ylim(min_value, max_value)

# Set y-axis increment marks
increment_marks = np.arange(min_value, max_value + 1, 5)  # Adjust the increment as desired
ax.set_yticks(increment_marks)

# Add data point markers
ax.plot(dates, data_numeric, marker='o', linestyle='-', label='Data')

# Add grid lines
ax.grid(True, linestyle='--', alpha=0.5)

# Add data point labels
date_labels = [parser.parse(date).strftime('%b %d') for date in dates]  # Format dates as desired
for date, value, label in zip(dates, data_numeric, date_labels):
    ax.annotate(label, xy=(date, value), xytext=(10, 10),
                textcoords='offset points', ha='left', va='bottom', fontsize=8)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot using Streamlit
st.pyplot(fig)
