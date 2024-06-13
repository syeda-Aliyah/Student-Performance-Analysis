import streamlit as st
import pandas as pd
import joblib

st.set_page_config(layout="wide")  # Ensures the layout is wide

st.title("Student Performance Prediction") #Title of the page

# Load the trained model and model columns
model = joblib.load('D:/pythonProject/SPA project/src/student_performance_model.pkl')
model_columns = joblib.load('D:/pythonProject\SPA project/src/model_columns.pkl')

# Function to preprocess custom input values
def preprocess_input(g1, g2, gender, school, address, internet, age):
    # Determine the age group based on the provided age
    if 14 <= age < 16:
        age_group = '15-16'
    elif 16 <= age < 19:
        age_group = '17-19'
    elif 19 <= age < 21:
        age_group = '20-21'
    else:
        age_group = None
    
    input_data = {
        'G1': [g1],
        'G2': [g2],
        'sex': [gender],
        'school': [school],
        'address': [address],
        'internet': [internet],
        'age_group': [age_group]
    }
    input_df = pd.DataFrame(input_data)
    categorical_columns = ['sex', 'school', 'address', 'internet', 'age_group']
    input_df_encoded = pd.get_dummies(input_df, columns=categorical_columns, drop_first=True)

    # Reindex the DataFrame to match the training data structure
    for col in model_columns:
        if col not in input_df_encoded.columns:
            input_df_encoded[col] = 0

    input_df_encoded = input_df_encoded[model_columns]
    return input_df_encoded


# Get user inputs
gender = st.selectbox('Gender', ['male', 'female'])
school = st.selectbox('School', ['GP', 'MS'])
address = st.selectbox('Address', ['U', 'R'])
internet = st.selectbox('Internet Access', ['yes', 'no'])
age = st.slider('Age', 14, 21, 16)
g1 = st.slider('G1 (First Period Grade)', 0, 20, 10)
g2 = st.slider('G2 (Second Period Grade)', 0, 20, 10)

# Predict button
if st.button('Predict'):
    custom_input = preprocess_input(g1, g2, gender, school, address, internet, age)
    custom_prediction = model.predict(custom_input)
    st.success(f'Predicted G3 Score: {custom_prediction[0]}')

