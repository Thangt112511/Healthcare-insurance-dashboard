import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Insurance Cost Explorer",
    layout="wide"
)
@st.cache_data
def load_data():
    df = pd.read_csv("insurance.csv")
    df.columns = df.columns.str.lower().str.strip()
    df['smoker'] = df['smoker'].astype('category')
    df['region'] = df['region'].astype('category')
    df['sex'] = df['sex'].astype('category')

    df['age_group'] = pd.cut(df['age'], bins=[17,25,35,45,55,65,100],
                             labels=['18–25','26–35','36–45','46–55','56–65','65+'])
    def bmi_category(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi < 25:
            return 'Normal'
        elif 25 <= bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    df['bmi_category'] = df['bmi'].apply(bmi_category)
    return df

df = load_data()

st.sidebar.title("Filter Data")
region = st.sidebar.multiselect(
    "Region",
    options=sorted(df['region'].unique().tolist()),
    default=sorted(df['region'].unique().tolist())
)

smoker = st.sidebar.multiselect(
    "Smoker",
    options=sorted(df['smoker'].unique().tolist()),
    default=sorted(df['smoker'].unique().tolist())
)

age_group = st.sidebar.multiselect(
    "Age Group",
    options=sorted(df['age_group'].dropna().unique().tolist()),
    default=sorted(df['age_group'].dropna().unique().tolist())
)

filtered_df = df[df['region'].isin(region) & df['smoker'].isin(smoker) & df['age_group'].isin(age_group)]

st.title("Health Insurance Cost Dashboard")
st.markdown("Analyze how demographic traits affect medical insurance charges.")

fig1 = px.box(filtered_df, x='age_group', y='charges', color='smoker', title="Charges by Age Group and Smoking Status")
st.plotly_chart(fig1)

fig2 = px.box(filtered_df, x='bmi_category', y='charges', color='smoker', title="Charges by BMI Category")
st.plotly_chart(fig2)

region_avg = filtered_df.groupby('region', as_index=False)['charges'].mean()
fig3 = px.bar(region_avg, x='region', y='charges', title='Average Charges by Region')
st.plotly_chart(fig3)
