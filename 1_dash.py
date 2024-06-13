#import modules
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

import warnings

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Ensures the layout is wide
st.set_page_config(
    layout= 'wide',
    page_title="Student Performance Analysis and Prediction",
    page_icon="📊",
)


st.title("Student Performance Analysis") #Title of the page

#Load file
@st.cache_data
def load_data(file):
    data= pd.read_csv(file)
    # AVG grade of each student
    grad_mean= (data.G1 + data.G2 + data.G3) / 3
    data['G_Mean'] = grad_mean
    data['G_Mean']= data['G_Mean'].round()

    # Generating USN for each student
    data['USN'] = [random.randint(100, 700) for _ in range(len(data))]

    # Define age groups
    data['age_group'] = pd.cut(data['age'], bins=[14, 16, 19, 21], labels=["15-16", "17-19", "20-21"], right=False)

    # Define grade groups using pd.cut
    bins = [-np.inf, 12, 15, 17, np.inf]
    labels = ['Fail', 'Pass', 'Good', 'Excellent']
    data['grade_group'] = pd.cut(data['G_Mean'], bins=bins, labels=labels, right=False)
    return data

file="D:/trail/data/student-por.csv"
df= load_data(file)
#uploaded=st.file_uploader("Choose a CSV file")

#if uploaded is None:    
#    st.info("Upload a file through config", icon= "i")
#    st.stop()

#df= load_data(uploaded)



with st.expander("Data Preview"):
    #enable edit data
    edited_df= st.data_editor(df, num_rows= "dynamic")

# Save the edited data
if st.button('Save Data'):
    edited_df.to_csv("D:/trail/data/student-por-edited.csv", index=False)
    st.success('Data saved successfully!')


