from Utils.load_data import load_data
import numpy as np
import pandas as pd
import streamlit as st

df = load_data()
# Total Applicants = count(SK_ID_CURR)

Total_Applicants= df['SK_ID_CURR'].count()
# Total_Applicants

st.write(f"The Total applicants in the Home Credit: {Total_Applicants}")

# Default Rate (%) = mean(TARGET) × 100

Default_Rate= df['TARGET'].mean() * 100

st.write(f"The Default Rate of the clients in the Home Credit: {Default_Rate}")

# Repaid Rate (%) = (1 - mean(TARGET)) × 100

Repaid_Rate = (1-df['TARGET'].mean()) * 100

st.write(f"The Repaid Rate of the clients in the Home Credit: {Repaid_Rate}")

# Total Features = number of columns
a=list(df.columns)
Total_Features = len(a)

st.write(f"The Total Features in the Home Credit dataset: {Total_Features}")

# Avg Missing per Feature (%) = mean(isnull(col)) × 100 averaged over columns

# # Numerical Features
# # Categorical Features

# Median Age (Years) = median(AGE_YEARS)
data=df['DAYS_BIRTH']
AGE_YEARS=(-data/ 365.25)
AGE_YEARS

Median_Age= AGE_YEARS.median()
Median_Age

# Median Annual Income
Median_Annual_Income= df['AMT_INCOME_TOTAL'].median()
Median_Annual_Income

# Average Credit Amount

x=df['AMT_CREDIT'].sum()
y=len(list(df.columns))

Average_Credit_Amount=x/y

st.write(f"The Average Credit Amount of the clients in the Home Credit dataset: {Average_Credit_Amount}")