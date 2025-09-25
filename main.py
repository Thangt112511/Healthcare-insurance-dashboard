import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

import pandas as pd

def load_data(path):
    try:
        df = pd.read_csv(path)
        print(" Dataset loaded successfully.")
        return df
    except FileNotFoundError:
        print(" File not found. Make sure 'insurance.csv' is in your project folder.")
        return None

df = load_data("insurance.csv")

if df is not None:
    print("\n📄 First 5 rows:")
    print(df.head())

print("\n Dataset Info:")
print(df.info())

print("\n Missing Values:")
print(df.isnull().sum())

df.columns = df.columns.str.lower().str.strip()

df['sex'] = df['sex'].astype('category')
df['smoker'] = df['smoker'].astype('category')
df['region'] = df['region'].astype('category')

print("\n Cleaned Data Preview:")
print(df.head())

bins = [17, 25, 35, 45, 55, 65, 100]
labels = ['18–25', '26–35', '36–45', '46–55', '56–65', '65+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

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

def children_label(n):
    if n == 0:
        return 'No kids'
    elif n == 1:
        return '1 child'
    else:
        return f'{n} children'

df['children_label'] = df['children'].apply(children_label)

print("\n Engineered Features Preview:")
print(df[['age', 'age_group', 'bmi', 'bmi_category', 'children', 'children_label']].head(10))


fig = px.box(
    df,
    x='age_group',
    y='charges',
    color='age_group',
    title='Charges by Age Group'
)
fig.show()


fig = px.box(
    df,
    x='smoker',
    y='charges',
    color='smoker',
    title='Charges by Smoking Status'
)
fig.show()


fig = px.box(
    df,
    x='bmi_category',
    y='charges',
    color='bmi_category',
    title='Charges by BMI Category',
    category_orders={'bmi_category': ['Underweight', 'Normal', 'Overweight', 'Obese']}
)
fig.show()


region_avg = df.groupby('region', as_index=False)['charges'].mean()

fig = px.bar(
    region_avg,
    x='region',
    y='charges',
    color='region',
    title='Average Charges by Region'
)
fig.show()

fig = px.box(
    df,
    x='children_label',
    y='charges',
    color='children_label',
    title='Charges by Number of Children'
)
fig.show()

fig = px.scatter(
    df,
    x='age',
    y='charges',
    color='smoker',
    hover_data=['bmi', 'region', 'children'],
    title='Interactive: Age vs Charges Colored by Smoking Status'
)

fig.show()