# Inject custom CSS
st.markdown(
    """
    <style>
    .custom-column {
        background-color: black;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
        margin: 10px;
    }
    .custom-header {
        color: #ff6347;
        font-size: 24px;
        font-weight: bold;
    }
    .custom-metric {
        color: #008080;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Define columns for the grid layout
col1, col2, col3, col4 = st.columns(4)

# Filters within columns
with col1:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.header("Select Gender" )
    gender_male = st.checkbox('Male')
    gender_female = st.checkbox('Female')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.header('Select Address')
    address_rural = st.checkbox('Rural')
    address_urban = st.checkbox('Urban')
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.header('Select Internet')
    internet_yes = st.checkbox('Yes')
    internet_no = st.checkbox('No')
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.header('Select School')
    school_ms = st.checkbox("P")
    school_gp = st.checkbox("G")
    st.markdown('</div>', unsafe_allow_html=True)

# Applying filters based on checkboxes
selected_genders = ['M', 'F']  # Default to include both genders if no selection
if gender_male and not gender_female:
    selected_genders = ['M']
if gender_female and not gender_male:
    selected_genders = ['F']
if not gender_male and not gender_female:
    selected_genders = ['M', 'F']  # Empty list to select no gender if no checkboxes are checked

selected_addresses = ['R', 'U']  # Default to include both addresses if no selection
if address_rural and not address_urban:
    selected_addresses = ['R']
if address_urban and not address_rural:
    selected_addresses = ['U']
if not address_rural and not address_urban:
    selected_addresses = ['R', 'U']  #list to select no address if no checkboxes are checked

selected_internet = ['yes', 'no']  # Default to include both internet options if no selection
if internet_yes and not internet_no:
    selected_internet = ['yes']
if internet_no and not internet_yes:
    selected_internet = ['no']
if not internet_yes and not internet_no:
    selected_internet = ['yes', 'no']  #list to select no internet option if no checkboxes are checked

selected_schools = ['GP', 'MS']  # Default to include both schools if no selection
if school_gp and not school_ms:
    selected_schools = ['GP']
if school_ms and not school_gp:
    selected_schools = ['MS']
if not school_gp and not school_ms:
    selected_schools = ['GP', 'MS']  #list to select no school if no checkboxes are checked

# Filter the dataframe
filtered_df = df[
    (df['sex'].isin(selected_genders)) &
    (df['address'].isin(selected_addresses)) &
    (df['internet'].isin(selected_internet)) &
    (df['school'].isin(selected_schools))
]

col5, col6 = st.columns(2)

with col5:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    st.header('Total No of Students')
    total_students = len(filtered_df)
    st.metric(label="Total Students", value=total_students, delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    average_studytime = filtered_df['studytime'].mean()
    average_freetime = filtered_df['freetime'].mean()
    st.metric(label="Average Studytime (hours)", value=f"{average_studytime:.2f}")
    st.metric(label="Average Freetime (hours)", value=f"{average_freetime:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)


# Visualizations
col7, col8 = st.columns(2)

with col7:
    with st.container():
        st.markdown('<div class="custom-header">Average of absences Vs Average of age by health</div>', unsafe_allow_html=True)
    
        fig, ax1 = plt.subplots(figsize=(8, 6))

    # Calculate average absences for each age group
        avg_absences_by_age_group = filtered_df.groupby('age_group')['absences'].mean()
        avg_health_by_age_group= filtered_df.groupby('age_group')['health'].mean()


    # Bar plot for average absences
        ax1.bar(avg_absences_by_age_group.index, avg_absences_by_age_group, color='blue', label='Average of absences')
        ax1.set_xlabel('Age group')
        ax1.set_ylabel('Average of absences', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

    # Line plot for sum of health
        ax2 = ax1.twinx()
        ax2.plot(avg_health_by_age_group.index, avg_health_by_age_group, color='orange', marker='o', label='Average of health')
        ax2.set_ylabel('Sum of health', color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')

    # Title and legend
        #fig.suptitle('Average of absences Vs Average of age by health', fontsize=16, color='#993399')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

    # Display plot
        st.pyplot(fig)



with col8:
     with st.container():
        st.markdown('<div class="custom-header">Average of studytime Vs Average of freetime by health</div>', unsafe_allow_html=True)
        #st.markdown('<div class="custom-column">', unsafe_allow_html=True)
        fig, ax1 = plt.subplots(figsize=(8, 6))
        
        # Group by age group
        average_freetime_by_age = filtered_df.groupby('age_group')['freetime'].mean()

        # Line plot for average freetime
        ax1.bar(average_freetime_by_age.index, average_freetime_by_age, color='blue', label='Average of freetime')
        ax1.set_xlabel('Age group')
        ax1.set_ylabel('Average of freetime', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Line plot for median failures
        ax2 = ax1.twinx()
        median_failures_by_age = filtered_df.groupby('age_group')['failures'].median()
        ax2.plot(median_failures_by_age.index, median_failures_by_age, color='orange', marker='o', label='Median of failures')
        ax2.set_ylabel('Median of failures', color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

    # Display plot
        st.pyplot(fig)

        st.markdown('</div>', unsafe_allow_html=True)

col9, col10, col11 = st.columns(3)

with col9:
    with st.container():
        st.markdown('<div class="custom-header">Count of grade group in each age group</div>', unsafe_allow_html=True)

        # Group by age group and grade group, then count occurrences
        grade_group_counts = filtered_df.groupby(['age_group', 'grade_group']).size().unstack()

        # Plotting
        plt.figure(figsize=(8, 6))
        for grade_group in grade_group_counts.columns:
            plt.plot(grade_group_counts.index, grade_group_counts[grade_group], label=grade_group)

        plt.xlabel('Age Group')
        plt.ylabel('Count')
        plt.title('Count of Grade Group in Each Age Group')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.legend(title='Grade Group')
        plt.tight_layout()
        
        # Display plot using Streamlit
        st.pyplot(plt)
        st.markdown('</div>', unsafe_allow_html=True)

with col10:
        st.markdown('<div class="custom-header">Average Travel Time, Free Time, and Study Time</div>', unsafe_allow_html=True)
        # Calculate average values
        average_travel_time = filtered_df['traveltime'].mean()
        average_free_time = filtered_df['freetime'].mean()
        average_study_time = filtered_df['studytime'].mean()

        # Data for pie chart
        labels = ['Travel Time', 'Free Time', 'Study Time']
        sizes = [average_travel_time, average_free_time, average_study_time]
        colors = ['lightblue', 'lightgreen', 'lightcoral']
        explode = (0.1, 0, 0)  # explode the 1st slice (Travel Time)

        # Plotting the pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the pie chart
        st.pyplot(plt)
        st.markdown('</div>', unsafe_allow_html=True)

with col11:
    with st.container():
        st.markdown('<div class="custom-header">Count of Romance and Grade Group by Gender</div>', unsafe_allow_html=True)        
        
        # Group by 'sex' and 'romantic', then count occurrences of each grade group
        grouped_df = filtered_df.groupby(['sex', 'romantic', 'grade_group']).size().reset_index(name='count')

        # Plotting
        fig, ax1 = plt.subplots(figsize=(8, 6))
        
        # Bar plot for average grade by gender
        average_grade_by_gender = filtered_df.groupby('sex')['grade_group'].value_counts(normalize=True).unstack()
        average_grade_by_gender.plot(kind='bar', ax=ax1, color=['lightcoral', '#FFE5B4', 'lightblue', 'lightgreen'])
        ax1.set_xlabel('Gender')
        ax1.set_ylabel('Grade group')
        #ax1.set_title('Percentage of Grade Group by Gender')
        ax1.legend(title='Grade Group')

        # Line plot for romance status by gender
        ax2 = ax1.twinx()
        romance_by_gender = filtered_df.groupby('sex')['romantic'].value_counts(normalize=True).unstack()
        romance_by_gender.plot(kind='line', ax=ax2, color=['black', 'purple'], marker='o', linestyle='--')
        ax2.set_ylabel('Romantic Status')
        ax2.set_ylim(0, 1)
        ax2.legend(title='Romantic Status', loc='lower right')

        # Display plot
        st.pyplot(fig)

        st.markdown('</div>', unsafe_allow_html=True)



