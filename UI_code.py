import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
# Load Excel file
@st.cache_data


# Function to filter the data based on inputs
def filter_data(data, filters1, filters2):
    # Load the Excel file
    df = data
    
    # Apply filters
    if filters1:
        df = df[df['Date'].isin(filters1)]
    if filters2:
        df = df[df['Category'].isin(filters2)]
    
    return df

# Streamlit UI
st.title("The Hindu Newspaper Summarizer")

# Upload Excel file
# uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

# if uploaded_file is not None:
    # Load the data
data = pd.read_excel("C:\\Users\\RSPRASAD\\OneDrive - Danaher\\Learning\\UPSC_Crawler\\data\\Summary.xlsx")
data['Date'] = pd.to_datetime(data['Date']).dt.date
# Display the data

data = data[['Date', 'Title', 'Category', 'Content', 'Summary']]

data['Content'] = data['Content'].fillna('0')


def remove_up_to_nth_occurrence(s,delimiter, n):
    # Find the nth occurrence of the delimiter
 
    start = -1
    for _ in range(n):
        start = s.find(delimiter, start + 1)
        if start == -1:
            # If the delimiter is not found n times, return the original string or handle as needed
            return s
    # Return the string after the nth occurrence
    return s[start + 1:]

# Remove up to and including the 2nd occurrence of ','
data['Content'] = data['Content'].apply(lambda x:remove_up_to_nth_occurrence(x, '-', 2))
# data['Content'] = data['Content'].apply(lambda x : x.replace('Here is a summary of the article in 3 sentences:',' ', regex = True))
data['Summary'] = data['Summary'].str.replace('Here is a summary of the article in 3 sentences:',' ', regex = True)

st.write("Data Preview:")
st.dataframe(data.head(10))
# data['Date2'] = pd.to_datetime(data['Date'], format='%d-%m-%Y').dt.date

# Get unique values for radio buttons
column1_values = data['Date'].unique()
column2_values = data['Category'].unique()

# Radio buttons for filtering
filters1 = st.multiselect("Select Filters for Date", list(column1_values))
filters2 = st.multiselect("Select Filters for Category", list(column2_values))


# Filter the data
if(st.button('Click for viewing summary')):
    filtered_data = filter_data(data, filters1, filters2)

# Display the filtered data
# st.write("Filtered Data:")
    st.dataframe(filtered_data.reset_index(drop = True))