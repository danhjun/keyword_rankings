import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
fig, ax = plt.subplots()

# Select a subset of dates to display
num_dates = data.shape[1]  # Total number of dates
display_dates = np.linspace(0, num_dates - 1, num=20, dtype=int)  # Select 20 evenly spaced dates
dates = data.columns[display_dates]

# Convert values to numeric
data_numeric = data.loc[selected_country, dates].apply(pd.to_numeric, errors='coerce')

ax.plot(dates, data_numeric)
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title(f'{selected_country} Data')

# Reduce number of visible ticks on the x-axis
num_ticks = 8
step_size = len(dates) // (num_ticks - 1)
visible_dates = dates[::step_size]
ax.set_xticks(visible_dates)

# Set y-axis limits with padding
padding = 5  # Adjust the padding as desired
min_value = data_numeric.min() - padding
max_value = data_numeric.max() + padding
ax.set_ylim(min_value, max_value)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot using Streamlit
st.pyplot(fig)
