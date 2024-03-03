import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('day.csv')

# Convert 'dteday' column to datetime format
data['dteday'] = pd.to_datetime(data['dteday'])

# Streamlit Dashboard
st.title("Bike's Rent Dashboard")

# Add blank space
st.text("\n")

# Sidebar widgets
start_date = st.sidebar.date_input("Start Date", min(data['dteday']))
end_date = st.sidebar.date_input("End Date", max(data['dteday']))

# Convert start_date and end_date to datetime64[ns] format
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date)]

# Add horizontal line outside of columns
st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line


# Container for widgets
col1, col2 = st.columns([1, 1])
col3, col4 = st.columns([1, 1])
col5, col6 = st.columns([1, 1])

# Number of columns processed
num_columns = len(data.columns)
col1.write(f"<center><div style='font-size: 25px;'> Number of Columns Processed </div></center>", unsafe_allow_html=True)
col1.write(f"<center><div style='font-size: 20px; font-weight: bold;'> {num_columns}</div></center>", unsafe_allow_html=True)

# Add horizontal line outside of columns
col1.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line

# Sum of days in the data
sum_days = len(data)
col2.write(f"<center><div style='font-size: 25px;'> Sum of Days in the Data </div></center>", unsafe_allow_html=True)
col2.write(f"<center><div style='font-size: 20px; font-weight: bold;'> {sum_days}</div></center>", unsafe_allow_html=True)

# Add horizontal line outside of columns
col2.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line

# Add blank space
col3.write("\n")
col4.text("\n")

# QUESTION NO 1
with col5:
    # Group by 'season' and 'yr', and calculate the sum of 'cnt' for each group
    grouped_data = filtered_data.groupby(['season', 'yr'])['cnt'].sum().reset_index()

    # Map the year values to 'yr' column
    grouped_data['yr'] = grouped_data['yr'].map({0: '2011', 1: '2012'})

    # Replace season codes with descriptions
    grouped_data['season'] = grouped_data['season'].replace({1: 'Summer', 2: 'Fall/Autumn', 3: 'Winter', 4: 'Spring'})

    # Convert 'yr' column to strings
    grouped_data['yr'] = grouped_data['yr'].astype(str)

    # Set palette colors for each year
    palette = {'2011': 'lightgrey', '2012': 'mediumseagreen'}

    # Display grouped data
    st.subheader("Bike's Rent Throughout Each Season")
    st.caption("Count of Bike's Rented divides to 4 Season")
    sns.barplot(data=grouped_data, x='season', y='cnt', hue='yr', palette=palette)
    plt.xlabel('Season')
    plt.ylabel('Total Bike Rentals')
    plt.xticks(rotation=45)
    plt.legend(title='Year')
    st.pyplot(plt)


# QUESTION NO 2
with col6:
    # Select columns for correlation analysis
    columns = ['hum', 'temp', 'windspeed', 'cnt']

    # Calculate the correlation matrix
    correlation_matrix = data[columns].corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(8, 6))

    # Draw the heatmap with positive correlation values highlighted
    sns.heatmap(correlation_matrix, annot=True, cmap='YlGnBu', fmt=".2f", linewidths=.5,
                mask = correlation_matrix < 0)

    # Set title and labels
    st.subheader("Correlation Between Features")
    st.caption('Correlation Between Temperature, Humidity, Windspeed, and Bike Rentals (Positive Correlations)')
    plt.xlabel('Features')
    plt.ylabel('Features')

    # Rotate the y-axis labels for better readability
    plt.yticks(rotation=0)

    # Display the plot using st.pyplot()
    st.pyplot(plt.gcf())



# Add blank space
st.text("")


# QUESTION NO 3
st.subheader('Trend Bike Rentals by Day of the Week')

# Preprocessing
filtered_data['dteday'] = pd.to_datetime(filtered_data['dteday'])
filtered_data['day_of_week'] = filtered_data['dteday'].dt.day_name()

# Grouping by day of the week and calculating descriptive statistics
weekly_trend_stats = filtered_data.groupby('day_of_week')['cnt'].describe()

# Calculate mean, min, and max
weekly_trend_stats['min'] = filtered_data.groupby('day_of_week')['cnt'].min()
weekly_trend_stats['mean'] = filtered_data.groupby('day_of_week')['cnt'].mean()
weekly_trend_stats['max'] = filtered_data.groupby('day_of_week')['cnt'].max()

# Sort the days of the week
weekly_trend_stats = weekly_trend_stats.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Find top 3 days with highest mean rental counts
top_days = weekly_trend_stats.nlargest(3, 'mean').index

# Plotting
plt.figure(figsize=(10, 6))

# Plotting bars for mean, min, and max
plt.bar(weekly_trend_stats.index, weekly_trend_stats['mean'], color=['blue' if day in top_days else 'grey' for day in weekly_trend_stats.index], label='Mean')
plt.plot(weekly_trend_stats.index, weekly_trend_stats['min'], color='red', marker='_', markersize=10, label='Min')
plt.plot(weekly_trend_stats.index, weekly_trend_stats['max'], color='green', marker='_', markersize=10, label='Max')

plt.xlabel('Day of the Week')
plt.ylabel('Bike Rentals')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Display the plot
st.pyplot(plt)

