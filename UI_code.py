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

st.write("This app is a brainchild of myself and Sourabh Swarnkar. It's designed to help anyone \
-specificially UPSC/CAT aspirants or anyone interested in getting info on current affairs - a summary \
of any day's HINDU newspaper. Currently, it has just the data of a few days but if it seems useful, we can \
develop it to include daily updates. Tool leverages python for crawling Hindu's archives and GenAI\
to summarize the newspaper articles.\

In more advanced version, a GenAI enabled chatbot can be built on top of it, making it a ChatGPT \
like bot for Hindu newspaper. \

PS - We selected Hindu because UPSC/CAT aspirants mostly refer to Hindu for current affairs.")

# Upload Excel file
# uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

# if uploaded_file is not None:
    # Load the data
data = pd.read_excel("Summary.xlsx")
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
st.dataframe(data.head(3))
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
