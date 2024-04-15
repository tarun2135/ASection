import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
# Load the data
file_path = r"C:\Users\lenovo\Desktop\hii\ASection\Section - A.xlsx"
df = pd.read_excel(file_path)

# Function to filter data based on selected fee range
def filter_data(df, column, min_value, max_value):
    return df[(df[column] >= min_value) & (df[column] <= max_value)]

# Slider for fee range specific to bar chart
min_value, max_value = st.slider('Select Fee Range for Bar Chart (0k to 100k)', 0, 100000, (0, 100000), 1000)

# Filter data for Due Fees and Paid Fees using the bar chart specific slider
filtered_df = filter_data(df, 'Academic Due Fees', min_value, max_value)
filtered_df_paid = filter_data(df, 'Academic Fees Paid', min_value, max_value)

# Create a bar chart
fig = go.Figure()

fig.add_trace(go.Bar(x=filtered_df['Name'], y=filtered_df['Academic Due Fees'], name='Due Fees', marker_color='rgb(55, 83, 109)'))
fig.add_trace(go.Bar(x=filtered_df['Name'], y=filtered_df_paid['Academic Fees Paid'], name='Paid Fees', marker_color='rgb(26, 118, 255)'))

# Add a red line at y=100,000
fig.add_shape(type="line", x0=0, y0=100000, x1=len(filtered_df['Name'])-1, y1=100000,
              line=dict(color="rgb(184, 115, 51)", width=3))  # Hazel color

# Update layout
fig.update_layout(title='Academic Fees with Due Fees and Paid Fees',
                  xaxis_title='Student', yaxis_title='Amount', barmode='group', height=600)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Calculate overall paid fees
overall_paid_transportation = df['Transportation Fees Paid'].sum()
overall_paid_academic = df['Academic Fees Paid'].sum()
overall_paid_hostel = df['Hostel Fees Paid'].sum()

# Create a pie chart for overall paid fees
labels_paid = ['Transportation Fees Paid', 'Academic Fees Paid', 'Hostel Fees Paid']
values_paid = [overall_paid_transportation, overall_paid_academic, overall_paid_hostel]

fig_pie1 = px.pie(values=values_paid, names=labels_paid, title='Overall Paid Fees Distribution')
fig_pie1.update_traces(marker=dict(colors=['skyblue', 'lightgreen', 'lightcoral']))

# Calculate overall due fees
overall_due_transportation = df['Transportation Due Fees'].sum() if 'Transportation Due Fees' in df else 0
overall_due_academic = df['Academic Due Fees'].sum()
overall_due_hostel = df['Hostel Fees Due'].sum() if 'Hostel Fees Due' in df else 0

# Create a pie chart for overall due fees
labels_due = ['Transportation Due Fees', 'Academic Due Fees', 'Hostel Due Fees']
values_due = [overall_due_transportation, overall_due_academic, overall_due_hostel]

fig_pie2 = px.pie(values=values_due, names=labels_due, title='Overall Due Fees Distribution')
fig_pie2.update_traces(marker=dict(colors=['lightyellow', 'lightgreen', 'lightcoral']))

# Positioning the charts
col2, col3 = st.columns(2)  # Divide the space into two columns

# Display the first pie chart (overall paid fees)
col2.plotly_chart(fig_pie1)

# Display the second pie chart (overall due fees)
col3.plotly_chart(fig_pie2)

# Create a scatter plot for Academic Paid Fees, Hostel Paid Fees, and Transportation Paid Fees
fig_scatter = go.Figure()

fig_scatter.add_trace(go.Scatter(x=df['Name'], y=df['Academic Fees Paid'], mode='markers', name='Academic Fees Paid', marker_color='rgb(55, 83, 109)'))
fig_scatter.add_trace(go.Scatter(x=df['Name'], y=df['Hostel Fees Paid'], mode='markers', name='Hostel Fees Paid', marker_color='rgb(26, 118, 255)'))
fig_scatter.add_trace(go.Scatter(x=df['Name'], y=df['Transportation Fees Paid'], mode='markers', name='Transportation Fees Paid', marker_color='red'))

# Update layout
fig_scatter.update_layout(title='Paid Fees Scatter Plot',
                          xaxis_title='Student', yaxis_title='Amount', height=800)  # Increased height

# Display the scatter plot
st.plotly_chart(fig_scatter, use_container_width=True)
